# Architectural atlas — model and reproduction

The local atlas is an Astro page with a Three.js orthographic renderer. All
runtime scripts, styles and geometry are served by the site itself. Project
facts still come through the validated public display projection at build time;
the numeric city model is geographic context, not construction-status evidence.

## Coverage and limitations

The 7 September 2026 model contains 84,895 building/building-part shapes in
central Berlin, approximately 13 km east–west and 8 km north–south. It is not
whole-city coverage. The official source export contains 155,815 features;
shapes below 50 m² are omitted. Heights are 2022 source ridge heights, with no
vertical exaggeration. Roofs are flat extrusions rather than reconstructed LoD2
roof surfaces. Coordinates are quantized to 0.5 m. Terrain, road widths and
bridge elevations are illustrative. Water and park polygon holes are retained.

The compressed model is 26,252,745 bytes; it contains 3,056,925 triangles and
2,033,253 outline/rail segments. Geometry is grouped into 200 building tiles for
frustum culling, but this version downloads the complete model before use.
Progressive loading, lower-detail citywide coverage and low-end-device profiling
remain follow-up work. No frame-rate or mobile-performance benchmark is claimed.

## Provenance and licenses

- Buildings: [Geoportal Berlin, Gebäudehöhen 2022 (Umweltatlas)](https://daten.berlin.de/datensaetze/gebaudehohen-umweltatlas-wfs-d918088d),
  [dl-de/zero-2-0](https://www.govdata.de/dl-de/zero-2-0).
  WFS geometry is EPSG:25833. Only geometry, height, area and the numeric feature
  identifier were requested; names and addresses were not requested.
- Context: [OpenStreetMap contributors](https://www.openstreetmap.org/copyright),
  ODbL 1.0. Overpass snapshot timestamp: 2026-09-07T08:52:19Z. Numeric context
  geometry is distributed in the same model; its ODbL terms continue to apply.
- Input hashes, output hash, origin, transformation and retrieval date are in
  [`provenance.json`](../web/site-public/atlas/provenance.json). Model layout and
  coordinate quantization are in [`model.json`](../web/site-public/atlas/model.json).
  The model contains numeric coordinates only, not source-document artifacts.
- BKG boundary attribution remains visible in the static `/records/` fallback.

## Reproduce offline assets

Download data only when deliberately rebuilding the model. The owner authorized
command-line public geodata downloads after Chrome exports timed out; all
website browsing and visual testing remain in Chrome.

```sh
curl --fail --get 'https://gdi.berlin.de/services/wfs/ua_gebaeudehoehen' \
  --data-urlencode 'service=WFS' --data-urlencode 'version=2.0.0' \
  --data-urlencode 'request=GetFeature' \
  --data-urlencode 'typeNames=ua_gebaeudehoehen:gebaeudehoehen' \
  --data-urlencode 'outputFormat=application/json' \
  --data-urlencode 'propertyName=geom,hoehe,shape_area,gisid' \
  --data-urlencode 'bbox=13.3072,52.4742,13.4926,52.5432,urn:ogc:def:crs:OGC:1.3:CRS84' \
  --data-urlencode 'count=200000' -o /tmp/berlin-buildings.json
curl --fail --get 'https://overpass-api.de/api/interpreter' \
  --data-urlencode 'data=[out:json][timeout:90];(way["natural"="water"](52.47,13.30,52.55,13.50);relation["natural"="water"](52.47,13.30,52.55,13.50);way["leisure"="park"](52.47,13.30,52.55,13.50);relation["leisure"="park"](52.47,13.30,52.55,13.50);way["highway"~"^(primary|secondary|tertiary|residential|pedestrian)$"](52.47,13.30,52.55,13.50);way["railway"="rail"](52.47,13.30,52.55,13.50););out geom;' \
  -o /tmp/berlin-context.json
cd web
npm ci
node scripts/build-atlas.mjs /tmp/berlin-buildings.json /tmp/berlin-context.json
npm run typecheck
```

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
