from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest
from pydantic import ValidationError

from pipeline.coverage import (
    DepthCoverage,
    DepthSearch,
    DuplicateDepth,
    Inapplicable,
    NotChecked,
    SearchedAbsent,
    SearchedFound,
    UnknownDepth,
    Unavailable,
    financial_completion_validation,
    financial_coverage_gaps,
)
from pipeline.retrieval_config import load_retrieval_config


def config():
    return load_retrieval_config(Path("pipeline/config/retrieval.v1.toml"))[0]


def search(outcome: str = "no_hit") -> DepthSearch:
    return DepthSearch(
        method="url",
        target="https://pardok.parlament-berlin.de/starweb/adis/citat/VT/19/SchrAnfr/S19-18429.pdf",
        performed_at=datetime(2026, 8, 7, 12, 0, tzinfo=UTC),
        outcome=outcome,  # type: ignore[arg-type]
    )


def record(depth: int, disposition) -> DepthCoverage:
    return DepthCoverage(
        project_id="C-014", schema_version="1.0.0", depth=depth, disposition=disposition
    )


def test_no_coverage_at_all_gates_financial_completion() -> None:
    assert financial_coverage_gaps((), config()) == (4, 5)
    assert financial_completion_validation((), config()).outcome == "review_required"


def test_not_checked_is_not_a_disposition() -> None:
    """`not checked` must never satisfy the gate that `searched, absent` satisfies."""

    coverage = (
        record(4, NotChecked(status="not_checked")),
        record(5, NotChecked(status="not_checked")),
    )

    assert financial_coverage_gaps(coverage, config()) == (4, 5)


def test_searched_and_absent_satisfies_the_gate() -> None:
    coverage = (
        record(4, SearchedAbsent(status="searched_absent", searches=(search(),))),
        record(5, SearchedAbsent(status="searched_absent", searches=(search(),))),
    )

    assert financial_coverage_gaps(coverage, config()) == ()
    assert financial_completion_validation(coverage, config()).outcome == "pass"


def test_a_partially_covered_project_still_gates() -> None:
    coverage = (
        record(
            4,
            SearchedFound(
                status="searched_found", searches=(search("hit"),), source_ids=("source-1",)
            ),
        ),
    )

    assert financial_coverage_gaps(coverage, config()) == (5,)


def test_an_access_barrier_is_distinct_from_absence() -> None:
    coverage = (
        record(
            4,
            Unavailable(
                status="unavailable",
                searches=(search("blocked"),),
                access_barrier_detail="403 after default and browser User-Agent",
            ),
        ),
        record(5, SearchedAbsent(status="searched_absent", searches=(search(),))),
    )

    assert financial_coverage_gaps(coverage, config()) == ()


def test_a_disposition_cannot_be_recorded_without_naming_what_was_searched() -> None:
    for model, kwargs in (
        (SearchedAbsent, {"status": "searched_absent", "searches": ()}),
        (SearchedFound, {"status": "searched_found", "searches": (), "source_ids": ("s",)}),
        (
            Unavailable,
            {"status": "unavailable", "searches": (), "access_barrier_detail": "403"},
        ),
    ):
        with pytest.raises(ValidationError):
            model(**kwargs)


def test_searched_found_must_name_the_sources_it_found() -> None:
    with pytest.raises(ValidationError):
        SearchedFound(status="searched_found", searches=(search("hit"),), source_ids=())


def test_inapplicable_requires_a_human_review_decision() -> None:
    with pytest.raises(ValidationError):
        Inapplicable(status="inapplicable", rationale="kein Hauptausschuss-Vorgang")

    assigned = Inapplicable(
        status="inapplicable",
        rationale="kein Hauptausschuss-Vorgang",
        assigned_by_review_decision_id="review-7",
    )
    assert financial_coverage_gaps((record(4, assigned), record(5, assigned)), config()) == ()


def test_inapplicable_cannot_borrow_the_shape_of_a_search_result() -> None:
    with pytest.raises(ValidationError):
        Inapplicable(
            status="inapplicable",
            rationale="r",
            assigned_by_review_decision_id="review-7",
            searches=(search(),),
        )


def test_a_depth_outside_the_configured_ladder_is_rejected() -> None:
    with pytest.raises(ValidationError):
        record(6, NotChecked(status="not_checked"))


def test_a_depth_absent_from_this_configs_ladder_is_rejected() -> None:
    trimmed = config().model_copy(
        update={"evidence_depths": tuple(d for d in config().evidence_depths if d.depth != 5)}
    )

    with pytest.raises(UnknownDepth):
        financial_coverage_gaps((record(5, NotChecked(status="not_checked")),), trimmed)


def test_two_dispositions_for_one_depth_are_rejected() -> None:
    coverage = (
        record(4, SearchedAbsent(status="searched_absent", searches=(search(),))),
        record(4, NotChecked(status="not_checked")),
    )

    with pytest.raises(DuplicateDepth):
        financial_coverage_gaps(coverage, config())


def test_the_gate_reads_the_configured_depths_not_a_hardcoded_pair() -> None:
    narrowed = config().model_copy(
        update={"completion": config().completion.model_copy(update={"financial_requires_depths": (5,)})}
    )

    assert financial_coverage_gaps((), narrowed) == (5,)
