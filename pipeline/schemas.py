from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)


class PdfEvidenceSpan(StrictModel):
    kind: Literal["pdf"]
    exact_text_de: str = Field(min_length=1)
    page: int = Field(ge=1)
    bbox: tuple[float, float, float, float]


class HtmlEvidenceSpan(StrictModel):
    kind: Literal["html"]
    exact_text_de: str = Field(min_length=1)
    selector: str = Field(min_length=1)
    start: int = Field(ge=0)
    end: int = Field(gt=0)

    @model_validator(mode="after")
    def end_follows_start(self) -> "HtmlEvidenceSpan":
        if self.end <= self.start:
            raise ValueError("end must be greater than start")
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


class MilestoneClaim(StrictModel):
    claim_id: str = Field(min_length=1)
    project_id: str = Field(min_length=1)
    schema_version: str = Field(min_length=1)
    claim_kind: Literal["milestone"]
    canonical_value_de: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    artifact_id: str = Field(min_length=1)
    evidence_spans: tuple[EvidenceSpan, ...] = Field(min_length=1)
    qualifiers: tuple[dict[str, object], ...]
    confidence: Confidence
    review_state: Literal["proposed", "accepted", "rejected", "deferred"]
    validation_results: tuple[dict[str, object], ...]
    relations: tuple[dict[str, object], ...]
    publication_eligibility: Literal["eligible", "blocked", "review_required"]
    verification_state: Literal["verified", "unverified"]
    created_at: datetime
    milestone_type: MilestoneType
    milestone_term_de: str = Field(min_length=1)
    object_scope: str = Field(min_length=1)
    date_value: DateValue


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


def validate_exact_html_span(content: bytes, span: HtmlEvidenceSpan) -> bool:
    text = content.decode("utf-8")
    return text[span.start : span.end] == span.exact_text_de
