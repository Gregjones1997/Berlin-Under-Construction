from __future__ import annotations

import argparse
import json
import tomllib
from pathlib import Path

from pipeline.retrieval import retrieve_artifact
from pipeline.retrieval_config import load_retrieval_config


def reproduce(registry_path: Path, retrieval_config_path: Path) -> list[dict[str, object]]:
    registry = tomllib.loads(registry_path.read_text(encoding="utf-8"))
    config, config_digest = load_retrieval_config(retrieval_config_path)
    results: list[dict[str, object]] = []
    for source in registry["source"]:
        result = retrieve_artifact(source["url"], config)
        observed = result.artifact.hashes.pre_transform_response_hash
        results.append(
            {
                "id": source["id"],
                "request_url": source["url"],
                "final_url": result.attempts[-1].final_url,
                "expected_pre_transform_response_hash": source[
                    "expected_pre_transform_response_hash"
                ],
                "observed_pre_transform_response_hash": observed,
                "matches": observed == source["expected_pre_transform_response_hash"],
                "stored_content_hash": result.artifact.hashes.stored_content_hash,
                "transform_rule_version": result.artifact.transform.rule_version,
                "retrieval_config_digest": config_digest,
                "attempts": [attempt.__dict__ for attempt in result.attempts],
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
