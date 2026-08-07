from pathlib import Path

import pytest
from pydantic import ValidationError

from pipeline.retrieval_config import RetrievalConfig, load_retrieval_config


CONFIG_PATH = Path("pipeline/config/retrieval.v1.toml")


def test_playbook_policy_loads_as_strict_versioned_configuration() -> None:
    config, digest = load_retrieval_config(CONFIG_PATH)

    assert config.fetch_policy.steps == ("default", "browser", "browser_tool")
    assert config.completion.financial_requires_depths == (4, 5)
    assert config.artifact_transforms["application/pdf"] == "pdf-metadata-strip/v1"
    assert len(digest) == 64


def test_unknown_configuration_fields_are_rejected() -> None:
    config, _ = load_retrieval_config(CONFIG_PATH)
    payload = config.model_dump()
    payload["unreviewed_policy"] = True

    with pytest.raises(ValidationError):
        RetrievalConfig.model_validate(payload)


def test_parliamentary_templates_preserve_document_identifiers() -> None:
    config, _ = load_retrieval_config(CONFIG_PATH)

    question = config.source_families["parliamentary_question"].url_template.format(
        wp=19, number="18429"
    )
    assert question.endswith("/VT/19/SchrAnfr/S19-18429.pdf")
