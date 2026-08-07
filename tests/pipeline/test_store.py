from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
import hashlib

import pytest

from pipeline.schemas import (
    ActiveMilestoneClaim,
    Confidence,
    DateValue,
    HtmlEvidenceSpan,
    ValidationResult,
)
from pipeline.store import ArtifactRecord, LocalPipelineStore, RetrievalRecord
from pipeline.store import StoreInvariantError


NOW = datetime(2026, 8, 7, 12, 0, tzinfo=UTC)
STORED_BYTES = b"<main>Baubeginn 2026</main>"
STORED_HASH = hashlib.sha256(STORED_BYTES).hexdigest()


def artifact() -> ArtifactRecord:
    return ArtifactRecord(
        schema_version="1.0.0",
        artifact_id=STORED_HASH,
        media_type="text/html",
        byte_length=len(STORED_BYTES),
        retained_private=True,
        hash_algorithm="sha256",
        pre_transform_response_hash=STORED_HASH,
        stored_content_hash=STORED_HASH,
        stored_bytes=STORED_BYTES,
        transform_rule_version="identity/v1",
        transform_checks=("identity_hashes_equal",),
        created_at=NOW,
    )


def retrieval() -> RetrievalRecord:
    return RetrievalRecord(
        schema_version="1.0.0",
        retrieval_id="retrieval-1",
        project_id="C-014",
        source_id="source-1",
        artifact_id=STORED_HASH,
        retrieved_at=NOW,
        request_url="https://www.berlin.de/source",
        final_url="https://www.berlin.de/source",
        http_status=200,
        outcome="received",
        user_agent_class="default",
        retry_number=0,
    )


def claim() -> ActiveMilestoneClaim:
    return ActiveMilestoneClaim(
        claim_id="claim-1",
        project_id="C-014",
        schema_version="1.0.0",
        claim_kind="milestone",
        canonical_value_de="Baubeginn 2026",
        source_id="source-1",
        artifact_id=STORED_HASH,
        evidence_spans=(
            HtmlEvidenceSpan(
                kind="html",
                exact_text_de="Baubeginn 2026",
                selector="main",
                start=0,
                end=14,
            ),
        ),
        qualifiers=(),
        confidence=Confidence(
            score=Decimal("0.8"),
            source="extractor",
            threshold_config_version="thresholds-v1",
        ),
        review_state="proposed",
        validation_results=(
            ValidationResult(code="missing_evidence_span", outcome="pass"),
        ),
        relations=(),
        created_at=NOW,
        milestone_type="construction_start",
        milestone_term_de="Baubeginn",
        object_scope="Baumaßnahme",
        date_value=DateValue(precision="year", canonical="2026"),
        publication_eligibility="review_required",
        verification_state="unverified",
    )


def test_project_records_survive_store_reopen(tmp_path) -> None:
    database = tmp_path / "pipeline.sqlite3"

    with LocalPipelineStore(database) as store:
        store.record_retrieval_artifact(retrieval(), artifact())
        store.record_claim(claim())

    with LocalPipelineStore(database) as reopened:
        records = reopened.load_project("C-014")

    assert records.retrievals == (retrieval(),)
    assert records.artifacts == (artifact(),)
    assert records.milestone_claims == (claim(),)


def test_identical_replay_is_idempotent_but_conflicting_id_is_rejected(tmp_path) -> None:
    database = tmp_path / "pipeline.sqlite3"
    with LocalPipelineStore(database) as store:
        store.record_retrieval_artifact(retrieval(), artifact())
        store.record_retrieval_artifact(retrieval(), artifact())

        conflicting = retrieval().model_copy(update={"source_id": "different-source"})
        with pytest.raises(StoreInvariantError):
            store.record_retrieval_artifact(conflicting, artifact())

        assert store.load_project("C-014").retrievals == (retrieval(),)


def test_claim_must_match_a_stored_project_source_and_artifact(tmp_path) -> None:
    with LocalPipelineStore(tmp_path / "pipeline.sqlite3") as store:
        store.record_retrieval_artifact(retrieval(), artifact())
        mismatched = claim().model_copy(update={"source_id": "different-source"})

        with pytest.raises(StoreInvariantError):
            store.record_claim(mismatched)


def test_local_database_is_private(tmp_path) -> None:
    database = tmp_path / "pipeline.sqlite3"
    with LocalPipelineStore(database):
        pass

    assert database.stat().st_mode & 0o777 == 0o600
