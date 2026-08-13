from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

import pipeline.extract_once as extract_once_module
from pipeline.extract_once import extract_once
from pipeline.metering import (
    MeteringPolicy,
    MeteringRejected,
    ProviderResponse,
    ProviderUsage,
)
from pipeline.store import LocalPipelineStore
from tests.pipeline.test_metering import valid_output
from tests.pipeline.test_store import artifact, retrieval


class FakeProvider:
    def extract(self, request):
        output = json.loads(valid_output().replace("Baumaßnahme", "Technische Übergabe"))
        output["proposed_claims"][0]["evidence_spans"][0].update(
            {"selector": "main", "start": 6, "end": 15}
        )
        return ProviderResponse(
            output_json=json.dumps(output, ensure_ascii=False),
            usage=ProviderUsage(input_tokens=100, cached_input_tokens=20, output_tokens=30),
            latency_ms=450,
            provider_request_id="resp_safe",
        )


def policy() -> MeteringPolicy:
    return MeteringPolicy.load(
        Path("pipeline/config/thresholds.v1.toml"),
        Path("pipeline/config/pricing.openai-gpt-5.6-luna.2026-08-07.toml"),
    )


def test_extract_once_persists_review_claims_and_returns_safe_metering(tmp_path) -> None:
    with LocalPipelineStore(tmp_path / "pipeline.sqlite3") as store:
        store.record_retrieval_artifact(retrieval(), artifact())
        summary = extract_once(
            FakeProvider(),
            store=store,
            project_id="C-014",
            source_id="source-1",
            artifact_id=artifact().artifact_id,
            prompt="trusted frozen prompt",
            prompt_version="milestone-extraction-de-v1",
            policy=policy(),
        )
        claims = store.load_project("C-014").milestone_claims
        runs = store.load_extraction_runs("C-014")

    assert len(claims) == 1
    assert claims[0].publication_eligibility == "review_required"
    assert claims[0].review_state == "proposed"
    assert any(
        result.code == "possible_personal_name"
        and result.outcome == "review_required"
        for result in claims[0].validation_results
    )
    assert len(runs) == 1
    assert runs[0].run_id == summary["run_id"]
    assert summary["tokens"] == {
        "input": 100,
        "cached_input": 20,
        "cache_write_input": 0,
        "output": 30,
    }
    assert summary["latency_ms"] == 450
    assert summary["privacy"] == {
        "personal_data_high_confidence": "pass",
        "possible_personal_name": "review_required",
    }
    assert "raw_output_private" not in json.dumps(summary)


def test_module_command_refuses_missing_environment_key_even_if_dotenv_exists(tmp_path) -> None:
    (tmp_path / ".env").write_text("OPENAI_API_KEY=must-not-be-read\n", encoding="utf-8")
    environment = os.environ.copy()
    environment.pop("OPENAI_API_KEY", None)
    result = subprocess.run(
        [
            str(Path.cwd() / ".venv/bin/python"),
            "-m",
            "pipeline.extract_once",
            "--database",
            str(tmp_path / "missing.sqlite3"),
            "--project-id",
            "C-014",
            "--source-id",
            "source-1",
            "--artifact-id",
            "a" * 64,
        ],
        cwd=tmp_path,
        env={**environment, "PYTHONPATH": str(Path.cwd())},
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "OPENAI_API_KEY is required in the environment" in result.stderr
    assert "must-not-be-read" not in result.stderr


def test_cli_rejection_prints_failed_accounting_without_persisting(
    tmp_path, monkeypatch, capsys
) -> None:
    database = tmp_path / "pipeline.sqlite3"
    with LocalPipelineStore(database) as store:
        store.record_retrieval_artifact(retrieval(), artifact())

    class RejectingProvider:
        def extract(self, request):
            raise MeteringRejected(
                "provider_response_incomplete",
                incomplete_reason="max_output_tokens",
                billed_usage={
                    "input_tokens": 120,
                    "output_tokens": 40,
                    "cached_input_tokens": 20,
                    "cache_write_input_tokens": 0,
                },
                latency_ms=250,
            )

    monkeypatch.setattr(
        extract_once_module,
        "OpenAIResponsesProvider",
        lambda *, api_key: RejectingProvider(),
    )
    monkeypatch.setenv("OPENAI_API_KEY", "test-only")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "pipeline.extract_once",
            "--database",
            str(database),
            "--project-id",
            "C-014",
            "--source-id",
            "source-1",
            "--artifact-id",
            artifact().artifact_id,
        ],
    )

    with pytest.raises(SystemExit) as caught:
        extract_once_module.main()

    report = json.loads(capsys.readouterr().err)
    assert caught.value.code == 1
    assert report == {
        "failed_attempt_accounting": {
            "cost": {"amount": "0.0000684", "currency": "USD"},
            "tokens": {
                "input_tokens": 120,
                "output_tokens": 40,
                "cached_input_tokens": 20,
                "cache_write_input_tokens": 0,
            },
        },
        "incomplete_reason": "max_output_tokens",
        "latency_ms": 250,
        "rejection_code": "provider_response_incomplete",
    }
    with LocalPipelineStore(database) as store:
        assert store.load_extraction_runs("C-014") == ()
        assert store.load_project("C-014").milestone_claims == ()
