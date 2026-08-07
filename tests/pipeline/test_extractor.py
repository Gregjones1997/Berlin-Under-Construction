import json

import pytest

from pipeline.extractor import ExtractionOutputRejected, parse_extraction_output


def output_for_span(text: str) -> str:
    return json.dumps(
        {
            "proposed_claims": [
                {
                    "claim_kind": "milestone",
                    "canonical_value_de": text,
                    "evidence_spans": [
                        {
                            "kind": "html",
                            "exact_text_de": text,
                            "selector": "main",
                            "start": 0,
                            "end": len(text),
                        }
                    ],
                    "confidence": {
                        "score": 0.9,
                        "source": "extractor",
                        "threshold_config_version": "thresholds-v1",
                    },
                    "milestone_type": "construction_start",
                    "milestone_term_de": "Baubeginn",
                    "object_scope": "Baumaßnahme",
                    "date_value": {"precision": "year", "canonical": "2026"},
                }
            ]
        }
    )


def test_valid_model_output_preserves_german_and_remains_a_proposal() -> None:
    output = parse_extraction_output(
        output_for_span("Baubeginn"),
        artifact_bytes="Baubeginn 2026".encode(),
        media_type="text/html",
    )

    assert output.proposed_claims[0].canonical_value_de == "Baubeginn"
    assert not hasattr(output.proposed_claims[0], "publication_eligibility")


def test_one_bad_span_rejects_the_entire_model_output() -> None:
    with pytest.raises(ExtractionOutputRejected, match="evidence_span_mismatch"):
        parse_extraction_output(
            output_for_span("Inbetriebnahme"),
            artifact_bytes="Baubeginn 2026".encode(),
            media_type="text/html",
        )


def test_pdf_proposals_are_blocked_until_bbox_verification_exists() -> None:
    with pytest.raises(ExtractionOutputRejected, match="not_implemented"):
        parse_extraction_output(
            output_for_span("Baubeginn"),
            artifact_bytes=b"%PDF-placeholder",
            media_type="application/pdf",
        )
