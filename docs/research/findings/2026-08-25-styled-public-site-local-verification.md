# Styled public-site local verification

**Checked:** 25 August 2026

**Artifact:** uncommitted styled Astro public-site candidate built from the
current working tree

**Build inputs:** `PUBLICATION_AS_OF_DATE=2026-08-25` and a clearly marked
test-only legal address

**Status:** Local candidate verified; production and the real legal address
remain unverified.

## Automated verification

- `.venv/bin/python -m pytest -q` passed all 176 tests available at that
  checkpoint.
- The focused export suite passed 15 tests, including missing-address and
  missing-date build failures, all 12 generated footers, both sides of the
  C-010 31 August wording boundary, internal routes, conflict containment,
  zero client JavaScript and the real-export privacy scans.
- A normal 25 August build generated 12 HTML pages.
- `python -m public_release ... --export-output web/dist` scanned the CSS and
  all 12 HTML pages successfully against the known-withheld and sentinel gates.
- The owner's visual direction was reimplemented in the shared Astro layout and
  repository stylesheet; the external design artifact was not added to the tree.

## 320 CSS-pixel browser result

A local static server delivered all 12 generated routes to the gstack browser
at a 320 × 720 CSS-pixel viewport. Every route reported:

- `innerWidth === 320`;
- `document.documentElement.scrollWidth === 320`;
- no horizontal overflow; and
- `document.scripts.length === 0`.

The landing page and the longest C-014 dossier were captured and visually
inspected at that viewport. The map stayed within the document width, the
project links wrapped rather than clipping, and the conflict pair collapsed to
one equal-width column per member. No hidden horizontal content was observed.

## Keyboard result

On the C-010 dossier, the first Tab focused the home link and the second Tab
focused the first native `SUMMARY` element. Enter changed its parent `DETAILS`
from closed to open. The browser reported no console errors. This verifies a
real keyboard path to the evidence without client JavaScript.

## Local network and storage observation

On the landing page the browser recorded only two same-origin requests: the
HTML document and the single generated CSS asset. It observed:

- no cookies;
- empty local storage and session storage;
- zero service-worker registrations; and
- no script elements.

These are local application-layer observations only. They do not establish
production cookies, request logging, response headers, account analytics,
retention, subprocessors or transfers. Those checks must be repeated against
the exact deployed URL and commit.
