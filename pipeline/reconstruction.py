from __future__ import annotations

import hashlib
import difflib
import json
from dataclasses import dataclass
from typing import Literal

from pipeline.schemas import ActiveMilestoneClaim, HtmlEvidenceSpan, PdfEvidenceSpan
from pipeline.store import LocalPipelineStore


class IncompleteReconstruction(ValueError):
    """A content-free reconstruction failure safe to expose in logs."""


REQUIRED_RENDER_VALIDATIONS = frozenset(
    {"missing_evidence_span", "personal_data_high_confidence", "possible_personal_name"}
)


def _quoted(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _may_render(claim: ActiveMilestoneClaim) -> bool:
    if claim.publication_eligibility != "eligible":
        return False
    outcomes = {result.code: result.outcome for result in claim.validation_results}
    return all(outcomes.get(code) == "pass" for code in REQUIRED_RENDER_VALIDATIONS)


def reconstruct_milestone_fragment(store: LocalPipelineStore, project_id: str) -> str:
    """Render only stored, publication-safe milestone data in deterministic order."""

    records = store.load_project(project_id)
    if not records.milestone_claims:
        raise IncompleteReconstruction("project has no stored milestone claims")

    artifacts = {artifact.artifact_id: artifact for artifact in records.artifacts}
    retrievals = {
        (retrieval.source_id, retrieval.artifact_id): retrieval
        for retrieval in records.retrievals
    }
    lines = [f"# Milestone fragment — {project_id}", ""]
    for claim in records.milestone_claims:
        if not isinstance(claim, ActiveMilestoneClaim) or not _may_render(claim):
            codes = ", ".join(sorted(result.code for result in claim.validation_results)) or "none"
            lines.append(
                f"- {claim.claim_id} — withheld "
                f"({claim.publication_eligibility}; {claim.review_state}; validations: {codes})"
            )
            continue

        artifact = artifacts.get(claim.artifact_id)
        retrieval = retrievals.get((claim.source_id, claim.artifact_id))
        if artifact is None or retrieval is None:
            raise IncompleteReconstruction("claim evidence is not backed by a stored retrieval")

        lines.extend(
            [
                f"## {claim.milestone_type} — {claim.claim_id}",
                "",
                f"- Canonical German: {_quoted(claim.canonical_value_de)}",
                f"- Milestone term: {_quoted(claim.milestone_term_de)}",
                f"- Object scope: {_quoted(claim.object_scope)}",
                f"- Date ({claim.date_value.precision}): {_quoted(claim.date_value.canonical)}",
                f"- Source: {claim.source_id}",
                f"- Retrieved: {retrieval.retrieved_at.isoformat()}",
                f"- URL: {retrieval.final_url}",
                f"- Stored content (post-strip): sha256:{artifact.stored_content_hash}",
            ]
        )
        for span in claim.evidence_spans:
            if isinstance(span, HtmlEvidenceSpan):
                locator = f"{span.selector}:{span.start}-{span.end}"
            elif isinstance(span, PdfEvidenceSpan):
                locator = f"page {span.page}; bbox {span.bbox}"
            else:  # pragma: no cover - discriminated schema makes this unreachable
                raise IncompleteReconstruction("unsupported evidence locator")
            lines.append(f"- Evidence ({locator}): {_quoted(span.exact_text_de)}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


@dataclass(frozen=True)
class SmokeComparison:
    status: Literal["no_textual_difference", "differences_observed"]
    reference_sha256: str
    generated_sha256: str
    unified_diff: str


def compare_for_smoke(reference_text: str, generated_text: str) -> SmokeComparison:
    """Observe textual differences without scoring them or treating either text as truth."""

    difference = "".join(
        difflib.unified_diff(
            reference_text.splitlines(keepends=True),
            generated_text.splitlines(keepends=True),
            fromfile="committed-dossier-observation",
            tofile="stored-fragment-observation",
        )
    )
    return SmokeComparison(
        status="differences_observed" if difference else "no_textual_difference",
        reference_sha256=hashlib.sha256(reference_text.encode("utf-8")).hexdigest(),
        generated_sha256=hashlib.sha256(generated_text.encode("utf-8")).hexdigest(),
        unified_diff=difference,
    )
