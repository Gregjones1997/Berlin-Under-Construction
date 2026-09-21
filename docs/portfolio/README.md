# Portfolio handoff — Berlin, Under Construction

Prepared 21 September 2026. Ready to integrate into a personal portfolio; this
package has not been installed on a separate portfolio website.

## Use these files

- `case-study.md`: finished first-person case study. Preserve the distinction between the owner's role and AI implementation assistance.
- `project-card.json`: concise title, summary, tags, calls to action and image alt text for a portfolio grid or CMS.
- `assets/atlas-desktop.png`: lead image, captured from the live site.
- `assets/project-card-desktop.png`: supporting desktop image showing a reviewed dossier card.
- `assets/milestone-mobile.png`: supporting mobile image showing source-linked dates.
- `assets/evidence-mobile.png`: optional mobile detail with the original source wording expanded.
- `verification.json`: dated engineering and public-release check scope.

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

**Summary:** An AI-assisted city atlas that connects Berlin construction projects
to original sources, keeping planned dates, reported progress and uncertainty
clearly separated.

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
207 tests and TypeScript checks passed after the patch; npm reported zero known
vulnerabilities at that check. These checks do not establish production security
or independent extraction accuracy. See `verification.json` for the narrow
credential-pattern and live HTTP checks.

Before final portfolio publication, confirm the three buttons resolve from the
portfolio and inspect its own desktop/mobile layout. No new approval of the three
original dossiers is needed simply to integrate this case study.
