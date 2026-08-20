# Project Checklist

This is the operational source of truth for what is complete, what is in progress and what comes next. Update it only when completion evidence exists.

## Status legend

- `[x]` Complete and supported by evidence.
- `[ ]` Not complete.
- `IN PROGRESS` Work currently being performed.

## Delivery targets

- **Friday 21 August target:** Password-protected access-restricted preview.
- **First public release target:** Before 1 September 2026, after provider
  identity and the Article 13 privacy notice are resolved.
- **First release:** Three evidence-backed projects, bounded extraction with disclosed metering and limitations, evidence-backed dossiers, and a deployable 2D map. Scored evaluation follows post-v0.
- **After first release:** Expand toward ten projects, then ship the technical-illustration 3D experience as a second public milestone.

Targets are planning constraints, not promises. Scope should shrink before trust, evaluation or evidence quality is compromised.

## Current position

**Current phase:** Portfolio pivot sprint — Gate 3 design handoff; Phase 2
remains incomplete

**Current status:** IN PROGRESS — REVIEW REQUIRED

**Next action:** Hold C-014 styling until the owner's separate HTML/CSS design
handoff arrives, then reimplement it as Astro components rather than copying the
artifact. The pre-design baseline now contains contextual project correction
routes, all three dossier routes, the static local Berlin boundary presentation
and the AI-method route; preserve their green export-level regressions during
design integration. Do not add a client island; if one appears necessary, stop
for a separate owner decision. CI must keep scanning the real `web/dist/`
export. Phase 2 remains incomplete.
Make no provider call. The glossary-review handoff and 25 August C-010 recheck
remain required outside this sprint unless a displayed value depends on them.

Non-blocking later-gate preparation: the Gate 6 legal/privacy/source-use review
is recorded in
[`docs/research/findings/2026-08-19-public-site-legal-privacy-source-use.md`](research/findings/2026-08-19-public-site-legal-privacy-source-use.md).
It does not advance Gate 3. Public deployment remains blocked; use an
access-restricted preview until its attribution, host/privacy, provider identity
and correction-route requirements are evidenced.
Gate 5's evidence-backed prose and figures are recorded in
[`docs/ai-method.md`](ai-method.md) and rendered without styling at `/method`.
Page design remains deferred.

**Invoked fallback, 2026-08-20:** Friday's deployment is an access-restricted,
password-protected preview. It is not the public release. Public launch moves
to before 1 September after provider identity and the Article 13 privacy notice
are resolved. The interactive map is cut in favor of a zero-JavaScript inline
SVG using the bundled BKG boundary. C-014 and C-010 are placed; C-019 remains a
linked, explicitly unplaced entry because its location is withheld pending
source verification. The correction route moves into Gate 4. Preview invitees
use the monitored channel through which they received access; a permanent
monitored address is an additional pre-public-launch blocker and is not invented.

## Phase 0 — Minimal foundation

### Already complete

- [x] Define the product thesis and concept-stage status.
- [x] Define the primary user questions, including expected end date.
- [x] Define the evidence-first product principles.
- [x] Create the initial `README.md`.
- [x] Create the living project checklist.
- [x] Obtain and process an independent planning review.
- [x] Create the transparent build-log structure.

### Repository setup

- [x] Initialize Git repository on the `main` branch.
- [x] Add `.gitignore` for local settings, secrets and generated files.
- [x] Add `.env.example` when the first environment variables are defined.
  Evidence: the committed example names `OPENAI_API_KEY` without a value and the
  CLI refuses repository `.env` loading.
- [x] Create the application and test directory structure. Evidence: `pipeline/`
  and `tests/pipeline/` exercised by pytest at `d5d5806`.
- [x] Choose the smallest viable initial stack.
- [ ] Add formatting, linting and testing commands.
- [x] Add a basic CI workflow. Evidence: `.github/workflows/quality.yml` runs
  pytest and the build-log hash check at `b81ba61`.
- [x] Make the first clean repository commit.

### Minimal documentation

- [x] Create `docs/decision-log.md`.
- [x] Record ADR: German-first extraction and display-only translation.
- [x] Record ADR: organizations named by role; natural persons excluded from v0.
- [x] Record ADR: risk-specific precision and recall targets.
- [x] Record ADR: public 2D release before technical-illustration 3D.
- [x] Record ADR: v0 stack and local pipeline execution.
- [x] Create `docs/methodology.md` from actual publication rules.
- [ ] Create `docs/data-model.md` from the first working schema.
- [ ] Add later documents only when their systems produce real evidence.

**Phase 0 exit evidence:** The repository runs locally, automated checks pass, core decisions are recorded, and the first commit is clean.

## Phase 1 — Three-project research foundation

- [x] Define pilot-project selection criteria.
- [x] Select three projects spanning different document and product problems.
- [x] Record why each project was selected.
- [ ] Create the source registry structure.
- [ ] Record publisher, URL, access method, cadence, license and expected fields.
- [ ] Define construction categories and exclusions needed by the three pilots.
- [ ] Define lifecycle states and milestone types.
- [ ] Define financial-measure types.
- [ ] Create a controlled glossary of consequential German terms and fixed English display mappings.
- [ ] Define evidence labels and publication thresholds.
- [x] Manually research project one. Evidence: committed C-014 dossier.
- [x] Manually research projects two and three. Evidence: committed C-010 and C-019 dossiers.
- [x] Capture exact German supporting passages for material claims. Evidence: three frozen dossiers at `phase-1-research-complete`.
- [x] Record contradictions, ambiguity and missing information. Evidence: quarantine, open-question and access-barrier sections in each dossier.
- [ ] Create the first golden truth set (post-v0; not on the release critical path per ADR-015).

**Partial Phase 1 evidence — every related item remains open:**

- Milestone types: nine types are defined in `pipeline/schemas.py` at `d5d5806`,
  matching `AGENTS.md`; lifecycle states are still undefined.
- Evidence labels: `ValidationCode` exists at `15ce351`. The versioned
  `thresholds-v1` file exists at `06f8e27`, closing the nonexistent-reference
  gap for `Confidence.threshold_config_version`, but it is explicitly
  uncalibrated and forces human review. Accepted publication thresholds still do
  not exist, so the item remains open.
- Source registry: not started. The `allowed_hosts` and `source_families` in
  `pipeline/config/retrieval.v1.toml` (`d5d5806`, hardened at `e9c66b4`) are
  transport configuration, not a source registry, and imply neither evidence
  depth nor source tier.
- Financial-measure types: approved in prose in `docs/data-model-proposal.md` at
  `4b840d8`; absent from code.

**Phase 1 exit evidence:** Three manually verified dossiers, a source matrix, a controlled glossary and expected extraction outputs exist.

## Phase 2 — Trustworthy data core

- [ ] Implement project, organization and source schemas.
- [ ] Implement versioned claims with original German wording.
- [ ] Implement typed milestones and financial measures.
- [ ] Store source URL, hash, publication date and retrieval date.
- [ ] Keep retained artifacts private unless redistribution is approved.
- [ ] Link every publishable claim to an evidence span.
- [ ] Enforce the invariant that unsupported claims cannot publish.
- [ ] Preserve superseded and contradictory claims.
- [ ] Add deterministic date and financial validators.
- [ ] Add a minimal review state and audit history.
- [ ] Reconstruct a complete pilot dossier from stored data.

**Phase 2 exit evidence:** A pilot dossier reconstructs from stored data alone,
with every claim's real state faithfully rendered, including withheld claims and
the reason each was withheld. The local-only withheld-detail mode verifies stored
content without changing publication eligibility.

## Phase 3 — Bounded AI pipeline; scored evaluation post-v0

- [ ] Classify representative pilot documents.
- [ ] Extract in German before translation.
- [ ] Produce typed claims with exact evidence spans.
- [ ] Validate model output against strict schemas.
- [ ] Resolve project and organization aliases conservatively.
- [ ] Detect material changes and contradictions.
- [ ] Track provider, model, prompt and schema versions.
- [ ] Track cost and latency per document from the first run.
- [ ] Evaluate financial-measure type precision (post-v0).
- [ ] Evaluate organization-to-role precision (post-v0).
- [ ] Evaluate citation correctness (post-v0).
- [ ] Evaluate field, entity-match and contradiction recall separately (post-v0).
- [ ] Measure and publish the human-review rate.
- [ ] Add correct-refusal tests.
- [ ] Document failures and threshold changes.

### Evaluation and publication gates

Scored gates marked post-v0 await the human-authored golden set. The remaining
publication and disclosure gates are binding for v0.

- [ ] Financial-measure type precision reaches at least 99% on the defined pilot set (post-v0).
- [ ] Organization-to-role precision target is deferred until the role-vocabulary ADR is accepted and eligible human-labelled data exists (post-v0); report it explicitly as deferred meanwhile.
- [ ] Citation correctness reaches at least 99% on the defined pilot set (post-v0).
- [ ] Unsupported published claims remain at 0% through deterministic enforcement.
- [ ] Human-review rate is published honestly at v0.
- [ ] Recall results are published honestly after post-v0 evaluation, even when below target.

**Phase 3 exit evidence:** The pipeline has reproducible runs, visible failures,
measured costs and explicit human-review behavior. No accuracy figure publishes
before a human-authored golden set and verified glossary exist.

## Phase 4 — First public 2D vertical slice

- [ ] Create the responsive project dossier page.
- [ ] Display expected end date prominently.
- [ ] Display start date and all supported date changes.
- [ ] Display status, as-of date and freshness.
- [ ] Display precise financial measures without blending definitions.
- [ ] Display organizations only by documented role.
- [ ] Keep delay and cost variance attached to the project unless explicit causal evidence exists.
- [ ] Display evidence spans and links to original sources.
- [x] Add a working contextual correction route for every published project
  and named organization.
- [x] Create the accessible static Berlin boundary SVG with linked dossier
  markers and visible BKG changed-data attribution.
- [x] Connect project locations to dossiers, keeping C-019 explicitly linked
  but unplaced while its location fact is withheld.
- [ ] Add basic address or project search.
- [ ] Add stable URLs and share previews.
- [ ] Verify mobile and keyboard behavior.
- [ ] Verify public-site legal, privacy and source-use requirements using authoritative guidance.
- [ ] Deploy the password-protected access-restricted preview.
- [ ] Resolve provider identity and the Article 13 privacy notice, then deploy
  the first public release before 1 September 2026.
- [ ] Record a short demo walkthrough.
- [ ] Demonstrate that accepted, verified claims render publicly while withheld
  claims remain non-public.

**Phase 4 exit evidence:** A user can locate one of three projects, see its
expected end date and history, and inspect the evidence behind every
consequential claim; accepted, verified claims render publicly and withheld
claims do not.

## Phase 5 — Coverage and operational hardening

- [ ] Expand from three projects toward ten.
- [ ] Add representative low-quality and multi-project documents.
- [ ] Improve recall without weakening precision gates.
- [ ] Reduce human-review rate only when evaluation supports the change.
- [ ] Add source-health monitoring.
- [ ] Publish the first real evaluation report.
- [ ] Write the architecture document from the implemented system.
- [ ] Write the correction policy from the operating workflow.
- [ ] Publish measured progress as a second public milestone.

## Phase 6 — Technical-illustration 3D milestone

- [ ] Select one geometry area and flagship project.
- [ ] Record geometry source, license, CRS and accuracy.
- [ ] Measure MapLibre/deck.gl versus Cesium if still undecided.
- [ ] Measure Three.js versus React Three Fiber if still undecided.
- [ ] Prototype tiling, edge extraction and device-quality tiers.
- [ ] Create the technical-illustration style.
- [ ] Link one flagship model to live project data.
- [ ] Preserve the 2D fallback and accessible dossier.
- [ ] Measure load time and frame rate.
- [ ] Publish the 3D milestone as a distinct release.

## Phase 7 — Community, monitoring and platform

- [ ] Add missing-site reports and observations.
- [ ] Add correction and moderation workflows.
- [ ] Add project and area follows.
- [ ] Add alerts and verified change digest.
- [ ] Add citywide analytics.
- [ ] Add APIs, exports and embeddable cards where licensing permits.
- [ ] Add research workspace and organization responses.
- [ ] Isolate city-specific logic for potential multi-city support.

## Feature completion checklist

- [ ] Issue has a clear acceptance criterion.
- [ ] Dependencies and risks are identified.
- [ ] Implementation is complete.
- [ ] Tests are added or updated.
- [ ] Documentation reflects real behavior.
- [ ] Accessibility and failure states are considered.
- [ ] Security, privacy and licensing implications are considered.
- [ ] Screenshot, output or demo evidence is captured.
- [ ] Relevant checks pass.
- [ ] Build log records human and agent contributions.
- [ ] Focused commit is created.
- [ ] Checklist or feature register is updated.
- [ ] Known limitations are recorded.

## Commit and agent-use checklist

- [ ] Working tree was reviewed before starting.
- [ ] Change has one coherent purpose.
- [ ] Main agent and any subagents had explicit scopes.
- [ ] Accepted and rejected agent recommendations are summarized.
- [ ] Human decisions and manual work are identified.
- [ ] Tests and documentation are included where needed.
- [ ] No secrets, personal data or raw private reasoning are logged.
- [ ] Commit message follows the project convention.
- [ ] Commit hash is added to the build log after committing.
- [ ] Commit is easy to explain to a reviewer.

## Launch readiness

- [ ] Public 2D product is live.
- [ ] Three evidence-backed project stories are demonstrable.
- [ ] Original German extraction and controlled translation are demonstrated.
- [ ] Data and provenance model are explained.
- [ ] Cost, latency and review behavior are published; no precision, recall or
  accuracy figure is published before the post-v0 golden set exists.
- [ ] Every glossary-derived output identifies the glossary version and its
  verification status; contested English types remain unresolved.
- [ ] Failures and corrections are documented.
- [ ] Agent-assisted development process is disclosed honestly.
- [ ] Architecture diagram reflects the implemented system.
- [ ] 3D tradeoffs and later milestone are documented.
- [ ] Live demo walkthrough is recorded.
- [ ] Technical case study is written.
