from __future__ import annotations

import json
from pathlib import Path

import pytest

from public_release import (
    PublicReleaseError,
    build_public_bundle,
    regenerate_known_withheld_manifest,
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


def _write_manifest(
    tmp_path: Path, values: list[str]
) -> tuple[Path, Path]:
    projection = tmp_path / "scan-projection.json"
    projection.write_text(
        json.dumps(
            {
                "projects": [
                    {
                        "facts": [
                            {"factId": "withheld-fixture", "state": "withheld"}
                        ]
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    catalog = tmp_path / "scan-catalog.json"
    catalog.write_text(
        json.dumps({"valuesByFactId": {"withheld-fixture": values}}),
        encoding="utf-8",
    )
    manifest = tmp_path / "known-withheld.json"
    regenerate_known_withheld_manifest(
        projection_path=projection,
        candidate_catalog_path=catalog,
        manifest_path=manifest,
    )
    return projection, manifest


def test_known_withheld_manifest_is_regenerated_from_projection_state(
    tmp_path: Path,
) -> None:
    projection = tmp_path / "projection.json"
    projection.write_text(
        json.dumps(
            {
                "projects": [
                    {
                        "facts": [
                            {
                                "factId": "still-withheld",
                                "state": "withheld",
                            },
                            {
                                "factId": "now-published",
                                "state": "published",
                                "valueDe": "newly public",
                            },
                        ]
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    catalog = tmp_path / "catalog.json"
    catalog.write_text(
        json.dumps(
            {
                "valuesByFactId": {
                    "still-withheld": ["private current value"],
                    "now-published": ["stale old scan value"],
                }
            }
        ),
        encoding="utf-8",
    )
    manifest = tmp_path / "manifest.json"

    result = regenerate_known_withheld_manifest(
        projection_path=projection,
        candidate_catalog_path=catalog,
        manifest_path=manifest,
    )

    assert result["withheldFactIds"] == ["still-withheld"]
    assert result["values"] == ["private current value"]
    assert "stale old scan value" not in manifest.read_text(encoding="utf-8")


def test_manifest_regeneration_creates_its_output_directory(tmp_path: Path) -> None:
    projection = tmp_path / "projection.json"
    projection.write_text(
        json.dumps({"projects": [{"facts": []}]}), encoding="utf-8"
    )
    catalog = tmp_path / "catalog.json"
    catalog.write_text(json.dumps({"valuesByFactId": {}}), encoding="utf-8")
    manifest = tmp_path / "new-build-directory" / "known-withheld.json"

    regenerate_known_withheld_manifest(
        projection_path=projection,
        candidate_catalog_path=catalog,
        manifest_path=manifest,
    )

    assert manifest.is_file()


def test_withheld_fixture_sentinel_cannot_enter_generated_assets(
    tmp_path: Path,
) -> None:
    output = tmp_path / "out"
    projection_payload = json.loads(PROJECTION.read_text(encoding="utf-8"))
    withheld_ids = [
        fact["factId"]
        for project in projection_payload["projects"]
        for fact in project["facts"]
        if fact["state"] == "withheld"
    ]
    catalog = tmp_path / "known-withheld-catalog.json"
    catalog.write_text(
        json.dumps(
            {
                "valuesByFactId": {
                    fact_id: [SENTINEL] if index == 0 else []
                    for index, fact_id in enumerate(withheld_ids)
                }
            }
        ),
        encoding="utf-8",
    )
    manifest = tmp_path / "known-withheld.json"
    regenerate_known_withheld_manifest(
        projection_path=PROJECTION,
        candidate_catalog_path=catalog,
        manifest_path=manifest,
    )

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
        projection_path=PROJECTION,
    )

    assert {path.name for path in scanned} == {
        "berlin-boundary.geojson",
        "berlin-boundary.provenance.json",
        "index.html",
        "display-model.json",
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
    projection, manifest = _write_manifest(tmp_path, ["known local withheld value"])

    with pytest.raises(PublicReleaseError, match="generated output"):
        scan_static_output(
            output,
            known_withheld_manifest=manifest,
            projection_path=projection,
        )


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
    projection, manifest = _write_manifest(tmp_path, ["zurückgestellt"])

    with pytest.raises(PublicReleaseError, match="generated output"):
        scan_static_output(
            output,
            known_withheld_manifest=manifest,
            projection_path=projection,
        )


def test_scanner_rejects_a_manifest_for_an_older_projection(tmp_path: Path) -> None:
    output = tmp_path / "out"
    output.mkdir()
    (output / "index.html").write_text("safe", encoding="utf-8")
    projection, manifest = _write_manifest(tmp_path, ["private current value"])
    projection.write_text(
        json.dumps({"projects": [{"facts": []}]}), encoding="utf-8"
    )

    with pytest.raises(PublicReleaseError, match="does not match current projection"):
        scan_static_output(
            output,
            known_withheld_manifest=manifest,
            projection_path=projection,
        )


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
