# Methodology

This document defines how Berlin, Under Construction decides what to publish, how confident a claim is, and what the product will and will not assert. It is the operational rulebook behind the evidence model described in `README.md`. Where a rule here conflicts with an implementation detail elsewhere, this document governs until it is revised.

This is a policy document. It states what the product commits to doing, not a claim that every mechanism described here is already built. Current implementation status lives in `docs/project-checklist.md`.

## Independence

Berlin, Under Construction is independent and unofficial. It must never imply endorsement by the State of Berlin, a district authority, a public utility, a contractor, a developer, or any other organization that appears in the product. Every public page carries this statement or a visible link to it.

## What this product is not

- Not an official permit system, engineering record, or safety authority.
- Not a substitute for authoritative planning, procurement, or building-safety information.
- Not an accusation of waste, corruption, or misconduct. A schedule or budget change is not evidence of fault.
- Not a claim that a published contract value has been spent, unless an expenditure source specifically supports that.
- Not a claim that a reconstructed 3D model is architecturally or structurally accurate, unless it is built from authoritative design files.

## Evidence labels

Every published claim carries exactly one evidence label. The label is a statement about what kind of support exists, not a statement about likely truth.

| Label | Publication standard |
| --- | --- |
| Verified | Directly supported by an authoritative primary source whose meaning matches the displayed claim. |
| Corroborated | Supported by more than one reliable source, or a primary source plus independent confirmation. |
| Reported | Attributed to a reputable secondary source when primary evidence is unavailable. |
| Inferred | A system interpretation or model estimate, visually distinct and accompanied by method and confidence. |
| Observed | A dated field observation or photograph establishing visible conditions, not cause, cost, or responsibility. |
| Unverified lead | A submission or discovered reference awaiting evidence and entity matching. |
| Disputed | A claim challenged with relevant counterevidence while review remains open. |

A claim with no evidence span cannot carry any label above `Unverified lead`. This is enforced deterministically, not by model judgment — see `AGENTS.md`, rule 4.

## The claim model

A date, amount, contractor, or status is stored as a versioned claim with provenance, never as a bare field that gets overwritten. Each claim retains:

- Claim type and normalized value.
- Original wording and source language (see Language policy, below).
- Source artifact, publisher, and retrieval date.
- Publication and effective dates.
- Extraction model, prompt, and schema version, where a model produced it.
- Confidence and validation results.
- Reviewer decision and rationale.
- Relationships to claims it confirms, contradicts, or supersedes.

Superseding a claim never deletes it. The current view is computed from eligible claims under transparent precedence rules; the history remains inspectable behind it. This is what makes "what changed and when" a first-class feature rather than a changelog nobody can audit.

## The source ladder

The 2026-08-06 Berlin public-project evidence pass found the same project
published at up to five depths. Value increased sharply in the cases tested.

| Depth | Source | What it gives | What it costs |
| --- | --- | --- | --- |
| 1 | Project page | Status label, fact box, current headline date | Fields often undated, sometimes mislabelled |
| 2 | Press release | Narrative, rounded figures, organizations, one date | Rounded; no budget references |
| 3 | Programme index `Aktuelles` block | A **different text** from the press release, often with extra figures | Volatile; entries roll off |
| 4 | Schriftliche Anfrage (PARDOK) | Current status, cost tables, direct answers to "is it on time" | Table headers and rows split across pages |
| 5 | Hauptausschuss-Vorlage | Exact figures, tax basis, budget chapter and title, funding sources, approval dates, lot structure | Long, formal, occasionally typo'd |

A research pass that stops at depth 2 will report rounded figures with no tax
treatment, no budget reference and no approval date, and may record
"financing not published" for projects whose financing is fully published one
or two rungs down.

**Standard sequence:** establish identity and boundary at depths 1–2, then
check relevant parliamentary depths before recording a financial measure or a
`not found` for dates or costs. Where those families do not cover the project,
record that limitation rather than pretending every ladder depth exists.

## Relative date anchors

Sources routinely anchor milestones to named periods rather than dates:
`zum Schuljahresbeginn 2026/27`, `zum Sommeranfang`, `in den Winterferien`,
`zum Fahrplanwechsel`. These resolve against a published authority and must
be retrieved, never assumed. Retrieving the authority is an operation
permitted under `AGENTS.md` rule 1; deciding when the period "usually" falls
is not.

Store the source's anchor wording as the canonical value and the resolved date
as derived, with the resolving authority named. Never replace the anchor with
the date — the anchor is what the source committed to.

## Financial-measure definitions

These are different measures. They are never blended, and a headline number never hides which one it is:

| Measure | Meaning |
| --- | --- |
| Original estimate | The earliest supported cost figure for the project. |
| Approved budget | The amount formally authorized for a defined scope — not necessarily spent. |
| Current forecast | The latest supported cost expectation, which may differ from the approved budget. |
| Awarded contract value | The value of an awarded contract or lot, usually excluding VAT in procurement notices unless stated otherwise. |
| Contract amendment | A documented change to an awarded contract's value, scope, or schedule. |
| Expenditure to date | Money actually disbursed, as distinct from budgeted or contracted. |
| Final cost | The completed, settled cost of the project or a defined phase of it. |

Every figure retains currency, tax treatment, price basis, scope, and source date alongside its value. Aggregation across contracts is permitted only when the contracts are known to be non-overlapping and the resulting label states exactly what was summed.

## Milestone definitions

Planning approval, tender deadline, award, site start, construction start, substantial completion, handover, commissioning, and public opening are separate milestone types. A dossier may offer a simplified headline date, but the underlying milestone type stored behind it stays explicit and is never silently swapped for a different one.

## Status and claim rules

These rules bound what the product is permitted to assert. They apply to every claim, human-reviewed or AI-generated.

- Status is always stated **as of** a specific date and tied to evidence. A status with no date attached does not publish.
- "Delayed" requires comparison against a specific, previously supported milestone — not a resident's or reviewer's impression that a site has taken too long. See the lifecycle states in `docs/feature-register.md`.
- Never infer "over budget" from a contract award alone.
- Never infer that a project is delayed without a supported comparison milestone.
- Never infer contractor responsibility for a delay unless a source explicitly supports it.
- Never overwrite a previously supported figure or date. Supersede it and keep the history.
- Never treat a resident observation as proof of cause, financing, or formal status — see the `Observed` label above.
- Never present reconstructed or illustrative 3D geometry as authoritative design geometry.
- Never let a secondary summary outrank a newer, directly relevant primary source without a documented reason.
- Always display the as-of date, source date, and freshness state alongside any consequential claim.

## Naming and attribution policy

See `docs/decision-log.md`, ADR-002, for full context. In summary:

- Organizations are named only in a documented role — commissioner, financer, or contractor for a specific lot.
- Natural persons are not named in v0. No officials, signatories, or employees, even where a source names them.
- Delay and cost variance attach to the project, never visually to an organization, unless a source explicitly establishes causation.
- Every published project and every named organization carries a visible correction path.

## Language policy

See `docs/decision-log.md`, ADR-001, for full context. Extraction happens in the source language; the original German wording is the canonical evidence. Translation happens only at the display layer, through a controlled glossary of fixed English mappings for consequential procurement, budget, and milestone terms. A term with no glossary entry is shown untranslated rather than guessed at.

## Publication thresholds

See `docs/decision-log.md`, ADR-003, for the full quality-gate rationale. In summary: precision-critical fields (financial-measure type, organization-to-role linkage, citation correctness) target 99% on the pilot set, but the gate that actually governs publication is per-claim routing — a claim below threshold goes to human review instead of publishing, rather than blocking the whole release. The one true invariant, with no tolerance, is that an unsupported claim cannot publish at all.

Measured performance, including numbers below target, is published rather than withheld. A falling human-review rate is reported as evidence of improving reliability, not assumed from day one.

## Correction and dispute process

1. Receive a correction request identifying the affected claim and any counterevidence.
2. Do not automatically hide or freeze the claim, unless safety, privacy, or legal risk requires immediate action.
3. Compare the counterevidence against the existing source hierarchy and effective dates.
4. Record the reviewer, decision, and rationale.
5. Publish the correction or the `Disputed` state, and preserve the previous version rather than deleting it.
6. Notify anyone following the project when a correction materially changes the project's story.

## Source handling and retention

Source artifacts (documents, notices, pages, photographs) are archived privately with a content hash, publisher, retrieval date, and license note. The public product displays short evidence spans and links to the original source; full source documents are not rehosted publicly unless a specific redistribution license permits it. See `AGENTS.md`, rule 5, and the License and data policy section of `README.md`.

## Resident submissions

A resident report or observation creates a lead or an `Observed` claim. It does not become a verified project fact until it is matched to evidence and reviewed. Submissions are moderated for privacy before publication — see the naming policy above, which applies equally to third parties who might appear incidentally in a submitted photograph.

## Revising this document

A change to any rule in this document is a consequential decision under `docs/build-log-conventions.md` and gets a full log entry, not a short one. If a rule here is loosened after launch, the change and its rationale are recorded publicly, not silently absorbed into a future edit.

## Open, unresolved items

These are known gaps, not omissions to paper over:

- German legal review of this methodology (personality rights, database rights, copyright, defamation, data protection) has not yet occurred. See `README.md`, License and data policy.
- The controlled glossary referenced in the Language policy exists as
  discovery seed rows but has not yet completed project-owner and
  native-speaker verification.
- Publication thresholds in ADR-003 are proposed, not validated against real pilot data yet.
