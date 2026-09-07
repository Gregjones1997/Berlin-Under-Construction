"""The deployment envelope must contain only the dated, address-matched static export."""
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'web/scripts/package-vercel.mjs'
ADDRESS = 'Package fixture address'
DATE = '2026-09-07'


def fixture_export(tmp_path: Path) -> None:
    paths = ['index.html', 'impressum/index.html', 'privacy/index.html'] + [f'record-{i}/index.html' for i in range(11)]
    for name in paths:
        path = tmp_path / 'dist' / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f'<p>{ADDRESS}</p><p>This page was generated on {DATE}.</p>')
    atlas = tmp_path / 'dist/atlas'
    atlas.mkdir()
    (atlas / 'model.json').write_text(json.dumps({'geometry': '/atlas/berlin-fixture.bin.gz'}))
    (atlas / 'berlin-fixture.bin.gz').write_bytes(b'fixture')
    (tmp_path / 'package.json').write_text(json.dumps({'dependencies': {'astro': '7.2.3'}}))
    (tmp_path / 'private.pdf').write_text('must never be copied')


def package(tmp_path: Path, address: str = ADDRESS) -> subprocess.CompletedProcess[str]:
    return subprocess.run(['node', str(SCRIPT)], cwd=tmp_path, text=True, capture_output=True,
                          env={**os.environ, 'LEGAL_ADDRESS': address, 'PUBLICATION_AS_OF_DATE': DATE})


def test_package_routes_only_the_checked_static_export(tmp_path: Path) -> None:
    fixture_export(tmp_path)
    result = package(tmp_path)
    assert result.returncode == 0, result.stderr
    output = tmp_path / '.vercel/output'
    config = json.loads((output / 'config.json').read_text())
    assert config['version'] == 3
    assert {'src': '^/impressum/?$', 'dest': '/impressum/index.html'} in config['routes']
    assert not (output / 'static/private.pdf').exists()
    assert not (output / 'functions').exists()
    assert "connect-src 'self'" in config['routes'][0]['headers']['Content-Security-Policy']


def test_package_rejects_address_mismatch_and_private_artifacts(tmp_path: Path) -> None:
    fixture_export(tmp_path)
    assert package(tmp_path, address='Different address').returncode != 0
    (tmp_path / 'dist/private.pdf').write_text('retained source')
    result = package(tmp_path)
    assert result.returncode != 0
    assert 'Private artifact' in result.stderr
    assert not (tmp_path / '.vercel/output').exists()


def test_package_rejects_test_only_content(tmp_path: Path) -> None:
    fixture_export(tmp_path)
    with (tmp_path / 'dist/index.html').open('a') as page:
        page.write('test-only')
    result = package(tmp_path)
    assert result.returncode != 0
    assert 'Test address' in result.stderr
