# Build-log conventions

This document defines the logging policy, roles and full-entry template used by `how-this-was-built.md`.

## Logging policy

Logging is tiered so that this record survives a four-week sprint. A log that stops halfway through the project is worse than no log at all.

### Short entries — documentation, planning and routine work

Most work gets one line. Use this for documentation, planning, restructuring,
policy wording, scaffolding, wiring, styling, refactors, test additions and
anything mechanical:

```markdown
- 2026-08-12 — Codex: dossier page scaffold. Verified: renders pilot 1 from DB. `abc1234`
```

Format: date, participant, what changed, how it was verified, commit hash. Several small commits toward one outcome may share a line.

### Commit-hash recording procedure

Every logged change uses a two-commit sequence. This is the procedure, not an
exception to the requirement to log work at commit time:

1. Write the build-log entry as part of the work, with the commit hash omitted,
   and commit the work.
2. Immediately create a hash-recording commit in the same session that adds the
   work commit's reachable hash to the entry.
3. If the work commit is amended after its entry is written, re-check and update
   the recorded hash. Amending a commit changes its hash.
4. Verify every recorded hash against `git log`. Never use `git cat-file` for
   this check: an orphaned pre-amend object can still resolve under `cat-file`
   even though a clone cannot reach it from history.

The entry itself is never deferred to the follow-up commit, and no hash remains
omitted past the session that created the work. The hash-recording commit exists
only to complete the entry for the immediately preceding work commit.

### Multi-agent entries — mandatory when agents are spawned

Every task that delegates work to one or more agents is recorded, including
when none of the delegated output is accepted. The entry identifies:

- why parallel or specialized delegation was used;
- each agent's bounded lane or responsibility;
- the useful output, failure or duplication returned by each lane;
- what the main agent accepted, modified or rejected and why; and
- how the synthesized result was checked independently.

This is an architectural record of task decomposition, synthesis and
verification. It does not include raw prompts, private reasoning or
unnecessary internal context. The main agent remains the single repository
writer and owns the final result.

### Full entries — code, measurement or costly failure

Use the full template below only when the work references code, a measurement,
or a failure that cost real time. Documentation, planning, restructuring and
policy-wording changes use a short entry even when they change project policy.
Borderline cases default to short. See `docs/decision-log.md`, ADR-007.

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

Copy this section only for work that meets the full-entry bar above. All other
work uses the one-line short entry described above.

```markdown
## YYYY-MM-DD — Short task title

**Status:** Planned | In progress | Complete | Superseded

**Commit:** `<hash>` — `<message>`

### Goal

What outcome was needed and why?

### Participants and scopes

- Project owner: decision or review responsibility.
- Main agent (`provider/model or tool`): implementation and integration scope.
- Subagent (`provider/model or tool`): bounded delegated scope, if any.
- External reviewer (`provider/model or person`): review scope, if any.

### Multi-agent architecture

- Why delegation was used and how the task was partitioned.
- Agent or lane outputs, including failed or redundant work.
- Integration decision and independent verification.

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

In the work commit, omit the `**Commit:**` line from a new full entry. The
immediate hash-recording commit inserts the completed line shown in the template.
