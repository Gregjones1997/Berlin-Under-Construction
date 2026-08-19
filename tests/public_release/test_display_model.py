from __future__ import annotations

from pathlib import Path

from public_release import build_public_display_model, validate_projection


ROOT = Path(__file__).resolve().parents[2]
PROJECTION = ROOT / "public" / "data" / "projects.json"
SCHEMA = ROOT / "public" / "data" / "public-projection.schema.json"
DECISIONS = ROOT / "public" / "data" / "accepted-review-decisions.json"
NAME_ALLOWLIST = ROOT / "public" / "data" / "name-allowlist.json"


def _display_model() -> dict[str, object]:
    projection = validate_projection(
        PROJECTION,
        SCHEMA,
        review_decisions_path=DECISIONS,
        name_allowlist_path=NAME_ALLOWLIST,
        repository_root=ROOT,
    )
    return build_public_display_model(projection)


def test_conflict_members_render_only_inside_the_conflict_presentation() -> None:
    model = _display_model()
    project = model["projects"][0]  # type: ignore[index]
    standalone_ids = {fact["factId"] for fact in project["facts"]}
    conflicts = project["conflicts"]

    assert len(conflicts) == 1
    conflict = conflicts[0]
    conflict_ids = {fact["factId"] for fact in conflict["facts"]}
    assert conflict_ids == {
        "c014-places-programme-page-figure",
        "c014-places-programme-index-figure",
    }
    assert standalone_ids.isdisjoint(conflict_ids)
    assert conflict["presentationPriority"] == "conflict_over_evidence_label"
    assert "preferredFactId" not in conflict


def test_display_model_publicly_glosses_verified_without_claiming_truth() -> None:
    model = _display_model()
    verified = model["evidenceLabelGlossary"]["Verified"]  # type: ignore[index]

    assert "faithfully supported by the cited source" in verified
    assert "does not mean" in verified
    assert "conflicting value is resolved" in verified


def test_deferred_vocabulary_boundary_and_stale_status_remain_visible() -> None:
    model = _display_model()
    project = model["projects"][0]  # type: ignore[index]
    withheld = {fact["factId"]: fact for fact in project["withheldFacts"]}
    facts = {fact["factId"]: fact for fact in project["facts"]}

    assert withheld["c014-completion-period-2026"]["reasonCode"] == (
        "milestone_vocabulary_unresolved"
    )
    assert facts["c014-current-status"]["displayWarnings"] == [
        "Source status observed on 2026-08-06; freshness is unassessed. "
        "This does not verify the real-world completion state."
    ]
    assert project["leadFactId"] == "c014-expected-completion-current"
