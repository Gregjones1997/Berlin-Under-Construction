from __future__ import annotations

import copy
import hashlib
import html
import html.entities
import json
import re
import shutil
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse

from jsonschema import Draft202012Validator, FormatChecker


class PublicReleaseError(ValueError):
    """A content-safe build blocker for the public release projection."""


PRIVATE_FIELDS = frozenset(
    {
        "artifactid",
        "artifacthash",
        "storedbytes",
        "pretransformresponsehash",
        "rawoutputprivate",
        "rawoutput",
        "email",
        "contactemail",
        "requestid",
    }
)

PERSONAL_DATA_PATTERNS = (
    re.compile(r"\b(?:Herr|Frau|Dr\.|Prof\.)\s+[A-ZÄÖÜ][\wÄÖÜäöüß-]+"),
    re.compile(r"\bgez\.\s+[A-ZÄÖÜ]", re.IGNORECASE),
    re.compile(r"\bi\.\s*V\.\s+[A-ZÄÖÜ]", re.IGNORECASE),
    re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
)

POSSIBLE_PERSON_NAME = re.compile(
    r"\b(?!(?:Der|Die|Das|Ein|Eine)\b)"
    r"[A-ZÄÖÜ][a-zäöüß]+(?:-[A-ZÄÖÜ][a-zäöüß]+)?\s+"
    r"[A-ZÄÖÜ][a-zäöüß]+(?:-[A-ZÄÖÜ][a-zäöüß]+)?\b"
)

EVIDENCE_LABEL_GLOSSARY = {
    "Verified": (
        "The displayed wording is faithfully supported by the cited source. "
        "It does not mean the value is current, the only official value, or that "
        "a conflicting value is resolved."
    ),
    "Corroborated": "More than one reliable source supports the displayed claim.",
    "Reported": "A reputable secondary source reports the displayed claim.",
    "Observed": "A dated observation supports visible conditions, not cause.",
    "Disputed": "Relevant counterevidence exists and review remains open.",
}


def _load_object(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PublicReleaseError(f"cannot read public JSON: {path.name}") from exc
    if not isinstance(payload, dict):
        raise PublicReleaseError(f"public JSON must be an object: {path.name}")
    return payload


def _walk(value: Any, path: str = "$") -> Iterable[tuple[str, Any]]:
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from _walk(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk(child, f"{path}[{index}]")


def _is_https(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "https" and bool(parsed.netloc) and not parsed.username


def _format_schema_errors(payload: dict[str, Any], schema: dict[str, Any]) -> str:
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(payload),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    if not errors:
        return ""
    error = errors[0]
    location = "$" + "".join(
        f"[{part}]" if isinstance(part, int) else f".{part}" for part in error.absolute_path
    )
    return f"{location}: {error.message}"


def _load_name_allowlist(path: Path) -> tuple[str, ...]:
    payload = _load_object(path)
    if set(payload) != {"schemaVersion", "terms"}:
        raise PublicReleaseError("name allowlist fields are incomplete or unexpected")
    if payload["schemaVersion"] != "public-name-allowlist/v1":
        raise PublicReleaseError("unsupported name allowlist schema")
    terms = payload["terms"]
    if not isinstance(terms, list) or any(
        not isinstance(term, str) or not term.strip() for term in terms
    ):
        raise PublicReleaseError("name allowlist terms must be non-empty strings")
    if len(set(terms)) != len(terms):
        raise PublicReleaseError("name allowlist terms must be unique")
    return tuple(terms)


def _contains_possible_person_name(value: str, allowed_terms: tuple[str, ...]) -> bool:
    candidate = value
    for term in sorted(allowed_terms, key=len, reverse=True):
        candidate = candidate.replace(term, " ")
    return POSSIBLE_PERSON_NAME.search(candidate) is not None


def _subject_digest(subject: dict[str, Any]) -> str:
    public_subject = {
        key: value for key, value in subject.items() if key != "acceptedDecision"
    }
    encoded = json.dumps(
        public_subject,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def _load_review_decisions(
    path: Path, repository_root: Path
) -> dict[str, dict[str, Any]]:
    payload = _load_object(path)
    if set(payload) != {"schemaVersion", "decisions"}:
        raise PublicReleaseError("review-decision registry fields are incomplete or unexpected")
    if payload["schemaVersion"] != "public-review-decisions/v1":
        raise PublicReleaseError("unsupported review-decision registry schema")
    records = payload["decisions"]
    if not isinstance(records, list):
        raise PublicReleaseError("review-decision registry must contain a decisions list")
    required = {
        "reviewDecisionId",
        "decision",
        "actorClass",
        "decidedOn",
        "subjectKind",
        "subjectId",
        "subjectSha256",
        "basisRef",
        "basisExactTexts",
        "acceptanceRef",
        "acceptanceExactText",
    }
    indexed: dict[str, dict[str, Any]] = {}
    root = repository_root.resolve()
    for record in records:
        if not isinstance(record, dict) or set(record) != required:
            raise PublicReleaseError("review-decision record fields are incomplete or unexpected")
        decision_id = record["reviewDecisionId"]
        if not isinstance(decision_id, str) or not decision_id.startswith("review-"):
            raise PublicReleaseError("review-decision ID is invalid")
        if decision_id in indexed:
            raise PublicReleaseError(f"duplicate review-decision ID: {decision_id}")
        if record["decision"] != "accept" or record["actorClass"] != "project_owner":
            raise PublicReleaseError("public registry may contain only owner-accepted decisions")
        if record["subjectKind"] not in {"fact", "conflict"}:
            raise PublicReleaseError("review-decision subject kind is invalid")
        if not isinstance(record["subjectId"], str) or not record["subjectId"].strip():
            raise PublicReleaseError("review-decision subject ID is invalid")
        if not isinstance(record["decidedOn"], str) or not re.fullmatch(
            r"[0-9]{4}-[0-9]{2}-[0-9]{2}", record["decidedOn"]
        ):
            raise PublicReleaseError("review-decision date is invalid")
        if not isinstance(record["subjectSha256"], str) or not re.fullmatch(
            r"sha256:[0-9a-f]{64}", record["subjectSha256"]
        ):
            raise PublicReleaseError("review-decision subject digest is invalid")
        basis_texts = record["basisExactTexts"]
        if not isinstance(basis_texts, list) or not basis_texts or any(
            not isinstance(text, str) or not text.strip() for text in basis_texts
        ):
            raise PublicReleaseError("review-decision basis texts must be non-empty")
        for ref_key, exact_texts, label in (
            ("basisRef", basis_texts, "basis"),
            ("acceptanceRef", [record["acceptanceExactText"]], "acceptance"),
        ):
            document_ref = record[ref_key]
            if not isinstance(document_ref, str) or not document_ref.startswith("docs/"):
                raise PublicReleaseError(
                    f"review-decision {label} must be a repository document"
                )
            if any(not isinstance(text, str) or not text.strip() for text in exact_texts):
                raise PublicReleaseError(
                    f"review-decision {label} text must be non-empty"
                )
            document = (root / document_ref).resolve()
            if not document.is_relative_to(root) or not document.is_file():
                raise PublicReleaseError(
                    f"review-decision {label} document does not exist"
                )
            try:
                source_text = document.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                raise PublicReleaseError(
                    f"cannot read review-decision {label} document"
                ) from exc
            if any(text not in source_text for text in exact_texts):
                raise PublicReleaseError(
                    f"review-decision {label} text is absent from frozen record"
                )
        indexed[decision_id] = record
    return indexed


def _require_accepted_decision(
    subject: dict[str, Any],
    *,
    subject_kind: str,
    decisions: dict[str, dict[str, Any]],
) -> None:
    decision_id = subject["acceptedDecision"]["reviewDecisionId"]
    decision = decisions.get(decision_id)
    subject_id = subject["factId"] if subject_kind == "fact" else subject["conflictId"]
    if (
        decision is None
        or decision["subjectKind"] != subject_kind
        or decision["subjectId"] != subject_id
        or decision["subjectSha256"] != _subject_digest(subject)
    ):
        raise PublicReleaseError(f"no accepted owner decision matches: {subject_id}")


def validate_projection(
    projection_path: str | Path,
    schema_path: str | Path,
    *,
    review_decisions_path: str | Path,
    name_allowlist_path: str | Path,
    repository_root: str | Path,
) -> dict[str, Any]:
    """Validate the sole committed input allowed to reach public project pages."""

    projection_file = Path(projection_path)
    schema_file = Path(schema_path)
    payload = _load_object(projection_file)
    schema = _load_object(schema_file)
    allowed_names = _load_name_allowlist(Path(name_allowlist_path))

    for location, value in _walk(payload):
        if isinstance(value, dict):
            for key in value:
                if key.replace("_", "").lower() in PRIVATE_FIELDS:
                    raise PublicReleaseError(f"private field is forbidden at {location}.{key}")
        if isinstance(value, str) and any(
            pattern.search(value) for pattern in PERSONAL_DATA_PATTERNS
        ):
            raise PublicReleaseError(f"high-confidence personal data at {location}")
        if isinstance(value, str) and _contains_possible_person_name(value, allowed_names):
            raise PublicReleaseError(f"possible personal name requires review at {location}")

    schema_error = _format_schema_errors(payload, schema)
    if schema_error:
        raise PublicReleaseError(f"projection schema violation: {schema_error}")

    decisions = _load_review_decisions(
        Path(review_decisions_path), Path(repository_root)
    )
    for project in payload["projects"]:
        fact_ids: set[str] = set()
        published_fact_ids: set[str] = set()
        for fact in project["facts"]:
            fact_id = fact["factId"]
            if fact_id in fact_ids:
                raise PublicReleaseError(f"duplicate factId: {fact_id}")
            fact_ids.add(fact_id)
            if fact["state"] != "published":
                continue
            published_fact_ids.add(fact_id)
            exact_text = fact["evidence"]["exactTextDe"]
            if not exact_text.strip():
                raise PublicReleaseError(f"exactTextDe must be non-empty: {fact_id}")
            source_url = fact["evidence"]["sourceUrl"]
            if not _is_https(source_url):
                raise PublicReleaseError(f"sourceUrl must be HTTPS: {fact_id}")
            for qualifier in fact["qualifiers"]:
                if qualifier["tokenDe"] not in exact_text:
                    raise PublicReleaseError(
                        f"qualifier token must occur in exact evidence: {fact_id}"
                    )
            if fact["factType"] == "financial_measure":
                if fact["scope"]["wordingDe"] not in exact_text:
                    raise PublicReleaseError(
                        f"financial scope wording must occur in exact evidence: {fact_id}"
                    )
            try:
                _require_accepted_decision(
                    fact, subject_kind="fact", decisions=decisions
                )
            except (KeyError, TypeError) as exc:
                raise PublicReleaseError(
                    f"no accepted owner decision matches: {fact_id}"
                ) from exc

        for conflict in project["conflicts"]:
            if not set(conflict["memberFactIds"]).issubset(published_fact_ids):
                raise PublicReleaseError(
                    f"conflict members must be published facts: {conflict['conflictId']}"
                )
            member_facts = [
                fact
                for fact in project["facts"]
                if fact["factId"] in conflict["memberFactIds"]
            ]
            if any(
                fact.get("measureType") != conflict["measureType"]
                or fact.get("scope", {}).get("normalizedKey") != conflict["scopeKey"]
                for fact in member_facts
            ):
                raise PublicReleaseError(
                    f"conflict key does not match member facts: {conflict['conflictId']}"
                )
            try:
                _require_accepted_decision(
                    conflict, subject_kind="conflict", decisions=decisions
                )
            except (KeyError, TypeError) as exc:
                raise PublicReleaseError(
                    f"no accepted owner decision matches: {conflict['conflictId']}"
                ) from exc
    return payload


def _iter_coordinates(value: Any) -> Iterable[tuple[float, float]]:
    if (
        isinstance(value, list)
        and len(value) >= 2
        and isinstance(value[0], (int, float))
        and isinstance(value[1], (int, float))
    ):
        yield float(value[0]), float(value[1])
        return
    if isinstance(value, list):
        for child in value:
            yield from _iter_coordinates(child)


def validate_boundary_assets(
    boundary_path: str | Path, provenance_path: str | Path
) -> dict[str, Any]:
    """Validate one local Berlin boundary and the provenance that permits bundling it."""

    boundary_file = Path(boundary_path)
    provenance = _load_object(Path(provenance_path))
    required = {
        "assetId",
        "authority",
        "dataset",
        "datasetUrl",
        "serviceUrl",
        "requestUrl",
        "retrievedOn",
        "sourceCrs",
        "bundledCrs",
        "transformation",
        "license",
        "geometrySha256",
        "runtimeRequests",
    }
    if set(provenance) != required:
        raise PublicReleaseError("boundary provenance fields are incomplete or unexpected")
    for key in ("datasetUrl", "serviceUrl", "requestUrl"):
        if not _is_https(provenance[key]):
            raise PublicReleaseError(f"boundary {key} must be HTTPS")
    license_record = provenance["license"]
    if set(license_record) != {"id", "name", "url", "attribution"}:
        raise PublicReleaseError("boundary license fields are incomplete or unexpected")
    if not _is_https(license_record["url"]):
        raise PublicReleaseError("boundary license URL must be HTTPS")
    if provenance["runtimeRequests"] != []:
        raise PublicReleaseError("boundary must not require runtime network requests")
    if provenance["bundledCrs"] != "EPSG:4326":
        raise PublicReleaseError("bundled GeoJSON must use EPSG:4326")

    try:
        boundary_bytes = boundary_file.read_bytes()
    except OSError as exc:
        raise PublicReleaseError("cannot read bundled Berlin boundary") from exc
    digest = hashlib.sha256(boundary_bytes).hexdigest()
    if provenance["geometrySha256"] != f"sha256:{digest}":
        raise PublicReleaseError("boundary geometry hash does not match provenance")
    boundary = _load_object(boundary_file)
    if boundary.get("type") != "FeatureCollection" or len(boundary.get("features", [])) != 1:
        raise PublicReleaseError("boundary must be a one-feature GeoJSON FeatureCollection")
    feature = boundary["features"][0]
    if feature.get("properties") != {"assetId": provenance["assetId"]}:
        raise PublicReleaseError("boundary properties must contain only the matching assetId")
    geometry = feature.get("geometry", {})
    if geometry.get("type") not in {"Polygon", "MultiPolygon"}:
        raise PublicReleaseError("boundary geometry must be Polygon or MultiPolygon")
    coordinates = tuple(_iter_coordinates(geometry.get("coordinates")))
    if len(coordinates) < 4:
        raise PublicReleaseError("boundary geometry has too few coordinates")
    longitudes = [coordinate[0] for coordinate in coordinates]
    latitudes = [coordinate[1] for coordinate in coordinates]
    if not (
        13.0 < min(longitudes) < 13.2
        and 13.7 < max(longitudes) < 13.9
        and 52.3 < min(latitudes) < 52.4
        and 52.6 < max(latitudes) < 52.8
    ):
        raise PublicReleaseError("boundary extent does not plausibly cover Berlin")
    return provenance


def _display_fact(fact: dict[str, Any], *, in_conflict: bool) -> dict[str, Any]:
    displayed = copy.deepcopy(fact)
    label = fact["evidence"]["evidenceLabel"]
    displayed["evidenceLabelDisplay"] = {
        "label": label,
        "gloss": EVIDENCE_LABEL_GLOSSARY[label],
        "priority": "secondary_to_conflict" if in_conflict else "normal",
    }
    warnings: list[str] = []
    if fact["factType"] == "status" and fact["freshness"]["state"] == "unassessed":
        as_of = fact["asOfDate"]
        observed_on = as_of.get("value", "an unstated date")
        warnings.append(
            f"Source status observed on {observed_on}; freshness is unassessed. "
            "This does not verify the real-world completion state."
        )
    displayed["displayWarnings"] = warnings
    return displayed


def build_public_display_model(projection: dict[str, Any]) -> dict[str, Any]:
    """Create the only shape the public renderer may consume."""

    projects: list[dict[str, Any]] = []
    for project in projection["projects"]:
        facts_by_id = {fact["factId"]: fact for fact in project["facts"]}
        conflict_member_ids = {
            fact_id
            for conflict in project["conflicts"]
            for fact_id in conflict["memberFactIds"]
        }
        standalone = [
            _display_fact(fact, in_conflict=False)
            for fact in project["facts"]
            if fact["state"] == "published"
            and fact["factId"] not in conflict_member_ids
        ]
        conflicts = []
        for conflict in project["conflicts"]:
            displayed_conflict = copy.deepcopy(conflict)
            displayed_conflict["facts"] = [
                _display_fact(facts_by_id[fact_id], in_conflict=True)
                for fact_id in conflict["memberFactIds"]
            ]
            displayed_conflict["presentationPriority"] = (
                "conflict_over_evidence_label"
            )
            conflicts.append(displayed_conflict)
        withheld = [
            copy.deepcopy(fact)
            for fact in project["facts"]
            if fact["state"] == "withheld"
        ]
        completion_candidates = [
            fact
            for fact in standalone
            if fact["factType"] == "milestone"
            and fact.get("milestoneType") == "substantial_completion"
            and fact["asOfDate"]["state"] == "verified"
        ]
        lead_fact_id = (
            max(completion_candidates, key=lambda fact: fact["asOfDate"]["value"])[
                "factId"
            ]
            if completion_candidates
            else None
        )
        projects.append(
            {
                "projectId": project["projectId"],
                "slug": project["slug"],
                "correctionPath": project["correctionPath"],
                "leadFactId": lead_fact_id,
                "facts": standalone,
                "conflicts": conflicts,
                "withheldFacts": withheld,
            }
        )
    return {
        "schemaVersion": "public-display-model/v1",
        "evidenceLabelGlossary": copy.deepcopy(EVIDENCE_LABEL_GLOSSARY),
        "projects": projects,
    }


def build_public_bundle(
    *,
    projection_path: str | Path,
    schema_path: str | Path,
    boundary_path: str | Path,
    boundary_provenance_path: str | Path,
    review_decisions_path: str | Path,
    name_allowlist_path: str | Path,
    output_dir: str | Path,
) -> tuple[Path, ...]:
    """Validate and stage only the public projection and local map assets."""

    projection_file = Path(projection_path)
    repository_root = projection_file.resolve().parents[2]
    projection = validate_projection(
        projection_path,
        schema_path,
        review_decisions_path=review_decisions_path,
        name_allowlist_path=name_allowlist_path,
        repository_root=repository_root,
    )
    display_model = build_public_display_model(projection)
    validate_boundary_assets(boundary_path, boundary_provenance_path)
    output = Path(output_dir)
    expected_relative_files = {
        Path("data/display-model.json"),
        Path("data/map/berlin-boundary.geojson"),
        Path("data/map/berlin-boundary.provenance.json"),
        Path("static/projection.js"),
        Path("index.html"),
    }
    if output.exists():
        existing = {
            path.relative_to(output) for path in output.rglob("*") if path.is_file()
        }
        unexpected = existing - expected_relative_files
        if unexpected:
            raise PublicReleaseError(
                "generated output contains unexpected pre-existing files"
            )
    data_output = output / "data"
    map_output = data_output / "map"
    map_output.mkdir(parents=True, exist_ok=True)
    display_target = data_output / "display-model.json"
    display_target.write_text(
        json.dumps(display_model, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    targets = (
        (Path(boundary_path), map_output / "berlin-boundary.geojson"),
        (
            Path(boundary_provenance_path),
            map_output / "berlin-boundary.provenance.json",
        ),
    )
    for source, target in targets:
        shutil.copyfile(source, target)
    static_output = output / "static"
    static_output.mkdir(parents=True, exist_ok=True)
    inline_target = static_output / "projection.js"
    inline_target.write_text(
        "window.__PUBLIC_DISPLAY_MODEL__="
        + json.dumps(display_model, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )
    index_target = output / "index.html"
    index_target.write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<script src="/static/projection.js"></script></head><body></body></html>\n',
        encoding="utf-8",
    )
    return (display_target,) + tuple(target for _, target in targets) + (
        inline_target,
        index_target,
    )


def regenerate_known_withheld_manifest(
    *,
    projection_path: str | Path,
    candidate_catalog_path: str | Path,
    manifest_path: str | Path,
) -> dict[str, Any]:
    """Build the local scan list from the projection's current withheld IDs."""

    projection_file = Path(projection_path)
    projection = _load_object(projection_file)
    catalog = _load_object(Path(candidate_catalog_path))
    if set(catalog) != {"valuesByFactId"} or not isinstance(
        catalog["valuesByFactId"], dict
    ):
        raise PublicReleaseError(
            "known-withheld candidate catalog must contain only valuesByFactId"
        )
    values_by_fact_id = catalog["valuesByFactId"]
    withheld_ids = sorted(
        fact["factId"]
        for project in projection.get("projects", [])
        for fact in project.get("facts", [])
        if fact.get("state") == "withheld"
    )
    if len(set(withheld_ids)) != len(withheld_ids):
        raise PublicReleaseError("withheld fact IDs must be unique")
    missing = set(withheld_ids) - set(values_by_fact_id)
    if missing:
        raise PublicReleaseError("known-withheld catalog is missing current fact IDs")

    values: list[str] = []
    seen: set[str] = set()
    for fact_id in withheld_ids:
        candidates = values_by_fact_id[fact_id]
        if not isinstance(candidates, list) or any(
            not isinstance(value, str) or not value.strip() for value in candidates
        ):
            raise PublicReleaseError(
                "known-withheld catalog values must be lists of non-empty strings"
            )
        for value in candidates:
            if value not in seen:
                seen.add(value)
                values.append(value)

    result = {
        "schemaVersion": "known-withheld-manifest/v1",
        "projectionSha256": (
            "sha256:" + hashlib.sha256(projection_file.read_bytes()).hexdigest()
        ),
        "withheldFactIds": withheld_ids,
        "values": values,
    }
    manifest_file = Path(manifest_path)
    manifest_file.parent.mkdir(parents=True, exist_ok=True)
    manifest_file.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return result


def _known_withheld_values(
    manifest_path: Path | None, projection_path: Path | None
) -> tuple[str, ...]:
    if manifest_path is None:
        return ()
    if projection_path is None:
        raise PublicReleaseError(
            "current projection is required with a known-withheld manifest"
        )
    payload = _load_object(manifest_path)
    required = {
        "schemaVersion",
        "projectionSha256",
        "withheldFactIds",
        "values",
    }
    if set(payload) != required or payload["schemaVersion"] != (
        "known-withheld-manifest/v1"
    ):
        raise PublicReleaseError("known-withheld manifest fields are invalid")
    projection_bytes = projection_path.read_bytes()
    expected_hash = f"sha256:{hashlib.sha256(projection_bytes).hexdigest()}"
    projection = _load_object(projection_path)
    expected_ids = sorted(
        fact["factId"]
        for project in projection.get("projects", [])
        for fact in project.get("facts", [])
        if fact.get("state") == "withheld"
    )
    if (
        payload["projectionSha256"] != expected_hash
        or payload["withheldFactIds"] != expected_ids
    ):
        raise PublicReleaseError(
            "known-withheld manifest does not match current projection"
        )
    if not isinstance(payload["values"], list):
        raise PublicReleaseError("known-withheld values must be a list")
    values: list[str] = []
    for value in payload["values"]:
        if not isinstance(value, str) or not value.strip():
            raise PublicReleaseError("known-withheld values must be non-empty strings")
        values.append(value)
    return tuple(values)


def _needle_variants(value: str) -> tuple[bytes, ...]:
    json_escaped = json.dumps(value, ensure_ascii=True)[1:-1]
    named_entities = "".join(
        f"&{html.entities.codepoint2name[ord(character)]};"
        if ord(character) in html.entities.codepoint2name
        else character
        for character in value
    )
    variants = {
        value,
        json_escaped,
        re.sub(
            r"\\u([0-9a-f]{4})",
            lambda match: "\\u" + match.group(1).upper(),
            json_escaped,
        ),
        value.encode("ascii", "xmlcharrefreplace").decode("ascii"),
        named_entities,
    }
    return tuple(variant.encode("utf-8") for variant in variants if variant)


def scan_static_output(
    output_dir: str | Path,
    *,
    sentinels: Iterable[str] = (),
    known_withheld_manifest: str | Path | None = None,
    projection_path: str | Path | None = None,
) -> tuple[Path, ...]:
    """Scan every generated asset as bytes for values that must not ship."""

    output = Path(output_dir)
    if not output.is_dir():
        raise PublicReleaseError("generated output directory does not exist")
    values = tuple(
        value for value in sentinels if isinstance(value, str) and value
    ) + _known_withheld_values(
        Path(known_withheld_manifest) if known_withheld_manifest is not None else None,
        Path(projection_path) if projection_path is not None else None,
    )
    needles = tuple(
        variant for value in values for variant in _needle_variants(value)
    )
    files = tuple(sorted(path for path in output.rglob("*") if path.is_file()))
    if not files:
        raise PublicReleaseError("generated output contains no files")
    for path in files:
        content = path.read_bytes()
        decoded_html = html.unescape(content.decode("utf-8", errors="ignore"))
        if any(needle in content for needle in needles) or any(
            value in decoded_html for value in values
        ):
            relative = path.relative_to(output)
            raise PublicReleaseError(
                f"withheld value found in generated output: {relative.as_posix()}"
            )
    return files
