# Gstack workflow handoff — 22 September 2026

## Revisions implemented and verified

The local candidate now exposes existing source history from dossiers, uses action-led
index copy, and treats atlas initialization failure as one terminal, focusable recovery
state. It preserves the earlier milestone-first dossier, explicit mobile purpose,
coverage distinction and project-specific atlas return. No source facts, golden values,
publication rules or German canonical values changed.

Implementation commit: `e4a7466` (`feat(web): complete resident evidence journey`).

## Product, user and use-case assessment

The narrow useful product is a resident-facing path from a Berlin place to a dated
source statement, its exact German evidence, prior published statements where present,
and an honest account of what remains unsupported. The software demonstrates that
journey; it does **not** establish demand. Resident need, repeat use and willingness to
switch from official pages remain hypotheses. The next demand test is an owner-run
study with three German-capable residents using real construction questions.

## Journey results and screenshots

Browser QA exercised entry, failure recovery, phone reflow, keyboard evidence opening,
source-history navigation and correction handoff. Captures are in
[`evidence/gstack-2026-09-22/`](evidence/gstack-2026-09-22/).

- Desktop and 390/320 px atlas failure states offered the static index and retry.
- C-014 showed the current source-stated milestone before identity metadata.
- Keyboard activation opened the exact German evidence span.
- The history action reached the existing source-history section.
- The correction route preserved project context and exposed the three distinct
  contact purposes without sending anything.

## Fixes and remaining blockers

The implementation fixed a renderer-load race, repeated failure handling, stale atlas
controls after fatal failure, and ambiguous evidence/history actions. One reproduced
QA issue remains: at a 195 px CSS viewport (an approximation of 200% zoom at 390 px),
the atlas failure page can scroll horizontally because header/footer content and a long
renderer token do not fully wrap. The ordinary 320 px and 390 px phone widths pass.

The installed `/office-hours`, `/autoplan` and `/qa` skills were run. The owner asked
to wrap up before the planned `/design-review` and `/review` passes, so those passes,
the full test suite after `e4a7466`, and the narrow-reflow fix/retest remain undone.
The successful 3D atlas path could not be rerun in this browser host because WebGL
context creation failed; prior local review evidence exists, but this run makes no new
success-path claim. Production is unchanged.

## API and integration verification

No API credential is required for the implemented static/public journey. There is no
visitor-time AI, account persistence, export, correction submission endpoint or live
source refresh to verify. Original-source navigation and correction email delivery were
not completed because they leave the local product boundary.

## 60–90 second walkthrough

1. Open City Desk and state the boundary: three reviewed dossiers among 150 basic
   official-register listings; this is not a live progress survey.
2. Open Europaplatz Süd (C-014). Point out the current source-stated 2026 milestone,
   the as-of date and the warning against reading it as verified progress.
3. Expand Evidence with the keyboard. Show the exact German span and original-source
   link, then use “Review earlier source statements” to reach the retained history.
4. Return to `/#C-014` to demonstrate deterministic URL state and use the correction
   route to show the evidence, reply and data-protection channels.
5. Close on limitations: prepared committed data, deterministic rendering, no live AI,
   uneven coverage, and demand still unvalidated.

## Portfolio copy and demo CTA

**Copy:** Berlin, Under Construction is an evidence-first atlas for checking what an
official source actually says about a Berlin construction project, what it said before,
and what the record still cannot support. The public slice pairs three reviewed dossiers
with clearly labelled basic listings, preserves original German evidence and fails back
to a static index when the 3D view is unavailable.

**Demo CTA:** Follow one Berlin project from place to dated claim, exact source evidence
and correction route.

## Next concrete action

Fix and retest the 195 px reflow defect, run the full pytest suite, then complete the
installed `/design-review` and `/review` passes. Do not deploy until separately
authorized and freshly verified with valid production legal configuration.
