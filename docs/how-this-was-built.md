# How This Was Built

This document records how Berlin, Under Construction is developed: the human decisions, AI-agent contributions, manual work, failures, verification and resulting commits.

The purpose is accountability and reproducibility. It is not a transcript of private reasoning or every conversation.

## Logging policy

Logging is tiered so that this record survives a four-week sprint. A log that stops halfway through the project is worse than no log at all.

### Short entries — routine work

Most work gets one line. Use this for scaffolding, wiring, styling, refactors, test additions and anything mechanical:

```markdown
- 2026-08-12 — Codex: dossier page scaffold. Verified: renders pilot 1 from DB. `abc1234`
```

Format: date, participant, what changed, how it was verified, commit hash. Several small commits toward one outcome may share a line.

### Full entries — consequential work

Use the full template below only when the work changes the product plan, architecture, data model, publication policy, legal posture, model or provider choice, or evaluation thresholds. Expect roughly ten of these across the project. A consequential decision is recorded even when it produces no commit.

When a main agent delegates to subagents, the main agent owns the final entry. Record:

- The main agent and each subagent or external reviewer used.
- The narrow responsibility assigned to each participant.
- The useful output or recommendation each participant produced.
- Which recommendations were accepted, modified or rejected and why.
- What the project owner decided.
- What was completed manually.
- What files or systems changed.
- How the result was verified.
- Known limitations, failures and follow-up work.
- The final commit hash once available.

Do not record:

- Private chain-of-thought or hidden reasoning.
- Secrets, credentials, tokens or private environment values.
- Personal data that is unnecessary for understanding the work.
- Large raw prompt or chat transcripts.
- Claims that an agent completed work that was not independently checked.

## Roles

- **Project owner:** Defines the goal, makes product decisions, reviews outcomes and accepts tradeoffs.
- **Main agent:** Coordinates the task, integrates contributions, edits the repository and verifies the result.
- **Subagent:** Handles a clearly bounded research, implementation, testing or review task under the main agent.
- **External reviewer:** Provides independent critique but does not control the repository or final decision.

Agent output is treated as a proposal until the main agent or project owner verifies and accepts it.

## Full entry template

Copy this section for consequential work only. Routine work uses the one-line short entry described above.

```markdown
## YYYY-MM-DD — Short task title

**Status:** Planned | In progress | Complete | Superseded

**Commit:** Pending | `<hash>` — `<message>`

### Goal

What outcome was needed and why?

### Participants and scopes

- Project owner: decision or review responsibility.
- Main agent (`provider/model or tool`): implementation and integration scope.
- Subagent (`provider/model or tool`): bounded delegated scope, if any.
- External reviewer (`provider/model or person`): review scope, if any.

### Work performed

- Concrete implementation, research or documentation performed.
- Manual work performed by the project owner.

### Decisions

- Accepted recommendation and rationale.
- Modified or rejected recommendation and rationale.

### Verification

- Tests, checks, source review, screenshots or manual validation performed.

### Failures and limitations

- What failed, remains uncertain or requires follow-up.

### Evidence

- Changed files, test output, evaluation result, issue or demo link.
```

## 2026-08-05 — Product planning and release sequencing

**Status:** Complete

**Commit:** `6a84726` — docs: establish project foundation

### Goal

Turn the product blueprint into an honest README and an operational build sequence suitable for a first public release.

### Participants and scopes

- Project owner: provided the blueprint, established the expected-end-date priority, requested a persistent checklist and approved revising the delivery strategy.
- Main agent (OpenAI Codex): reviewed the blueprint, drafted the README and checklist, integrated review feedback and maintained the workspace documents.
- External reviewer (Claude): reviewed the initial plan for delivery risk, release timing, German terminology, publication precision, legal-risk boundaries and AI-development disclosure.
- Subagents: none used for this task.

### Work performed

- Created the initial project README from the blueprint.
- Made expected completion date a primary user-facing question.
- Created a living project checklist.
- Reframed the initial release around three verified projects, bounded AI evaluation and a 2D map.
- Deferred advanced 3D work to a distinct later milestone.
- Added a transparent process for recording AI-agent assistance.

### Decisions

- Accepted the recommendation to target a small public vertical slice before expanding coverage.
- Accepted German-first extraction with controlled translation at the display layer.
- Accepted separate precision and recall measures instead of one blended accuracy score.
- Accepted deterministic evidence-span enforcement for published claims.
- Accepted organization-by-role naming and exclusion of natural persons for v0 as a cautious product policy.
- Modified the ten-project starting scope to three projects for the first release, expanding toward ten afterward.
- Treated legal assertions from the review as research leads requiring authoritative verification before launch.

### Verification

- Compared the review feedback with the original blueprint, README and checklist.
- Checked that planned features remain described as future work rather than completed implementation.
- Checked that the revised order preserves the evidence-first product thesis.

### Failures and limitations

- The repository has not yet been initialized as Git, so no commit hash exists.
- Technology choices and metric thresholds remain proposals until prototypes and pilot data provide evidence.
- German legal, privacy and source-reuse requirements have not yet been verified against authoritative guidance.

### Evidence

- `README.md`
- `docs/project-checklist.md`
- `docs/how-this-was-built.md`

## Short entries

- 2026-08-05 — Codex: extracted the complete feature register, moved the blueprint binary to `~/Documents/berlin-blueprint-private`, removed recruitment framing and replaced the public history. Verified: one commit, no DOCX in history and no recruitment-framing hits. `6a84726`
- 2026-08-05 — Claude: drafted `docs/methodology.md` (evidence labels, financial-measure and milestone definitions, publication thresholds, status rules, correction process), cross-referencing the existing ADRs rather than duplicating them. Verified: reviewed against README, decision log and feature register for consistency; approved by the project owner. `af0e412`
- 2026-08-05 — Claude: backfilled build-log entries for `e029383` and `f5fb60b` (both previously un-logged or left `Commit: Pending`), added `**Amended**` notes to ADR-003 and ADR-004, and added a "log at commit time, not after" rule to `AGENTS.md`. Verified: reviewed and approved by the project owner. `03e9deb`

## 2026-08-05 — Initialize local Git repository

**Status:** Complete

**Commit:** `6a84726` — docs: establish project foundation

### Goal

Place the project under local version control and prevent machine-specific or sensitive local files from entering the first commit.

### Participants and scopes

- Project owner: authorized connecting the workspace to Git.
- Main agent (OpenAI Codex): initialized the repository, reviewed untracked files and added ignore rules.
- Subagents: none used for this task.

### Work performed

- Initialized a Git repository with `main` as the initial branch.
- Added `.gitignore` rules for macOS metadata, local AI-tool settings, environment files, dependencies, generated output, logs and editor settings.
- Preserved the project blueprint as an untracked project file pending the first-commit decision.
- Updated the project checklist.

### Decisions

- Kept `.claude/settings.local.json` out of version control because it is machine-specific configuration.
- Kept `.DS_Store` out of version control.
- Did not create a GitHub remote or make a commit because those are separate steps and Git author identity is not currently configured in this repository.

### Verification

- Confirmed the repository is on `main` with no commits.
- Confirmed ignored local files no longer appear as commit candidates.

### Failures and limitations

- No Git remote is configured.
- Git author name and email still need to be configured before the first commit.

### Evidence

- `.git/`
- `.gitignore`
- `docs/project-checklist.md`
- `docs/how-this-was-built.md`

## 2026-08-05 — Record initial architecture and policy decisions

**Status:** Complete

**Commit:** `e029383` — docs(decisions): record initial architecture and policy ADRs

### Goal

Record the five decisions needed to begin implementation without leaving architecture and publication rules implicit.

### Participants and scopes

- Project owner: confirmed that implementation should begin collaboratively and approved the decision-log step.
- Main agent (OpenAI Codex): drafted and cross-checked the ADRs against `AGENTS.md`, `README.md` and the project checklist.
- External reviewer (Claude): supplied the release-sequencing, German-first, naming-policy and evaluation recommendations that informed the decisions.
- Subagents: none used for this task.

### Decisions

- Preserve German source wording and translate only at the display layer.
- Name organizations by documented role and exclude natural persons from v0.
- Separate precision-critical quality gates from recall and report human review.
- Ship the accessible 2D public product before advanced 3D.
- Use the small typed v0 stack already specified in `AGENTS.md`, with the pipeline running locally until the first release.

### Verification

- Confirmed each ADR has context, decision, consequences and reconsideration conditions.
- Confirmed the stack matches `AGENTS.md`.
- Confirmed the checklist next action advances to methodology.

### Failures and limitations

- Metric thresholds remain proposals until the manually verified pilot set exists.
- Legal and privacy requirements still require authoritative review before launch.

### Evidence

- `docs/decision-log.md`
- `docs/project-checklist.md`

## 2026-08-05 — Clarify evaluation-gate and 3D-sequencing wording

**Status:** Complete

**Commit:** `f5fb60b` — docs(decisions): clarify evaluation gates and 3D sequencing

### Goal

Close two review findings against the newly recorded ADR-003 and ADR-004: the 99% evaluation targets read as firm commitments rather than provisional release hypotheses, and ADR-004's reconsideration clause had no floor, meaning a persuasive argument could pull 3D work into the first release ahead of its fixed date.

### Participants and scopes

- Project owner: reviewed both findings and asked for the wording fixed without a commit.
- External reviewer (Claude): identified the two findings during a decision-log review, drafted the replacement wording for ADR-003 and ADR-004 in place.
- Main agent (OpenAI Codex): committed the reviewed wording.
- Subagents: none used for this task.

### Work performed

- ADR-003: reworded the three 99% figures as targets rather than fixed thresholds, called out the unsupported-claims rule as the one true zero-tolerance invariant, and added that the release publishes its real measured numbers, including below-target ones, rather than withholding launch until targets are hit.
- ADR-004: added a floor to the reconsideration clause — the trigger conditions may be noted before the first release, but do not pull 3D work forward into it regardless of how compelling they look mid-sprint.

### Decisions

- Accepted both wording changes as drafted; the underlying decisions in ADR-003 and ADR-004 did not change, only their precision.
- Treated this as a clarification of the existing ADRs rather than a new ADR, since no decision reversed.

### Verification

- Re-read both ADRs end to end after editing to confirm the Decision and Reconsider-when sections no longer contradict the Context section's hedging language.
- Confirmed via `git diff` that no other ADR content was touched.

### Failures and limitations

- This edit was not recorded in this log at the time it was committed; it is being backfilled now. See the entry above for the same gap on `e029383`.

### Evidence

- `docs/decision-log.md`

## 2026-08-05 — Research plan: source availability as a product differentiator

**Status:** In progress

**Commit:** Pending review

### Goal

Design the first research pass for selecting three pilot projects while preserving the complexity of finding and verifying fragmented public information.

### Participants and scopes

- Project owner: reviewed the initial orchestration results and decided that source availability and discovery difficulty should be treated as core product value, not merely a research obstacle.
- Main agent (OpenAI Codex): coordinated six bounded, read-only Luna research tasks and synthesized their outputs.
- Luna research agents: one selection-rubric task, one official-source ecosystem map, three category-specific candidate scans, and one adversarial bias review.
- Claude: reserved for deeper finalist dossier review after the candidate pool and rubric are frozen.

### Decisions

- Agents will produce a broad candidate pool; they will not independently select the final three projects.
- The scoring rubric will be frozen before candidates are scored.
- Source availability and researchability will be scored separately from public value and research importance.
- The candidate pool will deliberately include projects whose public evidence is fragmented, difficult to discover, scanned, moved, or distributed across agencies and document types.
- The first three projects should form a balanced set: at least one bounded case, one complex multi-source case, and one hard-to-discover public-information case.
- The source-ecosystem map is a first-class research output. It should show where project identity, dates, budgets, procurement, planning, contracts, geometry and updates are actually found.
- Every candidate, exclusion reason, failed search path, dead or inaccessible source and unresolved gap should be retained in the research record.
- A candidate will not be rejected merely because its information is difficult to find; it will be rejected when the evidence cannot be recovered or verified within the release scope and rules.

### Verification

- Six Luna reports were returned as research proposals; no agent edited files, committed, or selected the final projects.
- The reports identified official-source families including Berlin Senate and district pages, procurement platforms, TED, budget and parliamentary records, operator pages, Geoportal/Open Data and planning records.
- The adversarial review identified famous-project, source-availability, survivorship, authority and selection-leakage biases.
- Candidate examples were treated as preliminary discovery leads, not verified project dossiers.

### Failures and limitations

- Agent-reported dates, budgets and URLs still require direct source verification.
- The candidate pool is not yet frozen and no pilot project has been selected.
- The methodology draft was approved by the project owner and pushed as `af0e412`; the research plan itself remains uncommitted.

### Next step

Freeze the scoring rubric and source-discovery record before conducting deeper finalist research.

## 2026-08-05 — Project-level multi-agent source discovery

**Status:** Proposed for review

**Commit:** Pending review

### Goal

Define how the system researches a project after it is proposed by the system, selected from the candidate pool, or added by the project owner or a future user.

### Decision proposed

Each project intake should trigger five or six lightweight, read-only research lanes with distinct source responsibilities:

1. Official project identity, authority and current project pages.
2. Procurement, tender, award and contract-lot records from Berlin and TED.
3. Budgets, investment plans, parliamentary records and oversight documents.
4. Planning, approvals, environmental records and geospatial sources.
5. Operator, district, construction-update and disruption sources.
6. Independent corroboration, contradiction and missing-source discovery.

Each lane returns structured source candidates, extracted claims, exact evidence spans, dates, source metadata, confidence and unresolved gaps. Agents do not publish, edit the golden truth set, or select the final project. A stronger review model handles ambiguity and cross-source synthesis after the lanes finish; lightweight models handle bounded discovery, extraction and deduplication.

### Project-intake inputs

- Candidate name and aliases.
- Address, district, coordinates or affected route.
- Organizations and known roles.
- Category and lifecycle hypothesis.
- User-submitted text, sign details or external identifiers where available.
- Discovery timestamp and origin: system candidate, owner-selected or user-submitted.

### Verification

- All lane outputs are proposals until checked against the original source.
- The system preserves failed searches, dead links, inaccessible documents, contradictions and duplicate sources.
- Claims are deduplicated by source identity and content hash before synthesis.
- The project owner establishes the golden truth values from the German source material.
- Human review is required before a project or consequential claim becomes public.

### Consequences and open questions

- Source discovery becomes repeatable across selected and user-submitted projects.
- Six lanes reduce blind spots caused by relying on a single agency or source type.
- The workflow increases model calls, so cost per project and diminishing returns must be measured.
- Source lanes may overlap; the schema must preserve provenance while deduplicating claims.
- We still need to define the exact structured output schema, stop conditions, retry policy and whether all six lanes run for every project or whether simple projects can use fewer lanes.

## 2026-08-05 — Pilot-selection and source-ecosystem research artifacts

**Status:** Proposed for project-owner review

**Commit:** `85a210a` — `docs(research): add pilot selection and source ecosystem artifacts`

### Goal

Turn the preliminary multi-agent research outputs into reviewable Phase 0
artifacts for selecting three pilots without treating agent-reported facts as
verified research.

### Participants and scopes

- Project owner Gregory Jones: supplied the scope, retained final selection and
  golden-truth authority, and must review the proposed artifacts.
- Main agent (OpenAI Codex): inspected the repository and existing policy
  documents, checked a limited set of official source entry points, and drafted
  the three research files and this proposed log entry.
- Prior multi-agent research outputs: preliminary leads only; no agent selected
  a winner, edited the golden truth set or verified candidate claims.

### Work performed

- Drafted hard eligibility and final-selection gates for project-owner review,
  intended to freeze the pilot process once accepted.
- Drafted a weighted 0–100 rubric with expected end-date evidence as the largest
  user-facing dimension.
- Separated source availability from public usefulness and recorded controls for
  source-availability, famous-project and public-usefulness bias.
- Mapped official Berlin source families across identity, dates, finance,
  procurement, planning, geospatial data, updates and oversight.
- Created a cross-category candidate ledger without selecting final projects.

### Decisions

- Proposed retaining difficult-to-research candidates rather than excluding
  them automatically.
- Proposed requiring a supported expected end date, or a supported statement
  that no expected end date is published, before final selection.
- Proposed treating official entry-point checks as source-family verification,
  not as verification of candidate-level facts or licensing permissions.

### Verification

- Confirmed the repository was clean on `main` before editing.
- Read `README.md`, `AGENTS.md`, `docs/project-checklist.md`,
  `docs/decision-log.md` and `docs/methodology.md`.
- Confirmed that `docs/research/source-discovery-orchestration.md` is absent;
  its available content is represented only by prior build-log and decision-log
  entries and was not reconstructed as if it were a verified file.
- Opened a limited set of official Berlin entry points for procurement, budget,
  parliamentary, planning, geospatial and Open Data discovery. Candidate-level
  claims remain unverified.

### Failures and limitations

- The prior multi-agent reports were not present as standalone files in the
  repository, so the ledger uses their recorded source families and preliminary
  leads without asserting their reported facts.
- No candidate has a manually verified dossier, final score or selection
  decision.
- Source retention, quotation, database rights, personal-data handling and
  machine-access conditions still require project- and dataset-specific review.

### Project-owner feedback incorporated for review

- Missing expected-end-date evidence remains exactly 0 in the rubric, but an
  undated observation can remain in a separate research backlog instead of
  being discarded.
- Public usefulness is framed around affected-place context and disruption,
  not an artificial exact headcount.
- Road closures and lane restrictions were added as a distinct candidate
  category because they directly affect residents and traffic users.
- Research-agent discoveries are proposed to flow into a human-owned backlog;
  agents still do not select pilots or edit the golden truth set.

### Evidence

- `docs/research/pilot-selection-criteria.md`
- `docs/research/source-ecosystem.md`
- `docs/research/candidate-ledger.md`
- Existing research record in this document and proposed source-specialization
  workflow in `docs/decision-log.md`, ADR-006.
