# C-014 publication decision list

**Status:** Owner decisions recorded 2026-08-19

**Scope:** C-014 only. The project name, location and the already accepted
unreconciled Plätzeprogramm figures are not repeated here. Their publication
basis is recorded in the frozen dossier and ADR-009. Only the explicit decisions
below authorize a state change; silence is not acceptance.

For each item, record **accept**, **reject**, **modify** or **defer** and a short
rationale. A modification needs a replacement German value, exact source span
and explicit fact subtype. An accepted choice is appended to
`public/data/accepted-review-decisions.json`; only its opaque ID enters the
projection. The original proposals remain beside the recorded decisions.

## Decisions

### 1. Current source status

- Fact ID: `c014-current-status`
- Proposed German value and exact span: `Laufende Maßnahme`
- Proposed fact type: `status`
- Proposed as-of date: `2026-08-06`, the dated observation recorded in the
  frozen dossier
- Proposed freshness: `unassessed`; the display must retain the dossier's stale
  warning and must not imply verified real-world completion state
- Proposed evidence label / source tier: `Verified` / `primary`, meaning only
  that the authoritative page directly supports this source-status wording
- Source: <https://www.berlin.de/sen/bauen/baukultur/berliner-plaetzeprogramm/europaplatz-sued-1567894.php>
- Publication date: not stated
- Decision needed: publish only with that as-of date and freshness warning,
  modify the treatment, or keep it withheld.
- Owner decision: **ACCEPT** — Publish only as the page status observed on
  2026-08-06 with freshness unassessed and the stale-source warning retained;
  do not imply verified real-world completion state.

### 2. Current completion field

- Fact ID: `c014-expected-completion-current`
- Proposed German value: `Fertigstellung: 2026`
- Exact German span: `Fertigstellung: 2026`
- Proposed milestone type: `substantial_completion`; this mapping is part of
  the decision and must not be assigned later by an agent
- Source: <https://www.berlin.de/sen/bauen/baukultur/berliner-plaetzeprogramm/europaplatz-sued-1567894.php>
- Publication date: not stated
- Decision needed: publish as the project page's undated current completion
  field, not as verified completion and not as a more precise date.
- Owner decision: **ACCEPT** — Publish as `substantial_completion` and as the
  page's undated current completion field, not a verified or more precise date.

### 3. Earlier completion target

- Fact ID: `c014-completion-history-2023`
- Proposed German value: `Die Fertigstellung der anspruchsvollen Bauaufgabe ist bis Ende 2025 vorgesehen.`
- Exact German span: `Die Fertigstellung der anspruchsvollen Bauaufgabe ist bis Ende 2025 vorgesehen.`
- Proposed milestone type: `substantial_completion`
- Source: <https://www.berlin.de/sen/stadt/presse/pressemeldungen/pressemitteilung.1374721.php>
- Publication date: 2023-10-12
- Decision needed: publish in the change history with `bis` and `vorgesehen`
  retained in the value.
- Owner decision: **ACCEPT** — Publish as `substantial_completion` with `bis`
  and `vorgesehen` retained in the displayed German value.

### 4. Three completion statements in the 2025 paper

- Fact ID A: `c014-completion-history-2025-a`
  - Proposed value/span: `Die Umsetzung der Baumaßnahme wird nach zeitnaher Ausschreibung (2025) in 2026 durchgeführt (Fertigstellung geplant für Sommer 2026).`
  - Proposed milestone type: `substantial_completion`
- Fact ID B: `c014-completion-history-2025-b`
  - Proposed value/span: `Die Baumaßnahme wird im Sommer 2026 abgeschlossen werden.`
  - Proposed milestone type: `substantial_completion`
- Fact ID C: `c014-completion-history-2025-c`
  - Proposed value/span: `Die Fertigstellung der Baumaßnahme wird voraussichtlich in 2026 erfolgen.`
  - Proposed milestone type: `substantial_completion`
- Source: <https://www.parlament-berlin.de/adosservice/19/Haupt/vorgang/h19-2449-v.pdf>
- Publication date: 2025-10-06 under the owner ruling recorded in the frozen
  dossier; the letterhead's 2026 year is a preserved source typo.
- Decision needed: publish all three distinctly, select a specified one with a
  rationale, or keep the group withheld. The dossier says an agent selection
  would be arbitrary.
- Owner decision: **ACCEPT ALL THREE** — Publish A, B and C distinctly as
  `substantial_completion`, side by side, with no selection, ranking or
  preferred-reading annotation.

### 5. January 2026 construction-period statement

- Fact ID: `c014-completion-period-2026`
- Proposed German value: `Der Europaplatz wird im ersten Halbjahr 2026 zu einem klimaresilienten, ansprechenden Bahnhofsvorplatz umgebaut.`
- Exact German span: same as the proposed value
- Proposed fact subtype: none. The accepted milestone vocabulary has no
  construction-period type, and the dossier explicitly says this is not
  `Fertigstellung`.
- Source: <https://www.berlin.de/sen/stadt/presse/pressemeldungen/pressemitteilung.1637393.php>
- Publication date: 2026-01-26
- Decision needed: keep withheld, specify an already accepted type with a
  rationale, or explicitly authorize a separate schema decision. A bare
  publication acceptance cannot be implemented and will not be inferred.
- Owner decision: **DEFER** — Do not add a construction-period milestone type
  this sprint; keep the fact withheld as `milestone_vocabulary_unresolved`.

### 6. Construction-start change

- Fact ID: `c014-construction-start-history`
- Proposed German value: `Der Baubeginn wird erst im Januar 2026 erfolgen.`
- Exact German span: same as the proposed value
- Proposed milestone type: `construction_start`
- Source: <https://www.parlament-berlin.de/adosservice/19/Haupt/vorgang/h19-2449-v.pdf>
- Publication date: 2025-10-06 under the recorded owner ruling
- Decision needed: publish as the source's own delay wording, preserving `erst`.
- Owner decision: **ACCEPT** — Publish as `construction_start`, preserving the
  source's `erst` wording.

### 7. Current construction-start date

- Fact ID: `c014-construction-start-current`
- Proposed German value: `Die Umgestaltung des südlichen Europaplatzes, dem Vorplatz des Hauptbahnhofs an der Invalidenstraße, beginnt am 2. Februar 2026.`
- Exact German span: same as the proposed value
- Proposed milestone type: `construction_start`
- Source: <https://www.berlin.de/sen/stadt/presse/pressemeldungen/pressemitteilung.1637393.php>
- Publication date: 2026-01-26
- Decision needed: publish as the announced construction-start date, not as
  evidence that construction actually began.
- Owner decision: **ACCEPT** — Publish as `construction_start` and as the
  announced date, not evidence that construction actually began.

### 8. Approved total cost

- Fact ID: `c014-approved-total-cost`
- Accepted German value and exact span: `Die Prüfung und Genehmigung der Bauplanungsunterlage mit Gesamtkosten in Höhe von 3.183.000 € brutto erfolgte mit Datum vom 31.01.2025 durch die zuständige Stelle der Senatsverwaltung für Stadtentwicklung, Bauen und Wohnen.`
- Proposed financial measure type: `approved_budget`; accepting this mapping is
  required because the source wording is approved `Gesamtkosten`, not spend
- Source: <https://www.parlament-berlin.de/adosservice/19/Haupt/vorgang/h19-2449-v.pdf>
- Publication date: 2025-10-06 under the recorded owner ruling
- Decision needed: verify the original PDF rendering before acceptance because
  the dossier identifies `3 .183.000` as an extraction spacing artifact.
- Owner decision: **ACCEPT** — The owner checked the original PDF: it renders
  `3.183.000`. Publish as `approved_budget`, amount 3,183,000 EUR and stated
  gross tax treatment; price basis and budget reference remain `not_stated`.

## Intentionally not offered for approval

- `c014-completion-outcome` remains withheld with
  `multi_source_synthesis_has_no_exact_span`. “Passed target window; completion
  not verified” is useful analysis but has no single exact German evidence span
  and therefore cannot satisfy the current display contract.
- `c014-organization-roles` remains withheld with
  `role_vocabulary_unresolved`. The frozen dossier records observations but
  assigns no commissioner, financer or contractor role.
