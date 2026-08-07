from __future__ import annotations

from time import perf_counter

import httpx

from pipeline.metering import MeteringRejected, ProviderRequest, ProviderResponse, ProviderUsage
from pipeline.schemas import ExtractionOutput


class OpenAIResponsesProvider:
    """Minimal no-retention Responses API adapter; errors never include model content."""

    def __init__(self, *, api_key: str, client: httpx.Client | None = None) -> None:
        if not api_key:
            raise MeteringRejected("missing_provider_credential")
        self._api_key = api_key
        self._client = client or httpx.Client(timeout=60)

    def extract(self, request: ProviderRequest) -> ProviderResponse:
        body = {
            "model": request.model,
            "store": request.store,
            "tools": [],
            "reasoning": {"effort": request.reasoning_effort},
            "max_output_tokens": request.max_output_tokens,
            "input": [
                {"role": "system", "content": request.prompt},
                {"role": "user", "content": f"Trusted threshold_config_version: {request.threshold_config_version}\n\n<untrusted_source_document>\n{request.artifact_text}\n</untrusted_source_document>"},
            ],
            "text": {"format": {"type": "json_schema", "name": "milestone_extraction", "strict": True, "schema": ExtractionOutput.model_json_schema()}},
        }
        started = perf_counter()
        try:
            response = self._client.post(
                "https://api.openai.com/v1/responses",
                headers={"Authorization": f"Bearer {self._api_key}"},
                json=body,
            )
            response.raise_for_status()
            payload = response.json()
            output_texts = [content["text"] for item in payload["output"] if item.get("type") == "message" for content in item.get("content", []) if content.get("type") == "output_text"]
            if len(output_texts) != 1:
                raise MeteringRejected("provider_output_shape")
            usage = payload["usage"]
            details = usage.get("input_tokens_details", {})
            return ProviderResponse(
                output_json=output_texts[0],
                usage=ProviderUsage(
                    input_tokens=usage["input_tokens"],
                    output_tokens=usage["output_tokens"],
                    cached_input_tokens=details.get("cached_tokens", 0),
                    cache_write_input_tokens=details.get("cache_write_tokens", 0),
                ),
                latency_ms=round((perf_counter() - started) * 1000),
                provider_request_id=response.headers.get("x-request-id", "unavailable"),
                model_version=payload.get("model", request.model),
            )
        except MeteringRejected:
            raise
        except (httpx.HTTPError, KeyError, TypeError, ValueError):
            raise MeteringRejected("provider_request_failed") from None
