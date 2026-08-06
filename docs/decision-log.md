# Decision Log

This log records decisions that shape the product, architecture, data policy and evaluation approach. Each decision includes its scope, consequences and conditions for reconsideration.

## ADR-001 — Extract in German and translate only for display

**Date:** 5 August 2026  
**Status:** Accepted  
**Scope:** Document ingestion, data model and user-facing language

### Context

The product must preserve distinctions that translation systems can flatten. For example, `Kostenschätzung`, `Haushaltsansatz`, `Auftragswert` and `Ist-Ausgaben` are different financial concepts. `Baubeginn`, `Inbetriebnahme` and `Verkehrsfreigabe` are different milestones.

### Decision

Documents will be extracted in their original language, with the original German wording retained as canonical evidence. Translation will happen only at the display layer. A controlled glossary will provide fixed English mappings for consequential procurement, budget and milestone terms.

### Consequences

- Source evidence remains auditable in the original language.
- Financial and milestone definitions can be validated before translation.
- The glossary becomes a maintained product artifact.
- The interface needs clear handling for untranslated or ambiguous terms.

### Reconsider when

The project adds another source language or evidence shows that a different representation preserves the source distinctions more reliably.

## ADR-002 — Name organizations by documented role; exclude natural persons from v0

**Date:** 5 August 2026  
**Status:** Accepted for v0  
**Scope:** Public display, project dossiers and correction workflows

### Context

Organizations are relevant to understanding a project, but true facts placed next to delay or cost information can create an unsupported implication of causation. Naming individuals adds significant privacy and legal risk without being necessary to explain the construction record.

### Decision

The v0 product may name organizations only in documented roles such as commissioner, financer or contractor for a named lot. It will not name natural persons. Delay and cost variance attach to the project unless a reliable source explicitly establishes causation. Published projects and named organizations will have a correction path.

### Consequences

- Project pages remain focused on documented institutional responsibility.
- The product avoids unnecessary personal-data processing.
- Role labels and source context must be visible wherever an organization is named.
- Legal and privacy review remains required before public launch.

### Reconsider when

The project has a documented public-interest reason, authoritative policy and legal review supporting a broader naming scope.

## ADR-003 — Use risk-specific quality gates instead of one accuracy score

**Date:** 5 August 2026  
**Status:** Accepted as proposed v0 gates  
**Scope:** Document intelligence, evaluation and publication policy

### Context

Different errors have different consequences. A missed field is visible as missing information; a wrong financial-measure type or unsupported citation can mislead users and damage trust.

### Decision

Evaluation will separate precision-critical measures from recall-oriented coverage measures. Proposed v0 gates are:

- Financial-measure type precision: target at least 99% on the defined pilot set.
- Organization-to-role precision: target at least 99% on the defined pilot set.
- Citation correctness: target at least 99% on the defined pilot set.
- Unsupported published claims: 0%, enforced by requiring an evidence span. This one is not a target — it is a deterministic invariant with no tolerance.
- Field extraction recall: measured separately, with an initial expected range of 80–90%.
- Entity-match and contradiction recall: measured separately rather than hidden inside a blended score.

These are release hypotheses, not achieved results, and the pilot set is small enough (three projects) that 99% precision means close to zero tolerated misses rather than a statistically meaningful rate. The publication gate is what a claim below threshold does — it routes to human review instead of publishing — not whether the measured number clears 99% on a given day. The first release publishes its actual measured numbers, including below-target ones, rather than withholding launch until the target is hit. The human-review rate will be reported rather than optimized away. Thresholds remain provisional until the manually verified pilot set exists.

### Consequences

- Evaluation reports explain which kinds of errors are safe, unsafe or unresolved.
- The publication gate can be implemented deterministically.
- The initial system may require substantial human review.
- Results cannot be summarized honestly with one headline accuracy number.

### Reconsider when

The pilot dataset reveals that the metrics do not predict real publication risk or that a new claim type requires a separate gate.

**Amended 5 August 2026** — reworded the precision figures as targets rather than fixed thresholds, called out the unsupported-claims rule as the one zero-tolerance invariant, and stated explicitly that the first release publishes its real measured numbers rather than withholding launch until targets are hit. The decision itself did not change. See `docs/how-this-was-built.md`, "Clarify evaluation-gate and 3D-sequencing wording."

## ADR-004 — Ship the public 2D product before advanced 3D

**Date:** 5 August 2026  
**Status:** Accepted for the first release sequence  
**Scope:** Product sequencing and geospatial delivery

### Context

The technical-illustration 3D experience is distinctive, but hidden-line rendering, geometry processing, coordinate conversion, tiling and device-quality tiers can become a project of its own. The core public value is the evidence-backed project story.

### Decision

The first public release will use an accessible 2D map connected to project dossiers, expected end dates, history and evidence. Advanced 3D will follow as a separate milestone after the data core and public flow are working.

### Consequences

- The first release can demonstrate the core information path sooner.
- The 2D experience remains the accessibility and performance baseline.
- 3D decisions can be tested with measured prototypes instead of assumptions.
- The product must preserve a clear visual direction for the later 3D milestone.

### Reconsider when

User research shows that the 3D representation is essential to understanding the first release, or the 2D prototype fails to communicate the core project story — but not before the first public release ships on its planned date. The first release date is fixed; if either signal appears beforehand, the response is to note it for the 3D milestone that follows, not to pull 3D work forward into the first release.

**Amended 5 August 2026** — added the floor on the reconsideration clause: trigger conditions may be noted before the first release, but do not pull 3D work forward into it. The decision itself did not change. See `docs/how-this-was-built.md`, "Clarify evaluation-gate and 3D-sequencing wording."

## ADR-005 — Use a small, typed stack with local pipeline execution for v0

**Date:** 5 August 2026  
**Status:** Accepted through the first public release  
**Scope:** Application, data, map, pipeline and evaluation infrastructure

### Context

The project needs a coherent stack that supports a public web experience, geospatial data, typed document processing and reproducible evaluation without adding unnecessary operations work before the first release.

### Decision

- **Web:** Next.js and TypeScript, deployed on Vercel, in `/web`.
- **Database:** Supabase Postgres with PostGIS. No authentication or user accounts in v0.
- **Map:** MapLibre GL JS. Berlin geodata is treated as EPSG:25833 and reprojected for web display.
- **Pipeline:** Python in `/pipeline`, with typed extraction schemas and strict validation.
- **Evaluation:** pytest against a JSON golden set committed to the repository. No evaluation framework is required for v0.
- **Execution:** Pipeline jobs are idempotent, content-addressed and deployable in shape, but run locally until the first public release.

### Consequences

- Web, database, map and pipeline boundaries are clear before implementation begins.
- Local execution reduces deployment and operations surface during the first release.
- The stack remains portable enough to replace providers behind adapters later.
- Environment variables and deployment configuration must be documented when they first appear.

### Reconsider when

Measured prototype results show a blocking performance, licensing, cost or reliability problem, or after the first public release when operational requirements change.

## ADR-006 — Use source-specialized lightweight agents to research selected projects

**Date:** 5 August 2026

**Status:** Accepted, rescoped

**Scope:** Researching a project whose identity is already established — the three selected pilots in Phase 1, and later user-submitted or system-discovered projects after naming. Not candidate discovery or naming.

### Context

Project information is distributed across official project pages, procurement systems, budgets, parliamentary records, planning documents, operator updates, geospatial services and independent corroboration. A single general search agent is likely to miss entire source families once a named project enters dossier research. This applies to the selected pilots and, later, to user-submitted or system-discovered projects after their identities and boundaries are established.

### Decision

Once a project has been named and selected, researching it will use five or six lightweight, read-only research lanes with distinct responsibilities:

1. Official project identity, authority and current project pages.
2. Procurement, tender, award and contract-lot records.
3. Budgets, investment plans, parliamentary records and oversight.
4. Planning, approvals, environmental records and geospatial sources.
5. Operator, district, construction-update and disruption sources.
6. Independent corroboration, contradiction and missing-source discovery.

The lanes return structured source candidates, claims, exact evidence spans, dates, metadata, confidence and unresolved gaps. A stronger review model performs cross-source synthesis and ambiguity review. No lane may publish, edit the golden truth set or make the final project-selection decision.

### Consequences

- The system searches the full public source ecosystem instead of repeatedly querying one general index.
- User-submitted projects can enter the same evidence workflow as system-discovered projects.
- Source gaps and failed searches become visible research outputs.
- Six calls per project may be wasteful for simple projects, so cost, coverage and diminishing returns must be measured.
- Claims need content-hash and source-identity deduplication before synthesis.

### Reconsider when

Evaluation shows that fewer lanes provide equivalent source coverage, a source family requires a specialized connector rather than an agent, or cost and latency make the default workflow unsustainable.

**Amended 6 August 2026** — the six lanes were originally proposed for candidate discovery and project intake generally. That is the wrong stage. Naming a candidate needs one identity-lookup pass; six lanes with claim extraction and cross-source synthesis is machinery aimed at a question that has not been asked yet. Rescoped to apply once a project is already named and selected, which is where parallel source-family research genuinely accelerates the project owner's manual dossier verification. Candidate naming uses a separate, much lighter single-pass lookup described in `docs/research/candidate-ledger.md`. The lanes themselves are unchanged; only the stage they apply to has moved. See `docs/how-this-was-built.md` for the review that prompted this.

## ADR-007 — Reserve full build-log entries for work with code, measurement or real cost

**Date:** 5 August 2026

**Status:** Accepted

**Scope:** Build logging in `docs/how-this-was-built.md`

### Context

The tiered logging policy separated short entries from full entries but defined "consequential" broadly enough that planning and documentation work qualified. Four consecutive full entries were written about documentation changes, totalling roughly 180 lines, on a repository with no implementation yet. The build log became mostly a record of writing documents rather than of building a system, which inverts its purpose: a reader learns that the project is governed carefully, but not whether it can be built.

### Decision

A full entry now requires that the work references code, a measurement, or a failure that cost real time. Everything else — documentation, planning, restructuring, policy wording, scope corrections — gets a one-line short entry.

Existing full entries are retained as written. They are not retroactively compressed; rewriting an accountability record to look tidier is a worse outcome than an uneven one.

This decision was made deliberately before implementation began, so that the log's shape matches the work that follows rather than being trimmed later when the volume became inconvenient.

### Consequences

- The build log's centre of gravity shifts to extraction runs, evaluation results, cost measurements and failures.
- Planning and documentation work remains recorded, but proportionately.
- The distinction is judgement-based, so borderline cases default to a short entry.
- The existing documentation-heavy entries stay visible, including this one's own rationale.

### Reconsider when

A category of non-code work turns out to carry enough consequence that a one-line entry loses information a reader needs — for example a legal, licensing or privacy determination that changes what the product may publish.
