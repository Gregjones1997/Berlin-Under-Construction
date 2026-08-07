from __future__ import annotations

import json

import httpx

from pipeline.metering import ProviderRequest
from pipeline.openai_provider import OpenAIResponsesProvider


def test_openai_adapter_disables_retention_and_reports_exact_usage() -> None:
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured.update(json.loads(request.content))
        return httpx.Response(200, headers={"x-request-id": "resp_123"}, json={"output": [{"type": "message", "content": [{"type": "output_text", "text": '{"proposed_claims":[]}'}]}], "usage": {"input_tokens": 12, "input_tokens_details": {"cached_tokens": 3, "cache_write_tokens": 2}, "output_tokens": 4}})

    client = httpx.Client(transport=httpx.MockTransport(handler))
    response = OpenAIResponsesProvider(api_key="secret", client=client).extract(ProviderRequest(model="gpt-5.6-luna", prompt="frozen", artifact_text="Baubeginn", threshold_config_version="thresholds-v1", max_output_tokens=2000, reasoning_effort="high", store=False))

    assert captured["store"] is False
    assert captured["tools"] == []
    assert captured["reasoning"] == {"effort": "high"}
    assert captured["text"]["format"]["strict"] is True
    assert response.usage.cached_input_tokens == 3
    assert response.usage.cache_write_input_tokens == 2
    assert response.provider_request_id == "resp_123"
