from __future__ import annotations

from decimal import Decimal

import pytest
from pydantic import ValidationError

from pipeline.schemas import (
    ArtifactNotDecodable,
    Confidence,
    HtmlEvidenceSpan,
    MilestoneProposal,
    decode_artifact,
    validate_exact_html_span,
)


def proposal_payload() -> dict[str, object]:
    return {
        "claim_kind": "milestone",
        "canonical_value_de": "Fertigstellung im Jahr 2026",
        "evidence_spans": (
            {
                "kind": "html",
                "exact_text_de": "Fertigstellung im Jahr 2026",
                "selector": "main p",
                "start": 0,
                "end": 27,
            },
        ),
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


def test_a_well_formed_proposal_validates() -> None:
    assert MilestoneProposal.model_validate(proposal_payload()).milestone_term_de == "Fertigstellung"


def test_extraction_proposal_requires_an_exact_german_evidence_span() -> None:
    payload = proposal_payload()
    payload["evidence_spans"] = ()

    with pytest.raises(ValidationError):
        MilestoneProposal.model_validate(payload)


def test_extractor_cannot_set_publication_or_review_state() -> None:
    for forbidden in (
        "publication_eligibility",
        "verification_state",
        "review_state",
        "claim_id",
        "quarantine",
        "scope_relation",
    ):
        payload = proposal_payload()
        payload[forbidden] = "eligible"

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


def test_span_offsets_are_codepoints_not_bytes() -> None:
    """`Baumaßnahme` is 11 codepoints and 12 UTF-8 bytes; the units must not blur."""

    artifact = "Baumaßnahme beginnt".encode("utf-8")
    codepoint_span = HtmlEvidenceSpan(
        kind="html", exact_text_de="Baumaßnahme", selector="main", start=0, end=11
    )

    assert validate_exact_html_span(artifact, codepoint_span)

    with pytest.raises(ValidationError):
        HtmlEvidenceSpan(
            kind="html", exact_text_de="Baumaßnahme", selector="main", start=0, end=12
        )


def test_a_span_reaching_past_the_end_of_the_artifact_does_not_validate() -> None:
    span = HtmlEvidenceSpan(
        kind="html", exact_text_de="Baubeginn", selector="main", start=5, end=14
    )

    assert not validate_exact_html_span(b"Baubeginn", span)


def test_a_non_utf8_artifact_is_reported_not_silently_mangled() -> None:
    span = HtmlEvidenceSpan(
        kind="html", exact_text_de="Baumaßnahme", selector="main", start=0, end=11
    )

    with pytest.raises(ArtifactNotDecodable):
        validate_exact_html_span("Baumaßnahme".encode("latin-1"), span)

    assert decode_artifact("Baumaßnahme".encode("latin-1"), "latin-1") == "Baumaßnahme"
