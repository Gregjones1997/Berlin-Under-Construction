from __future__ import annotations

import argparse
from pathlib import Path

from public_release import build_public_bundle, scan_static_output


ROOT = Path(__file__).resolve().parents[1]
WITHHELD_SENTINEL = "WITHHELD_SENTINEL_DO_NOT_SHIP"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate, stage and scan the public-only static data bundle."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "build" / "public-release",
        help="Generated output directory (default: build/public-release).",
    )
    parser.add_argument(
        "--known-withheld-manifest",
        type=Path,
        required=True,
        help="Gitignored JSON manifest containing every currently withheld value.",
    )
    args = parser.parse_args()

    build_public_bundle(
        projection_path=ROOT / "public" / "data" / "projects.json",
        schema_path=ROOT / "public" / "data" / "public-projection.schema.json",
        boundary_path=ROOT / "public" / "data" / "map" / "berlin-boundary.geojson",
        boundary_provenance_path=(
            ROOT / "public" / "data" / "map" / "berlin-boundary.provenance.json"
        ),
        review_decisions_path=(
            ROOT / "public" / "data" / "accepted-review-decisions.json"
        ),
        name_allowlist_path=ROOT / "public" / "data" / "name-allowlist.json",
        output_dir=args.output,
    )
    scanned = scan_static_output(
        args.output,
        sentinels=(WITHHELD_SENTINEL,),
        known_withheld_manifest=args.known_withheld_manifest,
    )
    print(f"public bundle valid; scanned {len(scanned)} generated files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
