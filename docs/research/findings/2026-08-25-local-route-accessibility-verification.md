# Local route, link and accessibility verification

**Checked:** 2026-08-25
**Artifact:** locally built unstyled Astro baseline
**Build date override:** `PUBLICATION_AS_OF_DATE=2026-08-25`
**Status:** Local baseline verified; the exact live deployment remains unverified.

## Route result

The browser loaded all 12 generated routes with HTTP 200:

- `/`
- `/corrections/`
- `/corrections/organizations/50hertz/`
- `/corrections/projects/C-014/`
- `/corrections/projects/C-010/`
- `/corrections/projects/C-019/`
- `/impressum/`
- `/method/`
- `/privacy/`
- `/projects/europaplatz-sued/`
- `/projects/heinrich-hertz-gymnasium-ostbahnhof/`
- `/projects/power-to-heat-heizkraftwerk-mitte/`

An export-level regression test parses every generated anchor whose `href`
starts with `/` and proves that its target HTML file exists. Each contextual
project and organization correction route retains its originating context and
separates evidence corrections, formal rights of reply and data-protection
requests.

## External links

The nine unique published evidence-source URLs and the four map attribution
targets were requested with a full browser User-Agent and redirects enabled.
All 13 returned HTTP 200 on 2026-08-25. The existing HOWOGE URL redirects to its
current `unternehmen.howoge.de` location; the committed link remains functional.

This proves current reachability from the test environment. The same links must
still be clicked or requested from the exact deployed artifact because host
headers, content-security policy or deployment routing can change behavior.

## Mobile width

At a 320 × 640 CSS-pixel viewport, every route reported:

- `document.documentElement.scrollWidth === 320`;
- no horizontal document overflow;
- `document.scripts.length === 0`; and
- every anchor had an `href`.

No styling or typography was added or changed during this check.

## Keyboard access

At 375 × 812, Tab traversed all 12 landing-page links in document order:

1. two placed project markers;
2. four map/source attribution links;
3. the linked unplaced C-019 entry;
4. all three dossier links; and
5. the Impressum and Article 13 draft links.

On the C-010 dossier, the first Tab focused the native `SUMMARY` element. Enter
opened the evidence `<details>`, and the next Tab focused its newly revealed
original-source link. This verifies the intended no-JavaScript keyboard path.

## Local application-layer privacy observation

After clearing the browser network buffer and reloading `/`, the only request
was `GET http://127.0.0.1:4173/`. The origin had:

- no cookies;
- empty local storage and session storage;
- no IndexedDB databases;
- no Cache Storage keys; and
- no service-worker registrations.

These observations apply only to the local static export. They are not evidence
about a deployment host, CDN, access layer or operational server logs.

## Verification commands and outputs

- `.venv/bin/python -m pytest -q` — 173 passed.
- `PUBLICATION_AS_OF_DATE=2026-08-25 npm run build` — 12 pages.
- `python -m public_release ... --export-output web/dist` — five generated
  bundle files and 12 Astro export files passed the known-withheld and sentinel
  scans.
- Local browser — 12 HTTP 200 routes, 320 px overflow checks and real keyboard
  traversal as described above.
