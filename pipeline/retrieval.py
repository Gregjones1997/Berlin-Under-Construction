from __future__ import annotations

from dataclasses import dataclass

import httpx

from pipeline.artifacts import PreparedArtifact, prepare_artifact
from pipeline.retrieval_config import RetrievalConfig


class RetrievalError(RuntimeError):
    pass


class BrowserToolRequired(RetrievalError):
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


def retrieve_artifact(
    url: str,
    config: RetrievalConfig,
    *,
    client: httpx.Client | None = None,
) -> RetrievalResult:
    """Retrieve to memory and pass bytes through the mandatory artifact gate."""

    owns_client = client is None
    active_client = client or httpx.Client(
        follow_redirects=True,
        timeout=config.http.timeout_seconds,
    )
    attempts: list[RetrievalAttempt] = []
    try:
        for retry_number, user_agent_class in enumerate(("default", "browser")):
            response = active_client.get(
                url,
                headers={
                    "User-Agent": config.http.user_agents[user_agent_class],
                    "Accept-Encoding": config.http.accept_encoding,
                },
            )
            is_retryable = response.status_code in config.fetch_policy.retry_statuses
            attempts.append(
                RetrievalAttempt(
                    user_agent_class=user_agent_class,
                    retry_number=retry_number,
                    status_code=response.status_code,
                    request_url=url,
                    final_url=str(response.url),
                    outcome="access_barrier" if is_retryable else "received",
                )
            )
            if is_retryable:
                continue
            response.raise_for_status()
            if len(response.content) > config.http.max_response_bytes:
                raise RetrievalError("response exceeds configured byte limit")
            media_type = response.headers.get("content-type", "application/octet-stream")
            return RetrievalResult(
                artifact=prepare_artifact(response.content, media_type),
                attempts=tuple(attempts),
            )
        raise BrowserToolRequired("default and browser User-Agent attempts were blocked")
    finally:
        if owns_client:
            active_client.close()
