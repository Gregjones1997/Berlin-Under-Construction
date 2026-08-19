# Public evidence context

This repository turns frozen, source-backed Berlin construction research into a deliberately smaller public display dataset. These terms keep review authority and public-data boundaries explicit.

## Language

**Public projection**:
The sole committed project-data input allowed into the public site build; it contains only publication-safe display records.
_Avoid_: Public database, export of the private store

**Published fact**:
A factual display record whose exact payload is bound to an accepted owner review decision and to exact German evidence at an HTTPS source.
_Avoid_: Approved claim, verified by the agent

**Withheld fact**:
A public-state marker containing only a stable fact identifier, broad fact type, `withheld` state and reason code; the withheld value and evidence are absent.
_Avoid_: Hidden fact, redacted value

**Accepted review decision**:
An append-only project-owner decision whose stable ID and subject digest authorize one exact public fact or conflict payload.
_Avoid_: Markdown reference, agent approval

**Known-withheld manifest**:
A gitignored local list of current withheld values used only to scan generated output before publication.
_Avoid_: Public denylist, committed fixture

**Boundary provenance**:
The authority, license, retrieval date, source and bundled coordinate systems, transformation and content hash that make the local Berlin boundary auditable.
_Avoid_: Map metadata
