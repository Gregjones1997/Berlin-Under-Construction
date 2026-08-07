from __future__ import annotations

from pydantic import ValidationError

from pipeline.schemas import (
    ArtifactNotDecodable,
    ExtractionOutput,
    HtmlEvidenceSpan,
    validate_exact_html_span,
)


class ExtractionOutputRejected(ValueError):
    pass


def _charset_of(media_type: str) -> str:
    for parameter in media_type.split(";")[1:]:
        name, _, value = parameter.partition("=")
        if name.strip().lower() == "charset":
            return value.strip().strip('"') or "utf-8"
    return "utf-8"


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

    if media_type.partition(";")[0].strip().lower() != "text/html":
        raise ExtractionOutputRejected("evidence_span_verification_not_implemented_for_media_type")

    charset = _charset_of(media_type)
    for proposal in output.proposed_claims:
        for span in proposal.evidence_spans:
            if not isinstance(span, HtmlEvidenceSpan):
                raise ExtractionOutputRejected("evidence_span_mismatch")
            try:
                matches = validate_exact_html_span(artifact_bytes, span, charset=charset)
            except ArtifactNotDecodable as exc:
                raise ExtractionOutputRejected("artifact_not_decodable") from exc
            if not matches:
                raise ExtractionOutputRejected("evidence_span_mismatch")
    return output
