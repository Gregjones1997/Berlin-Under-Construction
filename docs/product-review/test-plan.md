# Product-review implementation test plan

This is the executable test plan produced by `/autoplan` for the bounded resident
evidence journey. It does not authorize deployment.

## Deterministic export checks

- C-014 renders a current-answer link to `#history-heading`; the link follows the
  current heading and precedes the target.
- C-010 and C-019 render neither that link nor the history target because they have
  no published history facts.
- The atlas coverage link begins with an action and retains the dynamic counts for
  three full dossiers and 150 basic listings.
- The old “Full project overview” wording is absent.
- C-014 says “Review source history & evidence”; dossiers without history say
  “Review published facts & evidence”; “Open full dossier” remains a static route.
- Failure markup is a focusable, labelled alert with `/records/` and retry recovery.
- Existing conflict-placement, withheld/sentinel, evidence, no-serialized-object,
  internal-link, no-island and publication-date/legal-address checks still pass.

## Build and repository checks

```text
.venv/bin/python -m pytest tests/public_release/test_astro_export.py \
                         tests/public_release/test_projection.py \
                         tests/public_release/test_static_output.py
cd web && npm run typecheck
cd web && PUBLICATION_AS_OF_DATE=2026-09-22 \
  LEGAL_ADDRESS='Local product review — not for publication' npm run build
.venv/bin/python -m pytest
git diff --check
```

The final full suite is the privacy/publication gate. Local legal configuration is
test-only and must not be deployed.

## Browser matrix

| Surface | Check |
| --- | --- |
| Desktop success | C-014 → current answer → history/evidence → exact evidence → full dossier → `/#C-014` return/reload |
| 390 px and 320 px | Purpose/CTA visible, reviewed/basic boundary clear, no horizontal overflow |
| 200% text/zoom | CTA, trust caveats, correction link, failure alert, index and retry reflow and remain keyboard-reachable |
| Keyboard | Skip/index route, project selection, history expansion, native Evidence disclosure, dossier, return and recovery order |
| Initial model 503 | `map-failure` receives focus; `atlas-failed` exists; model-only controls are absent; index/retry remain; hash is retained |
| Retry | Remove failure response, reload, verify clean success and retained selection |
| Runtime context loss | After C-014 selection, alert is focused while record/hash remain; repeated error is idempotent |
| Partial detail failure | Status explains reduced detail; fatal class absent; records and map controls remain usable |
| Reduced motion | Orbit disabled; no automatic motion; normal and fatal focus remain correct |
| Record variants | C-019 withheld location; C-010 no-history/passed-date state; one basic record with and one without a milestone |

Browser accessibility inspection should confirm landmarks, alert name/description and
focus order. Physical VoiceOver announcement is a separate device check and must not
be reported as completed by automation.

## Acceptance

No journey blocker remains if deterministic checks pass and the supported browser
matrix demonstrates success, recovery and correction handoff without publishing or
sending anything. Any reproduced issue is fixed and the affected path rerun before
the workflow moves to `/design-review` and `/review`.
