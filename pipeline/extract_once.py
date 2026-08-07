from __future__ import annotations

import argparse
from datetime import UTC, datetime
import hashlib
import json
import os
from pathlib import Path

from pipeline.metering import (
    ExtractionProvider,
    MeteringPolicy,
    run_metered_extraction,
)
from pipeline.openai_provider import OpenAIResponsesProvider
from pipeline.schemas import ActiveMilestoneClaim, ValidationResult
from pipeline.store import ExtractionRunRecord, LocalPipelineStore, StoreInvariantError


DEFAULT_PROMPT = Path("pipeline/prompts/milestone-extraction-de-v1.md")
DEFAULT_THRESHOLDS = Path("pipeline/config/thresholds.v1.toml")
DEFAULT_PRICING = Path(
    "pipeline/config/pricing.openai-gpt-5.6-luna.2026-08-07.toml"
)
PROMPT_VERSION = "milestone-extraction-de-v1"


def _stable_id(prefix: str, *parts: object) -> str:
    material = "\0".join(str(part) for part in parts).encode("utf-8")
    return f"{prefix}-{hashlib.sha256(material).hexdigest()}"


def extract_once(
    provider: ExtractionProvider,
    *,
    store: LocalPipelineStore,
    project_id: str,
    source_id: str,
    artifact_id: str,
    prompt: str,
    prompt_version: str,
    policy: MeteringPolicy,
) -> dict[str, object]:
    """Run one metered extraction over an existing private stored artifact."""

    records = store.load_project(project_id)
    artifact = next(
        (item for item in records.artifacts if item.artifact_id == artifact_id), None
    )
    retrieval_exists = any(
        item.source_id == source_id and item.artifact_id == artifact_id
        for item in records.retrievals
    )
    if artifact is None or not retrieval_exists:
        raise StoreInvariantError(
            "project, source and artifact must match an existing stored retrieval"
        )

    result = run_metered_extraction(
        provider,
        artifact_bytes=artifact.stored_bytes,
        media_type=artifact.media_type,
        prompt=prompt,
        prompt_version=prompt_version,
        policy=policy,
    )
    created_at = datetime.now(UTC)
    run_id = _stable_id(
        "run",
        project_id,
        artifact_id,
        result.provider_request_id,
        prompt_version,
    )
    validations = (
        ValidationResult(code="missing_evidence_span", outcome="pass"),
        *result.validation_results,
    )
    claims = tuple(
        ActiveMilestoneClaim(
            **proposal.model_dump(),
            claim_id=_stable_id("claim", run_id, index),
            project_id=project_id,
            schema_version="1.0.0",
            source_id=source_id,
            artifact_id=artifact_id,
            qualifiers=(),
            review_state="proposed",
            validation_results=validations,
            relations=(),
            created_at=created_at,
            publication_eligibility="review_required",
            verification_state="unverified",
        )
        for index, proposal in enumerate(result.output.proposed_claims)
    )
    run = ExtractionRunRecord(
        run_id=run_id,
        project_id=project_id,
        artifact_id=artifact_id,
        provider_request_id=result.provider_request_id,
        created_at=created_at,
        metrics=result.metrics,
        validation_results=result.validation_results,
    )
    store.record_extraction_run(run, claims)

    privacy = {
        validation.code: validation.outcome
        for validation in result.validation_results
        if validation.code
        in {"personal_data_high_confidence", "possible_personal_name"}
    }
    return {
        "run_id": run_id,
        "tokens": {
            "input": result.metrics.input_tokens,
            "cached_input": result.metrics.cached_tokens or 0,
            "cache_write_input": result.metrics.cache_write_tokens,
            "output": result.metrics.output_tokens,
        },
        "cost": {
            "amount": str(result.metrics.cost_amount),
            "currency": result.metrics.cost_currency,
        },
        "latency_ms": result.metrics.latency_ms,
        "privacy": privacy,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run one metered extraction over an existing private artifact"
    )
    parser.add_argument("--database", required=True, type=Path)
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--artifact-id", required=True)
    parser.add_argument("--prompt", type=Path, default=DEFAULT_PROMPT)
    parser.add_argument("--thresholds", type=Path, default=DEFAULT_THRESHOLDS)
    parser.add_argument("--pricing", type=Path, default=DEFAULT_PRICING)
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        parser.error("OPENAI_API_KEY is required in the environment")

    policy = MeteringPolicy.load(args.thresholds, args.pricing)
    with LocalPipelineStore(args.database) as store:
        summary = extract_once(
            OpenAIResponsesProvider(api_key=api_key),
            store=store,
            project_id=args.project_id,
            source_id=args.source_id,
            artifact_id=args.artifact_id,
            prompt=args.prompt.read_text(encoding="utf-8"),
            prompt_version=PROMPT_VERSION,
            policy=policy,
        )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
