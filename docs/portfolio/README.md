# Portfolio handoff — Berlin, Under Construction

**READY AS CASE STUDY** — prepared for the 21 September 2026, 17:00
Europe/Berlin portfolio launch; handoff due by 15:00. Ready to integrate into a
personal portfolio; this package has not been installed on a separate portfolio
website.

**Public URL:** [Berlin, Under Construction](https://berlin-under-construction.vercel.app/)

**Published source revision:** `57c1e68d492d891dc57d3dd8f044f56521619cc2`
(9 September release). Verification date: **21 September 2026**; exact check
timestamps and the separate tested repository revision are in `verification.json`.

## Use these files

- `case-study.md`: finished first-person case study. Preserve the distinction between the owner's role and AI implementation assistance.
- `project-card.json`: concise title, summary, tags, calls to action and image alt text for a portfolio grid or CMS.
- `assets/atlas-desktop.jpg`: lead image, captured from the live site.
- `assets/project-card-desktop.jpg`: supporting desktop image showing a reviewed dossier card.
- `assets/milestone-mobile.jpg`: supporting mobile image showing source-linked dates.
- `assets/evidence-mobile.jpg`: optional mobile detail with the original source wording expanded.
- `walkthrough.md`: 80-second narration and click sequence for a live demo or recording.
- `verification.json`: dated engineering and public-release check scope.

All four screenshots are original JPEG captures from 21 September, inspected
after correcting their extensions. Desktop files are 1280 × 720; mobile files
are 390 × 844. No pixels were changed. The evidence detail is a viewport capture:
its internal panel continues below the visible area; use the live page to read
the full evidence. The desktop card likewise continues below its visible area.

## Suggested placement

Feature the project near the top of the portfolio. Use the desktop atlas as the
lead image; keep the project title and one-sentence summary outside the image.
On the case-study page, put the live demo and code links near the title. Pair the
mobile card with the paragraph about keeping the first view useful. Use the
expanded evidence image beside the discussion of traceability.

Do not crop away source context from evidence screenshots. The map attribution
is visible in the supplied captures; preserve it when using the full atlas image.
Use image alt text from `project-card.json`; give the live-demo button a descriptive
label. Preserve headings as real text rather than baking them into images.

## Suggested project-card copy

**Title:** Berlin, Under Construction

**Subtitle:** Making Berlin’s construction projects easier to understand

**Summary:** An independent Berlin construction atlas connecting three reviewed dossiers and 150 basic register listings to original sources. I led product direction, visual design and publication decisions, with AI assisting research and implementation. The prototype keeps conflicting dates, withheld facts and unverified German terminology visible; architectural geometry does not establish construction progress.

**Role:** Product direction, visual design and research workflow; built with AI agents.

**Status:** Working proof of concept

**Tags:** Applied AI · Civic technology · Evidence design · Geospatial UX

**Primary button:** Explore the atlas

**Secondary button:** Read the case study

**Code button:** View code — link to `phase-4-public-slice`, where this work lives.

## Editorial guardrails

150 basic listings are not 150 fully verified dossiers. Three full dossiers exist;
two have map positions. Five additional basic listings have six published date
fields. No accuracy score, adoption figure, time-saving percentage or commercial
integration has been established. The model geometry is not evidence of live
construction progress. The latest browser checks used a simulated mobile viewport,
not a physical phone. Source statements have their own dates; checking the site on
September 21 did not refresh every construction source.

Do not claim that the owner hand-coded the full system or that AI verified its own
ground truth. Keep the business translation-review idea clearly marked as a future
application. Preserve links to the repository method and build log for scrutiny.

## Verification and delivery

The demo was checked against its published September 9 build. This handoff includes
a September 21 repository dependency patch; no new production deployment was made.
Today's existing 207-test and TypeScript record is reused: application, pipeline,
test and dependency files are unchanged since tested revision
`2a1e6f33ebf0f6e4ec0a97a98abf4cf93dc665d3`. This pass changes handoff documents
and image filenames only. New checks cover JPEG signatures/dimensions, unchanged
image bytes, local references, copy lengths and live navigation. npm reported
zero known vulnerabilities at the earlier dependency check. These checks do not establish production security
or independent extraction accuracy. See `verification.json` for the narrow
credential-pattern and live HTTP checks.

Before final portfolio publication, confirm the three buttons resolve from the
portfolio and inspect its own desktop/mobile layout. No new approval of the three
original dossiers is needed simply to integrate this case study. Independent
German glossary review and the human-authored golden evaluation set remain
unfinished. No product expansion or deployment is needed for this handoff.
