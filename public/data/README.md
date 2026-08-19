# Public display data

This directory is the only committed project-data input permitted to enter the
static website build. It is deliberately separate from the private SQLite store
and `data/artifacts/`.

`projects.json` conforms to `public-projection.schema.json`. A published fact
must carry a non-empty exact German evidence span, an HTTPS source URL and a
reference to an existing accepted owner decision. A withheld fact carries only
its identity, type, `withheld` state and reason code; value and evidence fields
are structurally forbidden.

`map/berlin-boundary.geojson` is a local orientation asset. Its authority,
license, retrieval date, native and bundled coordinate reference systems,
transformation and content hash are recorded in the adjacent provenance file.
The asset requires no runtime tile, API, cookie or network request.

The release check stages these files into generated output and scans every
generated asset as bytes. It requires a gitignored manifest of the current
known-withheld values:

```bash
python -m public_release \
  --known-withheld-manifest data/artifacts/public-release-known-withheld.json
```

The same scanner is intended to run over the Next.js static export once that
build exists; it is not limited to JSON and tests explicitly exercise generated
HTML and JavaScript.
