# Phase 4 public-slice merge plan

**Prepared:** 2026-08-25
**Source branch:** `phase-4-public-slice`
**Target branch:** `main`
**Status:** Proposed; do not merge until the phase-boundary review and the
owner's separate design/map integration are complete.

The merge packages a restricted-preview candidate. It does not publish a site,
promote a deployment or satisfy the public-launch legal/privacy gate.

## Preconditions

1. The owner finishes or explicitly defers the separate Gate 3 design/map work.
   No design artifact is copied verbatim; accepted work is reimplemented as
   Astro components under the display contract.
2. Both branches and the shared worktree are clean. Record the exact `main` and
   `phase-4-public-slice` tips before review.
3. The exact candidate commit passes the Python suite, Astro build, zero-client-
   JavaScript check, generated-output known-withheld/sentinel scan, internal-link
   check, and 320 px/keyboard browser checks.
4. The live deployment lane supplies its URL and completes the production-
   behavior and live-route evidence, or the merge record explicitly retains
   those items as post-merge restricted-preview blockers. No incomplete live
   check is described as passed.
5. The phase-boundary reviewer completes one full-diff review against `main`, as
   required by `AGENTS.md`. The main agent verifies and disposes every finding.

## Integration sequence

1. Fetch the current remote refs and confirm whether `main` moved after this
   plan was prepared.
2. If `main` moved, merge `origin/main` into `phase-4-public-slice`, resolve only
   real conflicts, then rerun every precondition check. Do not rewrite or force-
   push the shared phase branch.
3. Request the phase-boundary full-diff review from the merge base through the
   candidate tip. Apply accepted fixes as coherent commits on
   `phase-4-public-slice`; record rejected findings and reasons in the review
   trail when material.
4. Run the final gate against the exact reviewed tip and record its commit hash,
   test count, page count and export-scan count.
5. Merge `phase-4-public-slice` into `main` with a non-fast-forward phase merge,
   preserving the coherent phase history. Do not deploy, promote or change
   domains as part of the Git merge.
6. On `main`, rerun the Python suite and Astro/export scans before pushing.
7. Push `main`, then verify that the remote commit is the tested merge commit.

## Required final-gate commands

Run from the repository root unless a working directory is stated:

```bash
.venv/bin/python -m pytest -q

cd web
# Set both variables in the process environment before running this command:
# PUBLICATION_AS_OF_DATE must be the real merge-day YYYY-MM-DD.
# LEGAL_ADDRESS must be the owner's complete serviceable postal address.
npm run build
cd ..

.venv/bin/python -m public_release \
  --output build/gate6-public-release \
  --known-withheld-catalog public_release/known-withheld-candidates.json \
  --known-withheld-manifest build/gate6-known-withheld.json \
  --export-output web/dist
```

The command must fail if either required value is absent. After 31 August the
C-010 display must render the passed-date/no-confirmation warning and must not
assert completion.

## Merge blockers that are not fixed by Git

- Provider/controller identity.
- Complete postal address.
- Permanent monitored contact.
- Owner decision on § 18(2) MStV and, if applicable, the eligible responsible
  person and address.
- Completed production observations for requests, cookies/storage, analytics,
  operational logs, retention, subprocessors and transfers.
- Live verification of every route, correction route and source link on the
  exact deployed artifact.

These blockers prevent public launch. They do not require the branch to be kept
out of `main` if `main` and the README continue to describe only a restricted-
preview candidate.
