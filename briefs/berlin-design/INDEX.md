# Berlin / personal design handoff

**Recommended and implemented locally: City Desk.** It preserves the large geographic
model while making the coverage and route to a full dossier easier to read. This is
an agent recommendation, not an owner-selected identity or a production release.

- [Proposal comparison](http://127.0.0.1:48767/) · [saved viewer](index.html)
- [Working atlas](http://127.0.0.1:48766/)
- [Redesigned project index](http://127.0.0.1:48766/records/)
- [Typography and component audition](http://127.0.0.1:48767/style-guide.html)
- [Project brief and recovered context](PROJECT.md)
- [Research recommendation and sources](RESEARCH.md)
- [Brand proposal and Lumos mapping](BRAND.md)
- [Three proposals and tradeoffs](proposals/COMPARISON.md)
- [Verification record](VERIFICATION.md)

## What changed

Original building-grid wordmark; shared native design tokens; compact atlas introduction;
visible dossier/listing counts with a mobile index link; dossier-first static index with
larger links and adjacent attributed boundary map; improved document heading hierarchy.
Technical background remains available in a native disclosure below the records.
The renderer, evidence data, publication decisions and original portfolio package are
unchanged. No external runtime assets or new client JavaScript were added.

## Rendered evidence

[Desktop atlas](assets/atlas-desktop.jpg) · [Mobile atlas](assets/atlas-mobile.jpg) ·
[Desktop index](assets/index-desktop.jpg) · [Mobile index](assets/index-mobile.jpg) ·
[Keyboard-open evidence](assets/evidence-mobile.jpg)

[City Desk](assets/proposal-city-desk.jpg) · [City Edition](assets/proposal-city-edition.jpg) ·
[Field Instrument](assets/proposal-field-instrument.jpg)

## Limits and restart

Local-only. The legal page deliberately says “Local design preview — not for publication”
because the production address is not present in this shell. Supply the existing valid
production configuration before packaging or deploying; this work does not change it.
The public release and existing portfolio screenshots remain the previous design.
Proposals are static composition studies using a real existing product screenshot;
the selected Astro implementation is the functioning atlas.

The terminal servers serve only web/dist and this handoff directory, bound to loopback.
To restart after they stop, build with PUBLICATION_AS_OF_DATE=2026-09-21 and the appropriate
LEGAL_ADDRESS environment value, then run `python3 -m http.server 48766 --bind 127.0.0.1
--directory web/dist` and `python3 -m http.server 48767 --bind 127.0.0.1 --directory
briefs/berlin-design` from the repository root. No private source artifacts are served.
