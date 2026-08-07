from __future__ import annotations

from decimal import Decimal

import pytest
from pydantic import ValidationError

from pipeline.schemas import Confidence, HtmlEvidenceSpan, MilestoneProposal, validate_exact_html_span


def proposal_payload() -> dict[str, object]:
    return {
        "claim_kind": "milestone",
        "canonical_value_de": "Fertigstellung im Jahr 2026",
        "evidence_spans": [
            {
                "kind": "html",
                "exact_text_de": "Fertigstellung im Jahr 2026",
                "selector": "main p",
                "start": 0,
                "end": 30,
            }
        ],
        "confidence": {
            "score": Decimal("0.91"),
            "source": "extractor",
            "threshold_config_version": "thresholds-v1",
        },
        "milestone_type": "substantial_completion",
        "milestone_term_de": "Fertigstellung",
        "object_scope": "Baumaßnahme",
        "date_value": {"precision": "year", "canonical": "2026"},
    }


def test_extraction_proposal_requires_an_exact_german_evidence_span() -> None:
    payload = proposal_payload()
    payload["evidence_spans"] = []

    with pytest.raises(ValidationError):
        MilestoneProposal.model_validate(payload)


def test_extractor_cannot_set_publication_or_review_state() -> None:
    payload = proposal_payload()
    payload["publication_eligibility"] = "eligible"

    with pytest.raises(ValidationError):
        MilestoneProposal.model_validate(payload)


def test_confidence_is_strict_and_bounded() -> None:
    with pytest.raises(ValidationError):
        Confidence.model_validate(
            {"score": 2, "source": "extractor", "threshold_config_version": "v1"}
        )


def test_html_span_is_checked_against_canonical_german_bytes() -> None:
    span = HtmlEvidenceSpan.model_validate(
        {
            "kind": "html",
            "exact_text_de": "Baubeginn",
            "selector": "main",
            "start": 0,
            "end": 9,
        }
    )
    assert validate_exact_html_span("Baubeginn 2026".encode(), span)
