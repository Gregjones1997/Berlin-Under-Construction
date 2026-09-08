# Seven-candidate expansion screening

**Retrieval date:** 8 September 2026. **Status:** Research proposals, not publication decisions.

## Result

Screened C-001, C-002, C-003, C-004, C-005, C-008 and C-009 from the existing ledger: two bridges, three rail projects and two school projects. This selection favors named sites/routes and existing primary-source leads; it is a preparation order, not an owner-approved replacement of the pilot set. All seven have source-stated schedule wording and at least textual location or route evidence. No numeric coordinates were checked and none was added to the app.

Ten official HTML sources were retrieved with HTTP 200 using a full browser User-Agent. Eighteen short excerpts (110 words) were checked against the decoded HTML with whitespace normalization. Full HTML is retained only in gitignored `data/artifacts/`; the [screening data](2026-09-08-seven-candidate-screening.json) records content hashes, source dates, retrieval dates, exact excerpts, review questions and glossary matches. Undated pages carry null publication dates, not retrieval dates used as substitutes.

## Candidate findings

### C-001 — Ersatzneubau der Elsenbrücke

**Preparation priority:** dossier preparation. Official page describes bridge and street approaches; no numeric coordinates checked.

- [Official source: elsen](https://www.berlin.de/sen/uvk/mobilitaet-und-verkehr/infrastruktur/brueckenbau/elsenbruecke/); published date not stated. Exact excerpts are retained in the screening data.

- Retain the construction-period wording rather than assigning an opening date.
- Reconcile staged works and remaining works before describing current completion.

### C-002 — Ersatzneubau der Mühlendammbrücke

**Preparation priority:** dossier preparation. Official text describes the crossing; no numeric coordinates checked.

- [Official source: muehlen](https://www.berlin.de/sen/uvk/mobilitaet-und-verkehr/infrastruktur/brueckenbau/muehlendammbruecke/); published date not stated. Exact excerpts are retained in the screening data.

- Preserve the expected construction period and distinguish partial works from whole-project completion.
- Earlier ledger sentence was not found on the current page; do not carry it forward as current.

### C-003 — Verlängerung der U3 zum Mexikoplatz

**Preparation priority:** dossier preparation; scope review. Official route endpoints given; underground storage beyond the station also described. No numeric coordinates checked.

- [Official source: u3](https://bvg-projekt.de/projekte/verlaengerung-u-bahnlinie-u3-nachhaltigkeits-pilotprojekt-berlin-steglitz-zehlendorf/); published date not stated. Exact excerpts are retained in the screening data.

- Retain soll and do not replace the current wording with the old ledger milestone label.
- Freeze station, tunnel and storage scope before mapping; a route is not a single building point.
- Page still labels planning status; calendar arrival alone does not establish construction start.

### C-004 — Reaktivierung der Siemensbahn

**Preparation priority:** dossier preparation; vocabulary exception. Route endpoints directly supported; route geometry and construction segments not checked.

- [Official source: siemens](https://www.deutschebahn.com/de/presse/presse-regional/pr-berlin-de/aktuell/presseinformationen/Meilenstein-fuer-die-Siemensbahn-Allianz-Partner-fuer-die-Reaktivierung-stehen-fest-13569054); published 2025-09-29. Exact excerpts are retained in the screening data.
- [Official source: db2026](https://www.deutschebahn.com/de/presse/presse-regional/pr-berlin-de/Bauprojekte/Bauen-bei-der-DB-InfraGO-2026-10057136); published date not stated. Exact excerpts are retained in the screening data.

- The current source uses wieder ans Netz, not the former ledger quotation. Keep it verbatim pending contextual mapping.
- Separate route reactivation from possible later extensions and adjacent works.

### C-005 — Umbau Bahnhof Köpenick zum Regionalbahnhof

**Preparation priority:** dossier preparation; station scope review. Station identity and bridge street supported; street address and numeric coordinates not checked.

- [Official source: koepenick](https://www.deutschebahn.com/de/presse/presse-regional/pr-berlin-de/aktuell/presseinformationen/Zeitplan-fuer-Ausbauprojekt-Berlin-Frankfurt-Oder-angepasst--13508236); published 2025-09-11. Exact excerpts are retained in the screening data.
- [Official source: db2026](https://www.deutschebahn.com/de/presse/presse-regional/pr-berlin-de/Bauprojekte/Bauen-bei-der-DB-InfraGO-2026-10057136); published date not stated. Exact excerpts are retained in the screening data.

- Station service timing differs from the wider corridor completion; do not merge them.
- IBN is not an existing glossary alias; retain it as a review question rather than expand it as verified.

### C-008 — Grundschule am Weißen See — Sanierung / Ausbau

**Preparation priority:** history example; confirm outcome. Official newer notice supplies Amalienstraße 6; no numeric coordinates checked.

- [Official source: school](https://www.berlin.de/ba-pankow/aktuelles/pressemitteilungen/2026/pressemitteilung.1703602.php); published 2026-08-17. Exact excerpts are retained in the screening data.
- [Official source: school-old](https://www.berlin.de/ba-pankow/aktuelles/pressemitteilungen/2026/pressemitteilung.1663498.php); published 2026-04-22. Exact excerpts are retained in the screening data.

- Newer notice schedules a move; it does not retrospectively confirm that it occurred.
- Keep the old uncertainty and new move statement as different dated claims.
- No calendar resolution of a relative anchor was performed in this screening.

### C-009 — Das Fliegende Klassenzimmer 2.0 — Friedenauer Gemeinschaftsschule

**Preparation priority:** dossier preparation. District invitation identifies school and address; building footprint and numeric coordinates unchecked.

- [Official source: dfk](https://www.berlin.de/ba-tempelhof-schoeneberg/aktuelles/pressemitteilungen/2026/pressemitteilung.1689531.php); published 2026-07-03. Exact excerpts are retained in the screening data.
- [Official source: dfk-location](https://www.berlin.de/ba-tempelhof-schoeneberg/aktuelles/pressemitteilungen/2026/pressemitteilung.1686950.php); published 2026-06-29. Exact excerpts are retained in the screening data.

- Scope is this school building, not the citywide building system.
- Preserve the source qualifier and full-completion wording.

## Vocabulary and review workload

Literal matching found 11 existing glossary rows in the selected excerpts. Three already occur in the current app review pack; eight are additional existing rows, bringing the combined preparation scope to 24 distinct glossary rows. These are row counts, including nested phrases, not independent meanings or accuracy measurements. No new translation was generated.

The candidate excerpts add 110 source words to the existing pack’s 184, for 294 excerpt words across 38 excerpts. This does not count full source context, reviewer instructions, or the complete dossiers. It is not a full-document workload.

The eight additional rows are G013, G014, G017, G020, G028, G081, G087 and G092 (glossary 1.1). Applying only the previously declared 1–3 minutes per glossary-row assumption gives **8–24 additional minutes for those term decisions**. Candidate passage checks, scope review, geolocation and source reading are additional and have not been estimated here. No saved time is claimed.

The Siemensbahn network-return wording and the DB abbreviation for the Köpenick date are contextual questions, not automatically verified glossary matches. Location words and proper project labels also fall outside much of the glossary. Even an existing match can have a different use: a word denoting an endpoint may refer to a route rather than a date.

## Retrieval trail and delegation

The research skill requested a background lane. One read-only agent screened C-003/004/005 while the main agent screened C-001/002/008/009. The lane returned official source candidates, short excerpts, timetable/scope caveats and access outcomes. The main agent independently reopened and downloaded the selected BVG Projekt, DB announcement and DB annual-programme sources, checked their excerpts, and accepted those as screening evidence. The main agent was the only repository writer.

The agent additionally used the vercel:agent-browser skill to read the Siemensbahn microsite, a BVG residents-event page and the DB BauInfoPortal after web retrieval returned errors, a challenge or empty text. It reported successful browser reads and closed its session. These supplementary outputs were useful leads but were not independently rechecked by the main agent and are not the basis of the retained candidate claims. No lane was redundant or abandoned; no agent verdict became a publication decision.

The main web tool twice returned Internal Error for the older C-008 district notice. A full browser User-Agent download returned HTTP 200 and the expected article; the excerpt check succeeded. This was a retrieval-tool problem, not evidence that the source was unavailable. All ten selected artifacts downloaded successfully; no selected source needed escalation to the owner.

## Remaining work

Prepare C-009 first as a bounded building dossier, then C-001/002 bridge dossiers. For every candidate, check map coordinates against an authoritative location record, establish the project boundary, inspect relevant source history and prepare eligible review decisions before app integration. C-003/004/005 require route or station scoping; C-008 is particularly useful as a dated change-history example but needs an outcome check.

This was a targeted project-page/press-release screening, not an exhaustive source audit. Budget, procurement and committee evidence were not investigated. No financial completeness claim, semantic accuracy score, new golden value, inferred date or construction-completion decision was produced. The existing three public dossiers and all publication gates remain unchanged.
