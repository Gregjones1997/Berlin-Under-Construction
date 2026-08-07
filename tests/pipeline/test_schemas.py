from __future__ import annotations

import pytest
from pydantic import ValidationError

from pipeline.schemas import MilestoneClaim


def test_milestone_date_requires_an_explicit_milestone_type() -> None:
    payload = {
        "claim_id": "claim-1",
        "project_id": "C-010",
        "schema_version": "1.0.0",
        "claim_kind": "milestone",
        "canonical_value_de": "Fertigstellung: 2026",
        "source_id": "source-1",
        "artifact_id": "artifact-1",
        "evidence_spans": [],
        "qualifiers": [],
        "confidence": {
            "score": 0.9,
            "source": "extractor",
            "threshold_config_version": "thresholds-v1",
        },
        "review_state": "proposed",
        "validation_results": [],
        "relations": [],
        "publication_eligibility": "review_required",
        "verification_state": "unverified",
        "created_at": "2026-08-07T12:00:00Z",
        "date_value": {"precision": "year", "canonical": "2026"},
        "milestone_term_de": "Fertigstellung",
        "object_scope": "Baumaßnahme",
    }

    with pytest.raises(ValidationError) as error:
        MilestoneClaim.model_validate(payload)

    assert any(item["loc"] == ("milestone_type",) for item in error.value.errors())
