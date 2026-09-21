# City Desk — agent-selected brand direction

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
