# 150-candidate construction research batch

**Checked:** 9 September 2026. **Status:** Research records, not publication approvals.

[Individual cited records](records.md) · [Compact register](register.md) ·
[Machine-readable catalog](catalog.json) · [Blank review sheet](review.csv)

## Result

The official [meinBerlin plan register](https://mein.berlin.de/api/plans/) returned
1,230 records. A deterministic title/location filter selected 150 construction-related
candidate records. All 150 canonical titles match the heading of the corresponding
official project page. All 150 have official register navigation coordinates and a
short German scope excerpt from that individual page. All twelve boroughs occur.

This is **not** 150 complete dossiers, 150 independently verified construction
sites, or a claim that 150 projects are currently under construction. Register
workflow status is not construction progress. Points may represent a route,
campus or project reference rather than the precise construction footprint.

| Proposed category | Records |
| --- | ---: |
| Public space | 53 |
| Education | 30 |
| Civic / sport | 27 |
| Transport | 26 |
| Energy | 11 |
| Housing | 2 |
| Category needs scope review | 1 |
| **Total** | **150** |

Categories are explicit lexical rules over source titles, recorded with the word
that triggered each proposal. They are not independent German-language judgments
or approved glossary values. The source's own topic codes are preserved separately.
The low housing count reflects this inventory/filter, not Berlin-wide housing
activity; additional housing-company inventories are retained for the next batch.

## Evidence per record

Each record has its source URL, original German title, short source excerpt and
selector, source-modification timestamp, district, original location label, supplied
coordinates, JSON pointers into the frozen inventory, and SHA-256 references to
retained inventory and page artifacts. Retrieval times and HTTP attempts are logged.
Full source responses remain only in ignored `data/artifacts/`.

The catalog exports no contacts, images, normalized financial or date claims or
construction-status verdicts. The 25-word descriptions are unreviewed source excerpts,
not agent-written summaries. Titles and excerpts were mechanically matched, which
establishes text correspondence—not semantic validity or model accuracy.

## Selection, exclusions and duplicate checks

Selection preserves inventory order with a 150-record batch cap. It is not a random
or representative sample. Required: explicit construction-related title term, valid
canonical project URL, non-archived register code, district other than citywide, and
a source Point within the broad Berlin review extent. That extent check is not
point-in-polygon validation or a project-footprint check.

Dispositions for all 1,230 inputs are retained in the catalog: 576 lacked the chosen
work-title terms; 454 were archived by the register; 15 lacked usable locations ;
3 were guidance/study records; 7 were participation/art processes; 1 matched existing
pilot C-010; 2 were citywide programmes; 2 broad-area programmes; 20 were reserve
candidates after the cap. Counts reconcile with 150 selected. Disposition order
means an entry is counted under its first failing criterion.

Canonical URLs are deduplicated. Identical coordinates and title similarity >= 0.90
produce review flags, not automatic merges. Two similarity pairs were flagged:
Ilsestraße/Weserstraße and Weserstraße/Oderstraße. Inspection of their source
location labels shows distinct named streets and different coordinates; retained
as separate proposals. This does not prove all parent/phase relationships resolved.

The selection is geographically uneven: Reinickendorf 33, Tempelhof-Schöneberg 26,
Mitte 23, Neukölln 21, Friedrichshain-Kreuzberg 12, Spandau 12, Pankow 8,
Steglitz-Zehlendorf 7, Marzahn-Hellersdorf 4, Treptow-Köpenick 2,
Charlottenburg-Wilmersdorf 1 and Lichtenberg 1.

## Further inventories independently retrieved

See [inventory evidence](supplemental-inventories.json). These are expansion sources,
not additional projects included in the 150 count:

- [Senate school construction XLSX](https://www.berlin.de/sen/bildung/service/daten/schulbaumassnahmen-2026.xlsx): 370 named measure rows; 124 have source handover-period prefixes 2026 or later. A school-year field is not evidence of current activity. Different measures at one school must retain separate scopes.
- [Senate bridge inventory](https://www.berlin.de/sen/uvk/mobilitaet-und-verkehr/infrastruktur/brueckenbau/): 36 marker sites linked to 31 distinct dossier URLs. Shared project pages must not be counted as separate projects merely because multiple components have pins.
- [BVG project catalogue](https://bvg-projekt.de/projekte/), [HOWOGE](https://www.howoge.de/immobiliensuche/neubauprojekte), [Gewobag](https://www.gewobag.de/bauen-in-berlin/bauprojekte/) and [STADT UND LAND](https://stadtundland.de/bauen/neubau): independently retrieved with HTTP 200 and retained hashes. These mix planning, construction and/or completed/rental stages; section-level imports remain follow-up. No secondary coordinates have been invented.

## Reproduce

```sh
.venv/bin/python -m pipeline.bulk_discovery --fetch-inventory --limit 150 --verify-pages
```

This fetches the official inventory and at most two concurrent individual pages.
It makes no model-provider calls. Current results can change with source updates.
For the frozen batch, use its retained inventory and page artifacts:

```sh
.venv/bin/python -m pipeline.bulk_discovery \
  --inventory data/artifacts/a66f6886b33fd0379e3e62942ec346d68f1b70bd058f8c3440e136ac06f126cb.json \
  --page-cache docs/research/findings/2026-09-09-bulk-discovery/catalog.json \
  --output-dir build/reproduced-bulk-catalog
```

The second command hashes retained page bytes and rechecks headings/excerpts.
A clone without private artifacts must use live retrieval; missing artifacts do
not become passed checks. Reports write to the specified directory; the internal
map preview is generated in ignored `build/bulk-research/`. No part is automatically
added to the public website. Recorded elapsed time in the current catalog is the
retained-artifact recheck, not a live-network performance benchmark.

## Portfolio value and remaining gates

This demonstrates reproducible acquisition, traceable field-level citations,
explicit exclusions, location provenance, repeatable checks and a review queue.
It does not establish extraction accuracy, citizen impact or human-review savings.
No paid AI extraction calls, scheduler or new golden reference values were created.

Before smaller basic-listing pins enter the public atlas, review project identity,
category and geographic scope, supply correction routes, and apply actual publication
decisions. Full-dossier pins remain a separate research-depth class. Start with a
reviewable batch rather than treating successful bulk retrieval as blanket approval.
