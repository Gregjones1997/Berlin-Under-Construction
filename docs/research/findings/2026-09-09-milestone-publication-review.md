# Basic milestone publication review — 9 September 2026

The owner authorized publishing straightforward source-stated dates while holding
ambiguous facts. This release follows ADR-026; it does not claim that the owner
reviewed individual new German passages, and it changes no golden data.

## Published scope

| Listing | Published field | Basis |
| --- | --- | --- |
| Friedrich-Bergius school gym | Planned finish: 2028 | Official register schedule explicitly identifies a completion forecast; actual start is withheld. |
| Jan-Petersen-Straße housing | Planned finish: Ende 2028 | Official register, with a newer developer release supporting the same horizon. Demolition and structural work remain separate. |
| Waldemarstraße playground | Planned finish: Frühjahr 2027 | Completion forecast retained; inconsistent start accounts do not block the separate finish field. |
| Ella-Kay-Straße replacement building | Planned finish: Mitte 2027 | Fresh official register wording. The older district page could not be counted as fresh corroboration. |
| Dorfteich Lichtenrade | Reported start: Ende Januar 2025; planned end: Herbst 2026 | Explicit source statements; responsible district project page independently carries the same wording/periods. |

Every public value is a substring of its German evidence span. The compact card
uses source arrows; expansion reveals wording, source edit date and retrieval date.
Seasonal precision stays intact. No elapsed duration, exact day, delay, current
site observation or on-time assessment is derived. The map references remain the
same; basic listings are not relabeled as full dossiers.

## Source trail and held facts

The [original ledger](2026-09-09-milestone-enrichment.json) retains all six candidates
and nine original passages. The [follow-up ledger](2026-09-09-milestone-followup-sources.json)
records fresh downloads, hashes, source dates and exact-match results.

- [Dorfteich responsible district](https://www.berlin.de/ba-tempelhof-schoeneberg/politik-und-verwaltung/aemter/strassen-und-gruenflaechenamt/aktuelles/projekte/artikel.1585456.php): same start and end periods. The project phase update is dated 26 November 2025, distinct from today's retrieval.
- [Waldemarstraße authority archive](https://www.berlin.de/ba-friedrichshain-kreuzberg/politik-und-verwaltung/aemter/strassen-und-gruenflaechenamt/artikel.1236256.php): February and April 2026 entries describe commencement differently. The start stays held; do not silently treat the later entry as a correction.
- [School gym Senate release](https://www.berlin.de/rbmskzl/aktuelles/pressemitteilungen/2026/pressemitteilung.1682290.php): June 2026 planning/approval context does not prove construction commencement. The register explicitly describes the gym at Lauterstraße 41 under the named school; no location correction or campus boundary is inferred.
- [German housing developer release](https://www.feldhoff-cie.de/media/pages/pressreleases/greystar-und-ten-brinke-legen-grundstein-fuer-428-mietwohnungen-in-berlin-marzahn/d190344444-1788425621/260903_fci_greystar_ten-brinke_pm-grundsteinlegung-berlin-marzahn_final_korrektur.pdf): dated 3 September 2026; demolition and following structural works are distinguished. Ceremonial groundbreaking is not substituted for actual building start. PDF retained privately after metadata stripping; page 2 passage matched with the bundled Poppler extractor. Unrelated retail figures were not accepted or published.
- [Older Ella-Kay district release](https://www.berlin.de/ba-pankow/aktuelles/pressemitteilungen/2025/pressemitteilung.1597361.php): search evidence suggested corroboration, but freshly retained HTML contained the heading/date without the expected body text. Recorded as `page_body_missing_expected_span`, not supporting evidence. The current register remains the publication source.
- Karl-Marx-Straße: the known 2024 expected schedule and reported summer-2025 completion remain together in research. Supersession and the precise affected milestone are unresolved; this release adds no date to that card.

## Publication checks

`public/data/basic-milestone-release.json` freezes the exact payload and source
ledger digests and records explicit fact exclusions. The build validates both,
checks supported project identities, rejects unknown fields and kinds, and requires
nonempty checked evidence containing every displayed value. It exports only the
six selected date fields; withheld values are not serialized to the basic cards.
Original full-dossier approval checks stay unchanged. Tests cover modified payloads,
missing spans, invented exact days, excluded projects and generated card contents.

Next: reconcile the start accounts and Karl-Marx-Straße supersession with explicit
authority updates, then review another bounded batch. Unresolved interpretation
is a targeted human review question, not a reason to relabel all 150 listings.
