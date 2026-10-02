# City Desk — agent-recommended brand direction

For people curious about a Berlin building project, Berlin, Under Construction
connects a place to the public statements behind it, helping them distinguish what
is supported, disputed and still unknown. This is a positioning hypothesis, not
validated user research or a claim of market uniqueness.

## Voice and visual behavior

| Trait | Copy | Visual / interaction | Boundary |
| --- | --- | --- | --- |
| Specific | Name the place, source and information depth | Real model, German titles, visible coverage | Never imply geometry proves progress |
| Accountable | Make missing evidence visible | Reasons stay beside withheld states; corrections remain linked | No unsupported authority or accuracy claim |
| Direct | Start with the reader's next action | Compact navigation, large dossier links | Avoid an implementation pitch before the content |

Headline: **A city in progress. A record of change.**
Explanation: Explore Berlin's construction projects and the public sources behind them.
CTA: **Read the dossier**. State: **Location withheld**.

## Design decisions

| Fact / evidence | Choice | Intended effect |
| --- | --- | --- |
| Live atlas is strongest existing media | Preserve the full geographic stage | Product is immediately visible |
| Three dossiers differ from 150 listings | Dynamic coverage strip with index link | Avoid equating all pins with full research |
| Long German titles | Strong system sans, wrapping cards | Remain readable without truncating static index |
| Existing phone layout hid introduction | Compact coverage entry on mobile | Reach records without manipulating a map |
| Earlier index led with technical explanation | Dossier navigation first; method disclosure below | Shorter path to the evidence |
| Local rendering and privacy rules | System fonts and original inline building mark | No third-party asset request |

Palette roles: paper #f6f7f4, white panels, ink #202925, secondary #536059,
rules #d7ded8, action #a83d1c. Existing map geometry colors and categorical pin
semantics are preserved. Action color is not a progress/status assertion.

## Lumos adaptation

Source date: 21 September 2026, official current typography/color/size docs linked
in RESEARCH. Astro remains the framework; no Webflow starter or Lumos package imported.

| Lumos concept | Native implementation |
| --- | --- |
| Primitive typography | font-ui, font-reading, font-reference in design-tokens.css |
| Named text styles | display/mast, section heading, body, mono eyebrow/source |
| Swatches → themes | swatch-* values → paper/panel/ink/muted/rule/accent |
| Fluid sizes and layout | space-1…4, text-display, page gutter, content-width; 700px narrow layout |
| Components and variants | header, dossier cards, atlas intro, coverage, native disclosure; inherited evidence conflict/withheld states |
| States | hover tint, visible focus outline, active navigation underline, selected record, native open/closed evidence |

Typography metrics are explicit line heights and browser-native alignment. No font
trim emulation; system-font metrics vary by OS. This is a documented production
adaptation for changed components, not full Webflow Lumos conformance or a wholesale
rewrite of the legacy atlas CSS. The rendered style guide exercises these roles.

## Media and motion

Main media is the actual self-hosted architectural model. Proposal studies use the
existing public-release screenshot, clearly labeled; no speculative construction
photo or AI-generated evidence. Source attribution remains with map presentations.
The wordmark's open building grid is original inline SVG, not a source asset.

Signature sequence: select a project → map focuses and the record opens → read overview
or expand history/evidence → return to previous view. Existing native and controller
behavior is retained; surrounding UI remains anchored. Reduced-motion rules disable
automatic orbit and page transitions. New card feedback is a 150ms surface tint only,
disabled under reduced motion. Timing is proposed tuning, not measured from references.


## 26 September production contract

The current rendered guide is `/style-guide/`, built from `web/src/pages/style-guide.astro`; the earlier static HTML is a historical proposal. `web/src/styles/design-tokens.css` is authoritative. This is a native Lumos adaptation, not imported Webflow code or a certification.

| Layer | Production contract |
| --- | --- |
| Typography | Helvetica Neue/Arial interface; Georgia/Times New Roman source context; system monospace references. Named display, heading, body, context and label roles separate family/size/leading/tracking. |
| Metrics | Weights 400/500/600/700; display leading 1.04; heading 1.16; body 1.62; label tracking .13em. Fluid display 2.25–4.5rem; heading 1.5–2.25rem. |
| Layout | Reading container 51.25rem, wide 78rem; gutter 18–32px; space-1 through space-5 from .5rem to fluid 3–7rem. Ordinary controls target 44px. |
| Surfaces | Canvas paper, nearly opaque white panels, subtle green-grey and inverse ink. Text, borders and focus consume semantic roles. |
| Action | Rust #a83d1c, hover #873116, active #6f2812. Primary controls use ink/paper. Focus stays visible; action color does not assert evidence status. |
| States | Conflict red #a5121a/pale red; withheld olive #7e6f20/pale yellow; warning #915022; selected subtle surface; disabled opacity .45 with surrounding explanation. |
| Components | Real header, record/index navigation, RawFact, evidence disclosure, selected atlas card and recovery routes. The guide shows focus, disabled, empty/withheld and recoverable error specimens; specimens are not successful production failures. |
| Media | Fresh real WebGL and static evidence captures; no generated geometry or fabricated source text. Original map attribution remains visible. |

Use hierarchy and typography to distinguish the geographic overview from the source-reading surface. Never reuse conflict red for ordinary links or show a withheld value through a component variant. Preserve native disclosure/keyboard behavior and reduced-motion CSS; this pass does not claim new reduced-motion runtime testing. Current evidence and actual limits: `docs/design-refresh-2026-09-26/HANDOFF.md`.
