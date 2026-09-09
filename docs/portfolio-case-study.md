# Berlin, Under Construction — portfolio evidence guide

An independent map that connects Berlin construction projects to the German
sources behind their dates and status. The public prototype contains three
reviewed dossiers; two have published map positions. The map is an architectural
model, not evidence of current construction progress.

## The problem and the owner's role

Project information is scattered across official pages and documents. Similar
words can describe different milestones: completion, handover and commissioning
must remain distinct. A polished card is useful only if its claims are traceable.

The owner directed the product, selected the visual and information hierarchy,
checked source spans for the three dossiers, and made publication decisions.
As a non-native German speaker, the owner made the language barrier an explicit
design constraint. Literal span checking does not establish independent German
semantic expertise; controlled-glossary verification remains unfinished.

AI agents helped research, implement and test the product. Historical models and
reviewers are attributed in the [build log](how-this-was-built.md); current builder
work uses Codex with GPT-6 Astra. This is an AI-assisted build, not a claim that
the owner manually wrote all code or that AI independently verified its output.

## A two-minute review

1. Open the [live atlas](https://berlin-under-construction.vercel.app).
   Choose Europaplatz Süd and follow a dated claim to its original source.
2. Compare the [school dossier](https://berlin-under-construction.vercel.app/projects/heinrich-hertz-gymnasium-ostbahnhof/)
   with the energy project: milestone uncertainty and withheld location are part
   of the product, not gaps filled with guessed values.
3. Read [AI method and measurements](ai-method.md) for the recorded extraction,
   rejection behavior, cost and limitations.
4. Use the evidence links below to inspect the implementation and decisions.

The live site and current branch can differ. [Deployment evidence](public-deployment.md)
identifies the published commit; September 9 interface refinements are repository
checkpoints until separately deployed.

## How the evidence reaches the interface

German source → exact evidence span → structured extraction proposal → deterministic
validation → human publication decision → public projection → project card/dossier.

See the [C-014 dossier](research/dossiers/),
[accepted publication decisions](../public/data/accepted-review-decisions.json),
[public projection](../public/data/projects.json),
[release implementation](../public_release/), and [tests](../tests/).
Source artifacts stay private; public pages expose short spans and original links.

The recorded successful extraction used gpt-5.6-luna, took 10,017 ms, and recorded
USD 0.00161784 in provider cost. It produced a proposal for review. These figures
represent one stored run, not a benchmark or total project cost. The method page
also documents an incomplete response that was rejected and the missing accounting
for that failed attempt.

## Engineering and product decisions worth inspecting

- Astro static pages and a Three.js atlas; self-hosted model assets avoid external
  map/font runtime requests. [Model architecture and limits](atlas-model.md).
- Evidence and approval gates prevent unsupported facts reaching public pages.
  Conflicts and withheld facts have dedicated presentations.
- Source values remain German and milestone types stay distinct. The proposed
  German-default / English interface is not yet implemented.
- The small card prioritizes status and dates, with source links and an expanded
  history. Owner feedback and rejected design directions are recorded in the log.

## What has been demonstrated—and what remains open

The September 9 checkpoint passes 187 engineering tests and TypeScript checking.
That validates tested software behavior, not model accuracy. Three dossier reviews
are complete; independent glossary verification and the scored golden set remain
unfinished. No extraction accuracy, precision, recall or user-impact percentage
is claimed. Mobile/performance acceptance of the latest interface remains open.

A business adaptation could route terminology and translation through an existing
internal review team. That is a proposed application, not implemented departmental
integration. Approval may change a visible review label while retaining evidence
and decision history.

## Reproduce and scrutinize

Start with the [README](../README.md), [decision log](decision-log.md),
[build log](how-this-was-built.md), [release plan](portfolio-release-plan.md) and
[deployment record](public-deployment.md). Run the documented setup, pytest and
web TypeScript checks. CI builds use a test-only address and are never deployment
artifacts. Deployment requires a fresh, correctly configured and checked export.
