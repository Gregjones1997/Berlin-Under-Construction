from __future__ import annotations

import hashlib
import json
import tomllib
from pathlib import Path
from types import MappingProxyType
from typing import Annotated, Literal, Mapping, TypeVar

from pydantic import AfterValidator, BeforeValidator, Field, PlainSerializer

from pipeline.schemas import StrictModel


T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


def _toml_array(value: object) -> object:
    return tuple(value) if isinstance(value, list) else value


def _freeze_mapping(value: Mapping[K, V]) -> Mapping[K, V]:
    return MappingProxyType(dict(value))


TomlTuple = Annotated[tuple[T, ...], BeforeValidator(_toml_array)]
FrozenMap = Annotated[
    dict[K, V],
    AfterValidator(_freeze_mapping),
    # MappingProxyType is not JSON-serializable; the digest must still round-trip.
    PlainSerializer(lambda value: dict(value), return_type=dict, when_used="always"),
]


class UserAgents(StrictModel):
    """Both classes are mandatory: AGENTS.md requires a browser retry before any 403 is final."""

    default: str = Field(min_length=1)
    browser: str = Field(min_length=1)


class HttpConfig(StrictModel):
    timeout_seconds: int = Field(gt=0)
    max_response_bytes: int = Field(gt=0)
    max_redirects: int = Field(ge=0, le=10)
    accept_encoding: Literal["identity"]
    allowed_hosts: TomlTuple[str] = Field(min_length=1)
    user_agents: UserAgents


class FetchPolicy(StrictModel):
    steps: TomlTuple[Literal["default", "browser", "browser_tool"]] = Field(min_length=1)
    retry_statuses: TomlTuple[int]
    manual_only_after: Literal["browser_tool_failure"]
    record_resolved_barriers: Literal[True]


class EvidenceDepth(StrictModel):
    depth: int = Field(ge=1, le=5)
    name: str = Field(min_length=1)


class SourceFamily(StrictModel):
    url_template: str = Field(pattern=r"^https://")
    evidence_depth: int = Field(ge=1, le=5)


class CompletionConfig(StrictModel):
    financial_requires_depths: TomlTuple[int]
    record_inapplicable_or_unavailable: Literal[True]


class RetrievalConfig(StrictModel):
    schema_version: Literal["1.0.0"]
    config_version: str = Field(min_length=1)
    http: HttpConfig
    fetch_policy: FetchPolicy
    artifact_transforms: FrozenMap[str, Literal["pdf-metadata-strip/v1", "identity/v1"]]
    evidence_depths: TomlTuple[EvidenceDepth]
    source_families: FrozenMap[str, SourceFamily]
    completion: CompletionConfig

    def allows_host(self, host: str | None) -> bool:
        return bool(host) and host.lower() in self.http.allowed_hosts


def load_retrieval_config(path: Path) -> tuple[RetrievalConfig, str]:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    config = RetrievalConfig.model_validate(data)
    canonical = json.dumps(config.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return config, digest
