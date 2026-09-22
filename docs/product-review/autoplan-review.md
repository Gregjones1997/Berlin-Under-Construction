# `/autoplan` review: resident evidence journey

Generated 22 September 2026 from
[`office-hours-design.md`](office-hours-design.md). Base branch: `main`.
Review mode: **SELECTIVE EXPANSION**. UI scope: yes. Developer-product scope:
no. Current owner direction keeps the implemented atlas and authorizes bounded
verification and fixes, not deployment or a strategic product pivot.

## Phase 1 — CEO review

### 0A. Premise challenge

| Premise | Assessment | Decision |
| --- | --- | --- |
| Exact evidence and limitations should travel with a date. | Supported by the product's trust rules and current UI. | Keep. |
| The atlas is useful only when place discovery or history adds value beyond the official page. | Correct and falsifiable. | Keep; do not call it validated. |
| Three dossiers can coexist honestly with 150 basic listings. | Possible only while the distinction is immediate and shallow records do not imply current/history coverage. | Keep with a comprehension acceptance check. |
| Map-first should stand until disproved. | Owner-approved visual direction, but not a validated acquisition or entry strategy. | Preserve implementation; keep entry strategy open to research. |
| Residents are the primary segment. | Hypothesis. Both independent voices argue civic evidence users may have more recurring need. | **USER CHALLENGE:** owner direction remains the default; no segment pivot is applied. |
| The flagship outcome is finding a supported date. | Too weak: the official page already exposes 2026. | Reframe demonstration copy around what changed, the evidence trail, and what remains unsupported. This is already within the repository's product thesis. |

The premise gate for local implementation is satisfied by the owner's current
instruction: preserve the established product/visual direction and complete the
accepted resident journey. The broader user-segment premise remains unresolved and
blocks demand claims, not local QA.

### 0B. What already exists

| Sub-problem | Existing implementation | Reuse decision |
| --- | --- | --- |
| Place discovery | `web/src/pages/index.astro`, Three.js atlas, project picker and `/records/` fallback | Reuse; no new map or search. |
| Project selection state | `web/src/atlas/controller.ts` reads and writes project IDs in the URL hash | Reuse `/#C-014`; no new state store. |
| Useful dated answer | `web/src/pages/projects/[slug].astro` selects the current milestone; `RawFact.astro` renders as-of/freshness/evidence | Reuse; verify ordering and warning language. |
| Evidence inspection | Native `<details>/<summary>` with exact German span and original-source link | Reuse; verify keyboard behavior. |
| Coverage boundary | Separate dossier/basic-listing controls, exact counts, static index | Reuse; verify a basic listing cannot imply reviewed progress. |
| Failure recovery | Atlas error panel, retry button, and static-index link | Reuse; exercise isolated `/atlas/model.json` 503. |
| Correction handoff | Contextual static routes | Reuse; stop before external email/send. |
| Publication safety | Static projection validators, withheld-value scans and Astro export tests | Reuse; no schema or publication-rule change. |

### 0C. Dream state

```text
CURRENT
3 reviewed dossiers + 150 basic listings + self-hosted atlas
        |
        v
THIS PLAN
one unambiguous place -> change/date -> evidence -> source -> return journey,
with coverage and failure boundaries visible and locally verified
        |
        v
12-MONTH IDEAL (not authorized here)
repeatable source refresh + verified change history + proven high-need segment +
distribution that brings people to relevant records
```

The plan closes the interaction loop. It does not establish the target segment,
distribution, repeat use, German semantic authority, or a sustainable refresh
operation.

### 0C-bis. Alternatives

| Approach | Effort | Risk | Result |
| --- | --- | --- | --- |
| Preserve atlas; verify the evidence loop | Small | Low | **Selected by current owner direction.** Smallest coherent implementation. |
| Make dossier/index the default entry | Medium | Medium | Viable research variant; not implemented without evidence that map-first fails. |
| Manual verified change digest for civic users | Medium | Medium | Strategically credible test of recurring value; deferred because it changes segment/distribution and requires owner direction. |
| Accounts, alerts and broad monitoring | Large | High | Deferred until repeat value is demonstrated. |

### 0D. Selective-expansion decisions

- **Accepted:** make the flagship explanation about change history and unsupported
  conclusions, not merely recovering the same date as the official page.
- **Accepted:** add deterministic regression coverage for the three already-shipped
  presentation revisions if missing.
- **Deferred:** civic-journalist/neighborhood-group segment test. Material product
  decision, not an automatic implementation expansion.
- **Deferred:** manual refresh contract or verified change digest. Valuable, but it
  changes the operating model and is outside the bounded local journey.
- **Rejected:** accounts, automated alerts, analytics, address search and new atlas
  scope. They do not remove a blocker from the accepted journey.

### 0E. Temporal interrogation

| Time | What matters |
| --- | --- |
| Hour 1 | Confirm already-implemented revisions and add missing regression assertions. |
| Hours 2–4 | Build and operate desktop, 390 px, keyboard, correction, return/reload and isolated failure paths. |
| Hours 4–6 | Design review rendered screens, fix reproduced defects, rerun affected checks. |
| Hour 6+ | Code review, documentation/handoff, then stop. No deployment. |
| After this workflow | Human segment/demand research and physical-browser warning reproduction. No further atlas scope until those produce evidence. |

### 0F. Mode confirmation

**SELECTIVE EXPANSION** is the right mode. The accepted implementation is small and
reversible. Completeness applies to its tests and error paths, not to expanding the
product into monitoring, accounts or a new user segment.

### CEO dual voices

**Claude subagent:** the official page already supplies the headline year; the
defensible differentiation is longitudinal evidence, conflicts, withholding and
change. It challenged resident fit, map-first burden of proof, freshness and the
expectation created by 150 shallow listings.

**Codex:** reached the same strategic conclusion more strongly: C-014 is a polished
demonstration case, the three-person test measures comprehension more than demand,
distribution is absent, and a maintained cross-source change graph would be more
defensible than atlas discovery alone.

| Dimension | Claude | Codex | Consensus |
| --- | --- | --- | --- |
| Premises valid? | Segment/map/freshness assumptions weak | Same | **Confirmed concern** |
| Right problem? | Reframe to change/unsupported conclusions | Same | **Confirmed** |
| Scope calibration? | No immediate redesign; stop new atlas scope | Same | **Confirmed** |
| Alternatives sufficient? | No; dossier-first/change feed/civic user under-tested | Same | **Confirmed concern** |
| Market/status-quo risk? | Official products dominate date/disruption lookup | Same | **Confirmed concern** |
| Six-month trajectory? | Risk of polished stale demo | Same | **Confirmed concern** |

#### User challenge 1 — primary user and recurring product

The owner-approved direction treats a resident place-to-evidence journey as the
primary product demonstration. Both independent voices recommend testing a civic
evidence user and a manually distributed change product because those users may have
more recurring need. The models may be missing the owner's portfolio goal and prior
visual decisions. Changing now would invalidate the bounded implementation lane and
expand operating scope. **The owner's resident direction therefore stands unless the
owner explicitly changes it; the challenge remains recorded, not silently applied.**

### Sections 1–11

#### 1. Architecture

The plan adds no new runtime architecture. It reuses static Astro dossier pages and
the atlas's existing hash selection. The privacy boundary remains intact because no
new data, hydration props or client persistence is introduced. The direct dossier
link is a reversible HTML change.

```text
approved public projection
        |
        v (build time)
Astro HTML dossier ---- exact evidence/source links
        |
        +---- /#C-014 ----> existing atlas controller ----> selected record
        |
        +---- /records/ --> JS-independent recovery/index

/atlas/model.json --success--> self-hosted city renderer
                  --error----> visible failure + retry + /records/
```

No coupling or scaling issue is introduced by this plan.

#### 2. Error and rescue map

| Operation | Failure | Rescued? | Rescue action | User impact | Test/evidence |
| --- | --- | --- | --- | --- | --- |
| `CityRenderer.load()` | manifest HTTP non-2xx | Yes | throws named message; `start()` shows failure panel | Atlas unavailable; index and dossiers remain reachable | Isolated 503 browser test; add/retain regression assertion for recovery links |
| `CityRenderer.load()` | unsupported manifest version | Yes | visible “Unsupported city model” failure | Same recovery | Export/source inspection; browser fixture covers generic error presentation |
| `start()` dynamic import/decoding | exception | Yes | dispose renderer and show message | Static recovery remains | Browser failure path |
| `choose(id)` | unknown URL hash | Partial | safely returns without selecting | Invalid deep link gives no explanation | Outside accepted links; no public link emits an unknown ID |
| fullscreen request | browser rejection | Yes | writes visible status | Atlas otherwise usable | Existing controller branch; not central to this plan |
| official source link | upstream unavailable | Browser-owned | dossier retains dated short evidence span | Original cannot be opened at that moment | Product policy; no artifact rehosting |
| correction link | no mail client/delivery | User-controlled handoff | instructions remain copyable | Delivery unverified | Stop before send by design |
| build configuration | missing publication date/legal address | Yes, fail closed | build exits nonzero | no publishable output | existing build tests/config |

No accepted journey failure is silent. The invalid-hash no-op is not generated by
the product and is not expanded in this bounded pass.

#### 3. Security and threat model

The change adds no authentication, form input, backend endpoint, storage or external
runtime request. Hash values are matched against server-rendered project controls;
they are not rendered as HTML. Existing public-projection and withheld-value scans
remain the critical security/privacy controls. No new security issue found.

#### 4. Data flow and interaction edge cases

- No location/marker: C-019 opens a record and states that location is withheld.
- Basic listing: no invented milestone or progress state when none is approved.
- Back/reload: `/#C-014` restores selection; browser Back can clear it.
- Map failure: static records remain usable.
- Stale source: as-of/freshness limits stay visible; no current-progress inference.
- Double activation: native links and idempotent hash selection do not create writes.
- Navigate away mid-load: page lifecycle disposes the renderer on non-persisted hide.

No new data mutation occurs.

#### 5. Code quality

The current change reuses `leadFact`, `RawFact`, existing hash handling and current
coverage markup. It creates no new abstraction. One gap remains: the core presentation
acceptance criteria rely mainly on browser evidence; small export assertions should
pin the purpose copy, source-statement caveat and project-specific return link.

#### 6. Test review

```text
NEW/CHANGED USER FLOWS                         COVERAGE
phone entry explains purpose                  browser screenshot; export assertion GAP
C-014 milestone precedes identity             browser screenshot; order assertion PARTIAL
evidence opens by keyboard                     browser verified
dossier returns to /#C-014                    browser verified; export assertion GAP
hash reload restores C-014                    browser verified
C-019 hash return without marker              browser verified
/atlas/model.json 503 -> recovery             isolated browser verified
basic listing remains explicitly shallow       browser verified

NEW DATA FLOWS: none
NEW BACKGROUND JOBS: none
NEW EXTERNAL CALLS: original-source navigation only
```

The plan should add narrow export assertions for the three markup regressions. Browser
execution remains necessary for hash/reload and keyboard behavior. No LLM prompt or
live-provider change is in scope.

#### 7. Performance

The three presentation changes add one paragraph and one static link and reorder
server-rendered facts. They add no fetch, query, listener, asset or bundle. The existing
large Three.js bundle/model warning remains outside this bounded change and is already
documented. No new performance issue found.

#### 8. Observability and debuggability

Visitor analytics are intentionally absent. For this static flow, deterministic build
checks, screenshots and browser traces are proportionate. Source freshness is an
operational product gap, not something this UI patch can observe. No runtime telemetry
is added because it would reopen privacy and third-party-request decisions.

#### 9. Deployment and rollout

No deployment is authorized. A later release must use valid production
`PUBLICATION_AS_OF_DATE` and `LEGAL_ADDRESS`, rerun the full suite/build/privacy scans,
then verify the public routes and asset hashes. Rollback is the previous known public
commit. Local legal placeholders must never be deployed.

#### 10. Long-term trajectory

Reversibility: **5/5**. The changes are static copy/order/link adjustments. The larger
risk is strategic: further atlas polish could outpace source freshness and segment
evidence. Post-workflow sequencing therefore stops new atlas scope until owner-led
research and at least one repeatable source-review cycle are decided.

#### 11. Design and UX

```text
arrival
  +-- atlas loads --> choose C-014 --> current changed/date statement
  |                                      |
  |                                      +--> Evidence --> original source
  |                                      |                     |
  |                                      +<----- Back ----------+
  |                                      +--> /#C-014 return/reload
  |
  +-- atlas fails --> readable error --> /records/ --> C-014 dossier
  |
  +-- basic listing --> explicit limited record + source
```

The plan explicitly covers desktop, 390 px mobile, keyboard, partial/basic content,
withheld location, error, success and return states. Deep visual quality is passed to
Phase 2 and post-implementation `/design-review`.

### Error and rescue registry

The complete registry is in Section 2. It contains eight operations, no accepted
silent failure, and one non-generated invalid-hash no-op.

### Failure modes registry

| Codepath | Failure mode | Rescued? | Test? | User sees | Logged? |
| --- | --- | --- | --- | --- | --- |
| Atlas manifest | HTTP 503 | Yes | Browser | Failure + index + retry | Browser evidence |
| Atlas hash selection | known dossier ID | N/A | Browser | Selected record | Browser evidence |
| Atlas hash selection | unknown ID | Safe no-op | No | General atlas | No |
| Dossier evidence | disclosure keyboard activation | Native | Browser | Exact span | Browser evidence |
| Dossier return | link loses ID | Fixed | Browser; export assertion pending | Restored record | Browser evidence |
| Basic listing | missing reviewed detail | Yes, bounded presentation | Browser | Limit and sources | Browser evidence |
| Official source | remote unavailable | Browser-owned | Not simulated | Dated retained span | No visitor telemetry |
| Build | withheld/private value leaks | Fail closed | Full suite | No release output | Test output |

No row is simultaneously unrescued, untested and silent on an accepted product path.

### NOT in scope

- Deployment, shared-portfolio edits or screenshot refresh: not authorized.
- New dossiers, monitoring, alerts, accounts, address search or source connectors:
  do not remove a blocker from the bounded journey.
- Target-segment pivot or distribution experiment: material owner decision.
- Golden-set values, glossary judgments or German semantic decisions: human authority.
- Live model calls or extraction evaluation: requires corpus/call/budget approval.
- Analytics: conflicts with current no-third-party runtime/privacy posture.

### Dream-state delta

After this plan, the C-014 demonstration is coherent and testable. Missing from the
12-month ideal are validated users, recurring distribution, maintained freshness,
human-verified language evaluation and evidence-complete breadth.

### CEO completion summary

| Area | Result |
| --- | --- |
| Mode | Selective expansion |
| System audit | Existing fixes found; no duplicate implementation |
| Architecture | 0 new-architecture issues |
| Errors | 8 paths mapped; 0 critical gaps |
| Security | 0 new issues |
| Data/UX | 7 edge states covered |
| Quality | 1 missing deterministic regression group |
| Tests | browser coverage strong; 3 markup assertions to add |
| Performance | 0 new issues |
| Observability | no analytics by design; freshness remains strategic gap |
| Deployment | explicitly deferred |
| Future | 5/5 reversible; strategic user/freshness challenge open |
| Design | passes plan scope; deep review next |

**Phase 1 result:** 1 implementation task, 1 material user challenge, no blocker to
local implementation verification.

## Phase 2 — Design review

### Existing design system and artifacts

The repository has no root `DESIGN.md`; the applicable equivalent is
`briefs/berlin-design/BRAND.md` plus `PROJECT.md`. Together they fix the City Desk
direction: editorial paper surfaces, dark ink, green/orange map accents, system
fonts, self-hosted geometry, no remote runtime assets and mobile coverage that is
honest about evidence depth. The supplied rendered desktop, 390 px, dossier and
failure screenshots were therefore reviewed as the visual baseline. The optional
gstack design renderer is not installed, so no synthetic redesign was substituted
for those real artifacts.

### Journey and state review

```text
ENTRY                    ANSWER                    PROOF
atlas purpose + records -> selected project/date -> source history -> evidence
       |                       |                         |
       +-- static index        +-- progress caveat      +-- original source
       +-- model failure       +-- as-of/freshness      +-- dossier / correction
                                                           |
                                                           +-- return to /#project
```

The visual system is coherent. The reproduced design defects are within the middle
of this journey: the current date does not yet advertise the existing earlier-source
history; two successive actions both use “full” without explaining their different
depth; the mobile index link resembles a metric; fatal model failure leaves dead
atlas controls available; and trust-critical caveats are rendered at 9 px in the
compact record panel.

The existing selected-project panel already has the intended contract: a labelled,
nonmodal complementary region with no focus trap. That design is preserved. The
panel remains reachable alongside the atlas and will be tested as such rather than
converted into a pseudo-dialog.

### Design dual voices

**Claude subagent:** rated the baseline 7.7/10. It identified the buried
change-history payoff as the coherence blocker, then flagged the mobile CTA,
overview/dossier naming, fatal controls, trust-copy scale, panel contract and missing
edge-case evidence.

**Codex:** independently confirmed the first five issues, narrowed the failure issue
to model-dependent controls plus announcement/focus, and rejected a speculative
panel-semantics change because the existing `<aside aria-label="Selected project">`
already expresses the intended nonmodal contract.

| Dimension | Claude | Codex | Synthesis |
| --- | ---: | ---: | --- |
| Information hierarchy | 7 | 6 | Current answer leads; earlier-source value needs an immediate route. |
| States | 8 | 6 | Broad coverage; fatal state still exposes dead controls. |
| Complete journey / arc | 7 | 6 | Working loop, but the recognition moment is buried. |
| Specificity / AI slop | 9 | 8 | City Desk is specific; “full overview” is generic and inaccurate. |
| Design-system alignment | 9 | 8 | Preserve system; raise only trust-critical microcopy. |
| Responsive / accessibility | 7 | 5 | Strong foundations; edge evidence and fatal semantics remain. |
| Unresolved decisions | 7 | 7 | No architecture question; only bounded copy/state decisions. |

Overall synthesis: **7.2/10 before the bounded fixes**. No redesign or new visual
system is warranted.

### Accepted implementation gate

1. Add an explicit, structural route from the current answer to the already-published
   earlier source statements. Do not select, translate or infer a German meaning.
2. Give the mobile records link an action verb while retaining exact coverage counts.
3. Rename the in-atlas expansion action so it names source history and evidence;
   reserve “Open full dossier” for the separate page.
4. Make fatal model failure an announced, focused state and remove model-dependent
   controls from interaction while keeping retry and the static index.
5. Raise progress/source/correction caveats from the 9 px annotation tier to a
   readable 11–12 px secondary-text tier.

The following are QA gates rather than presumed defects: 320 px layout, 200% text
reflow, keyboard order, mobile basic/withheld/partial states and screen-reader
landmark/failure announcement. VoiceOver itself may require a later physical-device
check if the supported browser tooling cannot expose it.

**Phase 2 result:** five bounded implementation tasks, no redesign, no material owner
decision and no expansion of product scope.

## Phase 3 — Engineering review

### Architecture and data flow

The five design tasks remain inside the current static boundary:

```text
public/data/projects.json
       |
       v
loadPublicProjectPages() -- published facts only
       |                         |
       v                         v
index.astro record/history       static dossier current/history
       |
       v
controller.start() -> renderer.load()
       |                 |
       | success         +-- fatal -> one terminal atlas-failed state
       v                                    |
hash selection / nonmodal record            +-- alert + retry + /records/
```

No schema, API, storage, authentication, analytics, framework, dependency or source
artifact changes are required. The structural history link depends only on
`publishedFacts`; conflict and withheld members remain in their existing controlled
presentations.

### Engineering dual voices

**Claude subagent:** approved a five-file application patch, advised one
`atlas-failed` class, conditional dossier history link, dynamic coverage CTA,
conditional expansion labels, focused fatal alert, targeted type-scale changes,
export assertions and browser verification. It explicitly rejected a comparison
algorithm, new state abstraction and new JavaScript test framework.

**Codex:** agreed, then found one important race: WebGL context loss can dispatch a
fatal event while `start()` is awaiting `city.load()`, after which the success tail
could still select a hash record and steal focus. It therefore requires an
idempotent terminal transition, renderer disposal and a failed-state guard after the
await. It also requires negative history assertions and conditional atlas labels for
projects that have no published history.

### Minimal implementation shape

| File | Change | Boundary |
| --- | --- | --- |
| `web/src/pages/projects/[slug].astro` | Conditional link from current answer to `#history-heading` | No value comparison or translation |
| `web/src/pages/index.astro` | Action-led dynamic coverage link; conditional history/facts label; focusable labelled failure alert | Preserve full-dossier label and all exact counts |
| `web/src/atlas/controller.ts` | Idempotent fatal transition; close obscuring dialog/key, dispose renderer, preserve record/hash, focus alert; post-load guard | Partial tile errors remain nonfatal; reload is recovery |
| `web/src/styles/atlas.css` | Reflow-safe fatal panel; hide only model-dependent surfaces; 11 px trust copy | Keep record/index/retry/model explanation available |
| `tests/public_release/test_astro_export.py` | Conditional history, action/depth labels and fatal-structure assertions | Browser remains the behavior proof |

Expected new runtime modules, services and stored state: **zero**.

### Failure and rescue review

| Case | Required result |
| --- | --- |
| Manifest HTTP/schema/import failure | One focused fatal alert; renderer disposed; index and retry available |
| Context loss during initial load | First failure wins; post-load success path exits |
| Context loss after C-014 selection | Alert focused; selection, record and `#C-014` retained |
| Repeated fatal events | No double disposal, message churn or focus thrash |
| Retry succeeds | Fresh page clears failed state and restores retained hash selection |
| Retry fails | Same clean recovery state, no accumulation |
| One detail tile fails | Existing status message; atlas remains usable and not failed |
| Project key/model dialog open on failure | Close before focusing alert |
| 320 px / 200% zoom | Alert and both recovery actions remain reachable without horizontal clipping |
| Reduced motion | Orbit remains disabled; fatal focus/recovery unchanged |

### Security, performance, observability and deployment

- Failure text continues through `textContent`; no HTML sink is added.
- New English copy labels structure only. German values remain verbatim.
- No natural person, source artifact, input, persistence, external request or
  telemetry is introduced.
- Performance impact is negligible; fatal disposal stops failed renderer work.
- Deterministic output, console capture and screenshots remain the observability
  boundary; analytics are not added.
- Deployment remains outside authorization. Local legal placeholders must not ship.

### Test plan

The full executable plan is saved in [`test-plan.md`](test-plan.md). The key split is:

- export tests prove conditional markup, depth labels, recovery structure and all
  existing publication scans;
- typecheck/build prove the Astro/controller integration;
- browser QA proves focus, hidden model controls, retry/hash restoration, reflow,
  keyboard flow, reduced motion and nonfatal partial-detail behavior;
- the full pytest suite remains the final privacy/publication gate.

**Phase 3 result:** implementation is safe after the race guard and conditional-label
narrowing. No material product or architecture decision remains.

## Phase 3.5 — Developer Experience applicability audit

The installed `/plan-devex-review` applicability gate was evaluated. The accepted
user is a resident using a public static reading experience; this plan introduces no
API, SDK, CLI, webhook, plugin, configuration surface or developer-facing error
contract. Contributor documentation exists, but it is not the product surface under
review. A fabricated DX scorecard would therefore be noise.

**Result: skipped as not applicable after audit.** The ordinary engineering test and
handoff documentation obligations remain.

## `/autoplan` completion gate

- CEO: complete; one explicit user-segment challenge recorded, no silent pivot.
- Design: complete; five bounded defects accepted, visual direction preserved.
- Engineering: complete; race and conditional-history edge cases resolved in plan.
- Developer Experience: applicability gate evaluated; no developer product.
- Authorization: the owner's current instruction explicitly authorizes local
  implementation and verification, so no duplicate approval question is required.

## Decision Audit Trail

| # | Phase | Decision | Classification | Principle | Rationale | Rejected |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | CEO | Preserve current atlas implementation | Auto-decided | DRY / bias to action | The owner explicitly authorized verification and the fixes already exist. | Rebuild or switch entry now |
| 2 | CEO | Reframe demo around change and unsupported conclusions | Auto-decided | Explicit over clever | This is supported by existing history/conflict UI and differentiates from the official page. | Date lookup as the headline outcome |
| 3 | CEO | Add three narrow export assertions | Auto-decided | Completeness / boil lake | They pin the modified markup at tiny cost and complement browser checks. | Browser-only regression coverage |
| 4 | CEO | Do not add analytics or monitoring | Auto-decided | Pragmatic / scope | They expand privacy and operations without blocking the accepted journey. | Runtime telemetry and alerts |
| 5 | CEO | Keep resident segment pending owner decision | User challenge | User authority | Both voices recommend a civic evidence segment, but the owner has not changed direction. | Silent segment pivot |
| 6 | Design | Surface existing history through an immediate route | Auto-decided | Complete journey / evidence first | Both voices reproduced the buried differentiator; the fix exposes existing published facts without new interpretation. | Inline model-written comparison |
| 7 | Design | Keep the project panel nonmodal | Auto-decided | Native semantics / preserve work | The current labelled aside already matches the intended interaction contract. | Custom dialog or focus trap |
| 8 | Design | Disable model-only controls on fatal load | Auto-decided | Explicit state / recoverability | Controls that can only no-op should not remain actionable behind the failure. | Cosmetic overlay only |
| 9 | Design | Promote trust caveats to readable secondary text | Auto-decided | Trust over density | These sentences prevent dates from being read as observed progress. | Preserve 9 px microtype |
| 10 | Engineering | Make fatal state idempotent with post-load guard | Auto-decided | Complete recovery / race safety | A context-loss event can otherwise be followed by a stale success tail. | CSS-only failure state |
| 11 | Engineering | Preserve selected record and hash through failure | Auto-decided | Recovery / reversible state | Reload can restore the user's place without a new store. | Calling `close()` on failure |
| 12 | Engineering | Use conditional history/facts action labels | Auto-decided | Honest interfaces | Two dossiers do not have published milestone history. | Promise source history everywhere |
| 13 | Developer Experience | Skip full DX review after applicability audit | Auto-decided | Relevance | No developer-facing product surface changes. | Invent a developer persona or API contract |
