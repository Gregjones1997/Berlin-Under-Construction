from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Annotated, Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, TypeAdapter, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)


class ArtifactNotDecodable(ValueError):
    """Raised when an artifact cannot be decoded with its declared charset."""


class PdfEvidenceSpan(StrictModel):
    kind: Literal["pdf"]
    exact_text_de: str = Field(min_length=1)
    page: int = Field(ge=1)
    bbox: tuple[float, float, float, float]


class HtmlEvidenceSpan(StrictModel):
    """`start`/`end` are Unicode codepoint offsets into the decoded artifact, not bytes."""

    kind: Literal["html"]
    exact_text_de: str = Field(min_length=1)
    selector: str = Field(min_length=1)
    start: int = Field(ge=0, description="codepoint offset, not a byte offset")
    end: int = Field(gt=0, description="exclusive codepoint offset, not a byte offset")

    @model_validator(mode="after")
    def end_follows_start(self) -> "HtmlEvidenceSpan":
        if self.end <= self.start:
            raise ValueError("end must be greater than start")
        if self.end - self.start != len(self.exact_text_de):
            raise ValueError("span length must equal the length of exact_text_de")
        return self


EvidenceSpan = Annotated[PdfEvidenceSpan | HtmlEvidenceSpan, Field(discriminator="kind")]


class Confidence(StrictModel):
    score: Decimal = Field(ge=Decimal("0"), le=Decimal("1"), allow_inf_nan=False)
    source: Literal["extractor"]
    threshold_config_version: str = Field(min_length=1)


class DateValue(StrictModel):
    precision: Literal[
        "exact_day", "month", "season", "half_year", "year", "range", "relative_anchor"
    ]
    canonical: str = Field(min_length=1)


QualifierClass = Literal[
    "upper_bound",
    "lower_bound",
    "approximation",
    "range",
    "modal_intent",
    "source_stated_unreliability",
    "as_of_hedge",
]


class Qualifier(StrictModel):
    """Closed-class qualifier per docs/data-model-proposal.md; `applies_to` is mandatory."""

    qualifier_class: QualifierClass
    applies_to: Literal["amount", "date", "scope", "status"]
    token_de: str = Field(min_length=1)


ValidationCode = Literal[
    "missing_evidence_span",
    "personal_data_high_confidence",
    "possible_personal_name",
    "missing_milestone_type",
    "unresolved_financial_scope",
    "claim_conflict",
    "below_confidence_threshold",
    "missing_or_invalid_confidence",
    "malformed_extraction_output",
    "financial_depth_coverage_incomplete",
]


class ValidationResult(StrictModel):
    code: ValidationCode
    outcome: Literal["pass", "fail", "review_required"]


class ClaimRelation(StrictModel):
    relation: Literal["confirms", "contradicts", "supersedes"]
    target_claim_id: str = Field(min_length=1)


MilestoneType = Literal[
    "planning_approval",
    "tender_deadline",
    "award",
    "site_start",
    "construction_start",
    "substantial_completion",
    "handover",
    "commissioning",
    "public_opening",
]


ScopeRelation = Literal["superset", "subset", "overlapping", "disjoint", "unknown"]


class Quarantine(StrictModel):
    """Assigned by a human during review.

    `scope_relation` describes the source-published scope relative to the project
    boundary. It is stored but never rendered, and it must never be model-derived
    (docs/data-model-proposal.md). No field here is reachable from an extractor
    proposal.
    """

    reason: str = Field(min_length=1)
    scope_relation: ScopeRelation
    assigned_by_review_decision_id: str = Field(min_length=1)


class MilestoneClaimBase(StrictModel):
    claim_id: str = Field(min_length=1)
    project_id: str = Field(min_length=1)
    schema_version: str = Field(min_length=1)
    claim_kind: Literal["milestone"]
    canonical_value_de: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    artifact_id: str = Field(min_length=1)
    evidence_spans: tuple[EvidenceSpan, ...] = Field(min_length=1)
    qualifiers: tuple[Qualifier, ...]
    confidence: Confidence
    review_state: Literal["proposed", "accepted", "rejected", "deferred"]
    validation_results: tuple[ValidationResult, ...]
    relations: tuple[ClaimRelation, ...]
    created_at: AwareDatetime
    milestone_type: MilestoneType
    milestone_term_de: str = Field(min_length=1)
    object_scope: str = Field(min_length=1)
    date_value: DateValue


class ActiveMilestoneClaim(MilestoneClaimBase):
    publication_eligibility: Literal["eligible", "blocked", "review_required"]
    verification_state: Literal["verified", "unverified"]

    @model_validator(mode="after")
    def eligible_requires_verification_and_accepted_review(self) -> "ActiveMilestoneClaim":
        """AGENTS.md rule 4: publication eligibility is deterministic, never assumed."""

        if self.publication_eligibility != "eligible":
            return self
        if self.verification_state != "verified":
            raise ValueError("eligible claims must be verified")
        if self.review_state != "accepted":
            raise ValueError("eligible claims require an accepted review decision")
        if any(result.outcome != "pass" for result in self.validation_results):
            raise ValueError("eligible claims must have no failing or review-required validation")
        if not self.validation_results:
            raise ValueError("eligible claims must record the validations that passed")
        return self


class QuarantinedMilestoneClaim(MilestoneClaimBase):
    """Correctly extracted, not the project's value, never dropped, never rendered as the value.

    Quarantine is terminal publication eligibility. The claim keeps its exact
    German evidence span and source, and stays `unverified` by construction.
    """

    publication_eligibility: Literal["quarantined"]
    verification_state: Literal["unverified"]
    quarantine: Quarantine


MilestoneClaim = Annotated[
    ActiveMilestoneClaim | QuarantinedMilestoneClaim,
    Field(discriminator="publication_eligibility"),
]
milestone_claim_adapter: TypeAdapter[ActiveMilestoneClaim | QuarantinedMilestoneClaim] = (
    TypeAdapter(MilestoneClaim)
)


class MilestoneProposal(StrictModel):
    """Untrusted extractor output; publication and review fields are intentionally absent."""

    claim_kind: Literal["milestone"]
    canonical_value_de: str = Field(min_length=1)
    evidence_spans: tuple[EvidenceSpan, ...] = Field(min_length=1)
    confidence: Confidence
    milestone_type: MilestoneType
    milestone_term_de: str = Field(min_length=1)
    object_scope: str = Field(min_length=1)
    date_value: DateValue


class ExtractionMetrics(StrictModel):
    provider: str = Field(min_length=1)
    model: str = Field(min_length=1)
    model_version: str = Field(min_length=1)
    prompt_version: str = Field(min_length=1)
    extraction_schema_version: str = Field(min_length=1)
    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)
    cached_tokens: int | None = Field(default=None, ge=0)
    cost_amount: Decimal = Field(ge=0, allow_inf_nan=False)
    cost_currency: Literal["EUR", "USD"]
    pricing_reference: str = Field(min_length=1)


class ExtractionOutput(StrictModel):
    proposed_claims: tuple[MilestoneProposal, ...]


def decode_artifact(content: bytes, charset: str) -> str:
    """Decode with the artifact's declared charset. Never silently substitutes characters."""

    try:
        return content.decode(charset, errors="strict")
    except (UnicodeDecodeError, LookupError) as exc:
        raise ArtifactNotDecodable(f"artifact is not decodable as {charset!r}") from exc


def validate_exact_html_span(content: bytes, span: HtmlEvidenceSpan, *, charset: str = "utf-8") -> bool:
    """Deterministic verbatim check. Offsets are codepoints into the decoded artifact."""

    text = decode_artifact(content, charset)
    if span.end > len(text):
        return False
    return text[span.start : span.end] == span.exact_text_de
