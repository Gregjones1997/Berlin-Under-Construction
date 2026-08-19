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

The release check transforms the projection into a five-file pre-application
display bundle and scans every generated asset, including escaped JSON and HTML
representations. Before every scan it regenerates the gitignored manifest from
the projection's actual withheld fact IDs and a gitignored candidate catalog;
published facts cannot linger in the scan list:

```bash
python -m public_release \
  --known-withheld-catalog data/artifacts/public-release-withheld-candidates.json \
  --known-withheld-manifest data/artifacts/public-release-known-withheld.json
```

The generated display model is the only renderer input. Facts named by a
conflict are removed from the standalone list and nested only under that
conflict. It also carries the public evidence-label glossary and visible
withholding reason states.

This is the completed Gate 2 data bundle, not the Next.js application export.
The same scanner must run over the real Next.js static export during Gate 3 and
before any public deployment. Tests exercise generated
HTML, JavaScript and data assets now without claiming that later export exists.
