from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import subprocess

import pytest

from public_release import regenerate_known_withheld_manifest, scan_static_output


ROOT = Path(__file__).resolve().parents[2]
WEB = ROOT / "web"
DIST = WEB / "dist"
PROJECTION = ROOT / "public" / "data" / "projects.json"
WITHHELD_CATALOG = ROOT / "public_release" / "known-withheld-candidates.json"
SENTINEL = "WITHHELD_SENTINEL_DO_NOT_SHIP"


class _FactLocationParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.conflict_depth = 0
        self.fact_locations: dict[str, list[bool]] = {}

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attributes = dict(attrs)
        if tag == "section" and attributes.get("data-conflict-id"):
            self.conflict_depth += 1
        fact_id = attributes.get("data-fact-id")
        if fact_id:
            self.fact_locations.setdefault(fact_id, []).append(
                self.conflict_depth > 0
            )

    def handle_endtag(self, tag: str) -> None:
        if tag == "section" and self.conflict_depth:
            self.conflict_depth -= 1


@pytest.fixture(scope="module")
def c014_export() -> str:
    result = subprocess.run(
        ["npm", "run", "build"],
        cwd=WEB,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    page = DIST / "projects" / "europaplatz-sued" / "index.html"
    assert page.is_file()
    return page.read_text(encoding="utf-8")


def test_c014_static_route_renders_every_accepted_fact_and_withheld_state(
    c014_export: str,
) -> None:
    published_ids = {
        "c014-project-name",
        "c014-project-location",
        "c014-places-programme-page-figure",
        "c014-places-programme-index-figure",
        "c014-current-status",
        "c014-expected-completion-current",
        "c014-completion-history-2023",
        "c014-completion-history-2025-a",
        "c014-completion-history-2025-b",
        "c014-completion-history-2025-c",
        "c014-construction-start-history",
        "c014-construction-start-current",
        "c014-approved-total-cost",
    }
    withheld = {
        "c014-completion-period-2026": "milestone_vocabulary_unresolved",
        "c014-completion-outcome": "multi_source_synthesis_has_no_exact_span",
        "c014-organization-roles": "role_vocabulary_unresolved",
    }

    for fact_id in published_ids | set(withheld):
        assert f'data-fact-id="{fact_id}"' in c014_export
    for reason_code in withheld.values():
        assert reason_code in c014_export
    assert "3.183.000 € brutto" in c014_export
    assert "3 .183.000" not in c014_export


def test_conflict_members_exist_only_inside_the_conflict_presentation(
    c014_export: str,
) -> None:
    parser = _FactLocationParser()
    parser.feed(c014_export)

    for fact_id in (
        "c014-places-programme-page-figure",
        "c014-places-programme-index-figure",
    ):
        assert parser.fact_locations[fact_id] == [True]
    assert 'data-conflict-id="c014-places-programme-figures"' in c014_export


def test_raw_export_glosses_verified_as_source_fidelity(c014_export: str) -> None:
    assert "faithfully supported by the cited source" in c014_export
    assert "does not mean the value is current" in c014_export


def test_astro_export_ships_no_javascript(c014_export: str) -> None:
    assert "<script" not in c014_export.lower()
    assert not tuple(DIST.rglob("*.js"))
    assert not tuple(DIST.rglob("*.json"))
    assert not (DIST / "data").exists()


def test_real_astro_export_passes_withheld_and_sentinel_scans(
    c014_export: str, tmp_path: Path
) -> None:
    manifest = tmp_path / "known-withheld.json"
    regenerate_known_withheld_manifest(
        projection_path=PROJECTION,
        candidate_catalog_path=WITHHELD_CATALOG,
        manifest_path=manifest,
    )

    scanned = scan_static_output(
        DIST,
        sentinels=(SENTINEL,),
        known_withheld_manifest=manifest,
        projection_path=PROJECTION,
    )

    assert DIST / "projects" / "europaplatz-sued" / "index.html" in scanned
