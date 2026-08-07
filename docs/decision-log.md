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
