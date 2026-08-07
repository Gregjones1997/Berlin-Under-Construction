from __future__ import annotations

from pipeline.reconstruction import IncompleteReconstruction, reconstruct_milestone_fragment
from pipeline.schemas import ValidationResult
from pipeline.store import LocalPipelineStore
from tests.pipeline.test_store import artifact, claim, retrieval


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


def test_empty_project_cannot_vacuously_reconstruct(tmp_path) -> None:
    with LocalPipelineStore(tmp_path / "pipeline.sqlite3") as store:
        try:
            reconstruct_milestone_fragment(store, "C-014")
        except IncompleteReconstruction as exc:
            assert str(exc) == "project has no stored milestone claims"
        else:  # pragma: no cover
            raise AssertionError("empty reconstruction should fail")
