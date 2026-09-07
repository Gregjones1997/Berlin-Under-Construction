# Static Vercel release

The project is `berlin-under-construction` in the owner's existing Hobby team.
Only the checked Astro export is uploaded through Vercel's Build Output API.
The retained PDF artifacts, SQLite store, pipeline source and environment files
are never deployment inputs.

## Build and package

Supply the owner-approved serviceable address and the actual build date through
the shell environment; do not substitute test values for a public deployment.

```sh
cd web
npm ci
npm run typecheck
PUBLICATION_AS_OF_DATE=YYYY-MM-DD LEGAL_ADDRESS='owner-approved address' npm run build
PUBLICATION_AS_OF_DATE=YYYY-MM-DD LEGAL_ADDRESS='owner-approved address' npm run package:vercel
vercel deploy --prebuilt --prod
```

Run the full Python suite from the repository root before the release build.
The tests create dated test-address exports, so rebuild with the public values
after tests finish. The packager rejects test-only text, address/date mismatch,
source-document files and unexpected route counts. It emits fourteen explicit
HTML routes, self-hosted assets and no functions. `web/.gitignore` excludes the
Vercel link and environment files.

The packaged response policy limits scripts, connections and fonts to the same
origin. Inline styles remain necessary for map positioning. Hashed model and
script assets receive immutable caching; HTML and model metadata retain the
platform's ordinary revalidation behavior. The geometry has an explicit gzip
media type and is decompressed by the client renderer.

Configuration reference, inspected in Chrome:
[Vercel Build Output API configuration](https://vercel.com/docs/build-output-api/v3/configuration).

## Release evidence

Record the exact deployment URL, source commit, readiness, public routes,
Chrome visual checks, external-request/storage findings and platform error/log
results after deployment. Static application behavior must not be confused with
unverified hosting-layer behavior. Do not add a public URL to the README before
these checks are recorded.
