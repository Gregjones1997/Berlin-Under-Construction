---
name: design-with-depth
description: Develop a distinctive interactive product design from visual references, connect design choices to intended user effects, and implement and verify a polished vertical slice. Use for substantial visual redesigns or portfolio experiences where research, interaction, and technical depth matter.
---

# Design with depth

Produce a coherent experience whose visual impact comes from the product's subject,
interaction and underlying material. The deliverable is a working user journey
with a reason for its design decisions. Scale the workflow to the requested scope;
a consultation ends with a supported direction, while a build ends with verified
implementation. A small styling fix needs only the relevant checks.

## 1. Find the product's strongest material

Read the original brief, existing product, current implementation and accepted
decisions. Identify the audience, the action the interface should invite, and
what visitors should understand after that action. For a portfolio, identify the
engineering capability the working experience will actually demonstrate.

Inventory material already available: data, imagery, geometry, evidence, content,
and interactions. Distinguish a presentation problem from missing material. A city
boundary and two coordinates cannot become a realistic city through CSS alone.

Preserve existing authorization and constraints. In Berlin, read the current
repository instructions and decision log: the atlas has a specific JavaScript
exception, while evidence pages remain static. Geometry is context; claims still
pass the display contract. Other projects have their own boundaries.

**Done when:** a short brief identifies the first user action, the product material
that can make it compelling, what must be obtained, and the constraints that
change implementation choices.

## 2. Study references as experiences

Use the user's chosen browser and references. Interact with the opening view,
primary selection, motion, navigation and return path. Inspect a narrow viewport
when adapting a responsive product. Record the observed state before and after
each interaction; a screenshot alone establishes appearance, not behavior.

Extract mechanisms: framing, contrast, hierarchy, depth cues, camera behavior,
selection feedback, information disclosure and loading. Separate direct observations
from interpretations of why they work. If access fails, identify which behaviors
remain unobserved and continue the independent work; describe image-only analysis
as such.

For the Berlin precedent or a spatial interface, read
[the case study](references/berlin-case-study.md). Its observations are historical,
not a substitute for inspecting a reference whose current behavior matters.

**Done when:** each direction being considered has observed mechanisms, a relevant
interaction, and an explicit transfer decision: adopt, adapt or leave behind.
Avoid collecting more references once they no longer change the decision.

## 3. Connect choices to effects

Write a compact causal table for consequential choices:

| Observation or product need | Proposed mechanism | Intended user effect | Cost or failure risk | Verification |
| --- | --- | --- | --- | --- |
| A selection changes geographic context | Move the camera and update the adjacent record together | Help the visitor connect the place and its explanation | Motion can obscure orientation | Select, interrupt, return; inspect reduced-motion behavior |

Label intended effects as hypotheses until evidence supports them. A pleased owner
establishes visual acceptance; it does not establish faster comprehension,
accessibility, conversion or rendering performance.

Choose one governing visual idea and a signature interaction tied to the product's
purpose. Define enough of its system to make subsequent decisions consistent:
type roles, contrast hierarchy, accent meaning, spacing rhythm, surfaces and motion.
Use alternatives only where the user's taste or a consequential tradeoff remains
unresolved. Once a direction is accepted, refine it without repeatedly reopening it.

**Done when:** the direction explains what the visitor sees first, what they can do,
what responds, and how that response reveals useful information. Each expensive
visual treatment has a product reason and an observable check.

## 4. Build depth from the material

Apply the layers that serve this product:

- **Visual depth:** establish foreground, subject and background through framing,
  scale, light, edges and contrast. Tune their relationships before adding detail.
- **Interaction depth:** connect overview, selection and explanation; provide an
  obvious return path, predictable interruption and usable loading/failure states.
- **Information depth:** reveal evidence and exceptions where they help a decision,
  while keeping the opening view understandable.
- **Technical depth:** make the underlying system inspectable through provenance,
  measured limits and working behavior. Keep implementation jargon in the case
  study unless it helps someone use the product.

Research primary sources for unfamiliar data or rendering capabilities. Before
choosing a data-dependent direction, check coverage, units, coordinate systems,
freshness, license, completeness and runtime distribution requirements. Keep
concept imagery clearly separate from factual product material.

Choose the smallest architectural change that delivers the accepted experience.
An existing framework can host a new visual surface. A rewrite needs a demonstrated
constraint, not enthusiasm for a reference's appearance.

**Done when:** the source material can support the proposed depiction, its limits
are explicit, and one representative end-to-end implementation is feasible.

## 5. Implement one complete journey, then expand

Build the opening view → meaningful selection → explanation/evidence → return
journey against real representative content. Make typography, controls, motion,
loading and empty/error states work together before multiplying coverage.

For spatial work, validate metric scale, geometry, heights, outlines and camera
framing before polishing effects. For other domains, find the equivalent structural
foundation: authentic content, coherent data relationships or a useful manipulation.

Treat responsiveness as layout composition, not uniform shrinking. Test control
collisions, readable content and the visible subject at narrow widths. Honor
reduced motion and retain access to core information when the rich surface fails.

Measure the resource that expansion stresses: transfer size, decode time, GPU
residency, frame time or interaction latency. Use progressive detail, bounded work
and disposal where the evidence supports them. Record payload size separately from
measured performance. Compare visual quality after optimization.

**Done when:** the full journey works at representative sizes, failures preserve a
usable route, and expansion has a resource strategy with explicit limits.

## 6. Verify causes as well as appearance

Use the required browser to exercise the implemented interaction. Compare the
result against the causal table and original intent. Capture representative
screenshots, check keyboard use and console errors, and inspect intermediate
states rather than only a settled hero view.

When something disappoints, identify the broken relationship before changing
styles: missing material, weak hierarchy, conflicting controls, misleading motion,
or excessive rendering work. Change a focused mechanism and recheck the relevant
journey. A timed-out tool call is not evidence that its action completed.

Run checks appropriate to the changed contracts. Data-rich visuals need integrity
and provenance checks as well as visual inspection. Deployment, if authorized,
requires checking the deployed result; a local screenshot establishes local behavior.
This skill grants no new publication, download or external-action permissions.

**Done when:** each consequential design hypothesis has an observed result or a
clearly stated remaining uncertainty, the requested implementation works, and the
verification supports the completion claim.

## Handoff

Report the outcome, the important choice → effect relationships, the checks actually
performed, and remaining limits. Point to the implementation, source trail and
representative visual evidence. Preserve project-specific logging and handoff rules.
Describe the transferable method separately from the aesthetic selected for this
product; the next successful application need not resemble Berlin.
