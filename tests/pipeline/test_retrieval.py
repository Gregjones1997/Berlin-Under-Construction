from pathlib import Path

import httpx
import pytest

from pipeline.retrieval import BrowserToolRequired, retrieve_artifact
from pipeline.retrieval_config import load_retrieval_config


def config():
    return load_retrieval_config(Path("pipeline/config/retrieval.v1.toml"))[0]


def test_403_is_recorded_and_retried_with_browser_user_agent() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls == 1:
            return httpx.Response(403, request=request)
        return httpx.Response(
            200,
            content=b"<main>Baubeginn</main>",
            headers={"content-type": "text/html; charset=utf-8"},
            request=request,
        )

    with httpx.Client(transport=httpx.MockTransport(handler), follow_redirects=True) as client:
        result = retrieve_artifact("https://example.invalid/source", config(), client=client)

    assert [attempt.outcome for attempt in result.attempts] == ["access_barrier", "received"]
    assert result.attempts[1].user_agent_class == "browser"


def test_two_403_responses_require_browser_tool_before_manual_escalation() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(403, request=request)

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(BrowserToolRequired):
            retrieve_artifact("https://example.invalid/source", config(), client=client)
