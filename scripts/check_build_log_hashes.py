#!/usr/bin/env python3
"""Fail when a commit hash recorded in the build log is unreachable."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


HASH_PATTERN = re.compile(r"`(?!sha256:)([0-9a-f]{7,40})`")


def main() -> int:
    log_path = Path(sys.argv[1] if len(sys.argv) > 1 else "docs/how-this-was-built.md")
    hashes = list(dict.fromkeys(HASH_PATTERN.findall(log_path.read_text(encoding="utf-8"))))
    reachable = subprocess.run(
        ["git", "log", "--all", "--format=%H"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    missing = [recorded for recorded in hashes if not any(full.startswith(recorded) for full in reachable)]

    if missing:
        for recorded in missing:
            print(
                f"{log_path}: `{recorded}` is not reachable from git log --all",
                file=sys.stderr,
            )
        return 1

    noun = "hash" if len(hashes) == 1 else "hashes"
    print(f"Validated {len(hashes)} reachable build-log {noun}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
