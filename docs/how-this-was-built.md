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
- 2026-08-05 — Claude: drafted `docs/methodology.md` (evidence labels, financial-measure and milestone definitions, publication thresholds, status rules, correction process), cross-referencing the existing ADRs rather than duplicating them. Verified: reviewed against README, decision log and feature register for consistency; project owner approved. `<pending>`

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

**Commit:** Pending

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
