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

Released on 7 September 2026 at
[berlin-under-construction.vercel.app](https://berlin-under-construction.vercel.app).
Final production deployment: `dpl_6nmDkFLR7Uz88KtQkH3ZpSCZKTr3`, READY,
source commit `af3298c` (shared navigation and labels: `7952f79`).
[Immutable deployment](https://berlin-under-construction-hgir4mt0h-jonesg158-8681s-projects.vercel.app).

- All 183 Python tests and TypeScript checking passed before release. The final
  hosting-copy correction rebuilt all fourteen routes and passed static packaging.
- [Anonymous HTTP evidence](research/findings/2026-09-07-live-release.json): all
  fourteen HTML pages and seven assets return 200 and match the local export's
  SHA-256 hashes. Sampled responses have no Set-Cookie header and include the
  same-origin CSP. Four private paths return 404.
- Served JavaScript contains none of the checked browser-storage API identifiers.
  This is a source check, not inspection of browser storage; no browser profile,
  stored cookies or authentication state was read. CSP constrains runtime
  connections to the same origin. These checks do not prove host-wide retention
  or processing behavior.
- Chrome rendered the public 3D atlas with geographic labels and no reported
  warning/error console entries. Public dossier → index → method navigation
  worked. The [390 px public index](images/public-index-mobile.png) kept all three
  navigation links and readable content. The final legal pages displayed the
  supplied address and actual hosting wording.
- Local Chrome checks additionally covered independent label categories and
  smooth content transitions. Named-header transitions initially left the logo
  unpainted; limiting transitions to main content corrected that behavior.
- Vercel's runtime-error query returned no errors. Its static-log aggregation
  returned an empty table; that is not evidence of absent hosting logs or data
  retention. The public privacy notice preserves the unresolved Hobby DPA and
  transfer/retention limits.

The atlas still downloads approximately 26 MB and covers central Berlin. No
accuracy score is claimed; human glossary verification and golden-set work remain
open. Browser automation intermittently timed out on the heavy atlas; fresh static
route checks succeeded. This is not a comprehensive device-performance audit.
