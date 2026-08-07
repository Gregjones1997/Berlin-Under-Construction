from __future__ import annotations

import json
import logging

import httpx
import pytest

from pipeline.metering import MeteringRejected, ProviderRequest
from pipeline.openai_provider import OpenAIResponsesProvider


def request() -> ProviderRequest:
    return ProviderRequest(model="gpt-5.6-luna", prompt="frozen", artifact_text="Baubeginn", threshold_config_version="thresholds-v1", max_output_tokens=2000, reasoning_effort="high", store=False)


def test_openai_adapter_uses_non_strict_schema_and_reports_openai_usage(caplog) -> None:
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured.update(json.loads(request.content))
        return httpx.Response(200, headers={"x-request-id": "resp_123"}, json={"output": [{"type": "message", "content": [{"type": "output_text", "text": '{"proposed_claims":[]}'}]}], "usage": {"input_tokens": 12, "input_tokens_details": {"cached_tokens": 3}, "output_tokens": 4}})

    client = httpx.Client(transport=httpx.MockTransport(handler))
    with caplog.at_level(logging.INFO):
        response = OpenAIResponsesProvider(api_key="secret", client=client).extract(request())

    assert captured["store"] is False
    assert captured["tools"] == []
    assert captured["reasoning"] == {"effort": "high"}
    assert captured["text"]["format"]["strict"] is False
    assert captured["input"][0]["role"] == "system"
    assert "Trusted threshold_config_version: thresholds-v1" in captured["input"][0]["content"]
    assert "threshold_config_version" not in captured["input"][1]["content"]
    assert response.usage.cached_input_tokens == 3
    assert response.usage.cache_write_input_tokens == 0
    assert response.provider_request_id == "resp_123"
    assert "input_tokens_details" in caplog.text
    assert "cached_tokens" in caplog.text


def test_openai_http_rejection_preserves_safe_diagnostics_only() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            400,
            json={"error": {"type": "invalid_request_error", "code": "invalid_json_schema", "message": "echoed Baubeginn"}},
        )

    provider = OpenAIResponsesProvider(api_key="secret", client=httpx.Client(transport=httpx.MockTransport(handler)))
    with pytest.raises(MeteringRejected) as caught:
        provider.extract(request())

    assert caught.value.http_status == 400
    assert caught.value.provider_error_type == "invalid_request_error"
    assert caught.value.provider_error_code == "invalid_json_schema"
    assert "Baubeginn" not in str(caught.value)


def test_openai_incomplete_response_surfaces_reason() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"status": "incomplete", "incomplete_details": {"reason": "max_output_tokens"}, "output": [], "usage": {}})

    provider = OpenAIResponsesProvider(api_key="secret", client=httpx.Client(transport=httpx.MockTransport(handler)))
    with pytest.raises(MeteringRejected) as caught:
        provider.extract(request())

    assert str(caught.value) == "provider_response_incomplete"
    assert caught.value.incomplete_reason == "max_output_tokens"
