from __future__ import annotations

from datetime import UTC, date, datetime
from decimal import Decimal
import hashlib
import json

import pytest

from pipeline.schemas import (
    ActiveMilestoneClaim,
    Confidence,
    DateValue,
    HtmlEvidenceSpan,
    ValidationResult,
)
from pipeline.store import (
    ArtifactRecord,
    ExtractionRunRecord,
    LocalPipelineStore,
    PdfTimestampRecord,
    PublicationDateRecord,
    RetrievalRecord,
    ReviewDecisionRecord,
    StoreInvariantError,
)


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
        publication_date=PublicationDateRecord(
            status="verified",
            value=date(2026, 8, 7),
            provenance=("source-page",),
        ),
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
                start=6,
                end=20,
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


def review_decision() -> ReviewDecisionRecord:
    return ReviewDecisionRecord(
        schema_version="1.0.0",
        review_decision_id="review-1",
        project_id="C-014",
        claim_id="claim-1",
        decision="accept",
        actor_class="qualified_human_reviewer",
        created_at=NOW,
        prior_state="proposed",
        rationale="Approved for the reviewed display state.",
    )


def test_project_records_survive_store_reopen(tmp_path) -> None:
    database = tmp_path / "pipeline.sqlite3"

    with LocalPipelineStore(database) as store:
        store.record_retrieval_artifact(retrieval(), artifact())
        store.record_claim(claim())
        store.record_review_decision(review_decision())

    with LocalPipelineStore(database) as reopened:
        records = reopened.load_project("C-014")

    assert records.retrievals == (retrieval(),)
    assert records.artifacts == (artifact(),)
    assert records.milestone_claims == (claim(),)
    assert records.review_decisions == (review_decision(),)


def test_pdf_artifact_retains_extracted_timestamps(tmp_path) -> None:
    stored_bytes = b"%PDF-retention-record"
    stored_hash = hashlib.sha256(stored_bytes).hexdigest()
    retained = ArtifactRecord(
        schema_version="1.0.0",
        artifact_id=stored_hash,
        media_type="application/pdf",
        byte_length=len(stored_bytes),
        retained_private=True,
        hash_algorithm="sha256",
        pre_transform_response_hash="b" * 64,
        stored_content_hash=stored_hash,
        stored_bytes=stored_bytes,
        transform_rule_version="pdf-metadata-strip/v1",
        transform_checks=("forbidden_metadata_absent",),
        extracted_pdf_timestamps=PdfTimestampRecord(
            creation_date="D:20260807120000+02'00'",
            modification_date=None,
        ),
        created_at=NOW,
    )
    pdf_retrieval = retrieval().model_copy(update={"artifact_id": stored_hash})

    with LocalPipelineStore(tmp_path / "pipeline.sqlite3") as store:
        store.record_retrieval_artifact(pdf_retrieval, retained)
        assert store.load_project("C-014").artifacts == (retained,)


def test_pdf_artifact_without_timestamp_provenance_is_rejected() -> None:
    stored_bytes = b"%PDF-missing-provenance"
    stored_hash = hashlib.sha256(stored_bytes).hexdigest()

    with pytest.raises(ValueError, match="timestamp provenance"):
        ArtifactRecord(
            schema_version="1.0.0",
            artifact_id=stored_hash,
            media_type="application/pdf",
            byte_length=len(stored_bytes),
            retained_private=True,
            hash_algorithm="sha256",
            pre_transform_response_hash="b" * 64,
            stored_content_hash=stored_hash,
            stored_bytes=stored_bytes,
            transform_rule_version="pdf-metadata-strip/v1",
            transform_checks=("forbidden_metadata_absent",),
            created_at=NOW,
        )


def test_review_decision_requires_a_stored_claim_and_is_immutable(tmp_path) -> None:
    database = tmp_path / "pipeline.sqlite3"
    with LocalPipelineStore(database) as store:
        with pytest.raises(StoreInvariantError):
            store.record_review_decision(review_decision())

        store.record_retrieval_artifact(retrieval(), artifact())
        store.record_claim(claim())
        store.record_review_decision(review_decision())
        store.record_review_decision(review_decision())

        conflicting = review_decision().model_copy(update={"decision": "reject"})
        with pytest.raises(StoreInvariantError):
            store.record_review_decision(conflicting)

        same_timestamp_revocation = review_decision().model_copy(
            update={
                "review_decision_id": "review-a",
                "decision": "reject",
                "prior_state": "accepted",
                "rationale": "Approval withdrawn at an ambiguous timestamp.",
            }
        )
        with pytest.raises(StoreInvariantError, match="strictly increase"):
            store.record_review_decision(same_timestamp_revocation)


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


def test_extraction_run_metrics_round_trip_without_model_content(tmp_path) -> None:
    database = tmp_path / "pipeline.sqlite3"
    run = ExtractionRunRecord.model_validate_json(json.dumps({
        "run_id": "run-1", "project_id": "C-014", "artifact_id": STORED_HASH,
        "provider_request_id": "resp_123", "created_at": "2026-08-07T12:00:00+02:00",
        "metrics": {"provider": "openai", "model": "gpt-5.6-luna", "model_version": "gpt-5.6-luna", "prompt_version": "milestone-extraction-de-v1", "extraction_schema_version": "1.0.0", "input_tokens": 10, "output_tokens": 2, "cached_tokens": 1, "cache_write_tokens": 0, "latency_ms": 30, "cost_amount": "0.0000036", "cost_currency": "USD", "pricing_reference": "openai-gpt-5.6-luna-2026-08-07"},
        "validation_results": [{"code": "personal_data_high_confidence", "outcome": "pass"}, {"code": "possible_personal_name", "outcome": "pass"}],
    }))
    with LocalPipelineStore(database) as store:
        store.record_retrieval_artifact(retrieval(), artifact())
        store.record_extraction_run(run, (claim(),))
        assert store.load_extraction_runs("C-014") == (run,)
        assert store.load_project("C-014").milestone_claims == (claim(),)


def test_extraction_run_and_all_claims_commit_atomically(tmp_path) -> None:
    database = tmp_path / "pipeline.sqlite3"
    run = ExtractionRunRecord.model_validate_json(json.dumps({
        "run_id": "run-atomic", "project_id": "C-014", "artifact_id": STORED_HASH,
        "provider_request_id": "resp_123", "created_at": "2026-08-07T12:00:00+02:00",
        "metrics": {"provider": "openai", "model": "gpt-5.6-luna", "model_version": "gpt-5.6-luna", "prompt_version": "milestone-extraction-de-v1", "extraction_schema_version": "1.0.0", "input_tokens": 10, "output_tokens": 2, "cached_tokens": 1, "cache_write_tokens": 0, "latency_ms": 30, "cost_amount": "0.0000036", "cost_currency": "USD", "pricing_reference": "openai-gpt-5.6-luna-2026-08-07"},
        "validation_results": [{"code": "personal_data_high_confidence", "outcome": "pass"}],
    }))
    invalid = claim().model_copy(update={"claim_id": "claim-2", "source_id": "missing-source"})

    with LocalPipelineStore(database) as store:
        store.record_retrieval_artifact(retrieval(), artifact())
        with pytest.raises(StoreInvariantError):
            store.record_extraction_run(run, (claim(), invalid))

        assert store.load_extraction_runs("C-014") == ()
        assert store.load_project("C-014").milestone_claims == ()
