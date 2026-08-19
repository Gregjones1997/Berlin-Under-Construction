# Public display data

This directory is the only committed project-data input permitted to enter the
static website build. It is deliberately separate from the private SQLite store
and `data/artifacts/`.

`projects.json` conforms to `public-projection.schema.json`. A published fact
must carry a non-empty exact German evidence span, an HTTPS source URL and an
opaque decision ID resolved against the digest-bound accepted-owner-decision
registry. A withheld fact carries only its identity, type, `withheld` state and
reason code; value and evidence fields are structurally forbidden.

Consequential claim types retain their display semantics. Financial facts name
their measure and scope, milestone facts name their milestone type, qualifiers
are closed-class records, and every published fact carries source-date, as-of
and freshness states. Evidence labels use the methodology vocabulary and remain
separate from source tier. `name-allowlist.json` contains only reviewed public
toponyms or non-person entities; an unallowlisted capitalized bigram blocks the
projection for review.

`map/berlin-boundary.geojson` is a local orientation asset. Its authority,
license, retrieval date, native and bundled coordinate reference systems,
transformation and content hash are recorded in the adjacent provenance file.
The asset requires no runtime tile, API, cookie or network request.

The release check stages these files into a five-file pre-application bundle and
scans every generated asset, including escaped JSON and HTML representations.
It requires a gitignored manifest of the current known-withheld values:

```bash
python -m public_release \
  --known-withheld-manifest data/artifacts/public-release-known-withheld.json
```

This is the C-014 schema review checkpoint, not the Next.js application export.
The same scanner must run over the real Next.js static export after the owner
accepts the schema and before any public deployment. Tests exercise generated
HTML, JavaScript and data assets now without claiming that later export exists.
