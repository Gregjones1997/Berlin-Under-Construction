# Project selection: design study

9 September 2026. Proposal, not an accepted redesign or production implementation.
Open `project-selection-study.html` for the interactive comparison. The local served
copy is at http://127.0.0.1:48762 while its preview server runs.

## Brief

First action: choose a construction project in the atlas. The interface should
connect its place to one useful source-backed statement and offer a clear path to
its evidence. The owner likes the city but remains unsure of the small record card.
Repeatedly simplifying its contents has not resolved the choice of interaction.
The governing proposal is: the map invites discovery; the reading surface explains.

Material: actual self-hosted Berlin geometry, two approved positions, three frozen
project records, exact German wording and existing evidence pages. Missing actual
start/current progress facts cannot be supplied by a new layout. Unknowns remain
available and stale milestones retain required warnings in any implementation.

## Observations and alternatives

Observed in this session: selection moves the map and opens a floating side card;
source history expands to a full-width record; explicit back navigation restores
context. The owner accepted much of the map treatment but questioned the card.
The historical `../visual-direction-study.md` and the design-with-depth Berlin case
study describe earlier Marseille/Seoul reference work. Those references were not
freshly browsed for this consultation; their historical observations provide context,
not evidence of present behavior.

| Need / observation | Proposal | Intended effect (hypothesis) | Tradeoff | Check |
| --- | --- | --- | --- | --- |
| The city is the strongest visual material | Bottom strip with name, one milestone and one reading action | Connect selection and explanation without a side-card detour | Uses vertical map space | Select, read, return |
| Some visitors want uninterrupted exploration | Minimal map label opens reading sheet directly | Maximize visible city | Another click before seeing the milestone | Label to sheet, return |
| Others arrive to investigate records | Permanent split map/story view | Make reading predictable | Smaller map and less immersive first view | Switch selection, read evidence |

Recommendation to test first: bottom strip. The prototype implements all three
presentation choices and opening/closing a reading sheet. The map is a static
screenshot backdrop, visually framed with CSS; it does not implement geography
interaction or demonstrate a performance improvement. C-014 wording comes from
the existing accepted record. The full dossier remains linked.

## Palette meaning

- Public space: moss `#58755b`.
- School: ochre `#ae792f`.
- Energy: teal `#377b83`.
- Existing orange: selection and primary interaction only.

Colors indicate project type, never completion, delay or evidence approval. Use
icons and labels alongside color. These are proposed tokens, not changes to the
public atlas. This study is not a contrast/accessibility certification.

## Verification and next decision

Browser exercised the three alternatives, bottom-strip and label entry to the
reading sheet, and return controls. Desktop screenshot inspected. Reduced-motion
styles are included; mobile composition and real-map integration remain untested.
Choose the selection model before replacing production components. If accepted,
implement one complete selection → reading → return journey in Astro, keeping
existing approved facts, correction routes, withheld/conflict treatment and no
external runtime requests. No stack or legal decision is changed by this study.
