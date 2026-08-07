# Phase 2 review findings — 2026-08-07

These findings are deliberately separate from the frozen pilot dossiers. They
must not change a dossier claim, span, type, qualifier or status while the
German-speaking review is out.

## C-014 URL alias finding

The dossier describes the two Senate paths for one press release as the first
concrete instance of content-hash deduplication. The 2026-08-07 review found
that the `/sen/sbw/` request resolves with an effective `/sen/stadt/` URL after
redirect following. The existing retrieval fields `request_url` and `final_url`
capture that relationship directly.

**Disposition:** the source-identity requirement remains: equality of
`stored_content_hash` triggers source merging, while URL fields are descriptive.
However, this pilot case demonstrates redirect/alias handling, not necessarily
independent same-content documents at two stable URLs. Do not edit the dossier;
adjudicate the framing after the German review returns.
