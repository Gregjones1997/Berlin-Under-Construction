from pathlib import Path

import httpx
import pytest

from pipeline.retrieval import (
    BrowserToolRequired,
    DisallowedRedirect,
    ResponseTooLarge,
    RetrievalError,
    UpstreamHttpError,
    retrieve_artifact,
)
from pipeline.retrieval_config import load_retrieval_config


ALLOWED = "https://www.parlament-berlin.de/source"


def config():
    return load_retrieval_config(Path("pipeline/config/retrieval.v1.toml"))[0]


def html(body: bytes = b"<main>Baubeginn</main>") -> dict:
    return {"content": body, "headers": {"content-type": "text/html; charset=utf-8"}}


def client_for(handler) -> httpx.Client:
    return httpx.Client(transport=httpx.MockTransport(handler), follow_redirects=True)


def test_403_is_recorded_and_retried_with_browser_user_agent() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls == 1:
            return httpx.Response(403, request=request)
        return httpx.Response(200, request=request, **html())

    with client_for(handler) as client:
        result = retrieve_artifact(ALLOWED, config(), client=client)

    assert [attempt.outcome for attempt in result.attempts] == ["access_barrier", "received"]
    assert result.attempts[1].user_agent_class == "browser"


def test_two_403_responses_require_browser_tool_before_manual_escalation() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(403, request=request)

    with client_for(handler) as client:
        with pytest.raises(BrowserToolRequired):
            retrieve_artifact(ALLOWED, config(), client=client)


def test_redirect_to_another_host_is_refused() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.host == "www.parlament-berlin.de":
            return httpx.Response(
                302,
                headers={"location": "https://169.254.169.254/latest/meta-data/"},
                request=request,
            )
        return httpx.Response(200, request=request, **html(b"<p>attacker</p>"))

    with client_for(handler) as client:
        with pytest.raises(DisallowedRedirect):
            retrieve_artifact(ALLOWED, config(), client=client)


def test_redirect_downgrading_to_http_is_refused() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.scheme == "https":
            return httpx.Response(
                302,
                headers={"location": "http://www.parlament-berlin.de/source"},
                request=request,
            )
        return httpx.Response(200, request=request, **html())

    with client_for(handler) as client:
        with pytest.raises(DisallowedRedirect):
            retrieve_artifact(ALLOWED, config(), client=client)


def test_a_url_outside_the_allowlist_is_never_fetched() -> None:
    def handler(request: httpx.Request) -> httpx.Response:  # pragma: no cover
        raise AssertionError("no request should be issued")

    with client_for(handler) as client:
        with pytest.raises(DisallowedRedirect):
            retrieve_artifact("https://example.invalid/source", config(), client=client)


def test_same_host_redirect_is_followed_and_recorded() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/source":
            return httpx.Response(
                302,
                headers={"location": "https://www.parlament-berlin.de/final"},
                request=request,
            )
        return httpx.Response(200, request=request, **html())

    with client_for(handler) as client:
        result = retrieve_artifact(ALLOWED, config(), client=client)

    assert [attempt.outcome for attempt in result.attempts] == ["redirect", "received"]
    assert result.attempts[0].final_url == "https://www.parlament-berlin.de/final"


def test_oversize_response_is_refused_without_buffering_it_all() -> None:
    limit = config().http.max_response_bytes
    served = 0

    def handler(request: httpx.Request) -> httpx.Response:
        def stream():
            nonlocal served
            while True:
                served += 65536
                yield b"A" * 65536

        return httpx.Response(
            200, headers={"content-type": "text/html"}, content=stream(), request=request
        )

    with client_for(handler) as client:
        with pytest.raises(ResponseTooLarge):
            retrieve_artifact(ALLOWED, config(), client=client)

    assert served <= limit + 2 * 65536


def test_declared_oversize_content_length_is_refused_before_reading() -> None:
    limit = config().http.max_response_bytes

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            headers={"content-type": "text/html", "content-length": str(limit + 1)},
            content=b"A" * (limit + 1),
            request=request,
        )

    with client_for(handler) as client:
        with pytest.raises(ResponseTooLarge):
            retrieve_artifact(ALLOWED, config(), client=client)


def test_upstream_server_error_is_a_retrieval_error_not_a_raw_httpx_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, request=request)

    with client_for(handler) as client:
        with pytest.raises(UpstreamHttpError):
            retrieve_artifact(ALLOWED, config(), client=client)


def test_transport_failure_is_wrapped_as_a_retrieval_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("boom", request=request)

    with client_for(handler) as client:
        with pytest.raises(RetrievalError):
            retrieve_artifact(ALLOWED, config(), client=client)


def test_redirect_loop_is_capped() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            302, headers={"location": "https://www.parlament-berlin.de/next"}, request=request
        )

    with client_for(handler) as client:
        with pytest.raises(RetrievalError):
            retrieve_artifact(ALLOWED, config(), client=client)


def test_default_client_pins_the_configured_timeout_and_disables_auto_redirects() -> None:
    """The production client path is otherwise never exercised by the injected-client tests."""

    import pipeline.retrieval as retrieval

    captured = {}
    real_client = httpx.Client

    class RecordingClient(real_client):  # type: ignore[misc, valid-type]
        def __init__(self, *args, **kwargs):
            captured.update(kwargs)
            kwargs["transport"] = httpx.MockTransport(
                lambda request: httpx.Response(200, request=request, **html())
            )
            super().__init__(*args, **kwargs)

    retrieval.httpx.Client = RecordingClient
    try:
        retrieve_artifact(ALLOWED, config())
    finally:
        retrieval.httpx.Client = real_client

    assert captured["follow_redirects"] is False
    assert captured["timeout"] == config().http.timeout_seconds
