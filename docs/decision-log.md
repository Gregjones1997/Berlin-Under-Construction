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

Organizations, bodies and collective groups may be named and referred to.
Natural persons may not, including through a role descriptor that identifies one
individual at a point in time. A singular office plus a date is a name. Attribute
statements to the document, not to the person or office that signed it.

### Consequences

- Project pages remain focused on documented institutional responsibility.
- The product avoids unnecessary personal-data processing.
- Role labels and source context must be visible wherever an organization is named.
- Legal and privacy review remains required before public launch.

### Reconsider when

The project has a documented public-interest reason, authoritative policy and legal review supporting a broader naming scope.

**Amended 2026-08-07** — added the role-descriptor test for singular offices and
the document-attribution rule. See `docs/how-this-was-built.md`,
the 2026-08-07 phase-label and ADR reconciliation entry.

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

The organization-to-role precision target is explicitly **deferred**, not
omitted: the role-vocabulary ADR is still pending, the three pilot dossiers
assign no organization roles, and therefore the current set contains no valid
role-labelled denominator. The gate activates only after that ADR is accepted
and the human-authored golden set contains eligible organization-role values.
Until then, reports must show it as `deferred — no eligible labelled data`, not
as passed, failed or absent from a five-of-six summary.

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

**Amended 19 August 2026** — ADR-022 replaces only the web framework choice
with a no-island Astro static build. The remaining v0 stack decisions stay in
force. See the Gate 3 checkpoint entry in `docs/how-this-was-built.md`.

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

**Amended 6 August 2026** — the six lanes were originally proposed for candidate discovery and project intake generally. That is the wrong stage. Naming a candidate needs one identity-lookup pass; six lanes with claim extraction and cross-source synthesis is machinery aimed at a question that has not been asked yet. Rescoped to apply once a project is already named and selected, which is where parallel source-family research genuinely accelerates the project owner's manual dossier verification. Candidate naming uses a separate, much lighter single-pass lookup described in `docs/research/candidate-record-spec.md`. The lanes themselves are unchanged; only the stage they apply to has moved. See `docs/how-this-was-built.md` for the review that prompted this.

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

## ADR-008 — Use a human-verified glossary layer for German golden values

**Date:** 6 August 2026

**Status:** Accepted

**Scope:** Golden-set authorship, controlled vocabulary and evaluation provenance

### Context

The original non-negotiable rule assigned the golden truth set to the project
owner and required its values to come from a human reading the German source
documents. It therefore assumed that the project owner could read German. That
assumption was never true: the project owner does not read German. The
contradiction survived 21 commits without examination and was caught in reviewer
critique before golden-set construction began.

The correction cost documentation rework only. Had it surfaced after golden-set
construction, the counterfactual cost would have been rebuilding any values that
depended on the false authority assignment and invalidating evaluation results
derived from them. No golden set or evaluation existed, so that rebuild did not
occur.

The purpose of the rule remains unchanged: model-generated ground truth cannot
validly evaluate model extraction because agreement can measure shared bias
rather than correctness.

Three operating options were considered:

1. A German-speaking human authors or verifies every contextual value directly.
2. Multiple AI passes translate, classify and cross-check each other.
3. A human-verified controlled glossary supplies bounded, versioned mappings,
   while contextual disagreements and values outside that layer return to a
   German-speaking human.

### Decision

Use the controlled glossary as the verified layer. Every golden value receives
one provenance tag: `span-verified`, `glossary-derived`, `owner-judgment` or
`model-assisted`; `model-assisted` is prohibited in the golden set. A
`glossary-derived` value is eligible only when the glossary version and human
verification status are recorded and published with the evaluation result.

Agents may operate external, human-authored authorities but may not replace
them. They may retrieve dictionary entries and official parallel text, run
back-translation to detect divergence, and match spans verbatim. They may not
choose a contextual dictionary sense, assign a golden milestone type, resolve
authority disagreement or treat cross-model agreement as validation. Detected
divergence creates a human-review question.

The glossary layer was chosen because it makes a reusable, inspectable boundary
around recurring terms without pretending the owner's language constraint has
been removed. A German-speaking human remains necessary for contextual judgment,
glossary verification and unresolved or out-of-vocabulary values.

### Consequences

- Golden-set authority is human-authored but not necessarily owner-authored.
- Evaluation results must identify the glossary version and verification status.
- Provenance is attached per value rather than inferred from the dataset.
- Multiple agreeing model passes remain model assistance, not validation.
- Project boundary, identity and contextual sense decisions still require German
  comprehension outside the owner's capabilities.

### Reconsider when

A German-speaking human can directly author and maintain all golden values at
the required pace, or evidence shows that the glossary layer cannot keep
contextual ambiguity out of the evaluation set.

**Amended 6 August 2026** — recorded the false owner-language assumption, its
21-commit lifetime, how reviewer critique caught it and the actual versus
counterfactual cost. See `docs/how-this-was-built.md`, “Disclose the
German-language constraint and verification boundary.”

## ADR-009 — Precision and conflict are two markers, not one

**Date:** 6 August 2026

**Status:** Accepted 2026-08-06 by the project owner.

**Scope:** Public rendering of qualified and conflicting dates and amounts

**Origin.** The project owner required that a value carrying a bound, a range or
an approximation display an affordance revealing where the figure comes from,
rather than rendering as a bare number: *"we should just throw an icon above
that price in the UI. So that way, somebody could hover over it and see where
the sources are coming from."* The reviewer refined this into two mechanically
distinct markers after the pilot evidence showed that approximation and
disagreement are different states which a single marker would conflate. The
requirement and the decision to surface uncertainty in the UI are the owner's;
the split into two markers and the computation rules are the reviewer's.

**Context.** The 2026-08-06 evidence pass produced one clean example of each
state:

- `50Hertz finanziert den Bau der PtH-Anlage mit bis zu 75 Millionen Euro.`
  One source, deliberately precise, expressing an upper bound. Nothing is in
  conflict.
- The C-014 project page states `1.900.000 €` while a Senate news item of the
  same programme states `rund 1,7 Mio. Euro` for the programme's contribution.
  Two official publications, both precise, disagreeing.

A single "uncertain" icon renders these identically and destroys the
distinction between *the publisher hedged* and *the government contradicts
itself*. The second is closer to the reason this product exists.

**Decision.**

Two markers, both computed deterministically from stored fields. No model
participates at render time.

**Precision marker** — fires when a value's qualifier field is non-empty. The
qualifier set is closed and comes from the glossary:

| Class | Qualifiers | Renders as |
| --- | --- | --- |
| Upper bound | `bis`, `bis zu`, `spätestens` | `≤` |
| Lower bound | `frühestens`, `ab` | `≥` |
| Approximation | `rund`, `etwa`, `ca.`, `geschätzt` | `~` |
| Range | two endpoints | `–` |
| Modal / intent | `geplant`, `vorgesehen`, `soll`, `voraussichtlich`, `anvisiert` | typographic weight, not a glyph |
| Source-stated unreliability | `nicht belastbar` | distinct warning glyph |

**Conflict marker** — fires when two or more claims share a
`(project, measure_type, scope)` key with different values. Three sub-states:

- **Superseded** — same authority, different publication dates. Show current,
  offer history.
- **Unreconciled** — different sources, no supersession established. Show both
  values side by side. **Neither value is promoted.**
- **Scope-divergent** — values differ *and* scope strings differ. Render as
  "these describe different things", never as a plain numeric conflict.

**Consequences.**

- The glyph is part of the value string, not adjacent decoration. Render
  `≤ €75M`, not `€75M` with a hoverable dot, so the qualifier survives being
  copied out of the page.
- Modal force occupies a separate channel from numeric bound, because they
  compose: `bis Ende 2028 geplant` is a bound *and* an intention.
- Hover reveals the verbatim German span, publication date, source, and the
  glossary row that maps the qualifier. That last element is what keeps the
  display `glossary-derived` rather than model output.
- **The unreconciled state never promotes a value.** This will come under
  pressure — the instinct will be to show the more recent or the more official
  figure. Resisting that is the decision.
- Both markers are unit-testable, which keeps them inside rule 4 rather than
  being a model behaviour we hope for.

---

## ADR-010 — Source tier for a state-owned company acting as Bauherr

**Date:** 6 August 2026

**Status:** Accepted 2026-08-06 by the project owner, who delegated the exact
formulation to the reviewer.

**Scope:** Source hierarchy for state-owned delivery bodies

**Context.** C-010 is delivered under the Berliner Schulbauoffensive
Erbbaurecht-and-Mietvertrag model. The district holds the site, HOWOGE holds
the leasehold and delivers the building, and ZECH Hochbau AG builds it as
`Generalübernehmer`. Two findings depend on whether HOWOGE's own project pages
can carry dates:

- `Die Endfertigstellung ist für 2026 vorgesehen.`
- `Bauzeit` / `2024 bis 2026`

The frozen source-tier table admits `Operator acting as Bauherr for its own
project (BEW, BVG, BWB, DB)` as primary, and restricts `Contractor or developer`
to their own participation and lot scope only, never project dates, budget or
status. HOWOGE is on neither list and behaves like both.

The owner's ruling was *"if they are the builder or contractor they can be
trusted just label it"*, then delegated the wording. Applied literally this
would have let contractor-tier sources carry project dates, removing the rule
that prevents a subcontractor's lot completion from being read as the project's
completion — a rule that is load-bearing for C-001, C-004 and C-005. The owner's
premise also mis-identified the builder: HOWOGE is the Bauherr, ZECH is the
contractor.

**Decision.**

> A state-owned company acting as **Bauherr** for a project it delivers is
> primary for that project's dates, scope and status. HOWOGE under the Berliner
> Schulbauoffensive joins BEW, BVG, BWB and DB on that line.
>
> **The test is the documented Bauherr role — not state ownership, and not who
> holds the construction contract.**
>
> ZECH Hochbau AG remains contractor tier: own participation and lot scope
> only, never project dates, budget or status.

**Consequences.**

- The two HOWOGE findings above become primary evidence for C-010.
- The contractor rule survives intact for the transport pilots.
- Where a source labels one organization with two roles, the tier follows the
  documented role and the inconsistency is recorded in the dossier rather than
  silently resolved. HOWOGE's own project page is exactly this case: its fact
  box reads `Bauherr:` / `ZECH Hochbau AG` while its body text calls ZECH
  `der beauftragte Generalübernehmer`.
- This ADR assigns a **source tier**, not an organization role. Role assignment
  remains blocked pending the ADR expanding the role vocabulary.

---

## ADR-011 — Strip PDF metadata before artifact retention

**Date:** 6 August 2026

**Status:** Accepted 2026-08-07 by the project owner, as amended by the reviewer.

**Scope:** Private source-artifact retention and provenance

**Context.** During the 2026-08-06 pass, PDF metadata was both decisive and
hazardous.

Decisive: the Hauptausschuss paper `h19-2449-v.pdf` carries a letterhead date of
`6. Oktober 2026`, which is a typographical error. Its embedded
`/CreationDate` of `D:20251014143825+02'00'` corroborated the correct year
alongside the document's own internal evidence.

Hazardous: the same file's `/Author` field is a named official's email address.
Rule 3 forbids naming a natural person, with no exceptions. Nobody reading the
document text would know the name is there.

**Decision.**

1. Retained artifacts in `data/artifacts/` are written **after** a metadata
   strip that removes at minimum `/Author`, `/Creator`, `/Producer` and any
   XMP creator fields.

2. Timestamps (`/CreationDate`, `/ModDate`) are **extracted and stored as
   structured provenance before the strip**, because they resolve publication
   dates. They are provenance data, not authority statements: a creation
   timestamp corroborates a date, it does not publish one.

3. **The strip is performed by a PDF object-graph rewriter, not by pattern
   replacement over raw bytes.** In the 2026-08-07 verification pass, the
   `/Author` field of `h19-2449-v.pdf` was found inside a compressed object
   stream, invisible to any byte-level scan of the response. A regex strip would
   have reported success and removed nothing. Use a library that parses and
   rewrites the document structure, such as qpdf or pikepdf.

4. **The strip is verified, not assumed.** After stripping, the output is
   re-parsed and retention **fails** if `/Author`, `/Creator`, `/Producer` or an
   XMP creator field is still reachable in the rewritten document. A failed
   verification blocks retention of that artifact; it does not warn and proceed.

5. **This decision covers document metadata only.** Personal data appearing in
   visible body text is handled by the evidence-span validators
   (`personal_data_high_confidence`, `possible_personal_name`). ADR-011 must not
   be read as having removed all personal data from an artifact.

6. The stored content hash is computed over **stripped** content, so that a
   change to the strip rule does not silently invalidate every stored hash.

7. **The strip-rule version is recorded per artifact**, and the strip must be
   idempotent: stripping already-stripped bytes produces identical bytes.

8. This applies before the first bulk retrieval run, not after.

### Hash retention and roles

Both hashes are retained and are not interchangeable.

| | `stored_content_hash` (post-strip) | `pre_transform_response_hash` (pre-strip) |
| --- | --- | --- |
| Artifact and source identity key | **Yes — the only one** | Never |
| Deduplicates sources | **Yes** | Never |
| Displayed in the public source registry | **Yes** | **Never** |
| Target of `ExtractionRun.artifact_hash` | **Yes** | Never |
| Purpose | Content addressing | Chain of custody |

The post-strip hash is the identity key because metadata-only regeneration must
not create a false new source version. The pre-strip hash is never displayed:
the raw bytes are deliberately not retained and therefore cannot be reproduced
by a public reader.

For HTML and other media types with no metadata to strip, the transform is the
identity transform with a recorded rule version. Both hashes exist and are equal.

### Dossier registries

The frozen dossier registries record SHA-256 over raw response bytes: historical
pre-strip verification hashes. Three C-014 values were independently reproduced
on 2026-08-07: `sha256:36d47e13…70f4f5`, `sha256:6f341678…cdeab5` and
`sha256:a554a9df…49fa60`.

After this ADR is implemented, a PDF's `stored_content_hash` will not equal its
dossier registry hash. This is expected. Dossier values must not be updated,
recomputed or reconciled; where both kinds are shown, label them `raw response
(pre-strip)` and `stored content (post-strip)`.

### Consequences

- No retrieval job may write to `data/artifacts/` until the object-aware strip
  and its post-strip verification both exist and are tested.
- Strip verification is a deterministic test target under `AGENTS.md` rule 4.
- The two-hash model must exist before the first bulk run because a pre-strip
  hash cannot be backfilled after raw bytes are discarded.

---

## ADR-012 — Use SQLite for the local pipeline store

**Date:** 7 August 2026

**Status:** Accepted 2026-08-07 by the project owner

**Scope:** Local pipeline persistence before v0 ships

### Context

The pipeline is invoked locally until v0 ships, and the current Phase 2 exit
condition is to reconstruct a dossier from stored claims and evidence. Nothing
required for that reconstruction depends on PostGIS. Standing up Supabase before
the local pipeline can persist one claim would add an operations surface before
the thing it hosts exists.

ADR-005 remains unchanged: Supabase Postgres with PostGIS is the web
application's v0 database. This decision concerns the local Python pipeline
store only.

### Decision

Use SQLite as the local pipeline store for retrieval records, verified artifact
records, extraction runs and milestone claims. The store is private local state,
not a committed dataset and not a public artifact host.

Pydantic domain schemas remain the trust boundary. SQLite is an adapter behind
a small storage interface; database rows do not become a second, looser domain
model. Writes that form one retrieval/extraction unit are transactional, stable
IDs and schema versions are preserved, and corrections append rather than
silently overwriting history.

The dossier-fragment reconstruction test consumes stored records through that
interface. It does not depend on SQLite-specific queries, so the same behavior
can be exercised against a future Postgres adapter.

### Consequences

- Phase 2 can prove persistence and reconstruction without deployment, accounts,
  credentials or a network dependency.
- SQLite database files are local generated state and must be gitignored. Source
  artifacts remain separately private under `data/artifacts/` and continue to
  pass ADR-011 before any retention.
- SQLite provides no PostGIS capability and is not the web application's
  database. Geography remains in the Supabase/PostGIS path established by
  ADR-005.
- The adapter must preserve the two hash roles from ADR-011. Stored-content hash
  is identity and the extraction foreign key; the pre-transform response hash is
  private chain-of-custody data only.

### Migration consequences

- The future Postgres migration exports versioned records through the storage
  interface rather than copying SQLite implementation details or row IDs.
- Stable application IDs, UTC timestamps, schema versions, prompt/model versions,
  exact German evidence spans and both explicitly labelled hash roles must
  survive byte-for-byte or value-for-value as applicable.
- SQLite-specific representations such as JSON text, decimal text and boolean
  integers are decoded back into strict domain models before import. PostgreSQL
  types are chosen from those models, not inferred from SQLite column affinity.
- Content-addressed artifact identity is revalidated during migration. The raw
  response is not reconstructed, and the private pre-transform hash never
  becomes a public key or deduplication field.
- The storage/reconstruction contract tests must run unchanged against the
  Postgres adapter before cutover. Dual writes are not introduced unless a later
  decision establishes an operational need.

### Reconsider when

The map needs shared geographic persistence, the local-only execution decision
changes, or a measured SQLite limitation blocks deterministic reconstruction.

---

## ADR-013 — Phase 2 exits on reconstruction fidelity, not publication readiness

**Date:** 7 August 2026

**Status:** Accepted 2026-08-07 by the project owner

**Scope:** Phase 2 exit criteria and the private reconstruction boundary

### Context

Phase 2 previously required a dossier to be regenerated entirely from versioned
claims and evidence. The publication-safe reconstruction renders only claims
that are eligible, verified and accepted with every blocking validation passed.
Those states require human review of German claim values.

The first storage smoke test correctly reconstructed its unreviewed claim as
withheld. Under the old criterion, that safe result was indistinguishable from a
storage or reconstruction failure. It coupled proof that the pipeline faithfully
round-trips data to a separate human decision about whether the data may publish.

### Decision

Phase 2 exits on **reconstruction fidelity**, not publication readiness.

1. A pilot dossier must reconstruct from stored data alone, faithfully rendering
   every claim's real state, including withheld claims and their reasons.
2. The publication-safe render remains the default and the only mode available
   to public surfaces.
3. A local-only `include_withheld_detail` verification mode may render stored
   detail for withheld claims so the smoke test can distinguish correct
   withholding from incorrect storage. Its output is never published.
4. Rendering publication-eligible claims publicly is a Phase 4 criterion, where
   the public dossier and human-review workflow meet.
5. No publication rule changes: evidence spans, blocking validations and an
   accepted review decision remain mandatory.

### Consequences

- Phase 2 can be demonstrated with engineering evidence without treating human
  review as a prerequisite for proving persistence.
- The local smoke test becomes diagnostic for serialization and lost-span faults.
- The withheld-detail mode is a private surface containing stored German source
  text and must remain unreachable from public rendering paths.
- Phase 4 owns the proof that accepted, verified claims render publicly.

### Reconsider when

Human review becomes routine rather than blocked, so restoring publication-ready
claims to an earlier phase gate no longer couples unrelated work.

---

## ADR-014 — Keep all three pilot projects in v0

**Date:** 13 August 2026

**Status:** Accepted 2026-08-13 by the project owner

**Scope:** First-release project coverage

### Context

The 1 September deadline created a real scope question. The reviewer recommended
a single-project v0 centered on C-014 because it offered the safest schedule.
That alternative would have reduced the amount of source, schema and display work
required before release, but it would also have removed the cross-project cases
that expose different evidence and terminology problems.

### Decision

The v0 release keeps all three selected pilots: C-014, C-010 and C-019. The
project owner declined the reviewer-recommended single-project alternative.
Schedule pressure is handled by shrinking features around the three dossiers,
not by removing two pilots.

### Consequences

- The first release must support all three pilot dossiers.
- Optional product surface may be reduced to protect the deadline and trust
  rules.
- A working C-014 vertical slice remains the implementation path, but it is not
  the complete release scope.

### Reconsider when

A documented blocker makes three-project publication impossible without
weakening evidence quality, privacy or another non-negotiable rule.

**Amended 13 August 2026** — corrected the decision and acceptance date from
12 August to the owner-confirmed 13 August. See `docs/how-this-was-built.md`,
the 2026-08-13 acceptance-date and attribution correction entry.

---

## ADR-015 — Ship v0 with an explicitly unverified glossary

**Date:** 13 August 2026

**Status:** Accepted 2026-08-13 by the project owner

**Scope:** v0 translation, evaluation and disclosure boundary

### Context

ADR-008 defines the human-verification boundary required for golden values, but
German-speaking glossary verification will not complete on the v0 critical
path. Treating an agent-produced or otherwise unverified glossary as authority
would violate the golden-set rule; waiting for a golden set would put the first
release behind that unavailable authority.

C-010 is the live example of the risk: its five German completion terms are
contested and cannot be collapsed into one asserted English milestone type.

### Decision

v0 may ship with a versioned glossary whose status is explicitly `unverified`.
This changes sequencing, not the authority rule in ADR-008. The human-authored
golden truth set and glossary verification move off the v0 critical path to
post-v0.

Until verification exists, all of the following are binding:

1. No extraction accuracy figure is published.
2. No English milestone type or financial type is asserted where the German is
   contested. The unresolved German distinction remains visible instead.
3. German remains canonical in storage.
4. The glossary version and its verification status are published alongside
   every output derived from the glossary.

### Consequences

- v0 can demonstrate bounded extraction, evidence spans, withholding, cost and
  latency without presenting model self-consistency as accuracy.
- C-010's five completion terms remain unresolved in English until a qualified
  human settles the relevant vocabulary and context.
- Any display derived from the glossary is visibly provisional and traceable to
  its exact version.
- Golden-set evaluation becomes post-v0 work; agents still may not create or
  populate its values.

### Reconsider when

A German-speaking human has verified the relevant glossary version and authored
or verified the eligible golden values under ADR-008.

**Amended 13 August 2026** — corrected the decision and acceptance date from
12 August to the owner-confirmed 13 August. See `docs/how-this-was-built.md`,
the 2026-08-13 acceptance-date and attribution correction entry.

---

## ADR-016 — Use operator sign-off without contribution credit

**Date:** 13 August 2026

**Status:** Accepted 2026-08-13 by the project owner

**Scope:** Git commit trailers

### Context

The Buzz Nest `AGENTS.md` requires both `Signed-off-by` and `Co-authored-by`
trailers for the human operator. This public repository separately discloses AI
authorship in `docs/how-this-was-built.md`. Giving the operator contribution-
graph credit for agent-authored changes would make the commit metadata conflict
with that disclosure.

### Decision

Every agent-created commit carries `Signed-off-by` for the human operator, using
the repository-local Git name and email. It does not carry `Co-authored-by` for
the operator or an AI agent.

This knowingly overrides the Buzz Nest trailer rule for this repository.

### Consequences

- Sign-off records human accountability without misattributing authorship.
- AI participation remains disclosed in the canonical build log.
- A missing repository-local email blocks an agent-created commit rather than
  inviting a guessed identity.

### Reconsider when

The repository's public authorship policy or contribution-credit model changes.

---

## ADR-017 — Work in the existing artifact-bearing checkout

**Date:** 13 August 2026

**Status:** Accepted 2026-08-13 by the project owner

**Scope:** Agent workspace and private pipeline state

### Context

The canonical working tree is `/Users/gregai/Documents/berlin construction`.
The Buzz Nest convention already prefers an existing checkout, while an earlier
session treated an empty `REPOS/` directory as evidence that the repository was
unavailable and briefly created a replacement clone.

That clone could never reproduce the real working environment:
`data/artifacts/` is gitignored and private under rule 5, and the local SQLite
store contains the retained bytes required by `pipeline.extract_once`.

### Decision

Agents work in the existing local checkout and do not clone this repository into
the Buzz Nest `REPOS/` directory.

### Consequences

- Repository work and local extraction use the same canonical tree and private
  state.
- A fresh clone is suitable for public reproducibility checks, but cannot run
  artifact-backed extraction without separately authorized access to the
  private store.
- Private artifacts remain gitignored and must never be copied into Git to make
  another workspace convenient.

### Reconsider when

The project owner relocates the canonical checkout or introduces an authorized
private-store adapter that preserves rule 5.

---

## ADR-018 — Repository instructions take precedence

**Date:** 13 August 2026

**Status:** Accepted 2026-08-13 by the project owner

**Scope:** Agent instruction hierarchy

### Context

Two files named `AGENTS.md` apply during Buzz-coordinated work: the Buzz Nest
workspace file and the repository file. Their general instructions overlap, and
their commit-trailer rules conflict.

### Decision

For work on this project, the repository `AGENTS.md` wins over the Buzz Nest
`AGENTS.md`. An agent must state a conflict out loud when it encounters one
rather than silently choosing or blending the instructions.

### Consequences

- Project-specific trust, privacy, authorship and workflow rules remain
  authoritative in the project they govern.
- The Nest instructions continue to apply where they do not conflict.
- Instruction conflicts become visible decisions rather than hidden agent
  behavior.

### Reconsider when

The two instruction sets are consolidated or their precedence is defined by a
higher project-owned policy.

---

## ADR-019 — Keep one canonical public build record

**Date:** 13 August 2026

**Status:** Accepted 2026-08-13 by the project owner

**Scope:** Development-process documentation

### Context

Buzz provides workspace-level `WORK_LOGS/`, while this repository already has a
public, versioned accountability record with project-specific content and hash
verification rules. Splitting authoritative history between them would make a
reader reconstruct the process from two stores with different lifetimes.

### Decision

`docs/how-this-was-built.md` is the canonical project build record.
`WORK_LOGS/` in the Buzz Nest is scratch and never substitutes for a committed
build-log entry.

### Consequences

- Every lasting process claim is reviewed and versioned with the repository.
- Workspace logs may support a session but are not cited as the project record.
- The build-log commit and hash-recording procedure remains mandatory.

### Reconsider when

The repository adopts another public, versioned record with an explicit
migration of the existing history.

---

## ADR-020 — Treat pricing provenance and run limits as separate concerns

**Date:** 13 August 2026

**Status:** Accepted 2026-08-13 by the project owner

**Scope:** Extraction metering configuration and stored cost provenance

### Context

The metering configuration contains both dated provider rates and operator-set
run limits. Raising `max_output_tokens` from 2,000 to 4,000 changes request
policy without changing any price used to calculate stored costs. The current
filename and `pricing_reference` combine those concerns even though only the
rate block is the dated pricing observation.

### Decision

`pricing_reference` identifies the rate block, not the mutable `run_limits`
block in the same file. Run-limit changes do not restate historical rates and
must be recorded in the decision log and build log until the configuration is
split or run-policy provenance is stored separately.

### Consequences

- Existing and future costs using this reference remain comparable because the
  rates are unchanged.
- `pricing_reference` alone does not reproduce the exact request cap; the build
  record supplies that policy history for v0.
- A later schema may store a separate run-policy version without changing the
  meaning of existing cost rows.

### Reconsider when

The pipeline supports multiple run profiles, run limits affect a published
comparison, or exact request-policy provenance needs to travel with each run.

---

## ADR-021 — Ship the smallest honest product before completing the trust platform

**Date:** 19 August 2026

**Status:** Accepted 2026-08-19 by the project owner after external review

**Scope:** Delivery order through the 21 August portfolio handoff and the
1 September first public release

### Context

The repository has three frozen source-backed dossiers, a strict milestone
pipeline slice and 117 passing local tests, but no public web application, map or
dossier page. The public default branch still presents a concept-stage project,
and its strongest engineering work is both hidden on the Phase 2 branch and red
in CI because of one local-interpreter assumption. Continuing the existing
sequence would deepen the trust platform before demonstrating user value.

### Decision

Pivot delivery order: repair the public repository, create a public-safe static
projection, ship C-014 as the flagship dossier, add thin C-010 and C-019 pages
and a locally sourced MapLibre orientation view, expose only measured AI
behavior, then deploy after the required public-site checks. Phase 2 remains
incomplete, private artifacts never enter the web build, and no provider call is
authorized by this decision.

`docs/portfolio-pivot-plan.md` is the sprint's execution plan. Its active gate
and completion criterion control sequencing. Through the Friday handoff, build
logging uses one short entry per shipped gate or material failure and one closing
hash commit per day. Evidence, German-canonical storage, human authority,
natural-person exclusion, correction links and zero unsupported publication
remain binding.

### Consequences

- A working, honest user experience now outranks broader backend completion.
- Supabase, full domain schemas, address search, scored evaluation, broader
  extraction batches and 3D remain deferred.
- The public UI distinguishes human-curated dossier data from the single
  retained completed extraction run and makes no total provider-call or accuracy
  claim.
- The temporary process exception expires after the 21 August handoff.

### Reconsider when

A binding evidence, privacy, legal or source-use requirement blocks public
deployment. In that case the site remains a restricted preview and is not called
the public release; the trust rule is not weakened to preserve the date.

---

## ADR-022 — Use a no-island Astro static build for the public site

**Date:** 19 August 2026

**Status:** Accepted 2026-08-19 by the project owner

**Scope:** Public web framework and Gate 3 data boundary

### Context

The public projection intentionally omits every withheld value. A hydrated
application can nevertheless reopen the bundle-leak risk by serializing build
props into client payloads even when a component conditionally hides them. The
Gate 3 dossier needs no client-side state at its raw-render checkpoint.

### Decision

Replace the Next.js part of ADR-005 with an Astro and TypeScript static build in
`/web`. Gate 3 uses no client islands, runtime data access, API routes or
external requests. Astro reads `public/data/projects.json` only while building;
its public-copy directory is separate from the repository's `public/data/`
tree. CI builds the real `web/dist/` export and runs the sentinel and regenerated
known-withheld scans over every emitted file. Vercel remains the planned host
for the static output.

If a client island appears necessary during Gate 3, implementation stops for a
new owner decision rather than adding it implicitly.

### Consequences

- The initial dossier export contains HTML and no shipped JavaScript or
  serialized hydration props.
- The committed projection and supporting registry files cannot be copied by
  Astro's default public-directory behavior.
- Stable project routes are generated entirely at build time.
- Any future interaction that requires client JavaScript reopens the privacy
  boundary and must be reviewed explicitly.

### Reconsider when

A required, owner-approved user interaction cannot be delivered as static HTML.
The decision point is whether to add a narrowly bounded island, not whether to
weaken the withheld-value or generated-output scans.

---

## ADR-023 — Ship Friday as an access-restricted preview

**Date:** 20 August 2026

**Status:** Accepted 2026-08-20 by the project owner

**Amended 2026-08-25** — the owner removed password setup and deployment from
this repository lane because the Astro deployment is being handled separately.
No deployment or access-control outcome is inferred from that reassignment, and
no URL may be described as public or verified until the separate live checks are
recorded. See the 2026-08-25 Gate 6 local-package entry in
`docs/how-this-was-built.md`.

**Amended 2026-08-25 (public-launch decision)** — the owner subsequently
reversed the access-restriction decision and directed that the site launch
publicly on Vercel Hobby without password protection. This amendment supersedes
the password requirement and the deployment reassignment above; it does not
waive the legal, privacy, evidence or live-verification gates. The owner supplied
the provider/controller name Gregory Anthony Jones and monitored contact
`jonesg158@gmail.com`. The serviceable postal address must still be supplied and
the build fails closed without it. Official Vercel documents checked on the same
date create a new unresolved issue: the current canonical DPA expressly covers
Pro and Enterprise processor relationships, while the Hobby Terms incorporate a
different older DPA link. The repository and privacy notice must disclose that
conflict; the deployment must not represent current-DPA coverage as established.

**Scope:** Friday deployment, public-launch boundary, map scope and correction
route sequencing

### Context

The Gate 6 legal review established that a public launch needs approved provider
identity and an accurate Article 13 privacy notice. The project owner will not
publish an Impressum during the Friday sprint. Treating the Friday artifact as
public would therefore contradict the recorded legal fallback and create a
late deployment blocker.

The remaining time also cannot safely absorb an interactive map. The locally
bundled BKG boundary already supports a static orientation view without client
JavaScript, external tiles, cookies or API keys. Separately, every dossier
already links to a correction path that does not exist, so correction intake is
a current broken-link and deployment issue rather than final packaging.

### Decision

Invoke the `Public-site review is incomplete` fallback in the portfolio plan.
Friday 21 August ships only as a deployment-level password-protected,
access-restricted preview. It is not the public release, and no README, page or
deployment wording may describe it as public. Public launch moves to before
1 September 2026, after provider identity and the Article 13 privacy notice are
resolved.

Replace the interactive MapLibre sprint deliverable with a static inline SVG
drawn from the bundled BKG boundary. C-014 and C-010 receive source-recorded,
dossier-linked markers. C-019 receives no coordinates and no marker because its
location fact is withheld pending source verification; it remains visibly
listed and linked beside the map with the reason code. The caption states that
two of three pilots are placed. The map has no client JavaScript or runtime
request and carries a visible linked BKG source line including `(Daten
verändert)`. Correct the stored provenance attribution to the same wording.

Move the contextual correction route into Gate 4. It remains static and
JavaScript-free, preserves the originating project or organization context and
distinguishes ordinary evidence corrections from formal rights of reply and
data-protection requests. Application-owned authentication, a form backend and
an interactive correction workflow remain out of scope. During the restricted
preview, invitees use the monitored channel through which they received access;
the page labels this as a provisional preview arrangement. A permanent
monitored address is required before public launch and must not be invented.

### Consequences

- Friday can demonstrate the complete evidence path without implying public
  legal readiness.
- Public launch remains blocked until provider identity and the Article 13
  notice are resolved; password protection does not satisfy that later gate.
- The preview must be tested from a fresh browser for effective access control
  before its URL is shared.
- The static boundary preserves the zero-JavaScript and no-third-party-request
  positions while giving invited reviewers geographic orientation.
- Broken correction links are repaired before preview deployment. The invite
  channel provides monitored preview intake, while a permanent monitored
  address remains a pre-public-launch blocker alongside provider identity and
  the Article 13 notice.

### Reconsider when

Provider identity and the Article 13 notice are approved for public launch, or
an interactive map can be added without weakening the display, privacy,
licensing or no-client-JavaScript constraints.
