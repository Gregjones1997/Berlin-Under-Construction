from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from public_release import PublicReleaseError, validate_projection


ROOT = Path(__file__).resolve().parents[2]
PROJECTION = ROOT / "public" / "data" / "projects.json"
SCHEMA = ROOT / "public" / "data" / "public-projection.schema.json"


def _projection_payload() -> dict[str, object]:
    return json.loads(PROJECTION.read_text(encoding="utf-8"))


def _first_published_fact(payload: dict[str, object]) -> dict[str, object]:
    project = payload["projects"][0]  # type: ignore[index]
    return next(fact for fact in project["facts"] if fact["state"] == "published")


def _first_withheld_fact(payload: dict[str, object]) -> dict[str, object]:
    project = payload["projects"][0]  # type: ignore[index]
    return next(fact for fact in project["facts"] if fact["state"] == "withheld")


def test_committed_c014_projection_is_valid_and_contains_no_other_project() -> None:
    projection = validate_projection(PROJECTION, SCHEMA)

    assert [project["projectId"] for project in projection["projects"]] == ["C-014"]


def test_only_frozen_dossier_decisions_are_published_before_owner_review() -> None:
    projection = validate_projection(PROJECTION, SCHEMA)
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
        validate_projection(candidate, SCHEMA)


def test_published_factual_value_requires_https_source_url(tmp_path: Path) -> None:
    payload = _projection_payload()
    published = _first_published_fact(payload)
    published["evidence"]["sourceUrl"] = "http://example.test/source"  # type: ignore[index]
    candidate = tmp_path / "projects.json"
    candidate.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(PublicReleaseError, match="HTTPS"):
        validate_projection(candidate, SCHEMA)


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
        validate_projection(candidate, SCHEMA)


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
        validate_projection(candidate, SCHEMA)


def test_high_confidence_personal_data_is_rejected(tmp_path: Path) -> None:
    payload = _projection_payload()
    published = _first_published_fact(payload)
    published["evidence"]["exactTextDe"] = "gez. Max Mustermann"  # type: ignore[index]
    candidate = tmp_path / "projects.json"
    candidate.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(PublicReleaseError, match="personal data"):
        validate_projection(candidate, SCHEMA)


def test_published_fact_requires_an_existing_owner_decision_reference(
    tmp_path: Path,
) -> None:
    payload = _projection_payload()
    published = _first_published_fact(payload)
    published["acceptedDecision"]["decisionRef"] = "docs/review/not-a-decision.md"  # type: ignore[index]
    candidate = tmp_path / "projects.json"
    candidate.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(PublicReleaseError, match="decision reference"):
        validate_projection(candidate, SCHEMA)


def test_unreconciled_conflict_cannot_promote_a_value(tmp_path: Path) -> None:
    payload = _projection_payload()
    project = payload["projects"][0]  # type: ignore[index]
    conflict = project["conflicts"][0]
    conflict["promotedFactId"] = conflict["memberFactIds"][0]
    candidate = tmp_path / "projects.json"
    candidate.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(PublicReleaseError):
        validate_projection(candidate, SCHEMA)
