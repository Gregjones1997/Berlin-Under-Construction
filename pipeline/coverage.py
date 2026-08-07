"""Evidence-depth coverage.

The playbook's completion rule (section 2): before recording a financial measure,
or a `not found` for a date or cost, check whether depths 4 and 5 cover the
project; otherwise record that the depth is inapplicable or unavailable.

This module makes that rule executable. `evidence_depths` names the ladder and
`completion.financial_requires_depths` says which rungs gate financial
completeness; both were previously validated configuration that no code read.

Three states stay distinct throughout, per AGENTS.md: found, not found (searched,
absent) and not checked. A disposition can never be recorded without naming what
was searched, because a `not found` that does not name its searches is not a
finding. Deciding that a depth does not apply is a judgment call, so
`inapplicable` requires a human review decision the way `scope_relation` does.
"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import AwareDatetime, Field, TypeAdapter

from pipeline.retrieval_config import RetrievalConfig
from pipeline.schemas import StrictModel, ValidationResult


class DepthSearch(StrictModel):
    """One search actually performed. Records the target, never a person."""

    method: Literal["url", "site_query"]
    target: str = Field(min_length=1)
    performed_at: AwareDatetime
    outcome: Literal["hit", "no_hit", "blocked"]


class NotChecked(StrictModel):
    """The default. Distinct from a search that ran and found nothing."""

    status: Literal["not_checked"]


class SearchedFound(StrictModel):
    status: Literal["searched_found"]
    searches: tuple[DepthSearch, ...] = Field(min_length=1)
    source_ids: tuple[str, ...] = Field(min_length=1)


class SearchedAbsent(StrictModel):
    """Searched and absent. Publishable evidence, but only because it names its searches."""

    status: Literal["searched_absent"]
    searches: tuple[DepthSearch, ...] = Field(min_length=1)


class Unavailable(StrictModel):
    """An access barrier stopped the search. Not the same as absent."""

    status: Literal["unavailable"]
    searches: tuple[DepthSearch, ...] = Field(min_length=1)
    access_barrier_detail: str = Field(min_length=1)


class Inapplicable(StrictModel):
    """A human decided this depth does not cover this project. Never agent-assigned."""

    status: Literal["inapplicable"]
    rationale: str = Field(min_length=1)
    assigned_by_review_decision_id: str = Field(min_length=1)


Disposition = Annotated[
    NotChecked | SearchedFound | SearchedAbsent | Unavailable | Inapplicable,
    Field(discriminator="status"),
]
disposition_adapter: TypeAdapter[
    NotChecked | SearchedFound | SearchedAbsent | Unavailable | Inapplicable
] = TypeAdapter(Disposition)

RESOLVED_STATUSES = frozenset(
    {"searched_found", "searched_absent", "unavailable", "inapplicable"}
)


class DepthCoverage(StrictModel):
    project_id: str = Field(min_length=1)
    schema_version: str = Field(min_length=1)
    depth: int = Field(ge=1, le=5)
    disposition: Disposition


class UnknownDepth(ValueError):
    """A coverage record cites a depth the configured ladder does not define."""


class DuplicateDepth(ValueError):
    """A project recorded two dispositions for the same depth."""


def _indexed(
    coverage: tuple[DepthCoverage, ...], config: RetrievalConfig
) -> dict[int, DepthCoverage]:
    known = {rung.depth for rung in config.evidence_depths}
    by_depth: dict[int, DepthCoverage] = {}
    for record in coverage:
        if record.depth not in known:
            raise UnknownDepth(f"depth {record.depth} is not in the configured ladder")
        if record.depth in by_depth:
            raise DuplicateDepth(f"depth {record.depth} recorded twice")
        by_depth[record.depth] = record
    return by_depth


def financial_coverage_gaps(
    coverage: tuple[DepthCoverage, ...], config: RetrievalConfig
) -> tuple[int, ...]:
    """Depths that gate financial completeness and have no recorded disposition."""

    by_depth = _indexed(coverage, config)
    return tuple(
        depth
        for depth in sorted(config.completion.financial_requires_depths)
        if depth not in by_depth or by_depth[depth].disposition.status not in RESOLVED_STATUSES
    )


def financial_completion_validation(
    coverage: tuple[DepthCoverage, ...], config: RetrievalConfig
) -> ValidationResult:
    """Deterministic gate. Incomplete depth coverage routes to review; it never publishes."""

    if financial_coverage_gaps(coverage, config):
        return ValidationResult(
            code="financial_depth_coverage_incomplete", outcome="review_required"
        )
    return ValidationResult(code="financial_depth_coverage_incomplete", outcome="pass")
