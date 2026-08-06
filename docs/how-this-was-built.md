# How This Was Built

This document is the single newest-first timeline of how Berlin, Under Construction is developed. The logging policy, roles and full-entry template live in [`build-log-conventions.md`](build-log-conventions.md).

- **Course correction** — 2026-08-06 — Project owner and Codex: corrected an orphaned build-log hash, made the two-commit hash procedure executable, and recorded the false German-language assumption as the course correction it was. Verified: every backticked build-log hash resolves through `git log`; ADR-008 and the disclosure entry state the actual and counterfactual costs. `16f997c`

## 2026-08-06 — Disclose the German-language constraint and verification boundary

**Course correction**

**Status:** Complete; course correction recorded; native-speaker review pending

**Commit:** `7173758` — `docs(process): disclose German-language constraint and mitigations`

### Goal

State that the project owner does not read German, show what that means for the
evidence chain, and measure the first verification pass over the vocabulary on
which glossary-derived golden values will depend.

### Participants and scopes

- Project owner: confirmed the language constraint, required human rather than
  owner authorship of ground truth, set the authority boundary and requested the
  full-glossary verification run.
- Main agent (OpenAI Codex, `/research` skill and web research): integrated the
  policy, audited all glossary and candidate rows, ran back-translation,
  independently reopened primary sources, wrote the report and made all
  repository changes and commits.
- External reviewer (Claude): identified that the original rule assigned German
  ground-truth work to an owner who does not read German, before construction of
  the golden set began.
- Glossary-authorities subagent (OpenAI Codex, `/research` skill): read-only
  retrieval lane for Duden, DWDS, specialist primary authorities and official
  English publications. It returned a cited proposal and did not edit the tree.

### Multi-agent architecture

- Specialized delegation was used because the research skill requires a
  background primary-source lane while the main agent continued the ledger audit
  and policy work. The lane was limited to retrieval and divergence detection;
  the main agent remained the single writer and authority integrator.
- The subagent identified Duden's multiple senses for `Bauabnahme` and
  `Finanzierung`, the general-language overlap between `Kosten` and `Ausgaben`,
  specialist public-finance sources, three Berlin.de English publication paths,
  and DB/BVG English-site gaps. Its DWDS retrieval was blocked by robots policy.
- Accepted after independent reopening: the lexical ambiguities, specialist
  sources, Berlin.de pairs and the DWDS limitation. Modified: its pre-change
  74-row scope was expanded to the version-1.0 glossary's 88 rows, and English
  absence was reported as “not found in this pass,” not proof of nonexistence.
  Rejected: treating general dictionary synonymy, search-result agreement or an
  official-hosted machine translation as contextual validation.
- Independent check: the main agent reopened the cited Duden, Berlin.de,
  Destatis, Bundestag, Federal Ministry of Finance, DB and BVG sources; then
  recomputed report row, status, span and parallel-pair counts from the file.

### Work performed

- Added glossary version 1.0 and a date-qualifier/modal section that preserves
  bounds, direction, precision, confidence and as-of wording.
- Audited all 29 candidate rows against those qualifiers without editing the
  discovery ledger. No direct contradiction was found between quoted wording
  and a row's recorded milestone/date characterization; the ledger still lacks
  a typed qualifier field.
- Replaced owner authorship with human authorship as the golden-set invariant,
  added per-value provenance and recorded ADR-008.
- Checked 88 glossary rows, representing 87 distinct row labels because
  `geschätzt` appears in two sections. Results: 77 `agreed`, 6 `flagged` and 5
  `unresolved`. “Agreed” means only that consulted authorities did not diverge.
- Inspected 29 candidate rows. Twenty-eight contained a quoted German
  expected-end span group and were back-translated; C-026 had no quoted German
  expected-end span. Four of the 28 showed a material modal divergence.
- Found three project-specific German/English Berlin.de publication pairs
  (C-001, C-014 and C-019). No pair was found for the other 26 candidate rows;
  DB and BVG English sites existed but did not expose counterparts for the
  checked C-003, C-004 and C-005 publications.
- Added the verified-vocabulary premise to the README without claiming that the
  constraint has been overcome.

### Decisions

- The native-speaker queue is `Baubeginn`, `Bauabnahme`, `Kosten`,
  `Finanzierung`, `vorgesehen` and `soll`. No flagged glossary row was edited.
- Five terms remain `unresolved` because this pass retrieved no adequate
  authority for the complete term: `Ergänzungsunterlage zur Finanzierung`,
  `haushalterische Grundlage`, `finanziert aus dem Plätzeprogramm`,
  `Realisierungsverträge` and `Einbringungsverträge`.
- Back-translation and official-hosted English text are divergence detectors,
  not authorities. Three Berlin.de English pages were credited to automated
  translation and were not promoted to controlled glossary sources.
- Multiple model passes remain ineligible as golden-set validation regardless of
  agreement.

### Course correction

The original rule required the project owner to build the golden truth set by
hand from German source documents. It encoded the unexamined assumption that the
project owner could read German, which was never true. The assumption survived
21 commits and was caught in reviewer critique before any golden values were
constructed. The actual cost was documentation rework: the rule, role table,
ADR, README premise, verification report and build record had to be aligned.

Had the contradiction surfaced after golden-set construction, the
counterfactual cost would have been rebuilding affected values and invalidating
evaluation results derived from them. That did not happen; there was no golden
set or evaluation to rebuild. The controlled glossary and provenance design
bound the remaining risk but do not solve the owner's lack of German
comprehension.

### Verification

- Confirmed the glossary report has exactly 88 term rows: 77 `agreed`, 6
  `flagged` and 5 `unresolved`.
- Confirmed the back-translation appendix has 29 candidate rows, 28 completed
  span-group passes and one explicit source gap.
- Confirmed the parallel-text appendix has three German/English pairs and labels
  the remaining 26 as not found in this pass.
- Confirmed native-speaker review cells are empty and `docs/glossary.md` was not
  modified by the verification-report commit.
- Confirmed all five requested commits are focused and ordered:
  `309363d`, `32888b6`, `1a5ce5b`, `ba3de76`, then this disclosure commit.

### Failures and limitations

- The project owner cannot independently verify contextual German meaning.
  Project identity, boundary, applicable sense and disagreements between
  authorities remain outside the owner's comprehension.
- No native speaker has reviewed the glossary. Version 1.0 is therefore not
  eligible as a verified layer for `glossary-derived` golden values.
- DWDS pages could not be retrieved because of robots restrictions. Duden is a
  general-language dictionary and does not establish every domain-specific
  financial, planning or procurement sense.
- Back-translation used a model and is correlated with the system being bounded;
  agreement is not evidence of correctness.
- Official parallel English was sparse—3 pairs found, 26 absent in this pass—and
  the found English pages were official-hosted automated translations rather
  than controlled terminology.
- The ledger discrepancy—28 stored German span groups across 29 rows—must be
  resolved before claiming complete candidate-span coverage.

### Evidence

- `309363d` — glossary version and qualifier section
- `32888b6` — golden-set rule, provenance tags, ADR-008 and policy log
- `1a5ce5b` — 88-row glossary verification report and measured appendices
- `ba3de76` — public verified-vocabulary premise
- `docs/research/glossary-verification.md`
- `docs/project-checklist.md`, current handoff

## 2026-08-06 — Scope golden-set authorship and value provenance

**Status:** Complete

**Commit:** `32888b6` — `docs(process): scope golden-set authorship and add value provenance tags`

### Goal

Resolve the contradiction between owner-owned ground truth and the requirement
that a human understand the German source, while preserving the prohibition on
model-generated evaluation authority.

### Participants and scopes

- Project owner: disclosed the language constraint, chose human authorship rather
  than owner authorship as the invariant, and specified the permitted and
  prohibited operations.
- Main agent (OpenAI Codex): integrated the rule, role definition, ADR and public
  accountability record.
- Subagents: none contributed to this policy decision.

### Work performed

- Replaced owner authorship with human authorship as the binding golden-set rule.
- Added per-value provenance tags and prohibited `model-assisted` golden values.
- Defined the versioned, human-verified controlled glossary as the reusable layer.
- Separated agent operation of an authority from being the authority.
- Recorded the rejected multi-pass-AI option and the residual need for German
  comprehension in ADR-008.

### Decisions

- Accepted a human-verified glossary layer because recurring controlled terms can
  be versioned and audited without pretending that model agreement is validation.
- Rejected multiple AI passes as an independence mechanism because correlated
  systems reduce variance but do not remove shared bias.
- Retained German-speaking human review for contextual sense, project boundary,
  identity, disagreement and out-of-vocabulary decisions.

### Verification

- Cross-checked the role table, rule 1 and ADR-008 for the same authority boundary.
- Confirmed that the permitted operations are retrieval, divergence detection and
  verbatim matching, not contextual judgment.
- Confirmed that no golden value or candidate-ledger row was changed.

### Failures and limitations

- The glossary is not yet human-verified, so no value is currently eligible as
  `glossary-derived` ground truth.
- Provenance tags are policy only until the golden-set schema is implemented.
- The project owner still cannot independently resolve German contextual disputes.

### Evidence

- `AGENTS.md`, rule 1 and the roles table
- `docs/decision-log.md`, ADR-008
- `docs/glossary.md`, version 1.0

- 2026-08-06 — Codex: flipped the build log to newest-first and extracted its conventions. Verified: entry order follows Git commit order, the entry count is preserved, and moved prose is unchanged. `a00a129`
- 2026-08-06 — Codex: separated the candidate data ledger, frozen record specification and category coverage map. Verified: moved sections retain their prose and cross-references resolve. `356238f`
- 2026-08-06 — Codex: assigned stable candidate IDs C-001–C-029 to the discovery longlist, shortlist and provenance tables. Verified: 29 IDs, no gaps or duplicates, and ledger/trail names match. `e572bcf`
- **Course correction** -- 2026-08-06 — Claude review recomputed the final end-date gate column from the candidate ledger and caught a lane gate count that did not reconcile against its own source ledger. Corrected housing/mixed-use from 1 to 0 and total from 17 to 16; no repository rework, but the error was live in two commits. `a0baace`
- 2026-08-06 — Codex (skills CLI): ignored vendored third-party agent skills and retained `skills-lock.json` as the reproducibility record. Verified: a disposable fresh-clone simulation restored all 35 skill directories from the lockfile and matched the local `.agents/skills/` tree byte-for-byte. `681e9fc`

## 2026-08-06 — Named pilot-candidate discovery and end-date filter

**Status:** Complete; awaiting project-owner confirmation and selection

**Commit:** `3e70ad7` — `docs(research): name and filter pilot candidates`

### Goal

Replace the candidate ledger's category placeholders with named, geographically
bounded Berlin project leads, preserve the full discovery trail, and apply only
the cheapest hard finalist question: whether an official project-level expected
end date exists and what the exact German wording and milestone type are.

### Participants and scopes

- Project owner: froze the four discovery lanes, prohibited agent scoring and
  finalist selection, required full query/access trails and retains confirmation
  of project identity, German end wording and final-three selection.
- Main agent (Codex, web research and integration): froze the record, ran the
  utilities/environment lane, reopened all core identity links, deduplicated,
  applied eligibility/end-date gates, wrote the longlist, shortlist, glossary
  seeds and accountability record.
- Transport subagent (GPT-5.6-terra, high; Chrome fallback): roads, bridges,
  rail and transport infrastructure.
- Public subagent (GPT-5.6-terra, high): schools, public buildings, cultural
  facilities and public space.
- Development subagent (GPT-5.6-terra, high): housing, commercial redevelopment,
  demolition and mixed-use.
- Three initial GPT-5.6-sol/high subagent invocations were interrupted at the
  project owner's request before their output was accepted.

### Multi-agent architecture

- Delegation was used because the four category lanes were independent and the
  project owner explicitly requested multiple scouts with a research trail per
  lane. Each completed subagent was read-only and returned a proposal; only the
  main agent wrote the repository.
- Transport returned six leads and correctly rejected a bridge-closure date as
  project completion. Public returned eight leads and separated whole-project,
  phase-only and planning-stage milestones. Development returned eight leads
  and exposed that most official dates were phase-only, relative, stale or not
  typed as completion. The main agent returned seven utility/environment leads
  and separated duration wording from calendar end dates.
- Accepted: all 29 named identity leads, their source/access trails, explicit
  gaps and German terminology. Modified: confidence and eligibility were
  normalized against the frozen fields; linked subprojects were kept separate.
  Rejected: closure-only dates, programme-level dates presented as project ends,
  non-official developer dates, completed comparators, unbounded candidates for
  final eligibility and any inferred calendar date from a duration.
- Independent check: the main agent reopened all 29 core identity links. The DB
  Wollankstraße PDF that timed out in the lane opened during integration, but
  its date still described a closure rather than project completion.

### Work performed

- Froze the discovery record and the `found` / `not found` / `not checked`
  expected-end vocabulary before lane results were integrated.
- Named and bounded 29 candidates across four lanes with plausible official
  identity sources, explicit read-versus-inferred fields and one next check.
- Preserved every query, opened URL outcome, dead end, skipped source family,
  access barrier and cross-lane link in a dedicated research-trail document.
- Applied identity, construction-substance, geographic-boundary and end-date
  gates without assigning scores.
- Produced a four-project owner-review shortlist and retained every failed gate
  in the longlist with its reason.
- Added discovery seed rows for every consequential German milestone and
  financial term encountered. The glossary remains unconfirmed and is not
  marked complete.

### Lane performance

`Survived discovery gates` means identity, construction substance, an official
evidence path and a usable geographic boundary. `Survived final end-date gate`
also requires current project-level end wording; phase-only, programme-level,
closure-only and untyped period endpoints do not pass cleanly.

| Lane | Leads returned / requested | Core links open and identify project | Cited page did not support claim / project nonexistent | Survived discovery gates | Duplicates across lanes | Findable end-date evidence | Survived final end-date gate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Transport | 6 / 5–8 | 6 / 6 | 0 | 6 | 0 | 5 | 5 |
| Public buildings / culture / space | 8 / 5–8 | 8 / 8 | 0 | 6 | 0 | 8 | 6 |
| Utilities / energy / water / environment | 7 / 5–8 | 7 / 7 | 0 | 7 | 0 | 6 | 5 |
| Housing / commercial / mixed-use | 8 / 5–8 | 8 / 8 | 0 | 7 | 0 | 4 | 0 |
| **Total** | **29 / 20–32** | **29 / 29** | **0** | **26** | **0** | **23** | **16** |

Eight access-barrier paths were retained as source-registry seeds: a moved
Senate directory, CAPTCHA, an initial DB PDF timeout, an internal-error school
PDF, a timed-out legacy school page, a BWB PDF redirect to 404, a BEW PDF fetch
error and an internal-error Senate press page.

### What was surprising

The housing/mixed-use lane had abundant official identity and planning material
but almost no clean whole-project completion evidence. By contrast, operator
and transport pages often named `Inbetriebnahme`, `Bauende` or
`Gesamtfertigstellung` directly. The end-date-first filter therefore changed the
portfolio shape before any scoring: no development candidate entered the four,
even though several remain strong public-interest backlog items.

### Course correction

The first three delegated lanes were launched on GPT-5.6-sol/high. The project
owner stopped that choice because of credit use and asked that sol not be used
moving forward. Those invocations were interrupted, their partial work was not
accepted, and the same lanes were rerun on GPT-5.6-terra/high. Exact tokens and
cost are unavailable because the agent runtime exposes neither; no estimate was
invented. The correction cost was the aborted model usage and restart latency,
not repository rework. Browser fallback was then permitted for access failures.

### Decisions

- Shortlisted U3 to Mexikoplatz, Heinrich-Hertz-Gymnasium at Ostbahnhof, the
  HKW Mitte Power-to-Heat plant and Europaplatz Süd for owner review; no score
  was assigned.
- Kept a year-only public-space milestone as the spare despite weaker precision,
  because it is still official and project-level and adds a distinct public
  consequence.
- Did not force category balance by admitting a development lead that failed
  the frozen end-date or phase-boundary gate.
- Kept all non-shortlisted candidates and failed paths visible.

### Verification

- Reopened all 29 core identity links and confirmed that each names the claimed
  project; zero core citations failed the identity claim.
- Checked aliases and linked phases for overlaps; no returned rows were merged.
  Adjacent or linked projects are explicitly separated in the research trail.
- Confirmed no natural person is named in the candidate records or shortlist.
- Confirmed no closure notice is a candidate and no closure duration is stored
  as a project end date.
- Confirmed no score or golden-truth value was written.

### Failures and limitations

- Exact token and cost telemetry was unavailable for every lane. This remains
  an instrumentation gap before the first extraction run.
- A core identity page opening does not make every field current or
  authoritative. The project owner still needs to confirm the four identities,
  boundaries and exact German end wording before scoring.
- Source licensing, quote/retention rights, financial measures, organization
  roles, date history and dossier claims were intentionally not researched.

### Evidence

- `docs/research/candidate-ledger.md`
- `docs/research/candidate-record-spec.md`
- `docs/research/candidate-discovery-trail.md`
- `docs/glossary.md`
- `docs/project-checklist.md`
- **Course correction** — 2026-08-06 — Project owner and Codex: added skill/tool attribution and course-correction conventions, marked the ADR-006 stage mismatch, and gitignored private working notes. Verified: `notes/learning.md` is ignored and absent from Git status; diff check passes. `4d4e215`
- 2026-08-05 — Project owner: raised the bar for full build-log entries; documentation and planning work now gets a short entry. Recorded as ADR-007. `39be832`
- 2026-08-06 — Project owner and Codex: made spawned-agent orchestration mandatory in the build record, including failed, redundant and rejected lanes; preserved single-writer synthesis and verification. `39be832`

## 2026-08-06 — Rescope ADR-006 from candidate discovery to selected-project research

**Status:** Complete

**Commit:** `39be832` — `docs(process): raise build-log bar and rescope agent research`

### Goal

Correct the stage that the six-lane research workflow applies to. ADR-006 was drafted and recorded as covering candidate research and project intake generally, but the immediate task — turning category rows in the candidate ledger into named, addressed projects — needs a single identity lookup, not six lanes with claim extraction and cross-source synthesis.

### Participants and scopes

- Project owner: identified that the recorded ADR did not match what was intended by "six agents", and that approval was given to a build that was not the one needed.
- External reviewer (Claude): reviewed the three research artifacts and ADR-006,
  initially recommended deferring the ADR to Phase 5, then drafted the rescope
  separating lightweight candidate naming from six-lane selected-project
  dossier research after the project owner clarified the immediate need.
- Main agent (OpenAI Codex): reviewed the proposed rescope against the original
  ADR, corrected the remaining scope inconsistency and integrated the process
  documentation.
- Subagents: none used for this task.

### Multi-agent architecture

- This was sequential collaboration between the project owner, Claude as an
  external reviewer and Codex as the integrating main agent; no parallel
  subagents were spawned.
- Claude supplied an uncommitted working-tree draft of the rescope and amendment
  rationale. Codex inspected the full diff against the candidate ledger, prior
  orchestration record and repository policy, then corrected the stale context
  wording and dates before any commit.
- The project owner directed the scope correction and retains final acceptance
  of the integrated wording.

### Work performed

- Retitled ADR-006 from "per project intake" to "to research selected projects".
- Changed status from `Proposed for review` to `Accepted, rescoped`.
- Narrowed the scope statement to projects whose identity is already established, explicitly excluding candidate discovery and naming.
- Changed "Decision proposed" to "Decision" and reworded the opening line to apply after selection.
- Added an `Amended 6 August 2026` note recording what moved and why.

### Decisions

- Rejected the reviewer's initial recommendation to defer ADR-006 to Phase 5.
  The workflow belongs in Phase 1 dossier research once pilots are named, not
  in the preceding candidate-naming pass.
- Kept the six lanes themselves unchanged. Only the stage they apply to moved.
- Candidate naming will use a separate lightweight single-pass lookup rather than the full lane workflow.
- Retained the existing rule that agent output is a lead until the project owner verifies it against the original German source.

### Course correction

An agent produced a well-designed six-lane research system aimed at candidate
discovery and project intake generally. The project owner caught that the
workflow was aimed at the wrong pipeline stage: candidate naming needs a
lightweight identity lookup, while the six specialized lanes belong after a
project has been named and selected for dossier research. The mismatch was
caught before implementation. Its cost was one decision-log section and the
review time needed to rescope it; no pipeline code had to be discarded.

### Verification

- Re-read ADR-006 end to end after editing to confirm the title, status, scope, decision wording and amendment note agree with each other.
- Confirmed the lanes, consequences and reconsideration conditions were not altered.
- Confirmed the public record describes only project architecture,
  accountability and verification rationale.

### Failures and limitations

- The original ADR was recorded at a scope the project owner had not intended, and approved before that mismatch was noticed. Cost was one decision-log section, caught before any implementation work followed from it.
- The lightweight candidate-naming pass is not yet specified or run; the candidate ledger still contains category rows rather than named projects.
- Claude edited the shared working tree directly, which crossed the repository's
  reviewer/single-writer convention. No concurrent edit or commit occurred;
  Codex reviewed and integrated the complete diff. Future reviewer changes
  should be proposed for the main agent to apply.

### Evidence

- `docs/decision-log.md`, ADR-006
- 2026-08-05 — Claude: backfilled build-log entries for `e029383` and `f5fb60b` (both previously un-logged or left `Commit: Pending`), added `**Amended**` notes to ADR-003 and ADR-004, and added a "log at commit time, not after" rule to `AGENTS.md`. Verified: reviewed and approved by the project owner. `03e9deb`

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
- 2026-08-05 — Claude: drafted `docs/methodology.md` (evidence labels, financial-measure and milestone definitions, publication thresholds, status rules, correction process), cross-referencing the existing ADRs rather than duplicating them. Verified: reviewed against README, decision log and feature register for consistency; approved by the project owner. `af0e412`

## 2026-08-05 — Research plan: source availability as a product differentiator

**Status:** In progress

**Commit:** `1accf13` — `docs(research): define source discovery orchestration`

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
## 2026-08-05 — Pilot-selection and source-ecosystem research artifacts

**Status:** Proposed for project-owner review

**Commit:** `bdafec9` — `docs(research): add pilot selection and source ecosystem artifacts`

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
- `docs/research/candidate-record-spec.md`
- Existing research record in this document and proposed source-specialization
  workflow in `docs/decision-log.md`, ADR-006.
## 2026-08-05 — Project-level multi-agent source discovery

**Status:** Superseded

**Commit:** `1accf13` — `docs(research): define source discovery orchestration`

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

**Superseded 6 August 2026** — the lane design remains accepted for named,
selected-project dossier research, but no longer applies to candidate naming.
See “Rescope ADR-006 from candidate discovery to selected-project research.”
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
- 2026-08-05 — Codex: extracted the complete feature register, moved the blueprint binary to `~/Documents/berlin-blueprint-private`, removed recruitment framing and replaced the public history. Verified: one commit, no DOCX in history and no recruitment-framing hits. `6a84726`

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
