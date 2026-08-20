from __future__ import annotations

import json
from pathlib import Path

import pytest

from public_release import PublicReleaseError, validate_boundary_assets


ROOT = Path(__file__).resolve().parents[2]
BOUNDARY = ROOT / "public" / "data" / "map" / "berlin-boundary.geojson"
PROVENANCE = ROOT / "public" / "data" / "map" / "berlin-boundary.provenance.json"


def test_bundled_berlin_boundary_has_verified_local_provenance() -> None:
    result = validate_boundary_assets(BOUNDARY, PROVENANCE)

    assert result["authority"] == "Bundesamt für Kartographie und Geodäsie (BKG)"
    assert result["retrievedOn"] == "2026-08-19"
    assert result["sourceCrs"] == "EPSG:25832"
    assert result["bundledCrs"] == "EPSG:4326"
    assert result["license"]["id"] == "dl-de/by-2-0"
    assert "(Daten verändert)" in result["license"]["attribution"]
    assert result["runtimeRequests"] == []


def test_boundary_hash_blocks_an_unrecorded_geometry_change(tmp_path: Path) -> None:
    changed_boundary = tmp_path / "berlin-boundary.geojson"
    changed_boundary.write_bytes(BOUNDARY.read_bytes() + b" ")

    with pytest.raises(PublicReleaseError, match="hash"):
        validate_boundary_assets(changed_boundary, PROVENANCE)


def test_boundary_provenance_forbids_runtime_requests(tmp_path: Path) -> None:
    provenance = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    provenance["runtimeRequests"] = ["https://tiles.example.test/{z}/{x}/{y}"]
    changed_provenance = tmp_path / "provenance.json"
    changed_provenance.write_text(json.dumps(provenance), encoding="utf-8")

    with pytest.raises(PublicReleaseError, match="runtime network"):
        validate_boundary_assets(BOUNDARY, changed_provenance)
