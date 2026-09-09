# First milestone enrichment batch — 9 September 2026

Six existing basic listings researched using the original evidence workflow. Exact German passages, source URL, content hash, source edit date (distinct from publication date), retrieval timestamp and transport attempts are in the [machine-readable ledger](2026-09-09-milestone-enrichment.json). Full HTML remains private under `data/artifacts/`.

The ledger is research evidence, not a golden set or a public-fact approval. No milestone dates were added to the live basic cards. Seasonal expressions retain their original wording; no assumed day is substituted. On-time status is not established for any of these six projects.

| Project | Primary source | Finding and remaining scope |
| --- | --- | --- |
| Friedrich-Bergius-Schule: Neubau einer Typen-Sporthalle am Standort Perelsplatz 6-9 | [Official source](https://mein.berlin.de/vorhaben/2026-01441/) | Register schedule field; start year is not evidence of an actual start. Title and location use different street addresses; retain existing reference point only. |
| Wohnungsneubau Jan-Petersen-Straße 14 | [Official source](https://mein.berlin.de/vorhaben/2026-01347/) | Planned completion wording only; does not establish actual construction start. Demolition and new construction are distinct scopes. |
| Neugestaltung Spielplatz Waldemarstraße | [Official source](https://mein.berlin.de/vorhaben/2025-01200/) | March source is forward-looking; April passing does not verify actual commencement. Preserve seasonal wording. |
| Ersatzneubau Sport- und Funktionsgebäude Ella-Kay-Straße | [Official source](https://mein.berlin.de/vorhaben/2024-01075/) | Preserve Mitte 2027; do not manufacture an exact day. Distinguish the replacement building from the earlier sports-field works. |
| Sanierung des Dorfteichs Lichtenrade | [Official source](https://mein.berlin.de/vorhaben/2023-00823/) | Source reports actual start and anticipated end for pond and surrounding green-space works. Preserve season wording; no exact-date or on-time inference. |
| Umbau der Karl-Marx-Straße - 3. Bauabschnitt zwischen Briesestraße und Weichselstraße | [Official source](https://mein.berlin.de/vorhaben/2023-00716/) | Same page reports completion in summer 2025 while retaining an expected 2024 completion. Preserve both; scope is third street section, not all Karl-Marx-Straße. No computed delay. |

## Verification

All six pages were freshly retrieved through the existing allowlisted retrieval pipeline. All nine selected passages were exact-matched again with `pipeline.research_queue.check_source` against independently hashed retained artifacts. No model-provider extraction calls were made; no model API cost or evaluation score is claimed.

The Karl-Marx-Straße record intentionally retains incompatible-looking schedule and completion statements from the same page. A reviewer must establish supersession and scope before displaying a normalized status or calculating a delay. The school gym title and location use different street names; that is retained as a scope question, not silently corrected.

## Next pass

Follow the responsible authority’s linked progress reports for actual-start evidence and supersession. Prepare display proposals that keep expected and source-reported actual milestones separate, then apply the existing publication gate. Continue housing coverage using the retained housing-provider inventories.
