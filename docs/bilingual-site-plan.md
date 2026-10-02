# German and English public-site plan

**Date:** 2 October 2026
**Status:** Proposal following owner request; no implementation, translation
verification or deployment is claimed.

## Outcome and current position

Every visitor-facing screen supports German and English. German is the default,
with a DE / EN switch preserving page, selected project and supported atlas view
state. English can be the owner's editorial authoring language while German
remains canonical for extracted facts and evidence.

One shared implementation generates both versions. Layout, behavior and project
data change once; wording changes update linked translation pairs. Build checks
can detect missing or stale counterparts, but cannot prove semantic equivalence.

Current implementation evidence: `Base.astro` declares English and embeds shared
copy; pages and `RawFact.astro` embed English wording; `RawFact.astro` also exposes
internal enums through underscore replacement. The atlas controller and renderer
produce runtime status, loading and failure text. Glossary 1.1 and the app-linked
review pack remain explicitly unverified. The checklist already records the
9 September German-default language request.

## Shared content and editing

Use stable message IDs with paired `en` / `de` values, consumed through one
localization module for messages, localized links, explicit enum labels and
formatting. Long editorial pages use paired structured content and shared page
layouts. Thin locale route wrappers may differ; full layouts are shared.

Record editorial revision IDs, which revision each counterpart translates,
translation state and review metadata. Either language may originate an edit.
Changing one invalidates the other's matching revision until updated. Layout-only
changes require no translation. A changed fact/source revision also invalidates
dependent claim explanations. Reject missing keys and mismatched placeholders.

The owner selected English instructions to Codex as the editing workflow on
2 October: both versions update in one reviewed diff and are previewed together.
No editing screen is needed for this workflow. No external translation-provider
call is authorized by this proposal.

## Facts, confirmed terms and evidence

Keep one fact record with German wording, evidence, precision, qualifiers, scope,
conflicts and withheld state. English explanations reference fact ID, source
revision and relevant glossary version. Never synchronize editorial changes by
rewriting original quotations or creating a second fact database.

Separate interface translations from domain glossary meanings. Version a confirmed
term's German wording, permitted English meaning, allowed contexts, verification
status and review provenance. Reuse only within reviewed scope; a glossary match
does not approve a passage. A meaning change requires renewed review and preserves
the previous confirmation. Proposed model mappings do not become confirmed terms
or golden answers. Qualified German-speaking contextual review remains necessary
for verified consequential meanings. Contested meanings remain unresolved.

The standing display contract requires verbatim German values and limits English
to labels/glosses. Leading with full English claim explanations requires a recorded
owner decision about that display treatment before publication. This proposal does
not amend the rule. Preserve original German evidence in both locales, explicitly
identified as original text. Proper names remain identifiable; explanatory English
project titles must not imply an official English name. Planned/actual, bounds,
approximation, milestone kind and phase scope must survive translation.

## Routes and scope

Recommend existing paths as German-default routes, plus `/en/` equivalents. All
internal links become locale-aware. Both languages ship in one static Astro build
and Vercel package. Include page language, titles, descriptions, alternate-language
links and localized 404s. Switch by page/project identity, retaining context.

Inventory navigation, map controls/keys, basic listing explanations and descriptive
titles, dossiers, evidence labels, glossary definitions, freshness warnings,
conflicts, withheld reasons, correction links/email templates, method, Impressum,
privacy, style guide, captions, accessible names and live announcements. Include
plurals, tooltips and all empty/loading/error states, including renderer messages.
Format numbers/dates for the locale only where stored precision supports it;
preserve canonical relative anchors. Attribution remains visibly linked.

Carry supported atlas selection/filter/camera state through validated, bounded
URL state when switching language. Static reading pages remain JavaScript-free.
Language assets remain on the same origin, preserving the absence of third-party
runtime requests. Do not export private review material into language catalogs.

## Publication checks and migration

Required missing, stale or unreviewed translations block the new bilingual release;
the previous complete release remains available. Do not silently publish English
fallback inside a German page. Ordinary editorial review and qualified domain
meaning review remain distinct. Unresolved claims retain the existing withheld
treatment in both versions.

Check message/placeholder parity, revision links and review states, localized
internal routes, equal published fact IDs and conflict/withheld states, and original
evidence preservation. Run the existing privacy/withheld scans across both locale
exports and shipped language assets. Browser-check phone and desktop layouts,
keyboard access, selected project/filter/view switching, failures, correction
context and German text expansion. Complete ordinary package/deployment checks.

Implementation order:

1. Inventory all public copy; define the paired schema/revision checks and the
   English claim-explanation display decision.
2. Build shared localization and routing; prove an atlas → dossier → evidence →
   correction journey in both languages with project/view preservation.
3. Migrate remaining text/runtime states; prepare paired editorial copy and route
   consequential vocabulary/passages for qualified review.
4. Verify the full locale matrix, publication invariants and package; prepare the
   complete bilingual release.

Completion requires current coverage on every public surface and honest domain
review status. Key counts alone do not establish translation quality. Estimate
effort after inventory; no delivery-time estimate or review-time saving is claimed.

## Framework references

Astro supports locale routing/URL helpers and documents shared content with static
dynamic routes. This supports the proposal without a framework replacement.
Checked 2 October 2026: [routing guide](https://docs.astro.build/en/guides/internationalization/)
and [shared i18n content recipe](https://docs.astro.build/en/recipes/i18n/).
