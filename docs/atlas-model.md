# Architectural atlas — model and reproduction

The local atlas is an Astro page with a Three.js orthographic renderer. All
runtime scripts, styles and geometry are served by the site itself. Project
facts still come through the validated public display projection at build time;
the numeric city model is geographic context, not construction-status evidence.

## Coverage and limitations

The citywide 7 September expansion contains **440,361 building/building-part
shapes**, compiled from all **954,230** features returned by the official Berlin
building-height dataset. It spans approximately 45.4 km east–west and 36.2 km
north–south. Source shapes below 50 m² and missing/nonpositive heights remain
omitted. Heights describe the 2022 source, not current construction progress.
Roofs are flat extrusions; terrain, road widths and bridge elevations are illustrative.

The initial overview is **9,025,128 bytes**, compared with the previous central
model's 26,252,745-byte blocking download. It includes water, forests, parks,
transport and simplified flat footprints of shapes at least 500 m². Overview
coordinates use 1 m precision; detailed geometry retains 0.5 m precision.

There are **263 independently compressed, content-hashed detail tiles** grouped
on a 2 km grid. The complete asset set is **118,236,713 bytes**, but the browser
does not fetch it all on entry. At detailed zoom it requests visible areas,
prioritizes those nearest the camera target, limits concurrency to two requests
and keeps at most 32 detail tiles resident. Leaving an area disposes its GPU
geometry. Moving during a request discards an obsolete result before attaching
it. The same-origin immutable cache can serve revisited tiles. Failed areas keep
the overview visible and show a retry message; moving after fifteen seconds
allows another attempt. The largest compressed detail tile is 1,613,582 bytes.

The base overview contains 1,212,209 triangles. These are payload measurements,
not a frame-rate or low-end-device benchmark. Chrome checked central Berlin,
Spandau, Köpenick, Wannsee in Ink, whole-city Overview, and Tegel at 390 px.
The city picker exposes eleven source-backed area anchors; it is not an address
search. Construction evidence still covers three pilot dossiers and only two
published project positions. Wider geometry does not imply wider project coverage.

## Provenance and licenses

- Buildings: [Geoportal Berlin, Gebäudehöhen 2022 (Umweltatlas)](https://daten.berlin.de/datensaetze/gebaudehohen-umweltatlas-wfs-d918088d),
  [dl-de/zero-2-0](https://www.govdata.de/dl-de/zero-2-0).
  WFS geometry is EPSG:25833. Only geometry, height, area and the numeric feature
  identifier were requested; names and addresses were not requested.
- Context: [OpenStreetMap contributors](https://www.openstreetmap.org/copyright),
  ODbL 1.0. Overpass snapshot timestamps are recorded in the model and label provenance. Numeric context
  geometry is distributed in the same model; its ODbL terms continue to apply.
- Per-page input hashes, per-tile output hashes, origin, transformation and retrieval date are in
  [`provenance.json`](../web/site-public/atlas/provenance.json). Model layout and
  coordinate quantization are in [`model.json`](../web/site-public/atlas/model.json).
  The model contains numeric coordinates only, not source-document artifacts.
- BKG boundary attribution remains visible in the static `/records/` fallback.

## Reproduce offline assets

Download data only when deliberately rebuilding the model. The owner authorized
command-line public geodata downloads after Chrome exports timed out; all
website browsing and visual testing remain in Chrome.

```sh
python3 web/scripts/download-atlas-buildings.py /tmp/berlin-city
# Download the public OSM context/places queries recorded below into that directory.
cd web
npm ci
node --max-old-space-size=8192 scripts/build-atlas.mjs /tmp/berlin-city /tmp/berlin-city/context.json
node scripts/build-labels.mjs /tmp/berlin-city/context.json
node scripts/build-places.mjs /tmp/berlin-city/places.json
npm run typecheck
```

The context query uses Overpass JSON with `out geom`, bounding box
`(52.33,13.08,52.68,13.77)`, and a 180-second timeout. It selects ways and
relations with `natural=water|wood`, `leisure=park`, or `landuse=forest`, plus
ways with `highway=motorway|trunk|primary|secondary|tertiary|residential|pedestrian`
and `railway=rail`. The separate places query selects nodes with
`place=suburb|quarter` in the same box and uses `out`. These raw exports remain
outside the public site. The compiler partitions complete, duplicate-free WFS
pages before triangulating one tile at a time. Do not publish the raw downloads.


Live exports can change. The compiler rejects incomplete building exports,
Overpass error remarks and out-of-range coordinates; a new retrieval requires
updating the recorded date and checking counts, provenance and geometry tests.
Remove obsolete generated geometry files after checking the manifest; do not
ship several historical model binaries. Retained source PDFs are unaffected.

## Browser verification

Chrome was used for Paper/Ink, plan view, source history, the unplaced C-019
record, project flights and a 390 × 844 responsive layout. Native evidence
expansion and full dossier links preserve access to source spans. The automated
export tests keep JavaScript confined to the atlas route, enforce static routes,
scan withheld/sentinel values and check the numeric payload against its manifest
and SHA-256 provenance. These checks do not establish production network,
performance or legal readiness.

## Navigation and geographic labels — 7 September follow-up

The owner accepted the atlas visually and requested a shared, persistent top
navigation with smooth transitions, plus selectable label types. All fourteen
routes now use `SiteHeader.astro`. Native CSS cross-document transitions animate
only page content, leaving the header stable; reduced-motion preferences disable
them. Other browsers retain normal link navigation. This adds no scripts to the
static routes. Implementation reference, inspected in Chrome:
[Chrome cross-document view transitions](https://developer.chrome.com/docs/web-platform/view-transitions/cross-document).

The Labels menu independently controls project markers, water and green spaces.
Twenty-six selected geographic names are compiled verbatim from the citywide retained
OSM export by `web/scripts/build-labels.mjs`. Their source identifiers, input hash
and snapshot timestamp are retained in `web/src/atlas/context-labels.json`;
source links are available in the model-information dialog. Label anchors use
feature bounding-box centers for cartographic placement. These are orientation
labels, not new construction claims or precise project locations. The whole-city expansion also adds eleven source-linked OSM navigation anchors.

Rebuild label data from `/web` with:

```sh
node scripts/build-labels.mjs /tmp/berlin-city/context.json
```
