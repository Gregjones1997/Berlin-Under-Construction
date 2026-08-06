# Glossary verification report

**Run date:** 2026-08-06  
**Glossary version:** 1.0  
**Glossary verification status:** Pending native-speaker review  
**Scope:** 88 glossary rows (87 distinct row labels; `geschätzt` occurs in two sections)

This report records retrieval and divergence detection. It does not approve a
translation, select a contextual dictionary sense or edit `docs/glossary.md`.
Every native-speaker review cell is intentionally empty.

## Structural risk found in C-010

The 2026-08-06 evidence pass encountered five distinct completion or handover
forms for one project across four publishing bodies:

| Term | Source | Published |
| --- | --- | --- |
| `Fertigstellung und Übergabe` | Bezirksamt Friedrichshain-Kreuzberg | 2023-12-21 |
| `Fertigstellung` | Senate Schulbau portal | 2024-07-03 |
| `technische Übergabe` | SenBJF, Drucksache 19/26230 | 2026-06-19 |
| `bauliche Fertigstellung` + `Übergabe an den Bezirk` | Bezirksamt Friedrichshain-Kreuzberg | 2026-07-06 |
| `Endfertigstellung` | HOWOGE | undated |

This is a display-layer and schema risk, not merely a vocabulary-coverage
issue. A golden value for a C-010 “completion date” is ill-formed unless it
also identifies the milestone type. No default completion type should be
assumed. The seven glossary 1.1 seed rows added from this evidence pass remain
outside the version 1.0 verification counts below until separately verified.

## Method and limits

Three passes were run:

1. Each glossary row was checked against Duden and DWDS. `D` below means a
   standalone Duden article was retrieved; `S` means an exact Duden search or
   component article was retrieved but no standalone article for the complete
   phrase was established; `A` means a specialist primary authority was also
   retrieved. DWDS word pages were blocked by the retrieval service's robots
   policy, so the report does not claim that a DWDS entry is absent.
2. All 29 candidate-ledger rows were inspected for their stored German
   expected-end wording. Twenty-eight contained a quoted German span group and
   were back-translated once by Codex, German → English → German. C-026 contained
   no quoted German span, so 28—not 29—span groups were back-translated. This is
   divergence detection by a model, not validation by an independent authority.
3. Project-specific official English counterparts were sought on Berlin.de, DB
   and BVG. Three German/English Berlin.de news pairs were found (C-001, C-014
   and C-019). No project-specific English counterpart was found for the other
   26 candidate rows. DB and BVG have official English sites, but the checked
   C-003, C-004 and C-005 project publications had no counterpart in the search
   paths used. Absence means “not found in this pass,” not proof that none exists.

Primary lexical and domain checks included [Duden's `Baubeginn`](https://www.duden.de/rechtschreibung/Baubeginn),
[`Bauabnahme`](https://www.duden.de/rechtschreibung/Bauabnahme),
[`Fertigstellung`](https://www.duden.de/rechtschreibung/Fertigstellung),
[`Inbetriebnahme`](https://www.duden.de/rechtschreibung/Inbetriebnahme),
[`Kosten`](https://www.duden.de/rechtschreibung/Kosten),
[`Finanzierung`](https://www.duden.de/rechtschreibung/Finanzierung) and
[`voraussichtlich`](https://www.duden.de/rechtschreibung/voraussichtlich), plus
the [Berlin building-control glossary](https://www.berlin.de/sen/bauen/baurecht-und-bauplanung/bauaufsicht/glossar/),
[Destatis on the Baupreisindex](https://www.destatis.de/DE/Themen/Wirtschaft/Preise/Baupreise-Immobilienpreisindex/Methoden/Erlaeuterungen/baupreisindex.html),
the [Bundestag definition of Verpflichtungsermächtigung](https://www.bundestag.de/services/glossar/glossar/V/verpflichtungserm-245556)
and the [Federal Ministry of Finance on the budget hierarchy](https://www.bundesfinanzministerium.de/Content/DE/Glossareintraege/H/haushaltsplan.html?view=renderHelp).

## Result

- **Agreed:** 77 rows. No divergence was detected among the authorities actually
  consulted; this is not proof that the mapping is correct.
- **Flagged:** 6 rows. These form the native-speaker review queue below.
- **Unresolved:** 5 rows. No adequate standalone lexical or specialist authority
  was retrieved for the complete term in this pass.

### Native-speaker review queue

1. `Baubeginn` — Duden describes the beginning of construction works, while the
   Berlin building-control glossary says the term covers only preparatory
   measures. Which source sense applies must be decided from each evidence span.
2. `Bauabnahme` — Duden gives both an administrative confirmation sense and an
   owner's inspection sense; the glossary currently exposes one broad mapping.
3. `Kosten` — Duden treats `Ausgaben` as a general-language synonym, while this
   project's financial ontology must keep cost and expenditure measures typed.
4. `Finanzierung` — Duden includes both financing generally and credit-granting;
   `funding arrangement` is not safe without context.
5. `vorgesehen` — C-004 and C-009 back-translated through `planned` / `geplant`,
   losing the glossary's proposed weaker modality.
6. `soll` — C-002 and the second sentence in C-019 back-translated through
   `expected` or `scheduled`, collapsing the separate modal wording.

## Term-by-term record

`None` in the divergence column means no material change to bound, direction,
precision, confidence, scope or milestone type was detected. `Not available`
in the parallel-text column means no project-specific official English evidence
was found for that row in this pass.

| Term | DWDS/Duden retrieved | Back-translation divergence | Official parallel English found | Status | Native-speaker review |
| --- | --- | --- | --- | --- | --- |
| `Baubeginn` | D + A; DWDS blocked | None | Not available | flagged | |
| `Baustart` | S; DWDS blocked | None | Not available | agreed | |
| `Spatenstich` | S; DWDS blocked | None | Not available | agreed | |
| `Bauarbeiten` | D; DWDS blocked | None | [C-001](https://www.berlin.de/en/news/7675155-5559700-full-closure-elsenbruecke-saturday.en.html), [C-014](https://www.berlin.de/en/news/10163776-5559700-europaplatz-to-be-redesigned-from-februa.en.html) | agreed | |
| `Bauausführung` | D + A; DWDS blocked | None | Not available | agreed | |
| `Baumaßnahme` | D; DWDS blocked | None | Not available | agreed | |
| `Bauabschnitt` | D; DWDS blocked | None | [C-014](https://www.berlin.de/en/news/10163776-5559700-europaplatz-to-be-redesigned-from-februa.en.html) | agreed | |
| `erster Bauabschnitt` | S; DWDS blocked | None | Not available | agreed | |
| `Hauptmaßnahmen` | S; DWDS blocked | None | Not available | agreed | |
| `bauvorbereitende Maßnahmen` | S + A; DWDS blocked | None | Not available | agreed | |
| `Baufeldfreimachung` | S; DWDS blocked | None | Not available | agreed | |
| `Baufeld` | D; DWDS blocked | None | Not available | agreed | |
| `Bauzeit` | D; DWDS blocked | None | Not available | agreed | |
| `Voraussichtliche Bauzeit` | S; DWDS blocked | None | Not available | agreed | |
| `Bauende` | S; DWDS blocked | None | Not available | agreed | |
| `Fertigstellung` | D; DWDS blocked | None | Not available | agreed | |
| `vollständige Fertigstellung` | S; DWDS blocked | None | Not available | agreed | |
| `bauliche Fertigstellung` | S; DWDS blocked | None | Not available | agreed | |
| `geplante Fertigstellung` | S; DWDS blocked | None | Not available | agreed | |
| `Fertigstellungstermin` | D; DWDS blocked | None | Not available | agreed | |
| `Gesamtfertigstellung` | S; DWDS blocked | None | Not available | agreed | |
| `Abschluss des ersten Bauabschnitts` | S; DWDS blocked | None | Not available | agreed | |
| `Baumaßnahme abgeschlossen` | S; DWDS blocked | None | Not available | agreed | |
| `Bauabnahme` | D; DWDS blocked | None | Not available | flagged | |
| `Übergabe` | D; DWDS blocked | None | Not available | agreed | |
| `Übergabe an den Bezirk` | S; DWDS blocked | None | Not available | agreed | |
| `Eröffnung` | D; DWDS blocked | None | Not available | agreed | |
| `Umzug` | D; DWDS blocked | None | Not available | agreed | |
| `Aufnahme des Unterrichtsbetriebes` | S; DWDS blocked | None | Not available | agreed | |
| `Inbetriebnahme` | D; DWDS blocked | None | [C-019](https://www.berlin.de/en/news/10361011-5559700-district-heating-from-surplus-electricit.en.html) | agreed | |
| `Verkehrsfreigabe` | S; DWDS blocked | None | Not available | agreed | |
| `Regionalzüge werden dort ab … halten` | S; DWDS blocked | None | Not available | agreed | |
| `Bezugsfertigkeit` | S; DWDS blocked | None | Not available | agreed | |
| `bezogen` | D component; DWDS blocked | None | Not available | agreed | |
| `Planreife` | S; DWDS blocked | None | Not available | agreed | |
| `Bebauungsplanverfahren` | S + A; DWDS blocked | None | Not available | agreed | |
| `Bauleitplanung` | D + A; DWDS blocked | None | Not available | agreed | |
| `Rahmenplan` | D; DWDS blocked | None | Not available | agreed | |
| `Werkstattverfahren` | D; DWDS blocked | None | Not available | agreed | |
| `Vorbereitende Untersuchungen` | S; DWDS blocked | None | Not available | agreed | |
| `Realisierungswettbewerb` | D; DWDS blocked | None | Not available | agreed | |
| `Erschließung` | D + A; DWDS blocked | None | Not available | agreed | |
| `Projektzeitraum` | D; DWDS blocked | None | Not available | agreed | |
| `Laufzeit` | D; DWDS blocked | None | Not available | agreed | |
| `Gesamtmaßnahme` | D; DWDS blocked | None | Not available | agreed | |
| `Kosten` | D; DWDS blocked | None | [C-014](https://www.berlin.de/en/news/10163776-5559700-europaplatz-to-be-redesigned-from-februa.en.html) | flagged | |
| `Gesamtkosten` | D; DWDS blocked | None | Not available | agreed | |
| `Gesamtbausumme` | S; DWDS blocked | None | Not available | agreed | |
| `voraussichtliche Gesamtkosten` | S; DWDS blocked | None | Not available | agreed | |
| `Planungskosten` | D; DWDS blocked | None | Not available | agreed | |
| `Baukosten` | D; DWDS blocked | None | Not available | agreed | |
| `Investitionsvolumen` | D; DWDS blocked | None | Not available | agreed | |
| `Investitionen` | D component; DWDS blocked | None | Not available | agreed | |
| `Investitionsmittel` | D; DWDS blocked | None | Not available | agreed | |
| `Investitionsrahmen` | D; DWDS blocked | None | Not available | agreed | |
| `Finanzierung` | D; DWDS blocked | None | [C-019](https://www.berlin.de/en/news/10361011-5559700-district-heating-from-surplus-electricit.en.html) | flagged | |
| `Finanzierung aus Haushalt Berlin` | S; DWDS blocked | None | Not available | agreed | |
| `Finanzierungsvereinbarung` | D; DWDS blocked | None | Not available | agreed | |
| `Ergänzungsunterlage zur Finanzierung` | S; DWDS blocked | None | Not available | unresolved | |
| `haushalterische Grundlage` | S; DWDS blocked | None | Not available | unresolved | |
| `finanziert aus dem Plätzeprogramm` | S; DWDS blocked | None | Not available | unresolved | |
| `Finanzierungslücke` | D; DWDS blocked | None | Not available | agreed | |
| `GRW-Mittel` | S + A; DWDS blocked | None | Not available | agreed | |
| `Zuschüsse` | D component; DWDS blocked | None | Not available | agreed | |
| `Ausgaben` | D component + A; DWDS blocked | None | Not available | agreed | |
| `Verpflichtungsermächtigung` | A; Duden/DWDS unavailable | None | Not available | agreed | |
| `Einzelplan` | D + A; DWDS blocked | None | Not available | agreed | |
| `Kapitel` | D + A; DWDS blocked | None | Not available | agreed | |
| `Nachtragsleistungen` | D component; DWDS blocked | None | Not available | agreed | |
| `Baupreisindex` | A; Duden/DWDS unavailable | None | Not available | agreed | |
| `geschätzt` | D; DWDS blocked | None | Not available | agreed | |
| `Realisierungsverträge` | S; DWDS blocked | None | Not available | unresolved | |
| `Einbringungsverträge` | S; DWDS blocked | None | Not available | unresolved | |
| `Investorenprojekt` | S; DWDS blocked | None | Not available | agreed | |
| `bis` | S; DWDS blocked | None | [C-019](https://www.berlin.de/en/news/10361011-5559700-district-heating-from-surplus-electricit.en.html) | agreed | |
| `ab` | S; DWDS blocked | None | [C-014](https://www.berlin.de/en/news/10163776-5559700-europaplatz-to-be-redesigned-from-februa.en.html) | agreed | |
| `Anfang` / `Mitte` / `Ende` | D; DWDS blocked | None | [C-019](https://www.berlin.de/en/news/10361011-5559700-district-heating-from-surplus-electricit.en.html) | agreed | |
| `voraussichtlich` | D; DWDS blocked | None | Not available | agreed | |
| `geplant` | D; DWDS blocked | None | [C-019](https://www.berlin.de/en/news/10361011-5559700-district-heating-from-surplus-electricit.en.html) | agreed | |
| `vorgesehen` | D; DWDS blocked | C-004, C-009: weakened distinction collapsed to `geplant` | [C-014](https://www.berlin.de/en/news/10163776-5559700-europaplatz-to-be-redesigned-from-februa.en.html) | flagged | |
| `anvisiert` / `angestrebt` | D components; DWDS blocked | None | Not available | agreed | |
| `soll` | D component; DWDS blocked | C-002, C-019: separate modal wording collapsed | [C-001](https://www.berlin.de/en/news/7675155-5559700-full-closure-elsenbruecke-saturday.en.html), [C-014](https://www.berlin.de/en/news/10163776-5559700-europaplatz-to-be-redesigned-from-februa.en.html) | flagged | |
| `frühestens` | D; DWDS blocked | None | Not available | agreed | |
| `spätestens` | D; DWDS blocked | None | Not available | agreed | |
| `rund` / `etwa` / `ca.` | D components; DWDS blocked | None | [C-014](https://www.berlin.de/en/news/10163776-5559700-europaplatz-to-be-redesigned-from-februa.en.html) | agreed | |
| `geschätzt` | D; DWDS blocked | None | Not available | agreed | |
| `nicht belastbar` | D component; DWDS blocked | None | Not available | agreed | |
| `Stand` | D; DWDS blocked | None | Not available | agreed | |

## Candidate-span back-translation record

The comparison is semantic rather than character-for-character. Synonym changes
are recorded as material only when they change a bound, direction, precision,
confidence, scope or milestone type.

| Candidate | Stored German span group | English pass | German return | Material divergence |
| --- | --- | --- | --- | --- |
| C-001 | `Voraussichtliche Bauzeit: 2020 bis 2028`; `Gesamtfertigstellung … im Jahr 2028` | Expected construction period: 2020 to 2028; overall completion in 2028 | `Voraussichtliche Bauzeit: 2020 bis 2028`; `Gesamtfertigstellung … im Jahr 2028` | None |
| C-002 | `Die Bauarbeiten sollen voraussichtlich bis 2029 abgeschlossen sein.` | The construction works are expected to be completed by 2029. | `Die Bauarbeiten werden voraussichtlich bis 2029 abgeschlossen sein.` | `sollen` lost |
| C-003 | `Ende 2030`; `Fertigstellung`; `Inbetriebnahme …` | End of 2030; completion; commissioning … | `Ende 2030`; `Fertigstellung`; `Inbetriebnahme …` | None |
| C-004 | `Die Inbetriebnahme der Strecke ist für das Jahr 2029 vorgesehen.` | Commissioning of the line is planned for 2029. | `Die Inbetriebnahme der Strecke ist für 2029 geplant.` | `vorgesehen` collapsed to `geplant` |
| C-005 | `Regionalzüge werden dort ab Dezember 2027 halten.` | Regional trains will stop there from December 2027. | `Regionalzüge werden dort ab Dezember 2027 halten.` | None |
| C-006 | `Vollsperrung … bis voraussichtlich März 2027` | Full closure … until approximately March 2027 | `Vollsperrung … bis voraussichtlich März 2027` | None |
| C-007 | `bis zur Fertigstellung des Neubaus (voraussichtlich 2028)` | until completion of the new building (expected in 2028) | `bis zur Fertigstellung des Neubaus (voraussichtlich 2028)` | None |
| C-008 | `Fertigstellungstermin … nicht belastbar`; `Fertigstellung spätestens … 2026` | completion date not reliable; completion no later than … 2026 | `Fertigstellungstermin … nicht belastbar`; `Fertigstellung spätestens … 2026` | None |
| C-009 | `die vollständige Fertigstellung ist für Mai 2027 vorgesehen` | full completion is planned for May 2027 | `die vollständige Fertigstellung ist für Mai 2027 geplant` | `vorgesehen` collapsed to `geplant` |
| C-010 | `bauliche Fertigstellung … Übergabe … zum 31. August 2026 geplant` | physical completion and handover planned for 31 August 2026 | `bauliche Fertigstellung und Übergabe zum 31. August 2026 geplant` | None |
| C-011 | `Eine Fertigstellung wird frühestens im Juli 2029 prognostiziert.` | Completion is forecast for July 2029 at the earliest. | `Eine Fertigstellung wird frühestens für Juli 2029 prognostiziert.` | None |
| C-012 | `den ersten Bauabschnitt im Herbst 2026 abzuschließen` | to complete the first construction phase in autumn 2026 | `den ersten Bauabschnitt im Herbst 2026 abzuschließen` | None |
| C-013 | `Baumaßnahme abgeschlossen bis voraussichtlich 2030.` | Construction measure completed by an expected 2030. | `Baumaßnahme bis voraussichtlich 2030 abgeschlossen.` | None |
| C-014 | `Fertigstellung: 2026` | Completion: 2026 | `Fertigstellung: 2026` | None |
| C-015 | `Fertigstellung der Gesamtmaßnahme … Ende 2029 anvisiert` | completion of the overall measure targeted for the end of 2029 | `Fertigstellung der Gesamtmaßnahme … für Ende 2029 angestrebt` | None; aspiration retained |
| C-016 | `soll … bis Mitte 2027 fertiggestellt werden` | is to be completed by mid-2027 | `soll … bis Mitte 2027 fertiggestellt werden` | None |
| C-017 | `Bauende: geplant für 2026`; `Bauzeit von Ende 2022 bis Ende 2026` | construction end planned for 2026; construction period from end-2022 to end-2026 | `Bauende: geplant für 2026`; `Bauzeit von Ende 2022 bis Ende 2026` | None |
| C-018 | `Inbetriebnahme … mit rund 75 Megawatt … für 2027 geplant` | commissioning … approximately 75 MW … planned for 2027 | `Inbetriebnahme … mit rund 75 Megawatt … für 2027 geplant` | None |
| C-019 | `Inbetriebnahme … bis Ende 2028 geplant`; `… sollen bis Ende 2028 in Betrieb gehen` | commissioning planned by end-2028; … scheduled to enter operation by end-2028 | `Inbetriebnahme … bis Ende 2028 geplant`; `… sind bis Ende 2028 zur Inbetriebnahme geplant` | `sollen` collapsed in second sentence |
| C-020 | `statten bis 2028 alle ihre Klärwerke … aus`; `Klärwerk … erhält …` | will equip all treatment plants by 2028; the plant receives … | `statten bis 2028 alle Klärwerke … aus`; `das Klärwerk erhält …` | None |
| C-021 | `Bauzeit wird voraussichtlich rund 24 Monate in Anspruch nehmen` | construction period is expected to take approximately 24 months | `Bauzeit wird voraussichtlich rund 24 Monate dauern` | None |
| C-022 | `Fertigstellung erster Wohngebäude 2028` | completion of the first residential buildings in 2028 | `Fertigstellung der ersten Wohngebäude 2028` | None |
| C-023 | `Entwicklung des … Areals bis Ende 2027` | development of the site by the end of 2027 | `Entwicklung des Areals bis Ende 2027` | None |
| C-024 | `voraussichtlich ab 2029 wieder ans S-Bahn-Netz angeschlossen` | expected to be reconnected to the S-Bahn network from 2029 | `voraussichtlich ab 2029 wieder an das S-Bahn-Netz angeschlossen` | None |
| C-025 | `Projektzeitraum 2016 – 2034` | project period 2016–2034 | `Projektzeitraum 2016–2034` | None |
| C-026 | No quoted German expected-end span stored | Not run | Not run | Source gap; not counted among back-translated spans |
| C-027 | `Planreife` | planning maturity | `Planreife` | None |
| C-028 | `ungefähr anderthalb Jahre` | approximately one and a half years | `ungefähr anderthalb Jahre` | None |
| C-029 | `bis zur Fertigstellung in ca. 15 Jahren` | until completion in approximately 15 years | `bis zur Fertigstellung in ca. 15 Jahren` | None |

## Official parallel-text record

| Candidate | German publication | Official English publication | Finding |
| --- | --- | --- | --- |
| C-001 | [Berlin.de German](https://www.berlin.de/aktuelles/7675155-958090-vollsperrung-der-elsenbruecke-am-samstag.html) | [Berlin.de English](https://www.berlin.de/en/news/7675155-5559700-full-closure-elsenbruecke-saturday.en.html) | `Bauarbeiten` and completion modality remain distinguishable. English is credited to BerlinOnline/deepl.com. |
| C-014 | [Berlin.de German](https://www.berlin.de/aktuelles/10163776-958090-europaplatz-wird-ab-februar-umgestaltet.html) | [Berlin.de English](https://www.berlin.de/en/news/10163776-5559700-europaplatz-to-be-redesigned-from-februa.en.html) | `ab`, `soll`, `vorgesehen`, `geplant`, stages, costs and approximation are represented. English is credited to dpa/deepl.com and is not a controlled glossary authority. |
| C-019 | [Berlin.de German](https://www.berlin.de/aktuelles/10361011-958090-fernwaerme-aus-ueberschuessigem-strom-be.html) | [Berlin.de English](https://www.berlin.de/en/news/10361011-5559700-district-heating-from-surplus-electricit.en.html) | `Inbetriebnahme … bis Ende 2028 geplant` becomes “scheduled to go into operation by the end of 2028,” preserving the upper bound and planned status. English is credited to dpa/deepl.com. |

Useful non-project-specific English material was also retrieved from
[Deutsche Bahn's English infrastructure reporting](https://zbir.deutschebahn.com/2025/en/interim-group-management-report-unaudited/development-of-business-units/db-infrago-business-unit/development-of-the-infrastructure/),
which uses completion, commissioning and operation wording separately. It was
not treated as a parallel translation for C-004 or C-005. The
[BVG English site](https://www.bvg.de/en/company) was available, but no English
counterpart to the C-003 U3 project page was found.
