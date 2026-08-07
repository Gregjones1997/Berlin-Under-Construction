from __future__ import annotations

import hashlib
import json
import tomllib
from pathlib import Path
from typing import Annotated, Literal, TypeVar

from pydantic import BeforeValidator, Field

from pipeline.schemas import StrictModel


T = TypeVar("T")


def _toml_array(value: object) -> object:
    return tuple(value) if isinstance(value, list) else value


TomlTuple = Annotated[tuple[T, ...], BeforeValidator(_toml_array)]


class HttpConfig(StrictModel):
    timeout_seconds: int = Field(gt=0)
    max_response_bytes: int = Field(gt=0)
    accept_encoding: Literal["identity"]
    user_agents: dict[Literal["default", "browser"], str]


class FetchPolicy(StrictModel):
    steps: TomlTuple[Literal["default", "browser", "browser_tool"]]
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
    artifact_transforms: dict[str, Literal["pdf-metadata-strip/v1", "identity/v1"]]
    evidence_depths: TomlTuple[EvidenceDepth]
    source_families: dict[str, SourceFamily]
    completion: CompletionConfig


def load_retrieval_config(path: Path) -> tuple[RetrievalConfig, str]:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    config = RetrievalConfig.model_validate(data)
    canonical = json.dumps(config.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return config, digest
