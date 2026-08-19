from __future__ import annotations

import json
from pathlib import Path

import pytest

from public_release import (
    PublicReleaseError,
    build_public_bundle,
    scan_static_output,
)


ROOT = Path(__file__).resolve().parents[2]
PROJECTION = ROOT / "public" / "data" / "projects.json"
SCHEMA = ROOT / "public" / "data" / "public-projection.schema.json"
BOUNDARY = ROOT / "public" / "data" / "map" / "berlin-boundary.geojson"
PROVENANCE = ROOT / "public" / "data" / "map" / "berlin-boundary.provenance.json"
SENTINEL = "WITHHELD_SENTINEL_DO_NOT_SHIP"


def test_generated_bundle_passes_sentinel_and_known_withheld_scans(
    tmp_path: Path,
) -> None:
    output = tmp_path / "out"
    manifest = tmp_path / "known-withheld.json"
    manifest.write_text(
        json.dumps({"values": ["known local withheld value"]}), encoding="utf-8"
    )

    build_public_bundle(
        projection_path=PROJECTION,
        schema_path=SCHEMA,
        boundary_path=BOUNDARY,
        boundary_provenance_path=PROVENANCE,
        output_dir=output,
    )
    scanned = scan_static_output(
        output,
        sentinels=(SENTINEL,),
        known_withheld_manifest=manifest,
    )

    assert {path.name for path in scanned} == {
        "berlin-boundary.geojson",
        "berlin-boundary.provenance.json",
        "index.html",
        "projects.json",
        "projection.js",
    }


def test_scanner_checks_generated_javascript_not_only_source_json(
    tmp_path: Path,
) -> None:
    output = tmp_path / "out"
    chunk = output / "_next" / "static" / "chunks" / "app.js"
    chunk.parent.mkdir(parents=True)
    chunk.write_text(f'window.__data="{SENTINEL}"', encoding="utf-8")

    with pytest.raises(PublicReleaseError, match="generated output"):
        scan_static_output(output, sentinels=(SENTINEL,))


def test_scanner_checks_known_withheld_values_in_generated_html(
    tmp_path: Path,
) -> None:
    output = tmp_path / "out"
    output.mkdir()
    (output / "index.html").write_text(
        "<main>known local withheld value</main>", encoding="utf-8"
    )
    manifest = tmp_path / "known-withheld.json"
    manifest.write_text(
        json.dumps({"values": ["known local withheld value"]}), encoding="utf-8"
    )

    with pytest.raises(PublicReleaseError, match="generated output"):
        scan_static_output(output, known_withheld_manifest=manifest)
