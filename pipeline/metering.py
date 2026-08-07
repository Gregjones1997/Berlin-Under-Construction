from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
import re
import tomllib
from typing import Literal, Protocol

from pydantic import ConfigDict, Field, model_validator

from pipeline.extractor import parse_extraction_output
from pipeline.schemas import ExtractionMetrics, ExtractionOutput, StrictModel, ValidationResult


MILLION = Decimal(1_000_000)


class MeteringRejected(ValueError):
    """A stable, content-free rejection code safe for operational logs."""


class ProviderUsage(StrictModel):
    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)
    cached_input_tokens: int = Field(default=0, ge=0)
    cache_write_input_tokens: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def detail_counts_fit_input_total(self) -> "ProviderUsage":
        if self.cached_input_tokens + self.cache_write_input_tokens > self.input_tokens:
            raise ValueError("cached and cache-write tokens cannot exceed input_tokens")
        return self


@dataclass(frozen=True)
class ProviderRequest:
    model: str
    prompt: str
    artifact_text: str
    threshold_config_version: str
    max_output_tokens: int
    reasoning_effort: Literal["high"]
    store: Literal[False]


@dataclass(frozen=True)
class ProviderResponse:
    output_json: str
    usage: ProviderUsage
    latency_ms: int
    provider_request_id: str
    model_version: str = "gpt-5.6-luna"


class ExtractionProvider(Protocol):
    def extract(self, request: ProviderRequest) -> ProviderResponse: ...


class MeteringPolicy(StrictModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    threshold_config_version: str
    force_human_review: Literal[True]
    possible_name_allowlist_version: str
    possible_name_allowlist: frozenset[str]
    pricing_reference: str
    provider: Literal["openai"]
    model: Literal["gpt-5.6-luna"]
    currency: Literal["USD"]
    input_rate: Decimal
    cached_input_rate: Decimal
    cache_write_input_rate: Decimal
    output_rate: Decimal
    max_input_bytes: int
    max_output_tokens: int
    cost_ceiling: Decimal

    @classmethod
    def load(cls, thresholds_path: Path, pricing_path: Path) -> "MeteringPolicy":
        with thresholds_path.open("rb") as stream:
            thresholds = tomllib.load(stream)
        with pricing_path.open("rb") as stream:
            pricing = tomllib.load(stream)
        if thresholds["milestone"]["calibration_status"] != "uncalibrated":
            raise MeteringRejected("unsupported_threshold_calibration_status")
        rates = pricing["rates_per_million_tokens"]
        limits = pricing["run_limits"]
        return cls(
            threshold_config_version=thresholds["config_version"],
            force_human_review=thresholds["milestone"]["force_human_review"],
            possible_name_allowlist_version=thresholds["privacy"]["possible_name_allowlist_version"],
            possible_name_allowlist=frozenset(thresholds["privacy"]["possible_name_allowlist"]),
            pricing_reference=pricing["pricing_reference"],
            provider=pricing["provider"],
            model=pricing["model"],
            currency=pricing["currency"],
            input_rate=Decimal(rates["input"]),
            cached_input_rate=Decimal(rates["cached_input"]),
            cache_write_input_rate=Decimal(rates["cache_write_input"]),
            output_rate=Decimal(rates["output"]),
            max_input_bytes=limits["max_input_bytes"],
            max_output_tokens=limits["max_output_tokens"],
            cost_ceiling=Decimal(limits["cost_ceiling"]),
        )

    def cost(self, usage: ProviderUsage) -> Decimal:
        ordinary = usage.input_tokens - usage.cached_input_tokens - usage.cache_write_input_tokens
        return (
            Decimal(ordinary) * self.input_rate
            + Decimal(usage.cached_input_tokens) * self.cached_input_rate
            + Decimal(usage.cache_write_input_tokens) * self.cache_write_input_rate
            + Decimal(usage.output_tokens) * self.output_rate
        ) / MILLION


class MeteredExtraction(StrictModel):
    output: ExtractionOutput
    metrics: ExtractionMetrics
    validation_results: tuple[ValidationResult, ...]
    provider_request_id: str = Field(min_length=1)


_HIGH_CONFIDENCE = re.compile(
    r"(?:[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|\b(?:Herr|Frau|Dr\.)\s+[A-ZÄÖÜ][A-Za-zÄÖÜäöüß-]+|\b(?:gez\.|i\.\s*V\.)\s*[A-ZÄÖÜ])"
)
_POSSIBLE_NAME = re.compile(r"\b([A-ZÄÖÜ][a-zäöüß-]{2,}[ \t]+[A-ZÄÖÜ][a-zäöüß-]{2,})\b")


def _model_text(output: ExtractionOutput) -> str:
    values: list[str] = []
    for proposal in output.proposed_claims:
        values.extend((proposal.canonical_value_de, proposal.milestone_term_de, proposal.object_scope, proposal.date_value.canonical))
        values.extend(span.exact_text_de for span in proposal.evidence_spans)
    return "\n".join(values)


def _privacy_results(output: ExtractionOutput, policy: MeteringPolicy) -> tuple[ValidationResult, ...]:
    text = _model_text(output)
    high = "fail" if _HIGH_CONFIDENCE.search(text) else "pass"
    possible = "pass"
    for match in _POSSIBLE_NAME.finditer(text):
        if match.group(1) not in policy.possible_name_allowlist:
            possible = "review_required"
            break
    return (
        ValidationResult(code="personal_data_high_confidence", outcome=high),
        ValidationResult(code="possible_personal_name", outcome=possible),
    )


def run_metered_extraction(
    provider: ExtractionProvider,
    *,
    artifact_bytes: bytes,
    media_type: str,
    prompt: str,
    prompt_version: str,
    policy: MeteringPolicy,
) -> MeteredExtraction:
    if len(artifact_bytes) > policy.max_input_bytes:
        raise MeteringRejected("input_byte_limit")
    preflight_maximum = (
        Decimal(policy.max_input_bytes)
        * max(policy.input_rate, policy.cached_input_rate, policy.cache_write_input_rate)
        + Decimal(policy.max_output_tokens) * policy.output_rate
    ) / MILLION
    if preflight_maximum > policy.cost_ceiling:
        raise MeteringRejected("preflight_cost_ceiling")
    try:
        artifact_text = artifact_bytes.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        raise MeteringRejected("artifact_not_decodable") from None

    response = provider.extract(
        ProviderRequest(
            model=policy.model,
            prompt=prompt,
            artifact_text=artifact_text,
            threshold_config_version=policy.threshold_config_version,
            max_output_tokens=policy.max_output_tokens,
            reasoning_effort="high",
            store=False,
        )
    )
    cost = policy.cost(response.usage)
    if cost > policy.cost_ceiling:
        raise MeteringRejected("actual_cost_ceiling")
    output = parse_extraction_output(response.output_json, artifact_bytes=artifact_bytes, media_type=media_type)
    if any(proposal.confidence.threshold_config_version != policy.threshold_config_version for proposal in output.proposed_claims):
        raise MeteringRejected("threshold_config_version_mismatch")
    validations = _privacy_results(output, policy)
    for validation in validations:
        if validation.outcome != "pass":
            raise MeteringRejected(validation.code)
    return MeteredExtraction(
        output=output,
        metrics=ExtractionMetrics(
            provider=policy.provider,
            model=policy.model,
            model_version=response.model_version,
            prompt_version=prompt_version,
            extraction_schema_version="1.0.0",
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            cached_tokens=response.usage.cached_input_tokens,
            cache_write_tokens=response.usage.cache_write_input_tokens,
            latency_ms=response.latency_ms,
            cost_amount=cost,
            cost_currency=policy.currency,
            pricing_reference=policy.pricing_reference,
        ),
        validation_results=validations,
        provider_request_id=response.provider_request_id,
    )
