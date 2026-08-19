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
the projection's actual withheld fact IDs and the repository scan catalog;
published facts cannot linger in the scan list. Gate 3 adds the same scan over
the real Astro export:

```bash
python -m public_release \
  --output build/gate3-public-release \
  --known-withheld-catalog public_release/known-withheld-candidates.json \
  --known-withheld-manifest build/public-release-known-withheld.json \
  --export-output web/dist
```

The pre-application bundle still emits the generated display model. The Astro
loader applies the same boundary directly to the validated projection at build
time: facts named by a conflict are removed from the standalone list and nested
only under that conflict, evidence labels are publicly glossed and withholding
reason states remain visible.

The Astro site reads the projection only at build time. Its separate public
directory prevents repository data files from being copied into `dist/`, and
the no-island build emits no JavaScript. CI builds and scans the real export;
the same check remains required before public deployment.
