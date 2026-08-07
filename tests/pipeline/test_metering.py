from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

import pytest

from pipeline.metering import (
    MeteringPolicy,
    MeteringRejected,
    ProviderResponse,
    ProviderUsage,
    run_metered_extraction,
)


ARTIFACT = "Der Baubeginn ist 2026 vorgesehen.".encode()


def valid_output() -> str:
    text = "Baubeginn"
    start = ARTIFACT.decode().index(text)
    return json.dumps(
        {
            "proposed_claims": [
                {
                    "claim_kind": "milestone",
                    "canonical_value_de": text,
                    "evidence_spans": [{"kind": "html", "exact_text_de": text, "selector": "body", "start": start, "end": start + len(text)}],
                    "confidence": {"score": 0.8, "source": "extractor", "threshold_config_version": "thresholds-v1"},
                    "milestone_type": "construction_start",
                    "milestone_term_de": text,
                    "object_scope": "Baumaßnahme",
                    "date_value": {"precision": "year", "canonical": "2026"},
                }
            ]
        },
        ensure_ascii=False,
    )


class FakeProvider:
    def __init__(self, response: ProviderResponse) -> None:
        self.response = response
        self.calls = 0

    def extract(self, request):
        self.calls += 1
        assert request.store is False
        assert request.reasoning_effort == "high"
        assert request.max_output_tokens == 2000
        assert request.threshold_config_version == "thresholds-v1"
        return self.response


def policy() -> MeteringPolicy:
    return MeteringPolicy.load(Path("pipeline/config/thresholds.v1.toml"), Path("pipeline/config/pricing.openai-gpt-5.6-luna.2026-08-07.toml"))


def test_runner_records_exact_usage_cost_latency_and_privacy_results() -> None:
    provider = FakeProvider(ProviderResponse(output_json=valid_output(), usage=ProviderUsage(input_tokens=1000, cached_input_tokens=200, cache_write_input_tokens=100, output_tokens=500), latency_ms=1234, provider_request_id="resp_safe_identifier"))
    result = run_metered_extraction(provider, artifact_bytes=ARTIFACT, media_type="text/html; charset=utf-8", prompt="trusted frozen prompt", prompt_version="milestone-extraction-de-v1", policy=policy())

    assert result.metrics.input_tokens == 1000
    assert result.metrics.cached_tokens == 200
    assert result.metrics.cache_write_tokens == 100
    assert result.metrics.output_tokens == 500
    assert result.metrics.latency_ms == 1234
    assert result.metrics.cost_amount == Decimal("0.000769")
    assert [item.model_dump() for item in result.validation_results] == [
        {"code": "personal_data_high_confidence", "outcome": "pass"},
        {"code": "possible_personal_name", "outcome": "pass"},
    ]


def test_privacy_detection_returns_only_stable_codes_and_never_sensitive_text() -> None:
    raw = valid_output().replace("Baumaßnahme", "Kontakt person@example.invalid")
    provider = FakeProvider(ProviderResponse(output_json=raw, usage=ProviderUsage(input_tokens=10, output_tokens=10), latency_ms=4, provider_request_id="resp_safe_identifier"))

    with pytest.raises(MeteringRejected) as caught:
        run_metered_extraction(provider, artifact_bytes=ARTIFACT, media_type="text/html", prompt="trusted frozen prompt", prompt_version="milestone-extraction-de-v1", policy=policy())

    assert str(caught.value) == "personal_data_high_confidence"
    assert "example" not in str(caught.value)


def test_cost_ceiling_is_checked_before_provider_contact() -> None:
    provider = FakeProvider(ProviderResponse(output_json=valid_output(), usage=ProviderUsage(input_tokens=1, output_tokens=1), latency_ms=1, provider_request_id="unused"))
    with pytest.raises(MeteringRejected, match="input_byte_limit"):
        run_metered_extraction(provider, artifact_bytes=b"x" * 200_001, media_type="text/html", prompt="trusted frozen prompt", prompt_version="milestone-extraction-de-v1", policy=policy())
    assert provider.calls == 0


def test_provider_usage_must_be_auditable() -> None:
    with pytest.raises(ValueError, match="cannot exceed input_tokens"):
        ProviderUsage(input_tokens=1, cached_input_tokens=2, output_tokens=1)
