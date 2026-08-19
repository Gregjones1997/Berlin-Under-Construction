from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from pipeline.schemas import (
    ActiveMilestoneClaim,
    ClaimRelation,
    Confidence,
    DateValue,
    HtmlEvidenceSpan,
    Qualifier,
    QuarantinedMilestoneClaim,
    Quarantine,
    ValidationResult,
    milestone_claim_adapter,
)


def valid_claim_kwargs(**overrides: object) -> dict[str, object]:
    """A claim that is valid under strict mode: real tuples, aware datetime, typed members."""

    kwargs: dict[str, object] = {
        "claim_id": "claim-1",
        "project_id": "C-010",
        "schema_version": "1.0.0",
        "claim_kind": "milestone",
        "canonical_value_de": "Fertigstellung: 2026",
        "source_id": "source-1",
        "artifact_id": "artifact-1",
        "evidence_spans": (
            HtmlEvidenceSpan(
                kind="html",
                exact_text_de="Fertigstellung",
                selector="main p",
                start=0,
                end=14,
            ),
        ),
        "qualifiers": (
            Qualifier(qualifier_class="modal_intent", applies_to="date", token_de="geplant"),
        ),
        "confidence": Confidence(
            score=Decimal("0.90"), source="extractor", threshold_config_version="thresholds-v1"
        ),
        "review_state": "accepted",
        "validation_results": (ValidationResult(code="missing_evidence_span", outcome="pass"),),
        "relations": (ClaimRelation(relation="confirms", target_claim_id="claim-0"),),
        "publication_eligibility": "eligible",
        "verification_state": "verified",
        "created_at": datetime(2026, 8, 7, 12, 0, tzinfo=UTC),
        "milestone_type": "substantial_completion",
        "milestone_term_de": "Fertigstellung",
        "object_scope": "Baumaßnahme",
        "date_value": DateValue(precision="year", canonical="2026"),
    }
    kwargs.update(overrides)
    return kwargs


def test_a_fully_supported_claim_is_constructible() -> None:
    claim = ActiveMilestoneClaim(**valid_claim_kwargs())

    assert claim.publication_eligibility == "eligible"
    assert claim.qualifiers[0].applies_to == "date"


def test_milestone_date_requires_an_explicit_milestone_type() -> None:
    kwargs = valid_claim_kwargs()
    del kwargs["milestone_type"]

    with pytest.raises(ValidationError) as error:
        ActiveMilestoneClaim(**kwargs)

    assert [item["loc"] for item in error.value.errors()] == [("milestone_type",)]


def test_eligible_requires_a_verified_state() -> None:
    with pytest.raises(ValidationError, match="verified"):
        ActiveMilestoneClaim(**valid_claim_kwargs(verification_state="unverified"))


def test_eligible_requires_an_accepted_review_decision() -> None:
    with pytest.raises(ValidationError, match="accepted review"):
        ActiveMilestoneClaim(**valid_claim_kwargs(review_state="proposed"))


def test_eligible_requires_recorded_passing_validations() -> None:
    with pytest.raises(ValidationError):
        ActiveMilestoneClaim(**valid_claim_kwargs(validation_results=()))

    with pytest.raises(ValidationError):
        ActiveMilestoneClaim(
            **valid_claim_kwargs(
                validation_results=(
                    ValidationResult(code="claim_conflict", outcome="review_required"),
                )
            )
        )


def test_unpublishable_states_may_carry_failing_validations() -> None:
    claim = ActiveMilestoneClaim(
        **valid_claim_kwargs(
            publication_eligibility="review_required",
            review_state="proposed",
            verification_state="unverified",
            validation_results=(ValidationResult(code="claim_conflict", outcome="review_required"),),
        )
    )

    assert claim.publication_eligibility == "review_required"


def test_a_claim_cannot_publish_without_an_evidence_span() -> None:
    with pytest.raises(ValidationError):
        ActiveMilestoneClaim(**valid_claim_kwargs(evidence_spans=()))


def test_created_at_must_be_timezone_aware() -> None:
    with pytest.raises(ValidationError):
        ActiveMilestoneClaim(**valid_claim_kwargs(created_at=datetime(2026, 8, 7, 12, 0)))


def test_qualifiers_are_a_closed_class_and_cannot_be_mutated_after_validation() -> None:
    with pytest.raises(ValidationError):
        Qualifier(qualifier_class="vibes", applies_to="amount", token_de="rund")

    with pytest.raises(ValidationError):
        Qualifier(qualifier_class="approximation", token_de="rund")

    claim = ActiveMilestoneClaim(**valid_claim_kwargs())
    with pytest.raises(ValidationError):
        claim.qualifiers[0].applies_to = "amount"


def quarantine_kwargs(**overrides: object) -> dict[str, object]:
    kwargs = valid_claim_kwargs(
        publication_eligibility="quarantined",
        verification_state="unverified",
        review_state="deferred",
        quarantine=Quarantine(
            reason="Fertigstellung bezieht sich auf die Sporthalle, nicht auf das Vorhaben",
            scope_relation="disjoint",
            assigned_by_review_decision_id="review-1",
        ),
    )
    kwargs.update(overrides)
    return kwargs


def test_a_quarantined_claim_keeps_its_span_source_and_german_value() -> None:
    claim = QuarantinedMilestoneClaim(**quarantine_kwargs())

    assert claim.publication_eligibility == "quarantined"
    assert claim.canonical_value_de == "Fertigstellung: 2026"
    assert claim.evidence_spans[0].exact_text_de == "Fertigstellung"
    assert claim.quarantine.scope_relation == "disjoint"


def test_quarantine_cannot_be_declared_without_a_quarantine_record() -> None:
    kwargs = quarantine_kwargs()
    del kwargs["quarantine"]

    with pytest.raises(ValidationError):
        QuarantinedMilestoneClaim(**kwargs)


def test_a_quarantined_claim_can_never_be_verified() -> None:
    with pytest.raises(ValidationError):
        QuarantinedMilestoneClaim(**quarantine_kwargs(verification_state="verified"))


def test_an_active_claim_cannot_carry_a_quarantine_record() -> None:
    with pytest.raises(ValidationError):
        ActiveMilestoneClaim(
            **valid_claim_kwargs(
                quarantine=Quarantine(
                    reason="r", scope_relation="unknown", assigned_by_review_decision_id="d"
                )
            )
        )


def test_quarantine_is_not_reachable_as_a_publication_state_on_an_active_claim() -> None:
    with pytest.raises(ValidationError):
        ActiveMilestoneClaim(**valid_claim_kwargs(publication_eligibility="quarantined"))


def test_the_union_dispatches_on_publication_eligibility() -> None:
    active = milestone_claim_adapter.validate_python(valid_claim_kwargs())
    quarantined = milestone_claim_adapter.validate_python(quarantine_kwargs())

    assert isinstance(active, ActiveMilestoneClaim)
    assert isinstance(quarantined, QuarantinedMilestoneClaim)
