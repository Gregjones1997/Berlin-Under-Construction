# Berlin precedent: from a static map to an architectural atlas

This is a reconstruction of the recorded 7 September 2026 design work. It provides
specific decisions and their limits, not a recipe that every product should copy.
The causal explanations below are design rationale unless explicitly identified
as observed behavior or measured output.

## Brief and research

The owner wanted a striking AI product engineering portfolio piece while retaining
an independent, source-backed construction map. The starting product led with
methodology and implementation prose. Its geographic assets were a city boundary
and two published project positions. Realistic spatial depth required new geometry.

The owner supplied two references:

- [Marseille](https://marseille.laphase5.com/en): a dominant oblique city, warm
  buildings against dark terrain, sparse controls and place markers. The recorded
  browser study exercised dragging and wheel zoom.
- [Seoul 3D Atlas](https://seoul-3d-atlas.synabreu.chatgpt.site/): a pale miniature
  landscape, place navigation and a contextual card. The study exercised a
  Gwanghwamun selection/camera flight and a sunset setting. The displayed 4× height
  exaggeration was observed and deliberately left out of the Berlin depiction.

The transferable observation was that the city itself could become the surface
for discovery. Two generated image concepts helped discuss direction; their
imagined geometry and sample claims were not shipped as factual content.

## Decisions and causal reasoning

| Choice | Mechanism and intended effect | Evidence and qualification |
| --- | --- | --- |
| Lead with the city | Give exploration priority over introductory prose | The implemented opening view is the map; faster comprehension was not measured |
| Real footprints and source heights | Let street patterns, scale and recognizable massing supply visual richness | Official numeric geometry was compiled and checked; it remains a simplified 2022 depiction |
| Paper styling | Pale forms, fine dark edges and quiet terrain establish an architectural drawing hierarchy | The owner accepted the visual direction; no readability study was performed |
| Ink styling | Warm buildings against a dark ground change contrast while preserving geography and interaction | Browser checks exercised both modes; this is an alternate palette, not different data |
| Restrained accent | Concentrate orange on selection and active controls | Screenshots show the hierarchy; the color alone does not certify a claim's status |
| Camera flight plus record panel | Relate a selected place to the explanation beside it | Browser checks exercised selection and source history; history changes evidence, not building phases |
| Shared header and content transitions | Keep wayfinding stable while changing pages | A named-header transition initially hid the wordmark; limiting animation to main content fixed the observed bug |
| Selectable geographic labels | Let users choose orientation detail without permanently crowding the model | Category toggles were checked; geographic names and project claims remain separate |
| Overview plus streamed detail | Make wider coverage available without an upfront download of the entire model | Asset sizes were measured and live hashes checked; low-end frame rates remain unmeasured |

Depth came from several systems reinforcing one another: sourced geometry supplied
structure, visual hierarchy made it legible, selection revealed meaningful content,
and loading architecture allowed wider exploration. None of these alone accounts
for the owner's positive response, and their individual contributions were not
isolated experimentally.

## Research that made the visual feasible

Buildings came from Geoportal Berlin's Gebäudehöhen 2022 (Umweltatlas), with
EPSG:25833 geometry and source heights under dl-de/zero-2.0. OSM supplied water,
parks, forests, transport context and geographic names under ODbL. The compiler
checked pagination completeness, duplicate identifiers and packed coordinate bounds.
It retained input hashes and output provenance. Assets were self-hosted.

This enabled plausible city structure without substituting generated landmarks
or invented height data. Roofs remained flat extrusions, source gaps remained gaps,
and terrain, road widths and bridge elevations were explicitly illustrative.

The technical choice was Astro plus a Three.js atlas, preserving static evidence
pages. The useful capability was a rich spatial entry point connected to the
existing evidence system; replacing the rest of the framework was unnecessary.

## Expansion and measured tradeoffs

| Recorded stage | Scope | Compressed geometry |
| --- | --- | --- |
| Initial central model | 84,895 building/building-part shapes | 26,252,745 bytes downloaded as one model |
| Whole-city model | 440,361 eligible shapes from 954,230 official source features | 118,236,713 bytes across the full asset set |
| Citywide entry layer | Simplified flat footprints of shapes at least 500 m², plus context | 9,025,128 bytes before nearby detail |

Detail was partitioned into 263 tiles on a 2 km grid, fetched with two requests
at a time and capped at 32 resident detail tiles. Departed GPU geometry was
disposed; stale requests were discarded before attachment. Detailed coordinates
retained 0.5 m precision. The overview used 1 m precision and simplified outlines.
An initial 17 MB overview was reduced to 9 MB by adjusting this explicit coarse
layer, without changing the detailed building geometry.

These values describe this implementation, not universal tuning defaults. The
9 MB figure is not the total initial network transfer including nearby detail,
and neither it nor the 32-tile cap proves good performance on a low-end device.
Future applications should measure against their own density and device targets.

## Failures and useful boundaries

- The first area-picker placement overlapped Paper/Ink controls. Repositioning it
  below them resolved the observed collision; desktop placement alone was insufficient.
- Whole-city fitting required adapting minimum zoom to the mobile viewport.
- Browser automation sometimes timed out. Screenshots and completed interactions
  established the resulting state; failed calls were not counted as passes.
- Only two of three project records had approved map positions. The unplaced
  record remained accessible with a withheld-location explanation. More building
  geometry did not create more project evidence. The owner's later question about
  two markers also exposed a possible expectation gap around the word “coverage.”

The final expansion recorded 184 passing tests, live matching hashes for fourteen
pages and 270 assets, and Chrome inspection of outer-city geometry. These establish
specific technical and visual checks, not an accessibility certification, extraction
accuracy score or general performance benchmark.

## Trace the original evidence

When working inside the Berlin repository, consult:

- `docs/visual-direction-study.md` for the reference study and initial proposal.
  Its initial-stage scope/status is historical; use the later records for deployment.
- `docs/atlas-model.md` and `web/site-public/atlas/provenance.json` for source and model details.
- `docs/public-deployment.md` and its linked reports for production verification.
- `docs/how-this-was-built.md` for decisions, failures and actual participant attribution.
- `docs/images/atlas-paper.png`, `docs/images/atlas-wannsee-ink.png`,
  `docs/images/atlas-citywide-overview.png` and `docs/images/atlas-spandau-live.png`
  for representative visual evidence.

Outside that repository, use this case as historical context and research the
current project's own material. Historical download and deployment permissions
belong to the original session; they are not carried by this skill.
