"""Integrity checks for the self-hosted, numeric-only geographic model."""
import gzip
import hashlib
import json
import struct
from pathlib import Path

ATLAS = Path(__file__).resolve().parents[2] / "web/site-public/atlas"


def test_model_payload_matches_manifest_and_provenance() -> None:
    manifest = json.loads((ATLAS / "model.json").read_text())
    provenance = json.loads((ATLAS / "provenance.json").read_text())
    asset = ATLAS / Path(manifest["geometry"]).name
    packed = asset.read_bytes()
    assert provenance["modelSha256"] == "sha256:" + hashlib.sha256(packed).hexdigest()
    assert manifest["quantization"] == 2
    decoded = gzip.decompress(packed)
    assert len(decoded) == 2 * (manifest["surfaceFloats"] + manifest["edgeFloats"])
    assert manifest["buildings"] == provenance["buildings"] == 84895
    assert manifest["buildings"] < provenance["sourceFeatures"]
    assert len(tuple(ATLAS.glob("*.bin.gz"))) == 1
    # Every triangle and line segment refers to complete coordinates in bounds.
    for key, limit, stride in (("surface", manifest["surfaceFloats"], 9), ("edges", manifest["edgeFloats"], 6)):
        segments = [tile[key] for tile in manifest["tiles"]]
        segments += [manifest[k] for k in ("water", "parks", "roads") if key == "surface"]
        if key == "edges":
            segments.append(manifest["rail"])
        cursor = 0
        for segment in segments:
            assert segment["start"] == cursor
            assert segment["count"] % stride == 0
            cursor += segment["count"]
        assert cursor == limit
    # Source heights stay positive, metric and plausible; no fabricated towers.
    vertices = struct.iter_unpack("<hhh", decoded[: manifest["surfaceFloats"] * 2])
    heights = [y / manifest["quantization"] for _, y, _ in vertices]
    assert min(heights) >= 0
    assert 100 < max(heights) < 400


def test_numeric_geometry_has_public_license_and_retrieval_provenance() -> None:
    provenance = json.loads((ATLAS / "provenance.json").read_text())
    assert provenance["sourceCrs"] == "EPSG:25833"
    assert provenance["buildingLicense"] == "dl-de-zero-2.0"
    assert provenance["contextLicense"] == "ODbL-1.0"
    assert provenance["contextTimestamp"] == "2026-09-07T08:52:19Z"
    for key in ("buildingInputSha256", "contextInputSha256"):
        assert len(provenance[key]) == 71
    assert "no vertical exaggeration" in provenance["transformation"]
