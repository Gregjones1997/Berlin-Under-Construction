from __future__ import annotations

from datetime import datetime

from pipeline.reconstruction import IncompleteReconstruction, reconstruct_milestone_fragment
from pipeline.schemas import ValidationResult
from pipeline.store import LocalPipelineStore
from tests.pipeline.test_store import artifact, claim, retrieval, review_decision


def test_fragment_is_reconstructed_from_reopened_store_without_private_hash(tmp_path) -> None:
    database = tmp_path / "pipeline.sqlite3"
    retained = artifact().model_copy(
        update={
            "pre_transform_response_hash": "b" * 64,
            "transform_rule_version": "pdf-metadata-strip/v1",
        }
    )
    eligible = claim().model_copy(
        update={
            "review_state": "accepted",
            "publication_eligibility": "eligible",
            "verification_state": "verified",
            "validation_results": (
                ValidationResult(code="missing_evidence_span", outcome="pass"),
                ValidationResult(code="personal_data_high_confidence", outcome="pass"),
                ValidationResult(code="possible_personal_name", outcome="pass"),
            ),
        }
    )
    with LocalPipelineStore(database) as store:
        store.record_retrieval_artifact(retrieval(), retained)
        store.record_claim(eligible)
        store.record_review_decision(review_decision())

    with LocalPipelineStore(database) as reopened:
        fragment = reconstruct_milestone_fragment(reopened, "C-014")

    assert "Baubeginn 2026" in fragment
    assert "construction_start" in fragment
    assert artifact().stored_content_hash in fragment
    assert retained.pre_transform_response_hash not in fragment


def test_nonpublishable_claim_text_is_withheld(tmp_path) -> None:
    database = tmp_path / "pipeline.sqlite3"
    with LocalPipelineStore(database) as store:
        store.record_retrieval_artifact(retrieval(), artifact())
        store.record_claim(claim())
        fragment = reconstruct_milestone_fragment(store, "C-014")

    assert "claim-1 — withheld" in fragment
    assert "Baubeginn 2026" not in fragment


def test_local_withheld_detail_mode_exposes_stored_content_for_smoke_diagnosis(tmp_path) -> None:
    database = tmp_path / "pipeline.sqlite3"
    with LocalPipelineStore(database) as store:
        store.record_retrieval_artifact(retrieval(), artifact())
        store.record_claim(claim())
        fragment = reconstruct_milestone_fragment(
            store, "C-014", include_withheld_detail=True
        )

    assert "LOCAL-ONLY WITHHELD DETAIL" in fragment
    assert "claim-1 — withheld" in fragment
    assert 'Canonical German: "Baubeginn 2026"' in fragment
    assert 'Evidence (main:6-20): "Baubeginn 2026"' in fragment


def test_claim_without_stored_acceptance_decision_is_withheld(tmp_path) -> None:
    eligible = claim().model_copy(
        update={
            "review_state": "accepted",
            "publication_eligibility": "eligible",
            "verification_state": "verified",
            "validation_results": (
                ValidationResult(code="missing_evidence_span", outcome="pass"),
                ValidationResult(code="personal_data_high_confidence", outcome="pass"),
                ValidationResult(code="possible_personal_name", outcome="pass"),
            ),
        }
    )
    with LocalPipelineStore(tmp_path / "pipeline.sqlite3") as store:
        store.record_retrieval_artifact(retrieval(), artifact())
        store.record_claim(eligible)
        fragment = reconstruct_milestone_fragment(store, "C-014")

    assert "claim-1 — withheld" in fragment
    assert "Baubeginn 2026" not in fragment


def test_claim_with_mismatched_evidence_offsets_is_withheld(tmp_path) -> None:
    eligible = claim().model_copy(
        update={
            "review_state": "accepted",
            "publication_eligibility": "eligible",
            "verification_state": "verified",
            "validation_results": (
                ValidationResult(code="missing_evidence_span", outcome="pass"),
                ValidationResult(code="personal_data_high_confidence", outcome="pass"),
                ValidationResult(code="possible_personal_name", outcome="pass"),
            ),
            "evidence_spans": (
                claim().evidence_spans[0].model_copy(update={"start": 0, "end": 14}),
            ),
        }
    )
    with LocalPipelineStore(tmp_path / "pipeline.sqlite3") as store:
        store.record_retrieval_artifact(retrieval(), artifact())
        store.record_claim(eligible)
        store.record_review_decision(review_decision())
        fragment = reconstruct_milestone_fragment(store, "C-014")

    assert "claim-1 — withheld" in fragment
    assert "Baubeginn 2026" not in fragment


def test_latest_review_decision_controls_rendering(tmp_path) -> None:
    eligible = claim().model_copy(
        update={
            "review_state": "accepted",
            "publication_eligibility": "eligible",
            "verification_state": "verified",
            "validation_results": (
                ValidationResult(code="missing_evidence_span", outcome="pass"),
                ValidationResult(code="personal_data_high_confidence", outcome="pass"),
                ValidationResult(code="possible_personal_name", outcome="pass"),
            ),
        }
    )
    accepted = review_decision().model_copy(
        update={"created_at": datetime.fromisoformat("2026-08-07T14:00:00+02:00")}
    )
    rejected = review_decision().model_copy(
        update={
            "review_decision_id": "review-2",
            "decision": "reject",
            "prior_state": "accepted",
            "created_at": datetime.fromisoformat("2026-08-07T13:00:00+00:00"),
            "rationale": "Later review withdrew publication approval.",
        }
    )
    with LocalPipelineStore(tmp_path / "pipeline.sqlite3") as store:
        store.record_retrieval_artifact(retrieval(), artifact())
        store.record_claim(eligible)
        store.record_review_decision(accepted)
        store.record_review_decision(rejected)
        fragment = reconstruct_milestone_fragment(store, "C-014")

    assert "claim-1 — withheld" in fragment
    assert "Baubeginn 2026" not in fragment


def test_empty_project_cannot_vacuously_reconstruct(tmp_path) -> None:
    with LocalPipelineStore(tmp_path / "pipeline.sqlite3") as store:
        try:
            reconstruct_milestone_fragment(store, "C-014")
        except IncompleteReconstruction as exc:
            assert str(exc) == "project has no stored milestone claims"
        else:  # pragma: no cover
            raise AssertionError("empty reconstruction should fail")
