from __future__ import annotations

import json
import hashlib
import os
import sqlite3
from datetime import UTC, date
from pathlib import Path
from typing import Literal, Self

from pydantic import AwareDatetime, ConfigDict, Field, model_validator

from pipeline.schemas import (
    ActiveMilestoneClaim,
    QuarantinedMilestoneClaim,
    StrictModel,
    ExtractionMetrics,
    ValidationResult,
    milestone_claim_adapter,
)


class StoreInvariantError(ValueError):
    pass


class PdfTimestampRecord(StrictModel):
    creation_date: str | None
    modification_date: str | None


class PublicationDateRecord(StrictModel):
    status: Literal["not_checked", "verified", "not_stated", "unresolved"]
    value: date | None = None
    provenance: tuple[str, ...] = ()

    @model_validator(mode="after")
    def verified_values_require_provenance(self) -> "PublicationDateRecord":
        if self.status == "verified":
            if self.value is None or not self.provenance:
                raise ValueError("verified publication dates require a value and provenance")
        elif self.value is not None:
            raise ValueError("only verified publication dates may carry a value")
        return self


class ArtifactRecord(StrictModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
        frozen=True,
        ser_json_bytes="base64",
        val_json_bytes="base64",
    )

    schema_version: str = Field(min_length=1)
    artifact_id: str = Field(pattern=r"^[0-9a-f]{64}$")
    media_type: str = Field(min_length=1)
    byte_length: int = Field(ge=0)
    retained_private: Literal[True]
    hash_algorithm: Literal["sha256"]
    pre_transform_response_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    stored_content_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    stored_bytes: bytes
    transform_rule_version: str = Field(min_length=1)
    transform_checks: tuple[str, ...] = Field(min_length=1)
    extracted_pdf_timestamps: PdfTimestampRecord | None = None
    created_at: AwareDatetime

    @model_validator(mode="after")
    def identity_is_the_stored_hash(self) -> "ArtifactRecord":
        if self.artifact_id != self.stored_content_hash:
            raise ValueError("artifact_id must equal stored_content_hash")
        if len(self.stored_bytes) != self.byte_length:
            raise ValueError("byte_length must match stored_bytes")
        if hashlib.sha256(self.stored_bytes).hexdigest() != self.stored_content_hash:
            raise ValueError("stored_content_hash must match stored_bytes")
        if (
            self.transform_rule_version == "identity/v1"
            and self.pre_transform_response_hash != self.stored_content_hash
        ):
            raise ValueError("identity transforms require equal hash roles")
        media_type = self.media_type.partition(";")[0].strip().lower()
        if media_type == "application/pdf" and self.extracted_pdf_timestamps is None:
            raise ValueError("PDF artifacts require extracted timestamp provenance")
        if media_type != "application/pdf" and self.extracted_pdf_timestamps is not None:
            raise ValueError("only PDF artifacts may carry extracted PDF timestamps")
        return self


class RetrievalRecord(StrictModel):
    schema_version: str = Field(min_length=1)
    retrieval_id: str = Field(min_length=1)
    project_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    artifact_id: str = Field(pattern=r"^[0-9a-f]{64}$")
    retrieved_at: AwareDatetime
    request_url: str = Field(pattern=r"^https://")
    final_url: str = Field(pattern=r"^https://")
    http_status: int = Field(ge=100, le=599)
    outcome: Literal["received"]
    user_agent_class: Literal["default", "browser"]
    retry_number: int = Field(ge=0)
    publication_date: PublicationDateRecord = Field(
        default_factory=lambda: PublicationDateRecord(status="not_checked")
    )


class ReviewDecisionRecord(StrictModel):
    """Append-only, name-free proof of the human publication decision."""

    schema_version: str = Field(min_length=1)
    review_decision_id: str = Field(min_length=1)
    project_id: str = Field(min_length=1)
    claim_id: str = Field(min_length=1)
    decision: Literal["accept", "reject", "correct", "defer", "quarantine"]
    actor_class: Literal["project_owner", "qualified_human_reviewer"]
    created_at: AwareDatetime
    prior_state: Literal["proposed", "accepted", "rejected", "deferred"]
    rationale: str = Field(min_length=1)


class ProjectRecords(StrictModel):
    retrievals: tuple[RetrievalRecord, ...]
    artifacts: tuple[ArtifactRecord, ...]
    milestone_claims: tuple[ActiveMilestoneClaim | QuarantinedMilestoneClaim, ...]
    review_decisions: tuple[ReviewDecisionRecord, ...]


class ExtractionRunRecord(StrictModel):
    """Safe run metadata; raw provider output is intentionally not persisted."""

    run_id: str = Field(min_length=1)
    project_id: str = Field(min_length=1)
    artifact_id: str = Field(pattern=r"^[0-9a-f]{64}$")
    provider_request_id: str = Field(min_length=1)
    created_at: AwareDatetime
    metrics: ExtractionMetrics
    validation_results: tuple[ValidationResult, ...]


def _canonical_json(model: StrictModel) -> str:
    return json.dumps(
        model.model_dump(mode="json"),
        sort_keys=True,
        separators=(",", ":"),
    )


class LocalPipelineStore:
    """Transactional SQLite adapter for the local pipeline persistence seam."""

    def __init__(self, path: Path) -> None:
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(path)
        os.chmod(path, 0o600)
        self._connection.execute("PRAGMA foreign_keys = ON")
        self._create_schema()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.close()

    def close(self) -> None:
        self._connection.close()

    def _create_schema(self) -> None:
        self._connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS artifacts (
                artifact_id TEXT PRIMARY KEY,
                stored_bytes BLOB NOT NULL,
                record_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS retrievals (
                retrieval_id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                source_id TEXT NOT NULL,
                artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id),
                retrieved_at TEXT NOT NULL,
                record_json TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS retrievals_project_idx
                ON retrievals(project_id, retrieved_at, retrieval_id);
            CREATE TABLE IF NOT EXISTS milestone_claims (
                claim_id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id),
                created_at TEXT NOT NULL,
                record_json TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS milestone_claims_project_idx
                ON milestone_claims(project_id, created_at, claim_id);
            CREATE TABLE IF NOT EXISTS review_decisions (
                review_decision_id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                claim_id TEXT NOT NULL REFERENCES milestone_claims(claim_id),
                created_at TEXT NOT NULL,
                record_json TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS review_decisions_project_idx
                ON review_decisions(project_id, created_at, review_decision_id);
            CREATE TABLE IF NOT EXISTS extraction_runs (
                run_id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id),
                created_at TEXT NOT NULL,
                record_json TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS extraction_runs_project_idx
                ON extraction_runs(project_id, created_at, run_id);
            CREATE TRIGGER IF NOT EXISTS artifacts_no_update
                BEFORE UPDATE ON artifacts BEGIN SELECT RAISE(ABORT, 'append-only'); END;
            CREATE TRIGGER IF NOT EXISTS artifacts_no_delete
                BEFORE DELETE ON artifacts BEGIN SELECT RAISE(ABORT, 'append-only'); END;
            CREATE TRIGGER IF NOT EXISTS retrievals_no_update
                BEFORE UPDATE ON retrievals BEGIN SELECT RAISE(ABORT, 'append-only'); END;
            CREATE TRIGGER IF NOT EXISTS retrievals_no_delete
                BEFORE DELETE ON retrievals BEGIN SELECT RAISE(ABORT, 'append-only'); END;
            CREATE TRIGGER IF NOT EXISTS milestone_claims_no_update
                BEFORE UPDATE ON milestone_claims BEGIN SELECT RAISE(ABORT, 'append-only'); END;
            CREATE TRIGGER IF NOT EXISTS milestone_claims_no_delete
                BEFORE DELETE ON milestone_claims BEGIN SELECT RAISE(ABORT, 'append-only'); END;
            CREATE TRIGGER IF NOT EXISTS review_decisions_no_update
                BEFORE UPDATE ON review_decisions BEGIN SELECT RAISE(ABORT, 'append-only'); END;
            CREATE TRIGGER IF NOT EXISTS review_decisions_no_delete
                BEFORE DELETE ON review_decisions BEGIN SELECT RAISE(ABORT, 'append-only'); END;
            CREATE TRIGGER IF NOT EXISTS extraction_runs_no_update
                BEFORE UPDATE ON extraction_runs BEGIN SELECT RAISE(ABORT, 'append-only'); END;
            CREATE TRIGGER IF NOT EXISTS extraction_runs_no_delete
                BEFORE DELETE ON extraction_runs BEGIN SELECT RAISE(ABORT, 'append-only'); END;
            """
        )

    def _insert_immutable(
        self, table: str, key_column: str, key: str, values: dict[str, object]
    ) -> None:
        columns = (key_column, *values.keys())
        placeholders = ",".join("?" for _ in columns)
        sql = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})"
        parameters = (key, *values.values())
        try:
            self._connection.execute(sql, parameters)
        except sqlite3.IntegrityError as exc:
            selected = ",".join(values.keys())
            existing = self._connection.execute(
                f"SELECT {selected} FROM {table} WHERE {key_column} = ?", (key,)
            ).fetchone()
            if existing is None or existing != tuple(values.values()):
                raise StoreInvariantError(f"immutable {table} record {key!r} conflicts") from exc

    def record_retrieval_artifact(
        self, retrieval: RetrievalRecord, artifact: ArtifactRecord
    ) -> None:
        if retrieval.artifact_id != artifact.artifact_id:
            raise StoreInvariantError("retrieval must reference the supplied stored artifact")
        with self._connection:
            self._insert_immutable(
                "artifacts",
                "artifact_id",
                artifact.artifact_id,
                {
                    "stored_bytes": artifact.stored_bytes,
                    "record_json": _canonical_json(artifact),
                },
            )
            self._insert_immutable(
                "retrievals",
                "retrieval_id",
                retrieval.retrieval_id,
                {
                    "project_id": retrieval.project_id,
                    "source_id": retrieval.source_id,
                    "artifact_id": retrieval.artifact_id,
                    "retrieved_at": retrieval.retrieved_at.isoformat(),
                    "record_json": _canonical_json(retrieval),
                },
            )

    def record_claim(
        self, claim: ActiveMilestoneClaim | QuarantinedMilestoneClaim
    ) -> None:
        with self._connection:
            self._record_claim(claim)

    def _record_claim(
        self, claim: ActiveMilestoneClaim | QuarantinedMilestoneClaim
    ) -> None:
        matching_retrieval = self._connection.execute(
            """
            SELECT 1 FROM retrievals
            WHERE project_id = ? AND source_id = ? AND artifact_id = ?
            """,
            (claim.project_id, claim.source_id, claim.artifact_id),
        ).fetchone()
        if matching_retrieval is None:
            raise StoreInvariantError(
                "claim project, source and artifact must match a stored retrieval"
            )
        self._insert_immutable(
            "milestone_claims",
            "claim_id",
            claim.claim_id,
            {
                "project_id": claim.project_id,
                "artifact_id": claim.artifact_id,
                "created_at": claim.created_at.isoformat(),
                "record_json": _canonical_json(claim),
            },
        )

    def load_project(self, project_id: str) -> ProjectRecords:
        retrieval_json = self._connection.execute(
            """
            SELECT record_json FROM retrievals
            WHERE project_id = ? ORDER BY retrieved_at, retrieval_id
            """,
            (project_id,),
        ).fetchall()
        artifact_rows = self._connection.execute(
            """
            SELECT DISTINCT artifacts.record_json, artifacts.stored_bytes FROM artifacts
            JOIN retrievals USING (artifact_id)
            WHERE retrievals.project_id = ? ORDER BY artifacts.artifact_id
            """,
            (project_id,),
        ).fetchall()
        claim_json = self._connection.execute(
            """
            SELECT record_json FROM milestone_claims
            WHERE project_id = ? ORDER BY created_at, claim_id
            """,
            (project_id,),
        ).fetchall()
        review_json = self._connection.execute(
            """
            SELECT record_json FROM review_decisions
            WHERE project_id = ? ORDER BY created_at, review_decision_id
            """,
            (project_id,),
        ).fetchall()
        return ProjectRecords(
            retrievals=tuple(RetrievalRecord.model_validate_json(row[0]) for row in retrieval_json),
            artifacts=tuple(self._load_artifact(row[0], row[1]) for row in artifact_rows),
            milestone_claims=tuple(
                milestone_claim_adapter.validate_json(row[0]) for row in claim_json
            ),
            review_decisions=tuple(
                ReviewDecisionRecord.model_validate_json(row[0]) for row in review_json
            ),
        )

    def record_review_decision(self, decision: ReviewDecisionRecord) -> None:
        with self._connection:
            matching_claim = self._connection.execute(
                """
                SELECT 1 FROM milestone_claims
                WHERE claim_id = ? AND project_id = ?
                """,
                (decision.claim_id, decision.project_id),
            ).fetchone()
            if matching_claim is None:
                raise StoreInvariantError(
                    "review decision must reference a stored claim in the same project"
                )
            existing_row = self._connection.execute(
                """
                SELECT record_json FROM review_decisions
                WHERE review_decision_id = ?
                """,
                (decision.review_decision_id,),
            ).fetchone()
            if existing_row is not None:
                existing = ReviewDecisionRecord.model_validate_json(existing_row[0])
                if existing == decision:
                    return
                raise StoreInvariantError(
                    f"immutable review_decisions record {decision.review_decision_id!r} conflicts"
                )
            latest_row = self._connection.execute(
                """
                SELECT record_json FROM review_decisions
                WHERE claim_id = ?
                ORDER BY created_at DESC, review_decision_id DESC
                LIMIT 1
                """,
                (decision.claim_id,),
            ).fetchone()
            if latest_row is not None:
                latest = ReviewDecisionRecord.model_validate_json(latest_row[0])
                if decision.created_at <= latest.created_at:
                    raise StoreInvariantError(
                        "review decision timestamps must strictly increase per claim"
                    )
            self._insert_immutable(
                "review_decisions",
                "review_decision_id",
                decision.review_decision_id,
                {
                    "project_id": decision.project_id,
                    "claim_id": decision.claim_id,
                    "created_at": decision.created_at.astimezone(UTC).isoformat(),
                    "record_json": _canonical_json(decision),
                },
            )

    def record_extraction_run(
        self,
        run: ExtractionRunRecord,
        claims: tuple[ActiveMilestoneClaim | QuarantinedMilestoneClaim, ...],
    ) -> None:
        """Atomically persist one extraction run and every claim it produced."""

        with self._connection:
            matching_retrieval = self._connection.execute(
                "SELECT 1 FROM retrievals WHERE project_id = ? AND artifact_id = ?",
                (run.project_id, run.artifact_id),
            ).fetchone()
            if matching_retrieval is None:
                raise StoreInvariantError(
                    "extraction run project and artifact must match a stored retrieval"
                )
            self._insert_immutable(
                "extraction_runs", "run_id", run.run_id,
                {"project_id": run.project_id, "artifact_id": run.artifact_id, "created_at": run.created_at.isoformat(), "record_json": _canonical_json(run)},
            )
            for claim in claims:
                if claim.project_id != run.project_id or claim.artifact_id != run.artifact_id:
                    raise StoreInvariantError(
                        "extraction claims must match the run project and artifact"
                    )
                self._record_claim(claim)

    def load_extraction_runs(self, project_id: str) -> tuple[ExtractionRunRecord, ...]:
        rows = self._connection.execute(
            "SELECT record_json FROM extraction_runs WHERE project_id = ? ORDER BY created_at, run_id",
            (project_id,),
        ).fetchall()
        return tuple(ExtractionRunRecord.model_validate_json(row[0]) for row in rows)

    @staticmethod
    def _load_artifact(record_json: str, stored_bytes: bytes) -> ArtifactRecord:
        artifact = ArtifactRecord.model_validate_json(record_json)
        if artifact.stored_bytes != stored_bytes:
            raise StoreInvariantError("stored artifact bytes do not match their typed record")
        return artifact
