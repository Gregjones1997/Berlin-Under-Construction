"""Verify every streamed payload, source pagination, and citywide coverage."""
import gzip
import hashlib
import json
import struct
from pathlib import Path

ATLAS = Path(__file__).resolve().parents[2] / 'web/site-public/atlas'


def test_model_payload_matches_manifest_and_provenance() -> None:
    manifest = json.loads((ATLAS / 'model.json').read_text())
    provenance = json.loads((ATLAS / 'provenance.json').read_text())
    assert manifest['version'] == 2
    assert manifest['buildings'] == provenance['buildings'] == 440361
    assert sum(p['features'] for p in provenance['buildingInputs']) == provenance['sourceFeatures'] == 954230
    assert manifest['bounds'][2] - manifest['bounds'][0] > 45000
    assert manifest['bounds'][3] - manifest['bounds'][1] > 36000
    assert manifest['bytes'] < 10_000_000
    assert len(manifest['tiles']) == 263
    assets = set()
    for payload in [manifest, *manifest['tiles']]:
        asset = ATLAS / Path(payload['geometry']).name
        assets.add(asset.name)
        packed = asset.read_bytes()
        assert len(packed) == payload['bytes']
        assert 'sha256:' + hashlib.sha256(packed).hexdigest() == payload['sha256']
        decoded = gzip.decompress(packed)
        assert len(decoded) == 2 * (payload['surfaceFloats'] + payload['edgeFloats'])
        assert payload['surfaceFloats'] % 9 == 0
        assert payload['edgeFloats'] % 6 == 0
        if payload is not manifest:
            assert payload['quantization'] == 2
            x0, z0, x1, z1 = payload['bounds']
            ox, oz = payload['offset']
            # Tile-local encoding must reconstruct every building vertex, including borders.
            for x, y, z in struct.iter_unpack('<hhh', decoded[:payload['surfaceFloats'] * 2]):
                assert x0 - .3 <= x / 2 + ox <= x1 + .3
                assert z0 - .3 <= z / 2 + oz <= z1 + .3
                assert 0 <= y / 2 <= payload['maxHeight'] + .3
    assert assets == {p.name for p in ATLAS.glob('*.bin.gz')}
    assert provenance['modelSha256'] == manifest['sha256']
    for keys, limit, stride in [(['overview', 'water', 'parks', 'roads'], manifest['surfaceFloats'], 9), (['rail'], manifest['edgeFloats'], 6)]:
        cursor = 0
        for key in keys:
            segment = manifest[key]
            assert segment['start'] == cursor
            assert segment['count'] % stride == 0
            cursor += segment['count']
        assert cursor == limit


def test_numeric_geometry_has_public_license_and_retrieval_provenance() -> None:
    provenance = json.loads((ATLAS / 'provenance.json').read_text())
    assert provenance['sourceCrs'] == 'EPSG:25833'
    assert provenance['buildingLicense'] == 'dl-de-zero-2.0'
    assert provenance['contextLicense'] == 'ODbL-1.0'
    assert provenance['contextTimestamp'].startswith('2026-09-07T')
    assert len(provenance['contextInputSha256']) == 71
    assert all(len(p['sha256']) == 71 for p in provenance['buildingInputs'])
    assert 'no vertical exaggeration' in provenance['transformation']
    assert '500 m²' in provenance['transformation']
