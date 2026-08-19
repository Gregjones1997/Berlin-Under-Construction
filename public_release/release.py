from __future__ import annotations

import hashlib
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


def validate_projection(
    projection_path: str | Path, schema_path: str | Path
) -> dict[str, Any]:
    """Validate the sole committed input allowed to reach public project pages."""

    projection_file = Path(projection_path)
    schema_file = Path(schema_path)
    payload = _load_object(projection_file)
    schema = _load_object(schema_file)

    for location, value in _walk(payload):
        if isinstance(value, dict):
            for key in value:
                if key.replace("_", "").lower() in PRIVATE_FIELDS:
                    raise PublicReleaseError(f"private field is forbidden at {location}.{key}")
        if isinstance(value, str) and any(
            pattern.search(value) for pattern in PERSONAL_DATA_PATTERNS
        ):
            raise PublicReleaseError(f"high-confidence personal data at {location}")

    projects = payload.get("projects")
    if isinstance(projects, list):
        for project in projects:
            if not isinstance(project, dict) or not isinstance(project.get("facts"), list):
                continue
            for fact in project["facts"]:
                if not isinstance(fact, dict) or fact.get("state") != "published":
                    continue
                evidence = fact.get("evidence")
                if not isinstance(evidence, dict):
                    continue
                exact_text = evidence.get("exactTextDe")
                if not isinstance(exact_text, str) or not exact_text.strip():
                    raise PublicReleaseError("exactTextDe must be a non-empty German span")
                source_url = evidence.get("sourceUrl")
                if not isinstance(source_url, str) or not _is_https(source_url):
                    raise PublicReleaseError("every published sourceUrl must be HTTPS")

    schema_error = _format_schema_errors(payload, schema)
    if schema_error:
        raise PublicReleaseError(f"projection schema violation: {schema_error}")

    root = projection_file.resolve().parents[2]
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
            decision_ref = fact["acceptedDecision"]["decisionRef"]
            referenced_file = root / decision_ref.partition("#")[0]
            if not referenced_file.is_file():
                raise PublicReleaseError(
                    f"accepted decision reference does not exist: {fact_id}"
                )

        for conflict in project["conflicts"]:
            if not set(conflict["memberFactIds"]).issubset(published_fact_ids):
                raise PublicReleaseError(
                    f"conflict members must be published facts: {conflict['conflictId']}"
                )
            decision_ref = conflict["acceptedDecision"]["decisionRef"]
            referenced_file = root / decision_ref.partition("#")[0]
            if not referenced_file.is_file():
                raise PublicReleaseError(
                    f"accepted conflict decision reference does not exist: {conflict['conflictId']}"
                )
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


def build_public_bundle(
    *,
    projection_path: str | Path,
    schema_path: str | Path,
    boundary_path: str | Path,
    boundary_provenance_path: str | Path,
    output_dir: str | Path,
) -> tuple[Path, ...]:
    """Validate and stage only the public projection and local map assets."""

    projection = validate_projection(projection_path, schema_path)
    validate_boundary_assets(boundary_path, boundary_provenance_path)
    output = Path(output_dir)
    data_output = output / "data"
    map_output = data_output / "map"
    map_output.mkdir(parents=True, exist_ok=True)
    targets = (
        (Path(projection_path), data_output / "projects.json"),
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
        "window.__PUBLIC_PROJECTION__="
        + json.dumps(projection, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )
    index_target = output / "index.html"
    index_target.write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<script src="/static/projection.js"></script></head><body></body></html>\n',
        encoding="utf-8",
    )
    return tuple(target for _, target in targets) + (inline_target, index_target)


def _known_withheld_values(manifest_path: Path | None) -> tuple[bytes, ...]:
    if manifest_path is None:
        return ()
    payload = _load_object(manifest_path)
    if set(payload) != {"values"} or not isinstance(payload["values"], list):
        raise PublicReleaseError("known-withheld manifest must contain only a values list")
    values: list[bytes] = []
    for value in payload["values"]:
        if not isinstance(value, str) or not value.strip():
            raise PublicReleaseError("known-withheld values must be non-empty strings")
        values.append(value.encode("utf-8"))
    return tuple(values)


def scan_static_output(
    output_dir: str | Path,
    *,
    sentinels: Iterable[str] = (),
    known_withheld_manifest: str | Path | None = None,
) -> tuple[Path, ...]:
    """Scan every generated asset as bytes for values that must not ship."""

    output = Path(output_dir)
    if not output.is_dir():
        raise PublicReleaseError("generated output directory does not exist")
    needles = tuple(
        value.encode("utf-8") for value in sentinels if isinstance(value, str) and value
    ) + _known_withheld_values(
        Path(known_withheld_manifest) if known_withheld_manifest is not None else None
    )
    files = tuple(sorted(path for path in output.rglob("*") if path.is_file()))
    if not files:
        raise PublicReleaseError("generated output contains no files")
    for path in files:
        content = path.read_bytes()
        if any(needle in content for needle in needles):
            relative = path.relative_to(output)
            raise PublicReleaseError(
                f"withheld value found in generated output: {relative.as_posix()}"
            )
    return files
