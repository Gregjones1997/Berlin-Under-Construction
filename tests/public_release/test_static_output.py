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
DECISIONS = ROOT / "public" / "data" / "accepted-review-decisions.json"
NAME_ALLOWLIST = ROOT / "public" / "data" / "name-allowlist.json"
SENTINEL = "WITHHELD_SENTINEL_ZURÜCKGESTELLT_DO_NOT_SHIP"


def test_withheld_fixture_sentinel_cannot_enter_generated_assets(
    tmp_path: Path,
) -> None:
    output = tmp_path / "out"
    manifest = tmp_path / "known-withheld.json"
    manifest.write_text(json.dumps({"values": [SENTINEL]}), encoding="utf-8")

    build_public_bundle(
        projection_path=PROJECTION,
        schema_path=SCHEMA,
        boundary_path=BOUNDARY,
        boundary_provenance_path=PROVENANCE,
        review_decisions_path=DECISIONS,
        name_allowlist_path=NAME_ALLOWLIST,
        output_dir=output,
    )
    contaminated = json.loads(PROJECTION.read_text(encoding="utf-8"))
    withheld = next(
        fact
        for fact in contaminated["projects"][0]["facts"]
        if fact["state"] == "withheld"
    )
    withheld["valueDe"] = SENTINEL
    contaminated_projection = tmp_path / "projects-with-sentinel.json"
    contaminated_projection.write_text(json.dumps(contaminated), encoding="utf-8")

    with pytest.raises(PublicReleaseError):
        build_public_bundle(
            projection_path=contaminated_projection,
            schema_path=SCHEMA,
            boundary_path=BOUNDARY,
            boundary_provenance_path=PROVENANCE,
            review_decisions_path=DECISIONS,
            name_allowlist_path=NAME_ALLOWLIST,
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


@pytest.mark.parametrize(
    "encoded",
    (
        r"zur\u00fcckgestellt",
        r"zur\u00FCckgestellt",
        "zur&uuml;ckgestellt",
        "zur&#252;ckgestellt",
    ),
)
def test_scanner_rejects_encoded_known_withheld_values(
    tmp_path: Path, encoded: str
) -> None:
    output = tmp_path / "out"
    output.mkdir()
    (output / "app.js").write_text(encoded, encoding="utf-8")
    manifest = tmp_path / "known-withheld.json"
    manifest.write_text(json.dumps({"values": ["zurückgestellt"]}), encoding="utf-8")

    with pytest.raises(PublicReleaseError, match="generated output"):
        scan_static_output(output, known_withheld_manifest=manifest)


def test_bundle_rejects_unexpected_stale_output_file(tmp_path: Path) -> None:
    output = tmp_path / "out"
    output.mkdir()
    (output / "private-stale.txt").write_text("stale", encoding="utf-8")

    with pytest.raises(PublicReleaseError, match="unexpected pre-existing"):
        build_public_bundle(
            projection_path=PROJECTION,
            schema_path=SCHEMA,
            boundary_path=BOUNDARY,
            boundary_provenance_path=PROVENANCE,
            review_decisions_path=DECISIONS,
            name_allowlist_path=NAME_ALLOWLIST,
            output_dir=output,
        )
