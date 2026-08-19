# C-014 publication decision list

**Status:** Owner review required before any item below can move from
`withheld` to `published` in `public/data/projects.json`.

**Scope:** C-014 only. The project name, location and the already accepted
unreconciled Plätzeprogramm figures are not repeated here. Their publication
basis is recorded in the frozen dossier and ADR-009. No item below is approved
by this document, and no agent may interpret silence as acceptance.

For each item, record **accept**, **reject**, **modify** or **defer** and a short
rationale. A modification needs a replacement German value and the exact source
span that supports it. Approval will be copied into the projection as an
append-only owner-decision reference; it will not overwrite this list.

## Decisions

### 1. Current source status

- Fact ID: `c014-current-status`
- Proposed German value: `Laufende Maßnahme`
- Exact German span: `Laufende Maßnahme`
- Source: <https://www.berlin.de/sen/bauen/baukultur/berliner-plaetzeprogramm/europaplatz-sued-1567894.php>
- Publication date: not stated
- Decision needed: publish this only as a source status, knowing the frozen
  dossier says the field may be stale; or keep it withheld.
- Owner decision: **pending**

### 2. Current completion field

- Fact ID: `c014-expected-completion-current`
- Proposed German value: `Fertigstellung: 2026`
- Exact German span: `Fertigstellung: 2026`
- Source: <https://www.berlin.de/sen/bauen/baukultur/berliner-plaetzeprogramm/europaplatz-sued-1567894.php>
- Publication date: not stated
- Decision needed: publish as the project page's undated current completion
  field, not as verified completion and not as a more precise date.
- Owner decision: **pending**

### 3. Earlier completion target

- Fact ID: `c014-completion-history-2023`
- Proposed German value: `Die Fertigstellung der anspruchsvollen Bauaufgabe ist bis Ende 2025 vorgesehen.`
- Exact German span: `Die Fertigstellung der anspruchsvollen Bauaufgabe ist bis Ende 2025 vorgesehen.`
- Source: <https://www.berlin.de/sen/stadt/presse/pressemeldungen/pressemitteilung.1374721.php>
- Publication date: 2023-10-12
- Decision needed: publish in the change history with `bis` and `vorgesehen`
  retained in the value.
- Owner decision: **pending**

### 4. Three completion statements in the 2025 paper

- Fact ID: `c014-completion-history-2025`
- Candidate A: `Die Umsetzung der Baumaßnahme wird nach zeitnaher Ausschreibung (2025) in 2026 durchgeführt (Fertigstellung geplant für Sommer 2026).`
- Candidate B: `Die Baumaßnahme wird im Sommer 2026 abgeschlossen werden.`
- Candidate C: `Die Fertigstellung der Baumaßnahme wird voraussichtlich in 2026 erfolgen.`
- Source: <https://www.parlament-berlin.de/adosservice/19/Haupt/vorgang/h19-2449-v.pdf>
- Publication date: 2025-10-06 under the owner ruling recorded in the frozen
  dossier; the letterhead's 2026 year is a preserved source typo.
- Decision needed: publish all three distinctly, select a specified one with a
  rationale, or keep the group withheld. The dossier says an agent selection
  would be arbitrary.
- Owner decision: **pending**

### 5. January 2026 construction-period statement

- Fact ID: `c014-completion-period-2026`
- Proposed German value: `Der Europaplatz wird im ersten Halbjahr 2026 zu einem klimaresilienten, ansprechenden Bahnhofsvorplatz umgebaut.`
- Exact German span: same as the proposed value
- Source: <https://www.berlin.de/sen/stadt/presse/pressemeldungen/pressemitteilung.1637393.php>
- Publication date: 2026-01-26
- Decision needed: publish as a construction-period statement, not
  `Fertigstellung`.
- Owner decision: **pending**

### 6. Construction-start change

- Fact ID: `c014-construction-start-history`
- Proposed German value: `Der Baubeginn wird erst im Januar 2026 erfolgen.`
- Exact German span: same as the proposed value
- Source: <https://www.parlament-berlin.de/adosservice/19/Haupt/vorgang/h19-2449-v.pdf>
- Publication date: 2025-10-06 under the recorded owner ruling
- Decision needed: publish as the source's own delay wording, preserving `erst`.
- Owner decision: **pending**

### 7. Current construction-start date

- Fact ID: `c014-construction-start-current`
- Proposed German value: `Die Umgestaltung des südlichen Europaplatzes, dem Vorplatz des Hauptbahnhofs an der Invalidenstraße, beginnt am 2. Februar 2026.`
- Exact German span: same as the proposed value
- Source: <https://www.berlin.de/sen/stadt/presse/pressemeldungen/pressemitteilung.1637393.php>
- Publication date: 2026-01-26
- Decision needed: publish as the announced construction-start date, not as
  evidence that construction actually began.
- Owner decision: **pending**

### 8. Approved total cost

- Fact ID: `c014-approved-total-cost`
- Proposed German value: `Die Prüfung und Genehmigung der Bauplanungsunterlage mit Gesamtkosten in Höhe von 3 .183.000 € brutto erfolgte mit Datum vom 31.01.2025 durch die zuständige Stelle der Senatsverwaltung für Stadtentwicklung, Bauen und Wohnen.`
- Exact German span: same as the proposed value
- Source: <https://www.parlament-berlin.de/adosservice/19/Haupt/vorgang/h19-2449-v.pdf>
- Publication date: 2025-10-06 under the recorded owner ruling
- Decision needed: verify the original PDF rendering before acceptance because
  the dossier identifies `3 .183.000` as an extraction spacing artifact.
- Owner decision: **pending**

## Intentionally not offered for approval

- `c014-completion-outcome` remains withheld with
  `multi_source_synthesis_has_no_exact_span`. “Passed target window; completion
  not verified” is useful analysis but has no single exact German evidence span
  and therefore cannot satisfy the current display contract.
- `c014-organization-roles` remains withheld with
  `role_vocabulary_unresolved`. The frozen dossier records observations but
  assigns no commissioner, financer or contractor role.
