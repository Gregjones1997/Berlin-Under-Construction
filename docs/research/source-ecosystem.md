# Berlin official source ecosystem

**Status:** Research map; not yet a verified source registry
**Phase:** Phase 0 — research and foundation
**Last updated:** 2026-08-06

This is a discovery map for finding primary evidence about Berlin construction
projects. “Verified” below means that the named official entry point was opened
and its stated function was observed on 2026-08-05. It does **not** mean that a
particular project claim, date, amount, link permanence, licence or
completeness has been verified.

## Source-family map

| Research need | Likely official source family and entry point | Authority | Likely fields | Access friction | Licensing / reuse concern | Verification status |
| --- | --- | --- | --- | --- | --- | --- |
| Project identity, scope, commissioner | Senate and district project pages on [Berlin.de](https://www.berlin.de/) and agency/operator pages | State Senate, Bezirke, public bodies; varies by project | Official name, aliases, scope, location, responsible organization, status, contact | Names and pages vary by agency; old pages may move; projects may be nested in press or thematic pages | Link and quote only what is permitted; page terms and image rights need checking | Entry domain verified; project-level completeness unverified |
| Construction updates and disruptions | Senate mobility/construction pages, district pages, BVG, Berliner Verkehrsbetriebe, Berliner Wasserbetriebe, BSR and other operator pages | Competent authority or operator | Works notices, closures, phases, current status, expected reopening/end date, affected area | Updates may be short-lived, duplicated or published as PDFs/news items | Operator branding, photographs and map material may have separate rights | Source families are leads; candidate-specific verification required |
| Tenders, awards and contract lots | [Berlin Vergabeplattform](https://www.berlin.de/vergabeplattform/) and [published notices](https://www.berlin.de/vergabeplattform/veroeffentlichungen/bekanntmachungen/) | Berlin public contracting bodies / Vergabeservice | Notice title, CPV, lot, procedure, deadline, place, estimated or awarded value where published, contractor where lawfully disclosed | Detail documents may redirect to iTWO Tender; registration, pagination and retention can vary | Tender documents and attachments may have terms, personal data or restricted reuse | Entry points verified; individual records and reuse conditions unverified |
| EU procurement and award notices | TED and eForms search, linked from EU procurement records | European Union Publications Office / contracting authority | Notice ID, buyer, procedure, lot, award value, dates, CPV, winner | Search syntax and historical versions; not every local or below-threshold award appears | EU notice reuse and linked attachments need checking; do not assume all attachments are reusable | Likely source family; direct project test still required |
| State budget and investment planning | [Berlin Finance — Haushalt](https://www.berlin.de/sen/finanzen/haushalt/) and the finance/investment planning pages | Senate Department for Finance; House of Representatives adopts budget | Budget line, chapter/title, investment programme, planned years, commitments, actuals where available | Large PDFs, changing budget years, project names may be abbreviated or absent | Official legal texts may be linkable, but PDF/database rights and quotation limits require review | Entry point verified; extraction and licence status unverified |
| District budgets and investment programmes | District finance pages, e.g. district Haushaltsplan and Investitionsprogramm pages | Bezirksamt and BVV | Building/road measure, planned total, annual allocation, phase, district | Every district has a different information architecture; scanned PDFs likely | Per-page terms and document reuse need checking | Family observed through official district search; district-by-district verification pending |
| Parliamentary questions and oversight | [Abgeordnetenhaus Open Data / PARDOK](https://www.parlament-berlin.de/dokumente/open-data) and official Drucksachen | Abgeordnetenhaus Berlin; Senate responses are primary records for the response | Question, answer, project alias, date, cost, schedule, risk, responsibility, committee trail | XML/PDF corpus is large; matching aliases and attachments takes manual work | Metadata/XML availability is not blanket permission to rehost full PDFs | Entry point verified; claim-level and licence review pending |
| Planning, environmental review and approvals | [Berlin Planfeststellungsverfahren](https://www.berlin.de/sen/uvk/mobilitaet-und-verkehr/verkehrsplanung/planfeststellungen/), Bauleitplanung, district planning and official Bekanntmachungen | Competent planning/hearing/approval authority | Application, plan boundary, hearing, approval, conditions, dates, objections, decision | Formal German legal documents; drawings/attachments; project status may lag construction | Plans, maps, personal data and third-party reports need rights/privacy review | Planfeststellung entry point verified; other planning families pending direct checks |
| Geospatial identity and location | [Berlin Geodateninfrastruktur / Geoportal](https://www.berlin.de/sen/stadt/stadtdaten/geoinformation/geodateninfrastruktur/) and [Berlin Open Data](https://daten.berlin.de/datensaetze?geographical_coverage=Berlin) | Senate Department for Urban Development and participating data publishers | Address, coordinates, parcels, roads, buildings, boundaries, WMS/WFS/Atom service metadata | Services may be German-only, CRS-dependent, rate-limited or unavailable for some layers | Dataset-specific licence is decisive; Open Data entries can differ by dataset | Entry points and service types verified; candidate layer and licence unverified |
| Construction/project geometry and basemap context | Geoportal, district GIS, open cadastral/topographic layers and operator maps | Data owner varies | Geometry, CRS, feature ID, update date, accuracy, layer title | EPSG:25833 versus web CRS; geometry may show context, not project extent | Attribution, database rights, derived geometry and display terms must be checked | Family identified; authoritative project geometry not assumed |
| Legal notices and administrative publication | Amtsblatt für Berlin, official law database and authority Bekanntmachungen | State of Berlin | Formal notices, approvals, procurement/legal decisions, effective dates | Search and PDFs can be difficult; formal language and historic archives | Reuse, personal data and document-image rights require legal review | Candidate family; direct source and retention test pending |
| Oversight and audit | Rechnungshof Berlin, parliamentary committees, Senate reports and official audit publications | Court of Audit, Parliament, Senate | Findings, project controls, cost/schedule evidence, recommendations, responses | Reports can be periodic and not project-indexed | Reports may contain sensitive details; quote minimally and review reuse | Candidate family; project-level verification pending |

## Parliamentary depth and reference sources

**Schriftliche Anfragen (PARDOK).** Written questions and their answers. This
family is particularly strong for date revisions, current status and cost
tables, including direct answers to whether a project is on schedule.

Direct PDF pattern:
`pardok.parlament-berlin.de/starweb/adis/citat/VT/{WP}/SchrAnfr/S{WP}-{nr}.pdf`

**Hauptausschuss-Vorlagen.** Budget committee papers. This is where exact euro
figures, tax basis, budget chapter and title, funding sources, lot structure
and planning-approval dates may appear.

Direct PDF pattern:
`parlament-berlin.de/adosservice/{WP}/Haupt/vorgang/h{WP}-{nr}-v.pdf`

Both document families may contain named signatories. Cite the document, never
the signatory. Both returned HTTP 403 to a default script User-Agent during the
2026-08-06 evidence pass and served normally to a browser User-Agent.

**Reference sources.** These are not about a particular project, but resolve
wording used across projects. They are registered like project sources — URL,
publication date, retrieval date and content hash — but indexed by the term
they resolve and reused across dossiers.

| Term resolved | Authority | Source |
| --- | --- | --- |
| `Schuljahresbeginn` | SenBJF | Ferienordnung für das Land Berlin 2024/2025 bis 2029/2030 |

## Source-identity findings

Senate press releases can be served byte-identically at multiple URL paths,
including `/sen/sbw/presse/pressemeldungen/…` and
`/sen/stadt/presse/pressemeldungen/…`. This was confirmed by identical
SHA-256 values for Pressemitteilung 1374721. **Source identity is not URL
identity:** deduplicate by content hash.

A programme index page's `Aktuelles` block carries dated news items that are
separate publications, not necessarily summaries of same-date press releases.
For C-014 the index item contains a funding figure absent from the press
release. Retrieve and register index items rather than treating the page as
navigation only.

## Working verification states

- **Entry point verified:** the official page or catalogue was opened and its
  purpose was checked.
- **Family lead:** the source type is plausible from prior research but has not
  yet been tested against a named candidate.
- **Candidate verified:** the exact record was opened, matched to the project,
  and its relevant German evidence span was manually checked.
- **Blocked / stale:** the source is known but currently inaccessible, moved,
  incomplete or stale; retain the failed path and retrieval date.
- **Licence pending:** no public reuse decision has yet been made. Do not treat
  discoverability as permission to copy or rehost.

## Research protocol

For each candidate, search the source families in parallel and record the
result even when it is empty. Capture URL, publisher, source type, publication
date, retrieval date, content hash when an artifact is retained privately,
language, access method, relevant fields, evidence span, licence note and
failure reason. Keep the original German wording as canonical evidence.

An official source is not automatically complete, current or authoritative for
every field. For example, a budget line can support an approved allocation but
not expenditure; a procurement notice can support an award or lot but not final
project cost; a plan approval can support a decision but not construction start.
The milestone and financial-measure definitions in `docs/methodology.md` apply.

## Direct-verification queue

For future candidates, verify before selection at minimum: project identity and
boundary, location, current status, expected end date or an official statement
that none is published, and the exact source terms for any budget, contract or
award claim. Organization roles publish only under the naming policy.

C-010, C-014 and C-019 have completed their first evidence passes. Their
remaining candidate-specific checks are recorded in their dossiers rather than
being treated as proof that the source families are exhausted.
