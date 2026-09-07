# Visual direction study — 7 September 2026

Status: owner-authorized direction, implemented locally on 7 September 2026 (ADR-024).

The owner asked to revisit the visual experience against the original vision,
then supplied two references:

- https://marseille.laphase5.com/en
- https://seoul-3d-atlas.synabreu.chatgpt.site/

## Findings

The README and MAP-02 preserve a technical-illustration city: white forms with
black hidden-line outlines. The current landing-page screenshot and Astro source
instead lead with the project methodology and implementation summary. The map
comes after two prose sections. Its bundled assets contain a city boundary and
two point positions, not building geometry. A spatial redesign requires additional
geometry work, not only a stylesheet change.

Both owner references were inspected in the browser. Marseille uses a nearly
full-screen oblique city, peach buildings against dark blue terrain, sparse
controls and place markers. Seoul uses a pale miniature landscape, district and
landmark navigation, camera movement and a contextual place card. Selecting
Gwanghwamun changed the framing and corresponding card. Their shared strength is
making the city the main surface for discovery.

## Recommended proposal

Explore a full-screen architectural model with pale building forms, fine dark
outlines and a construction-orange selection accent. Keep navigation compact;
selection reveals a project summary alongside the city. German source wording,
completion history, unresolved evidence and correction links remain accessible.

The proposed signature interaction is dated source navigation: select a record
and inspect its supported changes. This represents changes in the evidence;
it must not imply observed construction progress or generate building phases
from dates. Geometric comparisons require separately supported geometry.

Begin with a small sourced area around C-014 and the existing dossier to judge
camera movement, line readability, selection, performance and evidence access.
Keep C-019 accessible in the list while its location remains withheld.

Two AI-generated image concepts illustrate the difference between an editorial
architectural atlas and a more immersive full-screen model. They are discussion
artifacts, not surveyed Berlin geometry or public project evidence. Generated
annotations and sample interface text are not approved publication copy.

## Accepted implementation

The owner asked to build the interactive direction, including realistic Berlin
geometry, and authorized changing the framework if useful. Astro was retained;
Three.js now renders self-hosted official building footprints and ridge heights.
Paper follows the architectural drawing concept; Ink adopts the warm-building,
dark-ground contrast admired in Marseille. Both use the same real geometry.

Chrome checks exercised Marseille drag and wheel zoom, plus Seoul's Gwanghwamun
flight and sunset setting. Smooth location transitions and restrained floating
controls were accepted. Seoul's displayed 4× height exaggeration was not adopted;
Berlin uses metric source heights. The generated image concepts remain design
references only: none of their imagined geometry or sample claims ships.

See `atlas-model.md` for scope and limitations. The map is central Berlin, not
the entire city. Project history changes the evidence panel; it does not pretend
to reconstruct historical construction geometry. The static index and dossiers
remain accessible without JavaScript. Owner visual acceptance remains open.

Participants/tools: main agent (Codex), design-consultation skill, imagegen skill
and built-in image generation for concepts; Browser skill and web research in
the initial study, Chrome skill for subsequent reference interaction and visual
verification. The owner then specified Chrome-only web work and later allowed
public-geodata command-line downloads. No delegated agents or deployment.
