from __future__ import annotations

import argparse
import dataclasses
import json
import tomllib
from pathlib import Path
from typing import Literal

from pydantic import Field

from pipeline.retrieval import retrieve_artifact
from pipeline.retrieval_config import TomlTuple, load_retrieval_config
from pipeline.schemas import StrictModel


class ReproductionSource(StrictModel):
    id: str = Field(min_length=1)
    url: str = Field(pattern=r"^https://")
    expected_pre_transform_response_hash: str = Field(pattern=r"^[0-9a-f]{64}$")


class ReproductionRegistry(StrictModel):
    schema_version: Literal["1.0.0"]
    source: TomlTuple[ReproductionSource] = Field(min_length=1)


def reproduce(registry_path: Path, retrieval_config_path: Path) -> list[dict[str, object]]:
    registry = ReproductionRegistry.model_validate(
        tomllib.loads(registry_path.read_text(encoding="utf-8"))
    )
    config, config_digest = load_retrieval_config(retrieval_config_path)
    results: list[dict[str, object]] = []
    for source in registry.source:
        result = retrieve_artifact(source.url, config)
        observed = result.artifact.hashes.pre_transform_response_hash
        results.append(
            {
                "id": source.id,
                "request_url": source.url,
                "final_url": result.attempts[-1].final_url,
                # ADR-011: label both hash roles wherever both are shown. The pre-strip
                # hash is chain of custody only and must never reach a public registry.
                "raw_response_pre_strip_expected": source.expected_pre_transform_response_hash,
                "raw_response_pre_strip_observed": observed,
                "raw_response_pre_strip_private": True,
                "matches": observed == source.expected_pre_transform_response_hash,
                "stored_content_post_strip": result.artifact.hashes.stored_content_hash,
                "transform_rule_version": result.artifact.transform.rule_version,
                "retrieval_config_digest": config_digest,
                "attempts": [dataclasses.asdict(attempt) for attempt in result.attempts],
            }
        )
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Reproduce frozen raw-response hashes safely")
    parser.add_argument("registry", type=Path)
    parser.add_argument(
        "--retrieval-config",
        type=Path,
        default=Path("pipeline/config/retrieval.v1.toml"),
    )
    args = parser.parse_args()
    print(json.dumps(reproduce(args.registry, args.retrieval_config), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
