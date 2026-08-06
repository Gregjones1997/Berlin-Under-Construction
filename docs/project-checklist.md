# Project Checklist

This is the operational source of truth for what is complete, what is in progress and what comes next. Update it only when completion evidence exists.

## Status legend

- `[x]` Complete and supported by evidence.
- `[ ]` Not complete.
- `IN PROGRESS` Work currently being performed.

## Delivery targets

- **First public release target:** 1 September 2026.
- **First release:** Three verified projects, bounded extraction and evaluation, evidence-backed dossiers, and a deployable 2D map.
- **After first release:** Expand toward ten projects, then ship the technical-illustration 3D experience as a second public milestone.

Targets are planning constraints, not promises. Scope should shrink before trust, evaluation or evidence quality is compromised.

## Current position

**Current phase:** Phase 0 — Minimal foundation

**Current status:** IN PROGRESS

**Next action:** Project owner confirms the four shortlisted project identities, boundaries and exact German expected-end wording in the original sources; then scores them and selects the final three pilots.

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
- [ ] Add `.env.example` when the first environment variables are defined.
- [ ] Create the application and test directory structure.
- [x] Choose the smallest viable initial stack.
- [ ] Add formatting, linting and testing commands.
- [ ] Add a basic CI workflow.
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

- [ ] Define pilot-project selection criteria.
- [ ] Select three projects spanning different document and product problems.
- [ ] Record why each project was selected.
- [ ] Create the source registry structure.
- [ ] Record publisher, URL, access method, cadence, license and expected fields.
- [ ] Define construction categories and exclusions needed by the three pilots.
- [ ] Define lifecycle states and milestone types.
- [ ] Define financial-measure types.
- [ ] Create a controlled glossary of consequential German terms and fixed English display mappings.
- [ ] Define evidence labels and publication thresholds.
- [ ] Manually research project one.
- [ ] Manually research projects two and three.
- [ ] Capture exact German supporting passages for material claims.
- [ ] Record contradictions, ambiguity and missing information.
- [ ] Create the first golden truth set.

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

**Phase 2 exit evidence:** A dossier can be regenerated entirely from versioned claims and evidence.

## Phase 3 — Bounded AI pipeline and evaluation

- [ ] Classify representative pilot documents.
- [ ] Extract in German before translation.
- [ ] Produce typed claims with exact evidence spans.
- [ ] Validate model output against strict schemas.
- [ ] Resolve project and organization aliases conservatively.
- [ ] Detect material changes and contradictions.
- [ ] Track provider, model, prompt and schema versions.
- [ ] Track cost and latency per document from the first run.
- [ ] Evaluate financial-measure type precision.
- [ ] Evaluate organization-to-role precision.
- [ ] Evaluate citation correctness.
- [ ] Evaluate field, entity-match and contradiction recall separately.
- [ ] Measure and publish the human-review rate.
- [ ] Add correct-refusal tests.
- [ ] Document failures and threshold changes.

### Proposed v0 gates

- [ ] Financial-measure type precision reaches at least 99% on the defined pilot set.
- [ ] Organization-to-role precision reaches at least 99% on the defined pilot set.
- [ ] Citation correctness reaches at least 99% on the defined pilot set.
- [ ] Unsupported published claims remain at 0% through deterministic enforcement.
- [ ] Recall and review-rate results are published honestly, even when below target.

**Phase 3 exit evidence:** The pipeline has reproducible results, visible failures, measured costs and explicit human-review behavior.

## Phase 4 — First public 2D vertical slice

- [ ] Create the responsive project dossier page.
- [ ] Display expected end date prominently.
- [ ] Display start date and all supported date changes.
- [ ] Display status, as-of date and freshness.
- [ ] Display precise financial measures without blending definitions.
- [ ] Display organizations only by documented role.
- [ ] Keep delay and cost variance attached to the project unless explicit causal evidence exists.
- [ ] Display evidence spans and links to original sources.
- [ ] Add a clear correction link for every published project and named organization.
- [ ] Create the accessible 2D Berlin map.
- [ ] Connect project locations to dossiers.
- [ ] Add basic address or project search.
- [ ] Add stable URLs and share previews.
- [ ] Verify mobile and keyboard behavior.
- [ ] Verify public-site legal, privacy and source-use requirements using authoritative guidance.
- [ ] Deploy the first public release.
- [ ] Record a short demo walkthrough.

**Phase 4 exit evidence:** A user can locate one of three projects, see its expected end date and history, and inspect the evidence behind every consequential claim.

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
- [ ] Precision, recall, review rate, cost and latency are published.
- [ ] Failures and corrections are documented.
- [ ] Agent-assisted development process is disclosed honestly.
- [ ] Architecture diagram reflects the implemented system.
- [ ] 3D tradeoffs and later milestone are documented.
- [ ] Live demo walkthrough is recorded.
- [ ] Technical case study is written.
