from __future__ import annotations

from dataclasses import dataclass

import httpx

from pipeline.artifacts import PreparedArtifact, prepare_artifact
from pipeline.retrieval_config import RetrievalConfig


class RetrievalError(RuntimeError):
    pass


class BrowserToolRequired(RetrievalError):
    pass


class DisallowedRedirect(RetrievalError):
    """A hop left the configured host allowlist or downgraded from https."""


class TooManyRedirects(RetrievalError):
    pass


class ResponseTooLarge(RetrievalError):
    pass


class UpstreamHttpError(RetrievalError):
    pass


@dataclass(frozen=True)
class RetrievalAttempt:
    user_agent_class: str
    retry_number: int
    status_code: int | None
    request_url: str
    final_url: str | None
    outcome: str


@dataclass(frozen=True)
class RetrievalResult:
    artifact: PreparedArtifact
    attempts: tuple[RetrievalAttempt, ...]


def _require_allowed(url: httpx.URL, config: RetrievalConfig) -> None:
    if url.scheme != "https":
        raise DisallowedRedirect(f"non-https URL rejected: scheme {url.scheme!r}")
    if not config.allows_host(url.host):
        raise DisallowedRedirect(f"host {url.host!r} is not in the configured allowlist")


def _read_capped(response: httpx.Response, limit: int) -> bytes:
    declared = response.headers.get("content-length")
    if declared is not None and declared.isdigit() and int(declared) > limit:
        raise ResponseTooLarge("declared content-length exceeds configured byte limit")
    buffer = bytearray()
    for chunk in response.iter_bytes():
        buffer.extend(chunk)
        if len(buffer) > limit:
            raise ResponseTooLarge("response exceeds configured byte limit")
    return bytes(buffer)


def _fetch_with_user_agent(
    client: httpx.Client,
    url: str,
    config: RetrievalConfig,
    user_agent_class: str,
    retry_number: int,
    attempts: list[RetrievalAttempt],
) -> tuple[httpx.Response, bytes] | None:
    """Return (response, body) or None when this User-Agent class was blocked."""

    headers = {
        "User-Agent": getattr(config.http.user_agents, user_agent_class),
        "Accept-Encoding": config.http.accept_encoding,
    }
    current = httpx.URL(url)
    for _ in range(config.http.max_redirects + 1):
        _require_allowed(current, config)
        with client.stream(
            "GET", current, headers=headers, follow_redirects=False
        ) as response:
            if response.is_redirect:
                response.read()
                nxt = response.next_request
                if nxt is None:
                    raise RetrievalError("redirect response carried no usable Location")
                attempts.append(
                    RetrievalAttempt(
                        user_agent_class=user_agent_class,
                        retry_number=retry_number,
                        status_code=response.status_code,
                        request_url=str(current),
                        final_url=str(nxt.url),
                        outcome="redirect",
                    )
                )
                current = nxt.url
                continue

            blocked = response.status_code in config.fetch_policy.retry_statuses
            attempts.append(
                RetrievalAttempt(
                    user_agent_class=user_agent_class,
                    retry_number=retry_number,
                    status_code=response.status_code,
                    request_url=str(current),
                    final_url=str(response.url),
                    outcome="access_barrier" if blocked else "received",
                )
            )
            if blocked:
                return None
            if response.status_code >= 400:
                raise UpstreamHttpError(f"upstream returned HTTP {response.status_code}")
            return response, _read_capped(response, config.http.max_response_bytes)

    raise TooManyRedirects(f"exceeded {config.http.max_redirects} redirects")


def retrieve_artifact(
    url: str,
    config: RetrievalConfig,
    *,
    client: httpx.Client | None = None,
) -> RetrievalResult:
    """Retrieve to memory and pass bytes through the mandatory artifact gate."""

    owns_client = client is None
    active_client = client or httpx.Client(
        follow_redirects=False,
        timeout=config.http.timeout_seconds,
    )
    attempts: list[RetrievalAttempt] = []
    try:
        for retry_number, user_agent_class in enumerate(
            step for step in config.fetch_policy.steps if step != "browser_tool"
        ):
            fetched = _fetch_with_user_agent(
                active_client, url, config, user_agent_class, retry_number, attempts
            )
            if fetched is None:
                continue
            response, body = fetched
            media_type = response.headers.get("content-type", "application/octet-stream")
            return RetrievalResult(
                artifact=prepare_artifact(
                    body, media_type, transforms=config.artifact_transforms
                ),
                attempts=tuple(attempts),
            )
        raise BrowserToolRequired("default and browser User-Agent attempts were blocked")
    except httpx.HTTPError as exc:
        raise RetrievalError(f"transport failure: {type(exc).__name__}") from exc
    finally:
        if owns_client:
            active_client.close()
