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


class _LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        if tag != "a":
            return
        href = dict(attrs).get("href")
        if href:
            self.hrefs.append(href)


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


def test_every_project_has_a_stable_static_dossier_route(c014_export: str) -> None:
    expected_routes = {
        "europaplatz-sued",
        "heinrich-hertz-gymnasium-ostbahnhof",
        "power-to-heat-heizkraftwerk-mitte",
    }

    for slug in expected_routes:
        page = DIST / "projects" / slug / "index.html"
        assert page.is_file(), slug


def test_project_correction_routes_preserve_context_and_request_type(
    c014_export: str,
) -> None:
    projects = {
        "C-014": "Europaplatz Süd — Umgestaltung",
        "C-010": "Schulneubau Heinrich-Hertz-Gymnasium am Ostbahnhof",
        "C-019": "Power-to-Heat-Anlage am Heizkraftwerk Berlin-Mitte",
    }

    for project_id, project_name in projects.items():
        route = f"/corrections/projects/{project_id}/"
        assert f'href="{route}"' in (
            DIST
            / "projects"
            / {
                "C-014": "europaplatz-sued",
                "C-010": "heinrich-hertz-gymnasium-ostbahnhof",
                "C-019": "power-to-heat-heizkraftwerk-mitte",
            }[project_id]
            / "index.html"
        ).read_text(encoding="utf-8")

        correction_page = (
            DIST / "corrections" / "projects" / project_id / "index.html"
        )
        assert correction_page.is_file()
        correction_export = correction_page.read_text(encoding="utf-8")
        assert project_id in correction_export
        assert project_name in correction_export
        assert "preview arrangement" in correction_export.lower()
        assert "channel through which you received access" in correction_export
        assert "Evidence correction" in correction_export
        assert "Formal right of reply" in correction_export
        assert "Data-protection request" in correction_export

    c019_export = (
        DIST / "projects" / "power-to-heat-heizkraftwerk-mitte" / "index.html"
    ).read_text(encoding="utf-8")
    organization_route = "/corrections/organizations/50hertz/"
    assert f'href="{organization_route}"' in c019_export
    organization_page = (
        DIST / "corrections" / "organizations" / "50hertz" / "index.html"
    )
    assert organization_page.is_file()
    organization_export = organization_page.read_text(encoding="utf-8")
    assert "Organization context: 50Hertz" in organization_export
    assert "preview arrangement" in organization_export.lower()
    assert "Evidence correction" in organization_export
    assert "Formal right of reply" in organization_export
    assert "Data-protection request" in organization_export


def test_static_boundary_places_two_projects_and_keeps_c019_visible_unplaced(
    c014_export: str,
) -> None:
    landing_page = DIST / "index.html"
    assert landing_page.is_file()
    landing_export = landing_page.read_text(encoding="utf-8")

    assert "<svg" in landing_export
    assert landing_export.count('data-map-marker="placed"') == 2
    assert 'data-project-id="C-014"' in landing_export
    assert 'data-project-id="C-010"' in landing_export
    assert 'data-project-id="C-019"' not in landing_export
    assert "Two of three pilot projects are placed" in landing_export
    assert "C-019" in landing_export
    assert "location withheld pending source verification" in landing_export
    assert "source_string_requires_owner_verification" in landing_export
    assert "/projects/power-to-heat-heizkraftwerk-mitte/" in landing_export
    assert "(Daten verändert)" in landing_export
    assert "https://www.bkg.bund.de" in landing_export
    assert "https://www.govdata.de/dl-de/by-2-0" in landing_export


def test_ai_method_route_reports_only_established_measurements(
    c014_export: str,
) -> None:
    method_page = DIST / "method" / "index.html"
    assert method_page.is_file()
    method_export = method_page.read_text(encoding="utf-8")

    for measurement in ("3", "17,682", "1,053", "USD 0.00161784", "10,017 ms"):
        assert measurement in method_export
    assert "primed the cache is unestablished" in method_export
    assert "no stored extraction run and no stored claim" in method_export
    assert "provider_response_incomplete" in method_export
    assert "adapter was subsequently corrected" in method_export
    assert "No accuracy, precision or recall result exists" in method_export
    assert "total provider-call count" not in method_export


def test_legal_draft_routes_keep_owner_and_live_facts_as_placeholders(
    c014_export: str,
) -> None:
    landing_export = (DIST / "index.html").read_text(encoding="utf-8")
    assert 'href="/impressum/"' in landing_export
    assert 'href="/privacy/"' in landing_export

    impressum = (DIST / "impressum" / "index.html").read_text(
        encoding="utf-8"
    )
    for placeholder in (
        "provider identity",
        "complete postal address",
        "permanent monitored contact",
        "decide whether § 18(2) MStV applies",
    ):
        assert f"OWNER DECISION REQUIRED: {placeholder}" in impressum
    assert "not approved for a public launch" in impressum

    privacy = (DIST / "privacy" / "index.html").read_text(encoding="utf-8")
    for placeholder in (
        "provider/controller identity",
        "complete postal address",
        "permanent monitored contact for privacy requests",
    ):
        assert f"OWNER DECISION REQUIRED: {placeholder}" in privacy
    for live_fact in (
        "request metadata actually processed",
        "cookies or browser storage",
        "applicable recipients and subprocessors",
        "non-EEA transfers",
        "retention period or evidenced deletion criterion",
    ):
        assert live_fact in privacy
    assert "It must not be presented as a complete public notice" in privacy


def test_every_internal_link_resolves_in_the_static_export(
    c014_export: str,
) -> None:
    for page in DIST.rglob("*.html"):
        parser = _LinkParser()
        parser.feed(page.read_text(encoding="utf-8"))
        for href in parser.hrefs:
            if not href.startswith("/"):
                continue
            target = DIST / href.lstrip("/")
            if href.endswith("/"):
                target = target / "index.html"
            assert target.is_file(), f"{page.relative_to(DIST)} -> {href}"


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


def test_export_contains_named_fields_not_serialized_objects(
    c014_export: str,
) -> None:
    exported_html = "\n".join(
        page.read_text(encoding="utf-8") for page in DIST.rglob("*.html")
    )
    assert "<pre" not in exported_html.lower()
    assert '&quot;factId&quot;' not in exported_html
    assert '&quot;memberFactIds&quot;' not in exported_html
    assert "Evidence" in c014_export
    assert "Milestone type:" in c014_export


def test_astro_export_ships_no_javascript(c014_export: str) -> None:
    exported_html = "\n".join(
        page.read_text(encoding="utf-8") for page in DIST.rglob("*.html")
    )
    assert "<script" not in exported_html.lower()
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
