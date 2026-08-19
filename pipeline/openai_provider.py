from __future__ import annotations

import logging
from time import perf_counter

import httpx

from pipeline.metering import MeteringRejected, ProviderRequest, ProviderResponse, ProviderUsage
from pipeline.schemas import ExtractionOutput


logger = logging.getLogger(__name__)


def _billed_usage(payload: object) -> dict[str, int] | None:
    """Return content-free token counts from a rejected response; never raise."""

    if not isinstance(payload, dict):
        return None
    usage = payload.get("usage")
    if not isinstance(usage, dict):
        return None
    details = usage.get("input_tokens_details")
    cached = details.get("cached_tokens") if isinstance(details, dict) else 0
    counts = {
        "input_tokens": usage.get("input_tokens"),
        "output_tokens": usage.get("output_tokens"),
        "cached_input_tokens": cached if cached is not None else 0,
        "cache_write_input_tokens": 0,
    }
    if any(
        isinstance(value, bool) or not isinstance(value, int) or value < 0
        for value in counts.values()
    ):
        return None
    return counts


class OpenAIResponsesProvider:
    """Minimal no-retention Responses API adapter; errors never include model content."""

    def __init__(self, *, api_key: str, client: httpx.Client | None = None) -> None:
        if not api_key:
            raise MeteringRejected("missing_provider_credential")
        self._api_key = api_key
        self._client = client or httpx.Client(timeout=60)
        self._usage_keys_logged = False

    def extract(self, request: ProviderRequest) -> ProviderResponse:
        body = {
            "model": request.model,
            "store": request.store,
            "tools": [],
            "reasoning": {"effort": request.reasoning_effort},
            "max_output_tokens": request.max_output_tokens,
            "input": [
                {"role": "system", "content": f"{request.prompt}\n\nTrusted threshold_config_version: {request.threshold_config_version}"},
                {"role": "user", "content": f"<untrusted_source_document>\n{request.artifact_text}\n</untrusted_source_document>"},
            ],
            "text": {"format": {"type": "json_schema", "name": "milestone_extraction", "strict": False, "schema": ExtractionOutput.model_json_schema()}},
        }
        started = perf_counter()
        try:
            response = self._client.post(
                "https://api.openai.com/v1/responses",
                headers={"Authorization": f"Bearer {self._api_key}"},
                json=body,
            )
            if response.is_error:
                error_type = None
                error_code = None
                try:
                    error_payload = response.json()
                    error = (
                        error_payload.get("error", {})
                        if isinstance(error_payload, dict)
                        else {}
                    )
                    if isinstance(error, dict):
                        error_type = error.get("type") if isinstance(error.get("type"), str) else None
                        error_code = error.get("code") if isinstance(error.get("code"), str) else None
                except (ValueError, TypeError):
                    pass
                raise MeteringRejected(
                    "provider_http_error",
                    http_status=response.status_code,
                    provider_error_type=error_type,
                    provider_error_code=error_code,
                )
            payload = response.json()
            if payload.get("status") == "incomplete":
                details = payload.get("incomplete_details", {})
                reason = details.get("reason") if isinstance(details, dict) else None
                raise MeteringRejected(
                    "provider_response_incomplete",
                    incomplete_reason=reason if isinstance(reason, str) else None,
                    billed_usage=_billed_usage(payload),
                    latency_ms=round((perf_counter() - started) * 1000),
                )
            output_texts = [content["text"] for item in payload["output"] if item.get("type") == "message" for content in item.get("content", []) if content.get("type") == "output_text"]
            if len(output_texts) != 1:
                raise MeteringRejected(
                    "provider_output_shape",
                    billed_usage=_billed_usage(payload),
                    latency_ms=round((perf_counter() - started) * 1000),
                )
            usage = payload["usage"]
            details = usage.get("input_tokens_details", {})
            if not self._usage_keys_logged:
                logger.info(
                    "OpenAI usage keys: usage=%s input_tokens_details=%s",
                    sorted(usage),
                    sorted(details) if isinstance(details, dict) else [],
                )
                self._usage_keys_logged = True
            return ProviderResponse(
                output_json=output_texts[0],
                usage=ProviderUsage(
                    input_tokens=usage["input_tokens"],
                    output_tokens=usage["output_tokens"],
                    cached_input_tokens=details.get("cached_tokens", 0),
                    cache_write_input_tokens=0,
                ),
                latency_ms=round((perf_counter() - started) * 1000),
                provider_request_id=response.headers.get("x-request-id", "unavailable"),
                model_version=payload.get("model", request.model),
            )
        except MeteringRejected:
            raise
        except (httpx.HTTPError, KeyError, TypeError, ValueError):
            raise MeteringRejected("provider_request_failed") from None
