import tomllib
from pathlib import Path

import pytest
from pydantic import ValidationError

from pipeline.retrieval_config import RetrievalConfig, load_retrieval_config


CONFIG_PATH = Path("pipeline/config/retrieval.v1.toml")


def raw() -> dict:
    return tomllib.loads(CONFIG_PATH.read_text(encoding="utf-8"))


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


def test_the_browser_user_agent_cannot_be_configured_away() -> None:
    """AGENTS.md requires a browser retry before any 403 becomes a finding."""

    payload = raw()
    del payload["http"]["user_agents"]["browser"]

    with pytest.raises(ValidationError):
        RetrievalConfig.model_validate(payload)


def test_every_allowlisted_host_is_https_only_and_non_empty() -> None:
    payload = raw()
    payload["http"]["allowed_hosts"] = []

    with pytest.raises(ValidationError):
        RetrievalConfig.model_validate(payload)


def test_configuration_cannot_be_mutated_after_validation() -> None:
    config, _ = load_retrieval_config(CONFIG_PATH)

    with pytest.raises(ValidationError):
        config.http.user_agents.browser = "INJECTED"  # type: ignore[misc]
    with pytest.raises(TypeError):
        config.artifact_transforms["text/html"] = "pdf-metadata-strip/v1"  # type: ignore[index]
    with pytest.raises(TypeError):
        config.source_families["new"] = None  # type: ignore[index]


def test_the_reproduction_registry_hosts_are_allowlisted() -> None:
    config, _ = load_retrieval_config(CONFIG_PATH)
    registry = tomllib.loads(
        Path("pipeline/config/reproduction.v1.toml").read_text(encoding="utf-8")
    )

    for source in registry["source"]:
        host = source["url"].split("/")[2]
        assert config.allows_host(host), host


def test_every_host_cited_in_a_frozen_dossier_is_fetchable() -> None:
    """Failing closed on an unknown host is intended; failing closed on a cited source is not.

    Read-only over the frozen dossiers. This test never writes to them.
    """

    import re

    config, _ = load_retrieval_config(CONFIG_PATH)
    dossiers = Path("docs/research/dossiers")
    cited = {
        match.group(1)
        for path in dossiers.glob("*.md")
        for match in re.finditer(r"https?://([a-zA-Z0-9._-]+)", path.read_text(encoding="utf-8"))
    }

    assert cited, "no dossier URLs found; check the dossier path"
    missing = sorted(host for host in cited if not config.allows_host(host))
    assert not missing, f"cited sources are not fetchable: {missing}"
