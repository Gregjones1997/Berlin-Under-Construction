
# C-019 — Power-to-Heat-Anlage am Heizkraftwerk Berlin-Mitte

**Dossier status:** Evidence pass complete; change history searched and absent
**Owner confirmation:** 2026-08-06
**Last evidence pass:** 2026-08-06
**Evidence boundary:** The Power-to-Heat plant as enumerated in `Das Vorhaben umfasst …`. The Fernwärmepumpstation is a linked measure OUTSIDE the boundary (ruled 2026-08-06, superseding the earlier declaration). The prospective river-water heat pump is outside.

## Identity and boundary

- **Canonical name:** Power-to-Heat-Anlage am Heizkraftwerk Berlin-Mitte
- **Existing HKW Mitte site address:** Köpenicker Straße 60, 10179 Berlin — read from the Störfall PDF for the existing installation; the Power-to-Heat project's own address was not independently stated
- **Bezirk:** **not found.** The Störfall PDF says `In Berlin-Mitte`, which
  carries the same Ortsteil/Bezirk ambiguity as C-014's `Berlin-Moabit`. Unlike
  C-014, no source encountered names a Bezirk as such. Not inferred.
- **Category:** Utilities, energy, water, environment and climate adaptation.
- **Owner confirmation:** identity, site boundary and end wording confirmed
  2026-08-06.

### Scope — stated by source

`Das Vorhaben umfasst den Neubau eines Gebäudes für die Anlagentechnik, drei Elektrodenkessel mit jeweils 40 Megawatt thermischer Leistung, zwei Netztransformatoren (110/22 Kilovolt) sowie eine Schaltanlage.`

### Pump station — OUTSIDE the boundary, ruled 2026-08-06

**This supersedes the earlier owner declaration** recorded in
`candidate-ledger.md`, which placed the pump station inside the declared scope.
The project owner ruled on 2026-08-06 that the boundary follows the source.

The source enumerates the project and does not include the pump station:

`Das Vorhaben umfasst den Neubau eines Gebäudes für die Anlagentechnik, drei Elektrodenkessel mit jeweils 40 Megawatt thermischer Leistung, zwei Netztransformatoren (110/22 Kilovolt) sowie eine Schaltanlage.`

The pump station appears in the following sentence, marked as an addition:

`Ergänzend erneuert die BEW die bestehende Fernwärmepumpstation zur Erhöhung der hydraulischen Kapazitäten im Fernwärmenetz.`

`Ergänzend` marks addition to, not membership of, `Das Vorhaben umfasst …`, and
`erneuert … die bestehende` describes renewal of existing plant rather than
new-build.

**Recorded as:** a **linked measure**, outside the project boundary, that
shares a commissioning statement with the project. The shared statement is
retained in full and is not read as evidence of shared scope:

`Die Power-to-Heat-Anlage und die Pumpstation sollen bis Ende 2028 in Betrieb gehen.`

**Consequence.** The `bis zu 75 Millionen Euro` financing span attaches to
`der PtH-Anlage` alone, matching the source's own scope wording. No financial
measure attaches to the pump station.

**Note for the record.** The counter-evidence is real and is preserved above:
the commissioning sentence does group the two objects, and a later source could
reasonably be read as treating them as one measure. The ruling follows the
enumerated scope sentence because it is the source's own explicit statement of
what the project comprises. If a later source enumerates the pump station
inside the Vorhaben, this is a supersession, not a correction.

### Excluded — confirmed by source

`Perspektivisch ist am Standort Mitte außerdem eine Flusswasserwärmepumpe geplant.`

`perspektivisch` places it beyond current planning. Cleanly outside.

## Dated milestones

All from the single publication of 2026-05-04.

| Verbatim | Milestone | Force | Note |
| --- | --- | --- | --- |
| `Die Inbetriebnahme ist bis Ende 2028 geplant.` | `Inbetriebnahme` | `bis` upper bound + `geplant` | Object: the plant |
| `Die Power-to-Heat-Anlage und die Pumpstation sollen bis Ende 2028 in Betrieb gehen.` | entry into operation | `bis` upper bound + `sollen` | **Weaker force, wider object** than the sentence above |
| `Inbetriebnahme bis Ende 2028` | `Inbetriebnahme` | `bis` upper bound, no verb | Header bullet |

Three framings of one date, at three forces, in one document. A flattening
extractor collapses these into a single "2028" and loses both the bound and the
distinction between what is planned and what is merely supposed to happen.

**No dated Baubeginn.** The release headline says
`geben Startschuss für Bau`, but `Startschuss` is not a dated construction-start
milestone and the publication date is not converted into one.

## Change history — NOT FOUND

**Searched and absent**, not unchecked. Sources checked:

- BEW press index and `Aktuelles` listing, including the older-releases route
- BEW Wärmewende and Fernwärmesystem sections
- 50Hertz newsroom (not reachable by scripted fetch — recorded as an access barrier)
- PARDOK, including Drucksache 19/23038 (`Wärmewende in Berlin – Fernwärme bezahlbar halten`, 2025) and 19/26369 (2026). Power-to-Heat appears only as a technology category; the HKW Mitte installation is not named with a date.
- Open web

Every source encountered traces to the single BEW press release of 2026-05-04.
No superseded date exists in public that this pass could locate.

**This is a material finding for pilot selection, recorded rather than hidden.**
Change history is the scarcest evidence in the project and the stated reason
these three pilots were chosen. C-019 currently cannot demonstrate it.

## Financial measures

### Financing commitment — primary, cleanly typed

`50Hertz finanziert den Bau der PtH-Anlage mit bis zu 75 Millionen Euro.`

- Amount: 75,000,000 EUR
- Qualifier: **`bis zu` — upper bound**, not a point estimate
- Measure type: third-party financing commitment for construction. **Not** a
  project total cost, not a budget, not an awarded contract value.
- Scope: `der PtH-Anlage` only. The pump station is not stated as covered.
- Tax treatment, price basis, as-of date: none stated.

Related, and **not** a financial measure:

`Nach fünf Betriebsjahren haben sich die Investitionen amortisiert.`

`Die BEW übernimmt den Bau, 50Hertz maßgeblich die Finanzierung.`

## Observed organizations and role hold

**No role is assigned.** Role assignment remains blocked pending the role ADR.

| Organization | Source wording |
| --- | --- |
| BEW Berliner Energie und Wärme | `Bauherr und Betreiber der Anlage ist die BEW` — the least ambiguous Bauherr statement across all three pilots. Full name from the Störfall PDF: `BEW Berliner Energie und Wärme GmbH` |
| 50Hertz | `50Hertz finanziert den Bau der PtH-Anlage mit bis zu 75 Millionen Euro.`; `50Hertz erhält im Rahmen eines gemeinsamen Redispatch-Vertrages über einen Zeitraum von fünf Jahren vollen Zugriff auf die Steuerung.` |
| Stromnetz Berlin | `Der Netzanschluss erfolgt über das Hochspannungsnetz von Stromnetz Berlin.` |

**The release quotes two named executives. Those spans are excluded under the
naming rule.**

## Source registry

Retrieval date for all: 2026-08-06. SHA-256 over raw response bytes.

| URL | Publication date | SHA-256 | Access / label |
| --- | --- | --- | --- |
| `https://www.bew.berlin/aktuelles-und-presse/2026/120-megawatt-am-heizkraftwerk-berlin-mitte/` | `Pressemitteilung • 04.05.2026` | `46fab695ac84c6767ab8bce2b25711b6c14d8858fef48d71ae40631530db5ba0` | Primary under ADR-010 |
| `https://www.bew.berlin/binaries/content/assets/website/erzeugungsanlagen/information-der-offentlichkeit-storfallv---hkw-mitte.pdf` | `zuletzt geändert 08.05.2026` | `d81289a0c76cc25f304f495b36bc4813f24394392420620e58ad3e40251ad1ff` | Primary. **Extraction unreliable — see below** |

### ⚠ Extraction reliability warning

The Störfall PDF was extracted without a proper PDF parser during this pass;
the resulting text has mangled inter-character spacing. The address reading —
that the BEW operates the Heizkraftwerk Mitte at Köpenicker Straße 60, 10179
Berlin — is sound, but **no span from this PDF is byte-reliable and none should
be used for string comparison until re-extracted with a real parser.**

Note also that this PDF documents the **existing** HKW Mitte site under the
Störfall regime. It is not a document about the Power-to-Heat project, and the
PtH installation's own address is nowhere independently stated.

### Access barriers

- 50Hertz newsroom not reachable by scripted fetch. 50Hertz is the financing
  party and its own wording on the 75-million figure would be primary for that
  claim. Worth one manual or browser-tool attempt.

## Still open

1. **Bezirk** from a source that names one.
2. **50Hertz's own release** for primary wording on the financing figure.
3. **Re-extraction** of the Störfall PDF spans with a real parser.
4. **Any pre-2026 publication** — would transform this pilot's value.

*(The pump-station scope question was ruled on 2026-08-06 and is closed. See
the boundary section.)*

## Pilot-selection note

C-019 was retained on the reviewer's recommendation and the owner's decision as
the **modal-and-financial-typing case, not the change-history case.** Recorded
explicitly so that its thin history is not later read as a research failure.

What it uniquely exercises:

- `bis zu` as a bound on a **sum**, distinct from `bis` on a date
- one date at three modal forces in one document
- a third-party financing commitment that is cleanly not a project cost
- the only unambiguous `Bauherr` statement in the pilot set
- a scope boundary where the source's own framing (`Ergänzend`) tensions
  against the owner's declared boundary

What it cannot exercise: supersession, delay display, or any change-history
feature.
