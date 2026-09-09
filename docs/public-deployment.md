# Static Vercel release

The project is `berlin-under-construction` in the owner's existing Hobby team.
Only the checked Astro export is uploaded through Vercel's Build Output API.
The retained PDF artifacts, SQLite store, pipeline source and environment files
are never deployment inputs.

## Current production update — source-stated milestone cards

Source commit `57c1e68` is READY on the stable public URL.
Deployment: `dpl_CS87Mn7ScXVj1CcpxWtR7Ldmk1P8`.
[Immutable release](https://berlin-under-construction-1juvnqtne-jonesg158-8681s-projects.vercel.app).

Six source-stated date fields now appear on five basic cards, with source arrows
and expandable exact German evidence. The total remains 150 basic listings and
three full dossiers (two located). Disputed dates and unsupported actual-start
claims stay excluded. Scope and authority: ADR-026 and the
[publication review](research/findings/2026-09-09-milestone-publication-review.md).

207 tests, TypeScript checking, static privacy/withheld scanning and packaging
passed. [Live file verification](research/findings/2026-09-09-milestones-live.json)
matched all 14 HTML routes, four CSS/JS files, two metadata files and overview
geometry; four private-path probes returned 404. Unchanged detail tiles were not
re-downloaded. The live mobile DOM showed six dates, 150 basic pins, and page
height equal to the 844 px viewport. [Mobile card evidence](images/atlas-milestone-mobile.png).
An initial authentication rejection cleared after verifying the existing CLI
session and retrying the same checked prebuilt release.

## Earlier production update — 150 basic listings, 9 September

Source commit `687058e` is READY on the stable public URL.
Deployment: `dpl_9w8A7TYp7GrxKra3FXubgfWzNc7g`.
[Immutable release](https://berlin-under-construction-3k46rk237-jonesg158-8681s-projects.vercel.app).

The main map now has 150 smaller outlined official-register reference pins and
two solid dossier pins. All three full dossiers remain available. Basic listings
publish source identity and reference location only, not verified progress or site
boundaries (ADR-025). The release also includes the previously local mobile
layout fixes and removal of Paper/Ink controls.

201 tests, TypeScript checking, the static privacy/withheld scan and packaging
passed. [Anonymous verification](research/findings/2026-09-09-basic-listings-live.json)
matched all 14 HTML routes, four CSS/JS files, two metadata files and overview
geometry to local hashes; four private-path probes returned 404. Unchanged detail
tiles were not downloaded again. Browser inspection confirmed 150 basic pins,
two dossier pins, and a 390 × 844 viewport with equal page height. Local browser
checks also exercised basic-card selection and return to the previous map view.
[Live mobile screenshot](images/atlas-basic-listings-mobile.png).

## Previous production update — whole Berlin

Source commit `7842a09` is deployed READY at the stable public URL.
Deployment: `dpl_AEZAWYx74e9z6iEEohAeYQkHrTgx`.
[Immutable citywide deployment](https://berlin-under-construction-aazimu4wt-jonesg158-8681s-projects.vercel.app).
The static envelope now contains fourteen HTML pages and 270 assets, including
263 detailed building tiles. All 184 Python tests and TypeScript checking passed.
The citywide model's coverage, 9 MB overview, tile-loading limits and remaining
source limitations are documented in [atlas-model.md](atlas-model.md).

[Anonymous citywide release checks](research/findings/2026-09-07-citywide-release.json)
passed: all fourteen pages and 270 assets returned 200 and matched local SHA-256
hashes. Sampled responses set no cookies; all four private-path probes returned
404. Served script identifier checks and same-origin CSP passed with the same
scope limits as the initial release. Chrome loaded the live Spandau detail view
with no warning/error console entries; see [public screenshot](images/atlas-spandau-live.png).
The [whole-city overview](images/atlas-citywide-overview.png) was checked locally,
including a keyboard-activated 390 px fit after adapting the minimum zoom to the
viewport. Browser automation intermittently timed out; the completed interaction
and screenshots, rather than timed-out calls, are the evidence.

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

## Initial release evidence (before the citywide expansion)

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
