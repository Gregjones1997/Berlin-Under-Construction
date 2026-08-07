# Berlin, Under Construction

> An independent, source-backed map that helps people understand what is being built across Berlin, who is responsible, what was promised, what changed, and what the public can reliably know.

**Project status:** Phase 2 — trustworthy data core; pilot dossier review in progress

**Geographic focus:** Berlin, Germany

**Project type:** Civic technology, geospatial product, applied AI

## Overview

Berlin, Under Construction is a planned AI-assisted and source-backed civic information product focused on visible construction and major works across Berlin.

Construction information often exists, but it is fragmented across planning pages, procurement notices, budgets, committee records, company reports, press releases, geospatial datasets and physical site signage. The same project may appear under different names, identifiers and definitions in each source.

The product vision is to connect those records into understandable project dossiers while preserving the evidence and history behind every important claim.

This repository will document the product, data model, engineering decisions, experiments, evaluation results and implementation as the project develops.

The living build checklist is maintained in [`docs/project-checklist.md`](docs/project-checklist.md). The use of AI agents, manual decisions, failures and verification is recorded in [`docs/how-this-was-built.md`](docs/how-this-was-built.md).

## Verified-vocabulary premise

This project deliberately tests whether a verifiable extraction system can be
built over a source language the author does not read. It uses a human-verified,
versioned controlled vocabulary, deterministic evidence-span verification and
per-value provenance to make that constraint inspectable rather than implicit.

The premise forces a strict boundary between operating an authority and being
the authority: agents may retrieve human-authored references, match spans and
detect divergence, but they cannot validate their own interpretations. It also
does not solve every language-dependent decision. Project boundary, identity,
contextual sense and conflicts between authorities still require German
comprehension the project owner does not have.

## Current status

This project is not yet a finished application. Three pilot dossiers are
evidence-complete and frozen while German-speaking review prepares the
human-authored golden set. Current implementation work is the Phase 2 typed data
core and review tooling.

The first public release will focus on a narrow, working vertical slice:

- Three representative Berlin construction projects, expanding toward ten after the first release.
- A source registry and manually verified project dossiers.
- Clear definitions for project status, milestones, financial measures and evidence.
- A versioned data model for projects, claims, sources, organizations and changes.
- A bounded document-intelligence workflow with evaluation results.
- A deployable 2D map connected to evidence-backed project pages.

The technical-illustration 3D experience remains an important differentiator, but it follows the first working 2D release so that geospatial rendering does not delay evidence of the core data and AI work.

Features described in the roadmap are planned work unless they are explicitly marked as complete in the project documentation.

## Product thesis

People should be able to notice construction in the physical city, locate the site digitally and understand its current story in less than one minute.

The product should answer questions such as:

- What is being built or repaired?
- Where is it and what area does it affect?
- Who owns, commissions, finances or operates the work?
- What is the expected end date, when did the work start, and has that date changed?
- How have the dates, scope or financial figures changed?
- Which contractors, contracts or lots are involved?
- What is directly supported by public evidence?
- Where are the records incomplete, stale or contradictory?

## Principles

### Evidence before certainty

Important dates, amounts, responsibilities and status claims should be traceable to supporting source material. The product should communicate uncertainty instead of filling gaps with confident-sounding assumptions.

### History should remain visible

New information should update the current view without deleting previously supported estimates, milestones or claims. Changes should remain inspectable.

### Definitions matter

An original estimate, approved budget, awarded contract value, expenditure and final cost are different measures. Likewise, construction start, handover, commissioning and public opening are different milestones. The data model should preserve these distinctions.

German-language source terms should be extracted and stored before translation. A controlled German-English glossary will map consequential budget, procurement and milestone terms for display without replacing the original wording.

### AI should be bounded and evaluated

AI is intended to assist with document classification, structured extraction, entity resolution, change detection and grounded explanation. It should not publish consequential conclusions without validation and appropriate review.

### Independent and transparent

The project is unofficial and independent. It must not imply endorsement by the State of Berlin, a public authority, a contractor or another organization. Methodology, limitations, corrections and model performance should be documented publicly.

### Accessible by default

The 3D experience is an important visual direction, but the core information must remain available through a performant 2D map, readable project pages, responsive layouts and keyboard-accessible interfaces.

## Planned product experience

The intended primary flow is:

```text
Map or address search
        ↓
Project overview
        ↓
Timeline, money and contracts
        ↓
Evidence and source passages
        ↓
What changed and what remains uncertain
```

The longer-term experience may include:

- A technical-illustration style 3D Berlin map.
- Search by address, location or nearby area.
- Filters by status, category, district, duration, organization, contractor, budget and confidence.
- Versioned project timelines and budget histories.
- Source archives with highlighted supporting passages.
- Planned versus current geometry for selected projects.
- Resident reports for missing construction and visible changes.
- Correction requests and public review states.
- Project and area follows with change alerts.
- Citywide analytics and reusable data exports.

These are part of the preserved product vision, not claims about the current state of the application.

## Decided v0 technical direction

The first-release stack is fixed in ADR-005. Prototypes may refine interfaces
inside these boundaries, but do not reopen the stack before 1 September 2026:

- **Web application:** Next.js and TypeScript in `/web`, deployed on Vercel.
- **Data layer:** Supabase Postgres with PostGIS.
- **Source archive:** Source metadata, retrieval dates and content hashes, with private artifact retention only where appropriate and lawful.
- **Document intelligence:** A Python pipeline in `/pipeline`, shaped as
  deployable idempotent jobs but invoked locally until v0 ships.
- **Review workflows:** Human review for uncertain claims, contradictions, corrections and resident submissions.
- **Geospatial layer:** MapLibre GL JS for the public 2D map, with Berlin
  EPSG:25833 data reprojected for web display. Experimental 3D follows v0.
- **Evaluation:** pytest against a committed, human-authored JSON golden set,
  with citation, routing, cost and latency checks.

## Data and trust model

The central data unit is a versioned claim rather than an unqualified field.

A claim is expected to retain:

- Normalized value and claim type.
- Original wording and source language.
- Supporting source artifact and evidence passage.
- Publication, effective and retrieval dates.
- Extraction model, prompt and schema versions where applicable.
- Confidence and validation results.
- Reviewer decision and rationale.
- Relationships to claims that confirm, contradict or supersede it.

Planned evidence labels include:

| Label | Meaning |
| --- | --- |
| Verified | Directly supported by a relevant authoritative primary source. |
| Corroborated | Supported by multiple reliable sources. |
| Reported | Attributed to a reputable secondary source. |
| Inferred | A clearly labelled system interpretation or estimate. |
| Observed | A dated observation of visible conditions. |
| Unverified lead | A report awaiting evidence or entity matching. |
| Disputed | A claim challenged with relevant counterevidence. |

## Release roadmap

The first delivery goal is a small public product that demonstrates the complete evidence path. Coverage and advanced presentation will expand after that path works reliably.

### Phase 0 — Repository and documentation foundation

- Establish repository structure, development conventions and contribution workflow.
- Create the decision log, methodology, initial data model and transparent build log.
- Define how features, tests, documentation and commits will be tracked.

### Phase 1 — Research foundation

- Select three representative pilot projects for the first release.
- Build the source registry.
- Define construction taxonomy, statuses, milestones and financial measures.
- Create a controlled German-English domain glossary.
- Research the pilot dossiers manually.
- Create the first golden truth set and contradiction log.
- Define evidence labels and publication thresholds.

**Exit evidence:** versioned definitions, a source matrix and three manually verified project records.

### Phase 2 — Trustworthy data core

- Implement project, organization, source and claim schemas.
- Add source artifact storage and provenance links.
- Preserve superseded and contradictory claims.
- Add deterministic validation and a human review queue.
- Build the first evaluation harness.

**Exit evidence:** a source-backed project dossier can be reconstructed from stored claims and evidence.

### Phase 3 — AI document intelligence

- Add document classification.
- Add typed extraction with evidence spans.
- Add entity resolution.
- Add change and contradiction detection.
- Add grounded explanations and citation checks.
- Measure accuracy, unsupported claims, review rate, cost and latency.

**Exit evidence:** the pipeline can process representative documents and show both successful outputs and known failures.

### Phase 4 — Public 2D vertical slice

- Connect the map to project dossiers.
- Display expected end dates prominently.
- Add timeline and financial history.
- Display sources, confidence and freshness.
- Add a “what changed?” view.
- Add basic address search and sharing.
- Deploy a small public release.

**Exit evidence:** a person can identify a site, understand its current story and inspect the evidence behind it.

### Phase 5 — Coverage and operational hardening

- Expand the pilot set from three projects toward ten.
- Add more source connectors and project categories.
- Improve evaluation coverage and reduce review burden safely.
- Add correction links for named organizations and published claims.
- Add source-health and review operations.

### Phase 6 — Technical-illustration 3D release

- Prototype a small Berlin geometry area.
- Record source, license, coordinate-system and accuracy decisions.
- Test hidden-line and technical-illustration rendering.
- Add one flagship project model.
- Preserve the performant and accessible 2D experience.

### Phase 7 — Community and monitoring

- Add missing-site reports and correction requests.
- Add moderation workflows.
- Add follows, alerts and citywide analytics.

### Phase 8 — Civic platform

- Expand flagship 3D models and planned/current comparisons.
- Add public APIs, exports and embeddable project cards.
- Add research workspaces and organization responses.
- Isolate city-specific connectors for potential multi-city support.

## Evaluation plan

A polished demo is not sufficient for this project. The AI system should be evaluated against a manually verified dataset containing representative failure cases, including:

- Long budget and investment documents.
- Tables split across pages.
- Scanned or low-quality German documents.
- Procurement awards and contract modifications.
- Documents containing multiple unrelated projects.
- Similar project names in the same district.
- Ambiguous gross/net and project/lot amounts.
- Conflicting completion estimates.
- Bilingual, source-grounded questions.

Proposed v0 targets are deliberately separated by risk. They are release hypotheses to refine against the pilot dataset, not achieved results:

- Financial-measure type precision: target at least 99%.
- Organization-to-role linkage precision: target at least 99%.
- Citation correctness: target at least 99%.
- Field extraction recall: expected initial range of 80–90%.
- Entity-match recall: expected initial target around 85%.
- Contradiction recall: expected initial target around 80%.
- Unsupported published claims: 0%, enforced by requiring an evidence span.
- Human-review rate: expected to begin around 30–50% and fall only as measured reliability improves.
- Correction rate.
- Cost per processed document.
- Freshness latency from source publication to verified update.

No consequential extraction workflow should be considered production-ready without representative regression tests and a documented failure analysis.

## Development workflow

Development will proceed feature by feature.

Each feature should have:

1. A small issue with a clear acceptance criterion.
2. A focused implementation branch.
3. Tests appropriate to the risk of the change.
4. Updated documentation and decision records where relevant.
5. A screenshot, example output or other evidence of behavior.
6. A clean, focused commit.
7. A completed checklist item in the roadmap or feature register.
8. A concise build-log entry describing agent use, human decisions, failures and verification.

Commit messages should describe one coherent change, for example:

```text
docs(data): define versioned claim schema
feat(map): add addressable pilot project markers
test(ai): add citation completeness regression cases
fix(review): preserve superseded claim history
```

Avoid mixing unrelated refactors, product features and documentation changes in one commit unless they are required for the same change.

AI assistance is expected and will be disclosed. The main agent records which agents or models were used, what each was asked to contribute, which suggestions were accepted or rejected, what was completed manually, and how the result was verified. The log summarizes decisions and evidence; it does not store private reasoning, secrets or raw prompt transcripts.

## Documentation structure

Documentation will be created when it has real decisions or evidence to record. The initial set is intentionally small:

- `data-model.md` — entities, claims, provenance and temporal rules.
- `methodology.md` — evidence hierarchy, definitions and limitations.
- `decision-log.md` — important choices, alternatives and rationale.
- `feature-register.md` — the preserved full product vision with stable feature IDs.
- `how-this-was-built.md` — human work, agent contributions, failures and verification.
- `build-log-conventions.md` — build-log policy, roles and full-entry template.
- `project-checklist.md` — current position and the next concrete action.

Evaluation reports, architecture documentation and correction policy will be added as their corresponding systems and decisions become concrete.

## What this project demonstrates

The project is intended to deliver more than an attractive map. Its engineering priorities include:

- Applied AI on messy real-world documents.
- Structured outputs and deterministic validation.
- Entity resolution and temporal data modeling.
- Retrieval grounded in source evidence.
- Human-in-the-loop review and correction workflows.
- Geospatial and 3D product development.
- Evaluation discipline beyond a successful demo.
- Clear communication of uncertainty, risks and tradeoffs.
- Production-minded documentation and commit history.

The eventual public release may include a live product, public repository, architecture diagrams, evaluation report, technical case study, methodology page and a short product demonstration.

## Scope and limitations

This project is independent and unofficial. It should not imply that a public authority, contractor, developer or other organization endorses the product.

Public information may be incomplete, inconsistent, delayed or legally restricted. Resident reports may establish observations or leads, but they do not automatically establish responsibility, financing, cause or official project status.

The initial public product will name organizations only in documented roles such as commissioner, financer or contractor. It will not name natural persons. Delay and cost variance will attach to the project, not be visually attributed to an organization unless a reliable source explicitly establishes causation. Published claims and named organizations should have a clear correction path.

Reconstructed or illustrative 3D geometry must be clearly labelled and must not be presented as authoritative design geometry.

## License and data policy

Licensing, source archiving, database rights, document retention and reuse policies will be reviewed before public release. The default public experience will link to original documents and display only the evidence spans needed to support commentary. Full source files will not be publicly rehosted unless review confirms that redistribution is permitted.

German legal and privacy requirements, including public-site identification, analytics disclosures and source quotation, must be verified against current authoritative guidance before launch.

## Initial next step

The first implementation task is to bootstrap the repository and create the minimal documentation foundation. The first product task is to select three pilot projects, define the German-first terminology model and build their manually verified source matrix before automating extraction.
