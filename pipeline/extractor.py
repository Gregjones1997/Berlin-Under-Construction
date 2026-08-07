from __future__ import annotations

from pydantic import ValidationError

from pipeline.schemas import ExtractionOutput, HtmlEvidenceSpan, validate_exact_html_span


class ExtractionOutputRejected(ValueError):
    pass


def parse_extraction_output(
    raw_output: str | bytes,
    *,
    artifact_bytes: bytes,
    media_type: str,
) -> ExtractionOutput:
    """Validate untrusted model JSON as one atomic, non-publishable proposal batch."""

    try:
        output = ExtractionOutput.model_validate_json(raw_output)
    except ValidationError as exc:
        raise ExtractionOutputRejected("malformed_extraction_output") from exc

    if media_type.partition(";")[0].lower() != "text/html":
        raise ExtractionOutputRejected("evidence_span_verification_not_implemented_for_media_type")

    for proposal in output.proposed_claims:
        for span in proposal.evidence_spans:
            if not isinstance(span, HtmlEvidenceSpan) or not validate_exact_html_span(
                artifact_bytes, span
            ):
                raise ExtractionOutputRejected("evidence_span_mismatch")
    return output
