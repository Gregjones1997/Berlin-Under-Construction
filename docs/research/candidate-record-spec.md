# Candidate ledger

**Status:** Frozen candidate-record specification; three pilots selected and no scores assigned
**Phase:** Phase 0 — research and foundation
**Last updated:** 2026-08-06

The rows below are discovery leads assembled from prior multi-agent research
and broad source-family review. They are not verified project dossiers. Names,
boundaries, dates, budgets, procurement facts and URLs require direct checking
against the original German sources. A blank or “unknown” value is intentional.

This document specifies the candidate record kept in `candidate-ledger.md`; the frozen date on the field table is unchanged by this move.

## Frozen discovery record

**Frozen:** 2026-08-06, before the named-candidate scouting lanes ran.

Every named lead uses the following fields. This is a discovery record, not a
project dossier and not a scorecard.

| Field | Required discovery value |
| --- | --- |
| ID | Flat opaque identifier assigned once in document order; never reused or renumbered, and survives renaming and re-bounding. If a candidate splits into two projects, the original ID stays with one and the other receives the next unused number; record the split. |
| Canonical name and aliases | Official project name as found; every other name retained as an alias. Do not silently merge phases. |
| Address / route / boundary | Exact address, route endpoints or a plainly stated bounded area when read from a source; otherwise the contextual location is labelled inferred and queued for confirmation. |
| District | Source-stated district, or an explicitly labelled geographic inference. |
| Category | One of the four scouting lanes; cross-lane leads are flagged rather than silently moved. |
| Public consequence | Short resident-facing consequence supported by the described works; no unsupported scale or causation claim. |
| Official identity-source lead | At least one plausible authority, public owner/operator, district, planning or official project page and its URL. |
| Expected-end-date evidence | Exactly one of `found`, `not found`, or `not checked`. `Found` also retains the exact German wording, source URL and milestone type. `Not found` means the named official source was actually searched and no project-level expected end date was located. `Not checked` means no end-date search has yet been performed. |
| Likely budget / procurement trail | Source-family lead only at discovery stage. No amount, financial-measure type, contract or organization role is asserted unless the original source states it. |
| Research difficulty | `low`, `medium`, or `high`, with the access, identity, phase or source-fragmentation reason. |
| Verification status | `lead`, `identity source opened`, `identity and boundary provisionally matched`, `blocked`, or `ineligible`. This is not publication verification. |
| Next check | One concrete check that would resolve the most important remaining uncertainty. |

For every field, the research trail states whether the value was read directly
from the cited source or inferred from context. `Unknown` means the question was
asked or the source was checked but the value was not established; `not checked`
means the question has not yet been investigated. Neither is a blank to fill by
guessing.

## How to read this ledger

- **Source availability** describes the research trail, not the project's
  importance.
- **Expected end-date evidence** is a required finalist check and a major
  selection criterion; “unknown” is not an implied date.
- **Budget/procurement signal** is a lead only. It must not be converted into a
  financial claim or an “over budget” conclusion.
- **Keep difficult candidates:** fragmented, scanned, moved or sparse sources
  remain in the pool until a human verification pass establishes that they are
  outside scope or cannot be bounded lawfully.

## Research backlog workflow

The ledger is also the intake point for works noticed in the city before their
official story is easy to find. A resident observation, road-closure notice,
construction sign, demolition site or agent discovery can create a backlog item
without creating a verified project claim.

1. Record the observation, date, location, visible work and discovery source.
2. Assign a status: `lead`, `searching`, `blocked`, `verified`, or `closed`.
3. Search the relevant official source families and preserve failed paths.
4. Record the exact open question, especially whether an expected end date is
   published and which milestone it represents.
5. Move the item into scored-candidate status only after its identity and
   project boundary are sufficiently clear.

An item with no expected-end-date evidence remains valuable as a public-interest
lead, but scores **0** on that rubric dimension and cannot be a final pilot
until the date question is resolved or an official “not published/not yet
determined” statement is verified. This distinguishes tracking what residents
need to know from selecting material that can demonstrate the first release's
evidence-backed end-date experience.
