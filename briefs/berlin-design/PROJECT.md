# Berlin design brief

21 September 2026 · agent-authored brief for the owner's personal-design request.

## Project and scope proposal

Existing civic product redesign, not a personal portfolio or company sales page.
Primary job: find a Berlin construction record and follow the evidence behind it.
Deliver three composition proposals, recommend one, implement it locally in Astro,
and verify the retained atlas → dossier → source journey. Keep the live release
and its portfolio package separate from this local design candidate.

## Audience and material

Primary audience hypothesis: residents curious about a place or project. Secondary:
readers and technical reviewers who need to inspect sources and uncertainty.
There has been no new audience study. Available material is stronger than stock
imagery: the working architectural atlas, three dossiers, 150 basic register
listings, six already-released date fields, local geometry and static evidence.
The model is not current construction progress. No accuracy or time-saving claim.

## Preserve

Name, geographic subject, German canonical values, all source and correction links,
conflict containment, withheld reasons, existing release gates and immutable data.
Astro, the current Three.js atlas and static JavaScript-free evidence pages remain.
ADR-024 supersedes the older no-JavaScript rule for the atlas only. No third-party
runtime requests; no new assets or data publication. No golden values are authored.
No shared portfolio edits and no external deployment.

## Recovered context

- “Build a personalized design agent”, task 01a0c409-7174-73a1-bb65-99f5ed388f58:
  owner wanted autonomous finished handoffs, project-first branding, real commissioned
  references, free-font research and alternatives that differ beyond palette. Expression
  was selected for the Forma study only; it is not Berlin's selected direction.
- “Fix portfolio handoff assets”, task 01a0c3ef-13a8-78f1-ae37-d0228ea3ef4d:
  owner affirmed their prior verification; no repeated approval required. Keep three
  dossiers distinct from 150 listings; do not expand the dataset or edit the shared portfolio.
- “Project manager September 9”, task 01a08556-58e7-75d0-b596-52f16b69ca5a:
  retrieved recent local-preview and bounded milestone-release context. Recent empty
  turn items could not be read as messages. Repository ADRs provide the durable decisions.
- README, project checklist, decision log ADR-024–026, portfolio handoff and current source.

Only these relevant accessible tasks were inspected. Earlier agent recommendations
are not owner decisions. The September 21 request authorizes a local design handoff,
not publication. The archived August sprint gate restriction has expired.

## Consequential choices

| Item | Status | Reason / consequence |
| --- | --- | --- |
| City Desk | Agent recommendation | Strong map plus readable evidence entry; owner has not selected it |
| System typography | Implementation choice | No font download, predictable local loading; platform glyph differences remain |
| Mobile coverage link | Implementation choice | Existing phone view hid desktop introduction; now the index has a visible entry |
| Index leads with dossiers | Audience hypothesis | Replaces implementation exposition with the reader's task |
| Motion | Existing approved behavior retained | Selection/orbit already demonstrate geography; no decorative loading delay added |

## Completion criteria

Working local atlas and static index, three distinct rendered proposal pages,
linked research and brand records, type audition/style guide, desktop/mobile and
keyboard evidence plus build/type/safety checks. Deployment remains a later action.
