# C-014 — Europaplatz Süd — Umgestaltung

**Dossier status:** First verified dossier evidence recorded  
**Owner confirmation:** 2026-08-06  
**Evidence boundary:** Europaplatz Süd only; adjacent S21 and high-rise works are excluded.

## Identity and boundary

- **Canonical name:** Europaplatz Süd — Umgestaltung
- **Alias:** `Entrée Berlin`
- **Location:** Europaplatz before Hauptbahnhof, Berlin-Moabit; the Bezirk remains open for confirmation.
- **Category:** Schools, public buildings, cultural facilities and public space.
- **Boundary:** The project is the southern forecourt redesign described by the official sources. The complete Bahnhofsumfeld, S21 works and high-rise works are not part of C-014.
- **Owner confirmation:** The project owner confirmed the identity, boundary and cited German wording directly against the original sources on 2026-08-06.

## Verified evidence

### Superseded completion target

**Evidence label:** Primary

**Source:** Senatsverwaltung für Stadtentwicklung, Bauen und Wohnen press release, published 2023-10-12. [Official press release](https://www.berlin.de/sen/stadt/presse/pressemeldungen/pressemitteilung.1374721.php)

**Verbatim span:** `Die Fertigstellung der anspruchsvollen Bauaufgabe ist bis Ende 2025 vorgesehen.`

- **Milestone:** `Fertigstellung`
- **Qualifiers:** `bis` is an upper bound; `vorgesehen` is weaker than `geplant`.
- **Interpretation:** This is a historical expected completion target, not a claim that completion occurred in 2025.

The same release states: `Vorgesehen ist, die Planungen bis Sommer 2024 abzuschließen und anschließend mit der baulichen Umsetzung zu beginnen.` The competition jury decided on 2023-10-11 and recommended the winning design by Rehwaldt Landschaftsarchitekten, Dresden. The release contains no cost figure.

### Current completion field

**Evidence label:** Primary

**Source:** [Senate project page](https://www.berlin.de/sen/bauen/baukultur/berliner-plaetzeprogramm/europaplatz-sued-1567894.php)

**Verbatim field:** `Fertigstellung: 2026`

- **Milestone:** `Fertigstellung`
- **Source date:** Not stated on the page.
- **As-of date:** Owner confirmation on 2026-08-06.
- **Interpretation:** The 2023 hedged upper bound and the current unmodalised page field are recorded as a supersession pair, not as a correction.

### Change-history pair

| As at | Wording | Source | Evidence label |
|---|---|---|---|
| 2023-10-12 | `Die Fertigstellung der anspruchsvollen Bauaufgabe ist bis Ende 2025 vorgesehen.` | Senate press release | Primary |
| Current page, confirmed 2026-08-06 | `Fertigstellung: 2026` | Senate project page | Primary |

The record structure currently stores both spans but does not provide a typed historical-milestone object that separately captures source date, as-of date, modal qualifier and supersession relation. This is a Phase 2 schema finding, not a reason to flatten either statement.

## Secondary sources — reported leads only

These sources are not evidence spans for dates. Their own chain is `wie die Berliner Senatsverwaltung laut einem Tagesspiegel-Bericht mitgeteilt hat`, so the claims are two removes from the authority.

### 2025-06-11

[Entwicklungsstadt: Hauptbahnhof-Vorplatz-Umgestaltung beginnt Ende 2025](https://www.entwicklungsstadt.de/hauptbahnhof-vorplatz-umgestaltung-beginnt-ende-2025-wohin-mit-den-taxis/)

Reported wording: `der Baubeginn ist für November dieses Jahres vorgesehen`.

**Evidence label:** Reported. The underlying Senate wording must still be located.

### 2025-11-24

[Entwicklungsstadt: Europaplatz Süd — Umbau am Hauptbahnhof startet 2026](https://www.entwicklungsstadt.de/das-sind-die-plaene-fuer-den-europaplatz-umbau-am-hauptbahnhof-startet-2026/)

Reported wording: `Der Baubeginn ist zwischen Januar und Sommer 2026 vorgesehen`.

**Evidence label:** Reported. The underlying Senate wording must still be located.

Together with the official 2023 planning statement, these form a three-point reported/primary Baubeginn chain: after summer 2024 → November 2025 → January–summer 2026. Only the first point is officially sourced. The two later points require Senate wording before they can become primary evidence.

### Excluded scope trap

The 2025 secondary article says: `sich die vollständige Neugestaltung des gesamten Bahnhofsumfelds bis Ende der 2020er-Jahre hinziehen dürfte`. This is excluded from C-014: it concerns the whole Bahnhofsumfeld, not Europaplatz Süd, and `dürfte` is author speculation. It must not be recorded as a C-014 date.

## Observed organizations and role hold

The primary release names or mentions Land Berlin, Deutsche Bahn AG, Berliner Feuerwehr, BVG, SenMVKU, SenSBW and Rehwaldt Landschaftsarchitekten. They are recorded here as observed organizations with source spans. No commissioner, financer or contractor role is assigned. Role assignment is blocked pending the ADR expanding the role vocabulary.

## Source registry capture

Retrieval date for all four pages: 2026-08-06.

| URL | Publication date | Content hash (SHA-256) | Access |
|---|---|---|---|
| https://www.berlin.de/sen/stadt/presse/pressemeldungen/pressemitteilung.1374721.php | 2023-10-12 | `6f341678a9ec8240f29a8d6f93091c0cadd1f5e4cc8b90acc54c3805a2cdeab5` | Loaded |
| https://www.berlin.de/sen/bauen/baukultur/berliner-plaetzeprogramm/europaplatz-sued-1567894.php | Not stated | `0001a38974e2a12637faa1c0642a5eb94983fd8d067d1a3cf7711eca50657920` | Loaded |
| https://www.entwicklungsstadt.de/hauptbahnhof-vorplatz-umgestaltung-beginnt-ende-2025-wohin-mit-den-taxis/ | 2025-06-11 | `a462dffe9e8696dffb31618cb6853f19b1fe1be224782aeb8fe2a38aad2704f7` | Loaded; Reported only |
| https://www.entwicklungsstadt.de/das-sind-die-plaene-fuer-den-europaplatz-umbau-am-hauptbahnhof-startet-2026/ | 2025-11-24 | `8e20cceebe6db0167703f957a0f6c37ef6276c8dd2de4646ce6584ed7b2155e2` | Loaded; Reported only |

## Still open

- Current status in August 2026; the nominal current field is 2026.
- Whether the current 2026 date exists as an official sentence anywhere or only as a page field.
- Commissioner role from a source that states it.
- Boundary precision where C-014 ends and the S21/high-rise works begin.
- Bezirk: the source says Berlin-Moabit, an Ortsteil; confirm the Bezirk rather than inheriting the inference.
- Senate wording for the two later reported Baubeginn points.
