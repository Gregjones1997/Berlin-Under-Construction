# Public candidate verification

**Checked:** 3 September 2026

**Artifact:** current uncommitted `phase-4-public-slice` candidate

**Build inputs:** `PUBLICATION_AS_OF_DATE=2026-09-03` and a clearly marked
test-only legal address

**Status:** Local release candidate verified; production address, deployment
and live-host evidence remain open.

## Automated release gate

- `.venv/bin/python -m pytest -q` passed all 178 tests.
- Astro generated 13 static HTML routes and one CSS asset.
- The public pre-application bundle contains only three data/map files. It
  contains no HTML shell or JavaScript asset.
- The local release scanner passed the three-file public bundle and all 14
  Astro export files against the known-withheld and sentinel manifests.
- `git diff --check` passed.

## Browser verification

The final candidate was served locally and checked in the gstack browser.

- At 1,280 × 720 CSS pixels, the landing page had no horizontal overflow,
  contained no script element, reported no console error and displayed the
  3 September generation date.
- At 375 × 812 CSS pixels, the flagship C-014 dossier had no horizontal
  overflow and contained no script element.
- The first Tab focused the site-home link. The second Tab focused the first
  native `summary` element. Enter opened its parent `details`, and the revealed
  original-source link was visible.
- The checked local route requested only its same-origin HTML and generated CSS.

The recruiter-facing screenshot is stored at
`docs/images/portfolio-preview.png` and embedded in the README. It contains no
legal address or private value.

## Phase-boundary review and disposition

Two read-only review lanes checked the full candidate against `main`.

- The standards lane found a legacy JavaScript display bundle, incomplete
  named-organization correction coverage, stale checklist wording, an overly
  literal stylesheet-integration record and missing disclosure for an earlier
  delegated privacy-source check. The candidate removes the legacy client
  bundle, adds the missing organization route, updates the operational record,
  reimplements the visual direction in repository CSS and records the
  orchestration in the build log.
- The specification lane found missing live deployment evidence, a weak C-014
  narrative hierarchy, missing visible translation status, a stale final-gate
  recipe and premature Vercel-host wording. The candidate keeps the live gate
  open, makes the current completion statement and history explicit, displays
  the unverified language boundary, updates the recipe and describes Vercel as
  the planned public host until live evidence exists.

The main agent independently reproduced each accepted finding against the diff,
implemented the fixes and reran the full test, build, scan and browser gates.
The reviewers made no repository edits.

## Remaining production blockers

1. Supply the owner's complete serviceable postal address through the deployment
   environment; the build fails closed without it.
2. Record the owner's choice either to launch on Vercel Hobby with the disclosed
   DPA ambiguity or to change plan/provider.
3. Create/link the Vercel project, deploy the exact candidate, then repeat the
   route, network, cookie, storage, analytics and operational-log checks against
   the live URL before calling the release public.
