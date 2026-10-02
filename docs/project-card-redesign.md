# Project cards and folders — 2 October 2026

Build target: the owner's two atlas screenshots and the existing City Desk design
system. Direct implementation of the owner's content order and folder interaction.
The existing paper/map, serif project names, dark text, hairline rules and red action
accent remain. No new imagery or framework is needed.

Owner acceptance, 2 October: accepted this local version and authorized a repository
push. The owner suggested a more modern deck as a possible later refinement. This
acceptance covers the visual direction; independent translation review and physical
phone acceptance remain open.

Refero style and screen research was attempted but returned NO_SUBSCRIPTION. The
fallback uses the supplied screenshots and Refero's motion/craft references: short,
interruptible transitions, reduced-motion support, visible keyboard focus and
accessible controls. No external visual reference is claimed.

| Decision | Source and role | Purpose |
| --- | --- | --- |
| Project label → title → numeric dates → short description | Owner's requested order | Make the first glance useful |
| Remove internal dossier ID subtitle | Owner's screenshot critique | Remove repeated administrative copy |
| Summary stays visible on left as folders open on right | Owner's folder/slide proposal | Preserve project context while browsing evidence |
| Schedule, budget, sources and open questions folders | Owner's budgeting/plans/source request; actual public fact types | Group existing evidence without inventing planning records |
| Bottom translation disclosure | Owner's explicit relocation request | Preserve honest review status without repeating it on every fact |
| Existing colors and typography, compact folder tabs | Existing screenshot/system target | Maintain site continuity |
| 240 ms reveal with reduced-motion override | Refero motion craft | Show expansion without blocking navigation |
| Approved budget shown with its measure label | Existing published budget fact | Avoid implying spending or variance |
| No inferred on-time/over-budget ticker | Evidence and naming invariants | The current public facts do not support those conclusions |

Numeric dates preserve precision: exact days become numeric day/month/year; year,
month, season and bound-qualified wording remain at their source precision. Planned
handover and commissioning retain their own labels, rather than becoming project
end dates. No original quotation, public fact, golden value or glossary review state
changes. Basic listings retain their narrower source-only treatment.

The desktop workspace has a persistent summary column and one visible folder at a
time. Phones use the same summary above horizontally scrollable folder tabs and a
bounded reading area. Keyboard arrow/Home/End navigation works for the tabs. Folder
selection travels with the existing validated language-switch state.

## Verification

The 213-test Python suite and ten Node checks passed. New coverage verifies card
content order, numeric dates without invented precision, handover/commissioning
labels, folder relationships, source-conflict containment, legacy URL compatibility
and invalid folder rejection. TypeScript and the 34-route preview package passed.
The full export privacy/withheld scan passed across 305 generated files.

Browser checks: the C-014 card opened into a persistent summary plus four folders;
Budget and Sources switched content, arrow-key navigation moved focus and selection,
and switching to German retained the Sources/Budget selection. Checked desktop
1280 × 720 and simulated phone widths 390 and 320 without horizontal page overflow.
The folder tabs scroll horizontally at 320 px. A passed-date regression also
checks that an unconfirmed milestone notice appears after the planned day. A phone check caught the close control
scrolling offscreen; it is now fixed while folders are open. Desktop back/close
controls were separated and the atlas document height matches the viewport.

Screenshots live in [card-redesign-evidence](card-redesign-evidence/). Reduced-motion
CSS disables the summary/folder reveal; OS preference switching and physical-phone
acceptance were not performed. The bilingual release review gate remains closed;
this is a local draft candidate, not a production deployment.


- [Compact desktop card](card-redesign-evidence/compact-en-desktop.jpg)
- [Desktop budget folder](card-redesign-evidence/budget-en-desktop.jpg)
- [Desktop source folder](card-redesign-evidence/sources-en-desktop.jpg)
- [Compact phone card](card-redesign-evidence/compact-en-phone.jpg)
- [Phone source folder with fixed close control](card-redesign-evidence/sources-en-phone.jpg)
