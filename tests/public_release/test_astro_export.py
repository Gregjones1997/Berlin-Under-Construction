from __future__ import annotations

from html.parser import HTMLParser
import os
from pathlib import Path
import subprocess
from urllib.parse import urlsplit

import pytest

from public_release import regenerate_known_withheld_manifest, scan_static_output


ROOT = Path(__file__).resolve().parents[2]
WEB = ROOT / "web"
DIST = WEB / "dist"
PROJECTION = ROOT / "public" / "data" / "projects.json"
WITHHELD_CATALOG = ROOT / "public_release" / "known-withheld-candidates.json"
SENTINEL = "WITHHELD_SENTINEL_DO_NOT_SHIP"
TEST_BUILD_DATE = "2026-08-25"
TEST_LEGAL_ADDRESS = "Testanschrift 1, 10115 Berlin (test-only)"
MONITORED_CONTACT = "jonesg158@gmail.com"


def _build_environment(
    *, publication_date: str | None = TEST_BUILD_DATE,
    legal_address: str | None = TEST_LEGAL_ADDRESS,
) -> dict[str, str]:
    environment = os.environ.copy()
    if publication_date is None:
        environment.pop("PUBLICATION_AS_OF_DATE", None)
    else:
        environment["PUBLICATION_AS_OF_DATE"] = publication_date
    if legal_address is None:
        environment.pop("LEGAL_ADDRESS", None)
    else:
        environment["LEGAL_ADDRESS"] = legal_address
    return environment


def _run_build(
    output_directory: Path | None = None,
    *,
    publication_date: str | None = TEST_BUILD_DATE,
    legal_address: str | None = TEST_LEGAL_ADDRESS,
) -> subprocess.CompletedProcess[str]:
    command = ["npm", "run", "build"]
    if output_directory is not None:
        command.extend(["--", "--outDir", str(output_directory)])
    return subprocess.run(
        command,
        cwd=WEB,
        env=_build_environment(
            publication_date=publication_date,
            legal_address=legal_address,
        ),
        capture_output=True,
        text=True,
        check=False,
    )


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
    result = _run_build()
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
    assert c014_export.index("Current source-stated position") < c014_export.index(
        "Completion and construction history"
    )
    assert "Earlier source-stated dates remain visible" in c014_export
    assert "Translation unverified" in c014_export


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
        assert f"mailto:{MONITORED_CONTACT}" in correction_export
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
    assert f"mailto:{MONITORED_CONTACT}" in organization_export
    assert "Evidence correction" in organization_export
    assert "Formal right of reply" in organization_export
    assert "Data-protection request" in organization_export

    c014_export = (
        DIST / "projects" / "europaplatz-sued" / "index.html"
    ).read_text(encoding="utf-8")
    senate_route = (
        "/corrections/organizations/"
        "senatsverwaltung-stadtentwicklung-bauen-wohnen/"
    )
    assert f'href="{senate_route}"' in c014_export
    senate_page = (
        DIST
        / "corrections"
        / "organizations"
        / "senatsverwaltung-stadtentwicklung-bauen-wohnen"
        / "index.html"
    )
    assert senate_page.is_file()
    senate_export = senate_page.read_text(encoding="utf-8")
    assert (
        "Organization context: Senatsverwaltung für Stadtentwicklung, Bauen und Wohnen"
        in senate_export
    )
    assert f"mailto:{MONITORED_CONTACT}" in senate_export
    assert "Evidence correction" in senate_export
    assert "Formal right of reply" in senate_export
    assert "Data-protection request" in senate_export


def test_static_boundary_places_two_projects_and_keeps_c019_visible_unplaced(
    c014_export: str,
) -> None:
    landing_page = DIST / "records" / "index.html"
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
    assert "typed Python extraction pipeline" in landing_export
    assert "AI assists with bounded document extraction" in landing_export
    assert (
        'href="https://github.com/Gregjones1997/Berlin-Under-Construction"'
        in landing_export
    )


def test_ai_method_route_reports_only_established_measurements(
    c014_export: str,
) -> None:
    method_page = DIST / "method" / "index.html"
    assert method_page.is_file()
    method_export = method_page.read_text(encoding="utf-8")

    for measurement in (
        "3",
        "17,682",
        "1,053",
        "USD 0.00161784",
        "10,017 ms",
        "178 tests",
    ):
        assert measurement in method_export
    assert "primed the cache is unestablished" in method_export
    assert "no stored extraction run and no stored claim" in method_export
    assert "provider_response_incomplete" in method_export
    assert "adapter was subsequently corrected" in method_export
    assert "No accuracy, precision or recall result exists" in method_export
    assert "total provider-call count" not in method_export


def test_legal_routes_publish_only_owner_supplied_identity_and_evidenced_facts(
    c014_export: str,
) -> None:
    landing_export = (DIST / "index.html").read_text(encoding="utf-8")
    assert 'href="/impressum/"' in landing_export
    assert 'href="/privacy/"' in landing_export

    impressum = (DIST / "impressum" / "index.html").read_text(
        encoding="utf-8"
    )
    assert "Gregory Anthony Jones" in impressum
    assert TEST_LEGAL_ADDRESS in impressum
    assert MONITORED_CONTACT in impressum
    assert "Verantwortlich für den Inhalt" in impressum
    assert "non-commercial personal project" in impressum
    assert "no advertising" in impressum
    assert "no affiliate links" in impressum
    assert "no monetisation" in impressum
    assert "[[ANSCHRIFT]]" not in impressum

    privacy = (DIST / "privacy" / "index.html").read_text(encoding="utf-8")
    for controller_detail in (
        "Gregory Anthony Jones",
        TEST_LEGAL_ADDRESS,
        MONITORED_CONTACT,
    ):
        assert controller_detail in privacy
    assert "IP address" in privacy
    assert "Art. 6(1)(f) GDPR" in privacy
    assert "Vercel" in privacy
    assert 'href="https://vercel.com/legal/dpa"' in privacy
    for right in ("Art. 15", "Art. 16", "Art. 17", "Art. 18", "Art. 20", "Art. 21"):
        assert right in privacy
    assert "Berliner Beauftragte für Datenschutz und Informationsfreiheit" in privacy
    for absent_feature in (
        "no cookies",
        "no analytics",
        "no tracking",
        "no third-party requests",
        "no user accounts",
        "no forms",
    ):
        assert absent_feature in privacy


def test_legal_address_placeholder_occurs_once_and_fails_closed(
    tmp_path: Path,
) -> None:
    route_sources = tuple((WEB / "src" / "pages").rglob("*.astro"))
    assert sum(
        source.read_text(encoding="utf-8").count("[[ANSCHRIFT]]")
        for source in route_sources
    ) == 1

    result = _run_build(tmp_path / "missing-address", legal_address=None)

    assert result.returncode != 0
    assert "LEGAL_ADDRESS" in result.stdout + result.stderr


def test_publication_date_is_required_and_appears_on_every_route(
    c014_export: str, tmp_path: Path
) -> None:
    result = _run_build(tmp_path / "missing-date", publication_date=None)
    assert result.returncode != 0
    assert "PUBLICATION_AS_OF_DATE" in result.stdout + result.stderr

    pages = tuple(DIST.rglob("*.html"))
    assert len(pages) == 14
    footer_sentence = f"This page was generated on {TEST_BUILD_DATE}."
    for page in pages:
        export = page.read_text(encoding="utf-8")
        assert footer_sentence in export, page.relative_to(DIST)


def test_rebuild_after_planned_date_changes_footer_and_c010_caveat(
    tmp_path: Path,
) -> None:
    before_dir = tmp_path / "before"
    after_dir = tmp_path / "after"
    before = _run_build(before_dir, publication_date="2026-08-25")
    after = _run_build(after_dir, publication_date="2026-09-01")
    assert before.returncode == 0, before.stdout + before.stderr
    assert after.returncode == 0, after.stdout + after.stderr

    route = Path("projects/heinrich-hertz-gymnasium-ostbahnhof/index.html")
    before_export = (before_dir / route).read_text(encoding="utf-8")
    after_export = (after_dir / route).read_text(encoding="utf-8")
    assert "This page was generated on 2026-08-25." in before_export
    assert "This page was generated on 2026-09-01." in after_export
    assert "This is not evidence that the milestone has happened." in before_export
    assert (
        "That date has passed, but no confirming source is recorded. "
        "Completion is not asserted."
    ) in after_export


def test_every_internal_link_resolves_in_the_static_export(
    c014_export: str,
) -> None:
    for page in DIST.rglob("*.html"):
        parser = _LinkParser()
        parser.feed(page.read_text(encoding="utf-8"))
        for href in parser.hrefs:
            if not href.startswith("/"):
                continue
            path = urlsplit(href).path
            target = DIST / path.lstrip("/")
            if path.endswith("/"):
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


def test_only_atlas_ships_javascript(c014_export: str) -> None:
    atlas = (DIST / "index.html").read_text(encoding="utf-8")
    assert '<script type="module" src="/_astro/' in atlas
    assert '<noscript>' in atlas
    for page in DIST.rglob("*.html"):
        if page != DIST / "index.html":
            assert "<script" not in page.read_text(encoding="utf-8").lower()
    assert {p.relative_to(DIST).as_posix() for p in DIST.rglob("*.json")} == {
        "atlas/model.json", "atlas/provenance.json"
    }
    assert not (DIST / "data").exists()
    assert atlas.count('class="project-pin"') == 2
    assert 'class="project-pin" data-project="C-019"' not in atlas


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


def test_basic_listings_have_evidence_and_addressable_map_cards(c014_export: str) -> None:
    import json
    listing = json.loads((WEB / "src/atlas/basic-listings.json").read_text())
    candidates = json.loads((ROOT / "docs/research/findings/2026-09-09-bulk-discovery/catalog.json").read_text())
    research = {r["candidate_id"]: r for r in candidates["records"]}
    atlas = (DIST / "index.html").read_text()
    assert len(listing["records"]) == 150
    assert atlas.count('data-depth="basic"') == 150
    assert len({r["id"] for r in listing["records"]}) == 150
    for row in listing["records"]:
        original = research[row["id"]]
        assert row["nameDe"] == original["evidence"]["exact_title_de"]
        assert [row["longitude"], row["latitude"]] == original["location"]["coordinates"]
        assert row["evidence"] == original["evidence"]
        assert row["pageHash"] == original["page_check"]["artifact_hash"]
        assert original["page_check"]["status"] == "title_matched"
        assert row["sourceUrl"].startswith("https://mein.berlin.de/vorhaben/")
        assert f'id="record-{row["id"]}"' in atlas
        assert f'data-project="{row["id"]}"' in atlas
        assert not {"status", "start", "end", "category_proposal", "register_status_code"}.intersection(row)
    assert "not verified site boundaries" in atlas


def test_basic_dates_publish_without_disputed_start_or_completion(c014_export: str) -> None:
    import re
    atlas = (DIST / "index.html").read_text()
    assert atlas.count('data-basic-milestone=') == 6
    for pid in ('MB-2023-00716', 'MB-2025-01200', 'MB-2026-01347'):
        card = re.search(r'id="record-' + pid + r'".*?</section>', atlas).group(0)
        assert 'data-basic-milestone="reported_start"' not in card
        if pid == 'MB-2023-00716':
            assert 'data-basic-milestone=' not in card
    assert 'data-basic-milestone="reported_start"' in atlas
