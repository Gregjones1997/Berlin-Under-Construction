from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from public_release import PublicReleaseError, validate_projection


ROOT = Path(__file__).resolve().parents[2]
PROJECTION = ROOT / "public" / "data" / "projects.json"
SCHEMA = ROOT / "public" / "data" / "public-projection.schema.json"
DECISIONS = ROOT / "public" / "data" / "accepted-review-decisions.json"
NAME_ALLOWLIST = ROOT / "public" / "data" / "name-allowlist.json"


def _validate(path: Path = PROJECTION) -> dict[str, object]:
    return validate_projection(
        path,
        SCHEMA,
        review_decisions_path=DECISIONS,
        name_allowlist_path=NAME_ALLOWLIST,
        repository_root=ROOT,
    )


def _projection_payload() -> dict[str, object]:
    return json.loads(PROJECTION.read_text(encoding="utf-8"))


def _first_published_fact(payload: dict[str, object]) -> dict[str, object]:
    project = payload["projects"][0]  # type: ignore[index]
    return next(fact for fact in project["facts"] if fact["state"] == "published")


def _first_withheld_fact(payload: dict[str, object]) -> dict[str, object]:
    project = payload["projects"][0]  # type: ignore[index]
    return next(fact for fact in project["facts"] if fact["state"] == "withheld")


def test_committed_projection_contains_all_three_pilots() -> None:
    projection = _validate()

    assert [project["projectId"] for project in projection["projects"]] == [
        "C-014",
        "C-010",
        "C-019",
    ]


def test_thin_pilot_records_publish_only_frozen_minimums() -> None:
    projection = _validate()
    projects = {project["projectId"]: project for project in projection["projects"]}

    assert {
        fact["factId"]
        for fact in projects["C-010"]["facts"]
        if fact["state"] == "published"
    } == {
        "c010-project-name",
        "c010-project-location",
        "c010-current-status",
        "c010-technical-handover-current",
    }
    assert {
        fact["factId"]
        for fact in projects["C-019"]["facts"]
        if fact["state"] == "published"
    } == {
        "c019-project-name",
        "c019-commissioning-current",
        "c019-financing-commitment",
    }
    c019_withheld = {
        fact["factId"]: fact
        for fact in projects["C-019"]["facts"]
        if fact["state"] == "withheld"
    }
    assert c019_withheld["c019-project-location"]["reasonCode"] == (
        "source_string_requires_owner_verification"
    )


def test_only_owner_accepted_c014_facts_are_published() -> None:
    projection = _validate()
    facts = projection["projects"][0]["facts"]

    assert {fact["factId"] for fact in facts if fact["state"] == "published"} == {
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
    assert {fact["factId"] for fact in facts if fact["state"] == "withheld"} == {
        "c014-completion-period-2026",
        "c014-completion-outcome",
        "c014-organization-roles",
    }
    for fact in facts:
        if fact["state"] == "withheld":
            assert set(fact) == {"factId", "factType", "state", "reasonCode"}


def test_c014_owner_decisions_preserve_exact_types_and_corrected_pdf_value() -> None:
    projection = _validate()
    facts = {
        fact["factId"]: fact for fact in projection["projects"][0]["facts"]
    }

    assert facts["c014-current-status"]["asOfDate"] == {
        "state": "verified",
        "value": "2026-08-06",
    }
    assert facts["c014-current-status"]["freshness"] == {"state": "unassessed"}
    assert facts["c014-completion-period-2026"] == {
        "factId": "c014-completion-period-2026",
        "factType": "milestone",
        "state": "withheld",
        "reasonCode": "milestone_vocabulary_unresolved",
    }
    assert {
        facts[fact_id]["milestoneType"]
        for fact_id in (
            "c014-expected-completion-current",
            "c014-completion-history-2023",
            "c014-completion-history-2025-a",
            "c014-completion-history-2025-b",
            "c014-completion-history-2025-c",
        )
    } == {"substantial_completion"}
    assert {
        facts[fact_id]["milestoneType"]
        for fact_id in (
            "c014-construction-start-history",
            "c014-construction-start-current",
        )
    } == {"construction_start"}
    cost = facts["c014-approved-total-cost"]
    assert cost["measureType"] == "approved_budget"
    assert cost["amount"] == {"value": 3183000, "currency": "EUR"}
    assert cost["taxTreatment"] == {"state": "stated", "value": "gross"}
    assert cost["priceBasis"] == {"state": "not_stated"}
    assert cost["budgetReference"] == {"state": "not_stated"}
    assert "3.183.000 € brutto" in cost["evidence"]["exactTextDe"]
    assert "3 .183.000" not in cost["evidence"]["exactTextDe"]


def test_published_factual_value_requires_exact_german_span(tmp_path: Path) -> None:
    payload = _projection_payload()
    published = _first_published_fact(payload)
    published["evidence"]["exactTextDe"] = ""  # type: ignore[index]
    candidate = tmp_path / "projects.json"
    candidate.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(PublicReleaseError, match="exactTextDe"):
        _validate(candidate)


def test_published_factual_value_requires_https_source_url(tmp_path: Path) -> None:
    payload = _projection_payload()
    published = _first_published_fact(payload)
    published["evidence"]["sourceUrl"] = "http://example.test/source"  # type: ignore[index]
    candidate = tmp_path / "projects.json"
    candidate.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(PublicReleaseError, match="schema violation"):
        _validate(candidate)


def test_withheld_fact_cannot_contain_value_or_evidence(tmp_path: Path) -> None:
    payload = _projection_payload()
    withheld = _first_withheld_fact(payload)
    withheld["valueDe"] = "WITHHELD_SENTINEL_DO_NOT_SHIP"
    withheld["evidence"] = {
        "exactTextDe": "WITHHELD_SENTINEL_DO_NOT_SHIP",
        "sourceId": "source-private",
        "sourceUrl": "https://example.test/private",
        "publicationDate": {"state": "not_stated"},
    }
    candidate = tmp_path / "projects.json"
    candidate.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(PublicReleaseError):
        _validate(candidate)


@pytest.mark.parametrize(
    "private_key",
    (
        "artifactId",
        "artifactHash",
        "storedBytes",
        "preTransformResponseHash",
        "rawOutputPrivate",
        "email",
    ),
)
def test_private_fields_are_rejected_at_any_depth(
    tmp_path: Path, private_key: str
) -> None:
    payload = _projection_payload()
    candidate_payload = copy.deepcopy(payload)
    published = _first_published_fact(candidate_payload)
    published["evidence"][private_key] = "must-not-ship"  # type: ignore[index]
    candidate = tmp_path / "projects.json"
    candidate.write_text(json.dumps(candidate_payload), encoding="utf-8")

    with pytest.raises(PublicReleaseError, match="private field"):
        _validate(candidate)


def test_high_confidence_personal_data_is_rejected(tmp_path: Path) -> None:
    payload = _projection_payload()
    published = _first_published_fact(payload)
    published["evidence"]["exactTextDe"] = "gez. Max Mustermann"  # type: ignore[index]
    candidate = tmp_path / "projects.json"
    candidate.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(PublicReleaseError, match="personal data"):
        _validate(candidate)


def test_bare_possible_personal_name_is_rejected(tmp_path: Path) -> None:
    payload = _projection_payload()
    published = _first_published_fact(payload)
    published["valueDe"] = "Max Mustermann"
    published["evidence"]["exactTextDe"] = "Max Mustermann"  # type: ignore[index]
    candidate = tmp_path / "projects.json"
    candidate.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(PublicReleaseError, match="possible personal name"):
        _validate(candidate)


def test_published_fact_requires_a_digest_bound_owner_decision(
    tmp_path: Path,
) -> None:
    payload = _projection_payload()
    published = _first_published_fact(payload)
    published["valueDe"] = "Unapproved changed value"
    candidate = tmp_path / "projects.json"
    candidate.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(PublicReleaseError, match="accepted owner decision"):
        _validate(candidate)


def test_review_decision_basis_must_be_verbatim_in_the_frozen_record(
    tmp_path: Path,
) -> None:
    decisions = json.loads(DECISIONS.read_text(encoding="utf-8"))
    decisions["decisions"][0]["basisExactTexts"] = ["invented owner approval"]
    candidate_decisions = tmp_path / "accepted-review-decisions.json"
    candidate_decisions.write_text(json.dumps(decisions), encoding="utf-8")

    with pytest.raises(PublicReleaseError, match="basis text"):
        validate_projection(
            PROJECTION,
            SCHEMA,
            review_decisions_path=candidate_decisions,
            name_allowlist_path=NAME_ALLOWLIST,
            repository_root=ROOT,
        )


def test_published_financial_fact_retains_required_domain_semantics() -> None:
    projection = _validate()
    facts = projection["projects"][0]["facts"]  # type: ignore[index]
    financial = [
        fact
        for fact in facts
        if fact["factType"] == "financial_measure"
        and fact["state"] == "published"
        and fact["measureType"] == "financing_commitment"
    ]

    assert {fact["measureType"] for fact in financial} == {"financing_commitment"}
    assert {fact["scope"]["normalizedKey"] for fact in financial} == {
        "c014-places-programme-contribution"
    }
    assert any(
        qualifier["qualifierClass"] == "approximation"
        and qualifier["tokenDe"] == "rund"
        for fact in financial
        for qualifier in fact["qualifiers"]
    )
    assert all("freshness" in fact and "asOfDate" in fact for fact in financial)
    assert all(
        fact["evidence"]["evidenceLabel"] == "Verified"
        and fact["evidence"]["sourceTier"] == "primary"
        for fact in financial
    )


def test_unreconciled_conflict_cannot_promote_a_value(tmp_path: Path) -> None:
    payload = _projection_payload()
    project = payload["projects"][0]  # type: ignore[index]
    conflict = project["conflicts"][0]
    conflict["promotedFactId"] = conflict["memberFactIds"][0]
    candidate = tmp_path / "projects.json"
    candidate.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(PublicReleaseError):
        _validate(candidate)
