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


def test_committed_c014_projection_is_valid_and_contains_no_other_project() -> None:
    projection = _validate()

    assert [project["projectId"] for project in projection["projects"]] == ["C-014"]


def test_only_frozen_dossier_decisions_are_published_before_owner_review() -> None:
    projection = _validate()
    facts = projection["projects"][0]["facts"]

    assert {fact["factId"] for fact in facts if fact["state"] == "published"} == {
        "c014-project-name",
        "c014-project-location",
        "c014-places-programme-page-figure",
        "c014-places-programme-index-figure",
    }
    for fact in facts:
        if fact["state"] == "withheld":
            assert set(fact) == {"factId", "factType", "state", "reasonCode"}


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
        if fact["factType"] == "financial_measure" and fact["state"] == "published"
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
