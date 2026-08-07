from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).parents[1]
SCHEMA_PATH = ROOT / "evaluation" / "golden-set.schema.json"
DATA_PATH = ROOT / "evaluation" / "golden-set.json"


@pytest.fixture
def schema() -> dict[str, object]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


@pytest.fixture
def golden_set() -> dict[str, object]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def validation_errors(schema: dict[str, object], instance: dict[str, object]) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [error.message for error in validator.iter_errors(instance)]


def test_empty_human_review_slots_match_the_schema(
    schema: dict[str, object], golden_set: dict[str, object]
) -> None:
    assert validation_errors(schema, golden_set) == []
    assert len(golden_set["claims"]) == 30
    assert all(claim["review_status"] == "pending-human-review" for claim in golden_set["claims"])
    assert all(claim["expected"] == {} for claim in golden_set["claims"])
    claim_ids = [claim["claim_id"] for claim in golden_set["claims"]]
    assert len(claim_ids) == len(set(claim_ids))


@pytest.mark.parametrize(
    "provenance_extras",
    [
        {},
        {"source_id": "source"},
        {"evidence_span": "span"},
        {"source_id": "source", "evidence_span": "span"},
        {"glossary_version": "1.1"},
        {"glossary_verification_status": "human-verified"},
        {
            "glossary_version": "1.1",
            "glossary_verification_status": "human-verified",
        },
        {"decision_date": "2026-08-07"},
        {"unexpected": "field"},
        {
            "source_id": "source",
            "evidence_span": "span",
            "decision_date": "2026-08-07",
        },
    ],
)
def test_model_assisted_value_is_never_valid_golden_truth(
    schema: dict[str, object],
    golden_set: dict[str, object],
    provenance_extras: dict[str, str],
) -> None:
    candidate = copy.deepcopy(golden_set)
    claim = candidate["claims"][0]
    claim["placeholder"] = False
    claim["claim_id"] = "human-assigned-claim-id"
    claim["review_status"] = "human-verified"
    claim["expected"] = {
        "canonical_value_de": {
            "value": "example",
            "provenance": {"tag": "model-assisted", **provenance_extras},
        }
    }

    errors = validation_errors(schema, candidate)

    assert any("model-assisted" in error for error in errors)


def test_populated_value_requires_exactly_one_allowed_provenance_tag(
    schema: dict[str, object], golden_set: dict[str, object]
) -> None:
    candidate = copy.deepcopy(golden_set)
    claim = candidate["claims"][0]
    claim["placeholder"] = False
    claim["claim_id"] = "human-assigned-claim-id"
    claim["review_status"] = "human-verified"
    claim["expected"] = {"canonical_value_de": {"value": "example"}}

    errors = validation_errors(schema, candidate)

    assert any("provenance" in error for error in errors)


def human_verified_claim(golden_set: dict[str, object]) -> dict[str, object]:
    claim = copy.deepcopy(golden_set["claims"][0])
    claim["placeholder"] = False
    claim["claim_id"] = "human-assigned-claim-id"
    claim["project_id"] = "C-010"
    claim["review_status"] = "human-verified"
    claim["human_review"] = {
        "reviewer_class": "german-speaking-human",
        "verified_at": "2026-08-07",
    }
    claim["expected"] = {
        "canonical_value_de": {
            "value": "example",
            "provenance": {
                "tag": "owner-judgment",
                "decision_date": "2026-08-07",
            },
        }
    }
    return claim


def test_awaiting_dataset_rejects_a_human_verified_claim(
    schema: dict[str, object], golden_set: dict[str, object]
) -> None:
    candidate = copy.deepcopy(golden_set)
    candidate["claims"][0] = human_verified_claim(golden_set)

    errors = validation_errors(schema, candidate)

    assert any("pending-human-review" in error for error in errors)


def test_human_verified_dataset_accepts_a_human_verified_claim(
    schema: dict[str, object], golden_set: dict[str, object]
) -> None:
    candidate = copy.deepcopy(golden_set)
    candidate["dataset_status"] = "human-verified"
    candidate["claims"] = [human_verified_claim(golden_set)]

    assert validation_errors(schema, candidate) == []
