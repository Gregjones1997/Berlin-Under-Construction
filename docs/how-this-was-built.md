# How This Was Built

This document is the single newest-first timeline of how Berlin, Under Construction is developed. The logging policy, roles and full-entry template live in [`build-log-conventions.md`](build-log-conventions.md).

## 2026-08-07 — Persist and reconstruct the first milestone slice

**Status:** In progress

**Commits:**

- `571e7a6` — `feat(pipeline): add SQLite claim and artifact store`
- `<reconstruction-hash>` — `feat(pipeline): reconstruct a pilot dossier fragment from stored data`
- `<metering-hash>` — `feat(pipeline): meter the first extraction run`
- `<process-hash>` — `docs(process): record vertical-slice evidence and next action`

### Goal

Move one milestone claim end to end through retrieval, verified artifact
retention, local persistence and storage-only reconstruction, then run the
frozen prompt once with real provider metrics. The dossier comparison is a
smoke observation, never a golden evaluation or accuracy measurement.

### Participants and scopes

- Project owner: approved SQLite for the local pipeline store, set the required
  sequencing and commit boundaries, and retained authority over all golden and
  publication decisions.
- Main agent (Codex, TDD and codebase-design skills): sole writer; froze the
  prompt before delegation, designed the public seams, integrated the proposals
  and owns every test, commit and live verification.
- SQLite storage subagent (inherited GPT-5.6 model, high effort;
  codebase-design and domain-modeling skills): proposed the append-only local
  store, atomic aggregates, canonical typed JSON, verified stored bytes and
  migration constraints.
- Reconstruction subagent (inherited GPT-5.6 model, high effort): proposed the
  deterministic storage-only fragment, privacy-safe withholding and a neutral
  dossier smoke comparison outside the reconstruction seam.
- Metering/privacy subagent (inherited GPT-5.6 model, high effort): proposed the
  provider seam, fail-closed threshold/pricing gates, exact usage accounting and
  content-free personal-data validation results.

### Multi-agent architecture

Delegation began only after the extraction prompt was frozen. Three read-only
lanes examined independent integration risks in parallel: storage transactions,
reconstruction semantics, and live metering/privacy. No lane read the frozen
dossiers or `evaluation/`, and no lane wrote to the repository.

The main agent accepted a concrete SQLite module rather than a hypothetical
generic repository, atomic immutable writes, post-transform hash identity,
private verified blobs, typed JSON round-trips and adapter-level migration
tests. Generic CRUD, URL identity, pre-transform hash foreign keys, silent
conflict ignores, early Supabase and dual writes were rejected. For
reconstruction, the main agent accepted deterministic storage-only rendering,
withholding of non-publishable text and neutral smoke differences outside the
renderer; a new protocol was rejected until a second backend exists. Metering
disposition and final independent verification are recorded below when the
runner is integrated.

### Work performed

- Frozen prompt and ADR-012 are recorded separately above because both preceded
  implementation by design.
- Added the SQLite persistence seam and its first transactional artifact,
  retrieval and milestone-claim round trips. Further work remains in the commits
  listed above.

### Verification

- Storage seam: four tests pass for close/reopen round-trip, idempotent replay,
  immutable-ID conflict rejection, relational consistency and mode `0600`.
- Full-suite, reconstruction, live retrieval, privacy and metering evidence are
  added as the remaining slices complete.

### Failures and limitations

- The current process exposes no `OPENAI_API_KEY`. No live extraction has been
  attempted and no token, cost or latency value has been invented. The main
  agent is checking whether another available provider path exposes auditable
  exact usage; otherwise Step 3 remains explicitly blocked.

- 2026-08-07 — Project owner and Codex (TDD and codebase-design skills): froze `milestone-extraction-de-v1` before any extraction run, derived only from approved schema and policy rather than the dossiers. Verified: the prompt declares its immutable version and enforces untrusted-document handling, German-first values, exact spans, closed milestone types and natural-person exclusion. `d0d17d8`

- 2026-08-07 — Project owner and Codex: accepted ADR-012, using SQLite for private local pipeline persistence while retaining Supabase/PostGIS for the web application. Verified: migration consequences preserve strict models, stable identities, German spans and ADR-011 hash roles. `3a1bf7f`

## 2026-08-07 — Gate financial completion on evidence-depth coverage

**Status:** Complete

**Commit:** `69c256c` — `feat(pipeline): gate financial completion on evidence-depth coverage`

### Goal

Close the remaining pipeline-review gap by making the configured evidence ladder
and required financial depths behavioral, while stopping short of claiming that
the financial claim slice itself exists.

### Participants and scopes

- Project owner: authorized the follow-up proposal and defined the Phase 1
  checklist reconciliation and threshold-configuration blocker.
- Main agent (Codex): remained the sole writer; read and applied the proposal,
  inspected the gate, reconciled the checklist and independently verified the
  integrated result.
- Reviewer (Claude): supplied the read-only follow-up patch under
  `docs/research/proposals/2026-08-07-financial-depth-coverage/`.

### Work performed

- Added immutable, discriminated per-project evidence-depth dispositions that
  preserve `not_checked`, `searched_found`, `searched_absent`, `unavailable` and
  human-assigned `inapplicable` as distinct states.
- Required every searched or unavailable disposition to name its actual search;
  found records name their source IDs, access barriers remain distinct from
  absence, and inapplicability requires a review-decision ID.
- Added a deterministic financial-completion gate that reads both
  `evidence_depths` and `completion.financial_requires_depths`, rejects unknown
  or duplicate depth records and routes incomplete coverage to review with
  `financial_depth_coverage_incomplete`.
- Reconciled Phase 1 checklist evidence without marking incomplete work done and
  recorded the missing threshold configuration as a blocker before the first
  metered extraction.

### Verification

- `.venv/bin/python -m pytest -q`: 91 tests passed, up from 78.
- Both previously unused configuration fields now have behavioral consumers;
  tests prove the required depths are read from configuration rather than
  hardcoded.
- Retrieval configuration digest remains
  `sha256:b5b9c1dcdb0a5483be1e9176503539adfc4dd30108161aa33a460565b983e4c5`.
- `git diff --check` passed. `docs/research/dossiers/` and `evaluation/` were
  unchanged.

### Failures and limitations

- This is the coverage record and gate only. `FinancialClaim`, conflict records,
  source and artifact persistence, review history and PDF evidence bounding
  boxes remain open.
- `Confidence.threshold_config_version` is required, but no threshold
  configuration exists under `pipeline/config/`. The first metered extraction
  remains blocked until that versioned configuration is implemented.

## 2026-08-07 — Close the first pipeline review findings

**Status:** Complete

**Commits:**

- `e9c66b4` — `fix(pipeline): constrain retrieval hosts and response size`
- `15ce351` — `feat(pipeline): make milestone quarantine structural`
- `8006010` — `fix(pipeline): block embedded files and honor declared charsets`

### Goal

Apply and independently verify the review findings against `d5d5806`, preserving
the owner's rulings on the transport allowlist, structural milestone quarantine,
HTML span length and timezone-aware creation dates.

### Participants and scopes

- Project owner: accepted four decisions incorporated into the proposal and
  authorized applying the reviewer patch in three coherent work commits.
- Main agent (Codex): remained the sole writer; inspected the proposal mapping,
  applied it, separated it by purpose and independently verified the integrated
  tree and live retrievals.
- Reviewer (Claude): reviewed `309fade..9d909e0` read-only and supplied the
  patch under `docs/research/proposals/2026-08-07-pipeline-review-fixes/`.

### Work performed

- Constrained the initial URL and every redirect hop to HTTPS and a configured
  host allowlist, streamed response bodies under the configured byte cap,
  wrapped upstream transport failures, required both User-Agent classes and
  made fetch steps and artifact-transform selection drive retrieval behaviour.
  The allowlist is transport permission only; it does not assign evidence depth
  or source tier. A regression reads every frozen dossier URL to prevent drift
  but never writes to the dossiers.
- Replaced the milestone option bag with a discriminated active/quarantined
  union. Eligible claims require verified state, accepted review and recorded
  passing validations. Quarantined claims structurally require their reason,
  human-assigned scope relation and review-decision ID, while extractor
  proposals cannot reach any quarantine field. Claim interiors are immutable,
  timestamps are timezone-aware and evidence-span length is explicit.
- Removed embedded-file references and file specifications before PDF retention,
  avoided creating an absent `/Info` dictionary, enforced the configured
  transform rule, honored declared HTML charsets and routed undecodable artifacts
  through the normal extraction-rejection channel. Reproduction registries are
  strict, and diagnostic output labels pre-strip hashes private and distinguishes
  them from stored-content hashes.

### Verification

- `.venv/bin/python -m pytest -q`: 78 tests passed after applying the proposal.
- Live no-retention reproduction: all three C-014 historical response hashes
  matched; the redirect hop was recorded; the PDF retained stored-content hash
  `sha256:2d4a8292a2c7d309831dc19d74729ceb74aadcb433f08b55ea3ce1a48ced8a6a`.
- Current retrieval configuration digest:
  `sha256:b5b9c1dcdb0a5483be1e9176503539adfc4dd30108161aa33a460565b983e4c5`.
  The older digest remains in the immutable `d5d5806` entry as the measurement
  for that earlier configuration; it was not silently rewritten.
- `git diff --check` passed. `docs/research/dossiers/` and `evaluation/` were
  unchanged.

### Failures and limitations

- `evidence_depths` and `completion.financial_requires_depths` are validated but
  still have no behavioural consumer. They remain forward-looking configuration
  and must be wired into the financial slice before being called executable
  policy.
- Financial, conflict, source-persistence and review-history schemas, PDF
  evidence bounding boxes and the private atomic retention adapter remain open.

## 2026-08-07 — Start the configured, retention-safe retrieval pipeline

**Status:** Complete

**Commit:** `d5d5806` — `feat(pipeline): add configured verified artifact retrieval`

### Goal

Turn the evidence-retrieval playbook into executable policy, implement ADR-011
before any bulk artifact retention, reproduce the three previously checked
C-014 responses, and establish a strict German-first extraction boundary.

### Participants and scopes

- Project owner: requested the pipeline start, commit and push, and requested
  high-effort GPT-5.6 Luna-compatible delegation.
- Main agent (Codex, TDD and codebase-design skills): sole writer; designed,
  integrated and independently tested the schemas, configuration, transformer,
  retrieval job and extractor boundary.
- Schema subagent (inherited GPT-5.6 model, high effort; domain-modeling, TDD and
  codebase-design skills): proposed strict Pydantic boundaries and separation of
  untrusted extraction proposals from trusted publication state.
- Retrieval-configuration subagent (inherited GPT-5.6 model, high effort):
  translated the playbook into a versioned TOML shape and identified the
  evidence-depth and User-Agent fallback semantics.
- Artifact subagent (inherited GPT-5.6 model, high effort; codebase-design
  skill): proposed the single preparation gate, object-aware PDF rewrite,
  reparse checks, idempotency test and safe reproduction inventory.

### Multi-agent architecture

Delegation split three read-only design risks that could be examined in
parallel: schema authority boundaries, retrieval policy, and PDF transformation.
The main agent accepted strict frozen models, the non-publishable proposal DTO,
the term `evidence_depth`, the default/browser/browser-tool fallback, and the
single `prepare_artifact` gate. The PDF proposal's exact 10.10.0 pin was modified
to the independently tested 10.11.0 runtime. Its broader retention adapter,
signed-PDF and embedded-file policies were deferred because this change does not
write artifacts. The full approved claim/conflict/source model was also not
claimed complete: this first vertical slice covers milestone proposals and
leaves financial, conflict, review-history and PDF evidence-bbox slices next.

The requested direct `gpt-5.6-luna` override was not accepted by the available
orchestrator; the lanes therefore used its supported inherited-model path with
high reasoning effort. All lanes remained read-only, and every accepted idea was
reimplemented and checked by the main agent.

### Work performed

- Added strict Pydantic milestone-claim and untrusted milestone-proposal models.
  Extractor output cannot contain publication or review fields, requires an
  exact German evidence span, and is rejected atomically on malformed JSON or a
  span mismatch. PDF proposal extraction remains blocked until bounding-box
  verification exists.
- Converted the operational retrieval rules into versioned TOML: five evidence
  depths, parliamentary URL templates, financial completion depths, content
  limits, exact identity encoding and the complete 403 fallback chain.
- Added an in-memory retrieval job that records redirect and access-barrier
  attempts and always passes successful bytes through the artifact preparation
  gate before returning them.
- Implemented ADR-011 with pikepdf/libqpdf: extract timestamp provenance, remove
  document information and reachable metadata objects, deterministically
  rewrite, reparse, verify forbidden fields are absent, and prove byte-level
  idempotency. HTML remains byte-exact under `identity/v1`; both pre-transform
  and stored hashes are computed, but only the stored hash is artifact identity.
- Added a no-retention reproduction registry and command. It keeps response
  bodies in memory only and does not modify the frozen dossiers.

### Verification

- `.venv/bin/python -m pytest -q`: 35 tests passed, including strict proposal
  authority boundaries, exact German HTML spans, 403 retry recording, MIME
  bypass rejection, object metadata removal, timestamp extraction, two hashes
  and byte idempotency.
- `.venv/bin/python -m pip check`: no broken requirements.
- Live no-retention run: all three C-014 historical raw-response hashes matched.
  The two HTML stored hashes remained equal to their raw hashes. The real
  `h19-2449-v.pdf` passed reparse and idempotency verification and produced
  stored-content `sha256:2d4a8292a2c7d309831dc19d74729ceb74aadcb433f08b55ea3ce1a48ced8a6a`
  under `pdf-metadata-strip/v1`. Retrieval configuration digest:
  `sha256:dfb0d5edc6a05ac04f147a31757db65d0022636a82d4907ab88b54fafed25496`.
- `git diff --check` passed; the frozen dossier directory remained unchanged.

### Course correction

**Course correction** — the first editable install failed because setuptools
auto-discovered the top-level `notes` and `evaluation` directories as packages.
Package discovery is now explicitly limited to `pipeline*`, and generated
`*.egg-info/` directories are ignored. Cost: one failed local install attempt;
no repository or retained-artifact data was changed.

### Failures and limitations

- This is the first pipeline slice, not completion of the approved Phase 2 data
  model. Financial claims, conflicts, source persistence, review history, PDF
  evidence bounding boxes and the private atomic retention adapter remain.
- No model extraction was executed and no golden value was generated or edited.
- Browser-tool retrieval is an explicit terminal handoff from the local job; the
  browser executor is not embedded in Python.

- 2026-08-07 — Project owner and Codex: clarified that recorded stack choices are working defaults which the owner may reopen at any time; agents should not repeatedly relitigate them unprompted. Verified: the deadline-linked prohibition is absent from `AGENTS.md` and `README.md`. `5f87e67`

- 2026-08-07 — Project owner, reviewer and Codex (domain-modeling skill): reconciled phase labels and ADR-002/003, accepted ADR-011 as amended, approved the claim/source/extraction design including quarantine and structural conflicts, and recorded the C-014 redirect finding outside the frozen dossier. Verified: owner rulings are explicit, three raw hashes reproduced, and dossiers remain unchanged. `4b840d8`

## 2026-08-07 — Enforce build-log reachability and empty golden-set schema

**Status:** Complete

**Commit:** `b81ba61` — `test(process): enforce build-log hash reachability and empty golden-set schema`

### Goal

Turn the twice-failed build-log hash procedure into an automated invariant and
prepare the golden-set engineering boundary without creating golden values.

### Participants and scopes

- Project owner: approved the empty golden-set engineering boundary and retained
  authority over commits and all future populated values.
- Main agent (Codex, TDD skill): remained the sole writer, implemented the CLI,
  schema, tests and CI wiring, and independently verified the integrated result.
- Reviewer (Claude): identified the amended-object test gap, dataset-status
  coupling gap and commit/content-hash ambiguity; independently exercised the
  proposed fixes before handoff.
- Subagents: none.

### Work performed

- Corrected the orphaned pilot-selection hash to reachable commit `9acacfa` and
  added a CLI plus full-history CI check for every recorded commit hash.
- Added a regression whose pre-amend object still resolves under `git cat-file`
  but is correctly rejected because it is absent from `git log --all`.
- Reserved the `sha256:` prefix for content hashes so the Git-hash scanner has a
  mechanical boundary.
- Added 30 empty human-review slots, a JSON Schema and pytest harness. Dataset
  status is coupled to claim review status, populated values require permitted
  provenance, and `model-assisted` is unconditionally rejected.

### Decisions

- CI checks a full clone (`fetch-depth: 0`); object existence is never treated
  as reachability.
- The 30 IDs are capacity placeholders, not claim selection. Their `expected`
  objects remain empty until the German-speaking review returns.

### Verification

- Main-agent run: 18 tests passed, including the real orphan precondition,
  dataset-state transitions and ten adversarial `model-assisted` variants.
- Main-agent run: all 28 distinct recorded commit hashes are reachable.
- Reviewer independently verified 28/28 reachable hashes, unchanged dossiers,
  an empty golden set, rejection across ten adversarial `model-assisted`
  variants, and three byte-for-byte C-014 raw-response hashes.
- Main agent independently reproduced those three hashes as
  `sha256:36d47e13604b30115339bd75090a452296d9ebd1f8919bf9cf2440299070f4f5`,
  `sha256:6f341678a9ec8240f29a8d6f93091c0cadd1f5e4cc8b90acc54c3805a2cdeab5`
  and `sha256:a554a9df39ccba3b641e48264d3442a755178e60f3f7dea7c6de2398bb49fa60`
  without retaining the response bodies.
- The dossier directory is unchanged from `phase-1-research-complete`.

### Course correction

**Course correction** — the build log again recorded an amended commit's
orphaned pre-amend hash after the first occurrence had already produced a
written `git log` rule. The second failure proved prose was not an effective
control. CI now enforces the rule, and the regression preserves the precise
reason `git cat-file` is insufficient. Cost: one blocking cleanup item and the
implementation of the missing automated guard.

### Failures and limitations

- No golden value exists; the harness validates structure and authority only.

## 2026-08-06 — Establish the Phase 2 data-core boundary

**Status:** Complete

**Commit:** `b15af07` — `docs(process): record phase-2 branch boundary`

### Goal

Create an explicit phase boundary before pipeline work begins and record the
branching-policy failure that required the recovery.

### Course correction

**Course correction** — 2026-08-06 — Project owner: caught that Phase 0/1 ran
entirely on `main` despite the one-branch-per-phase convention in `AGENTS.md`.
Neither the main agent nor the reviewer flagged it. Consequence: no clean phase
boundary, so the required full-diff phase-boundary review never triggered.
Recovered with the retroactive `phase-1-research-complete` tag; the
`phase-2-data-core` branch was created from `9573baa` before pipeline work
began.

### Evidence

- Annotated tag: `phase-1-research-complete`
- Branch: `phase-2-data-core`

## 2026-08-06 — Pilot evidence pass for C-014, C-010 and C-019

**Status:** Complete; owner review of open values remains

**Commit:** `00cd463` — `docs(research): add verified evidence dossiers for three pilots`

### Goal

Integrate the independently prepared evidence-pass proposals for the three
selected pilots, preserve exact German wording and scope conflicts, and turn
the retrieval failures into repeatable repository policy without creating any
golden-set values.

### Participants and scopes

- Project owner: supplied the source confirmations and binding rulings on
  precision versus conflict, the state-owned Bauherr source tier, C-010's
  quarantined amount, the h19-2449 publication date, the relative-date
  interpretation and the C-019 pump-station boundary.
- Main agent (OpenAI Codex): remained the sole writer; independently verified
  source availability and hashes, qualified overstrong proposal wording,
  reconciled repository collisions and integrated the accepted material.
- External reviewer (Claude Opus 5): retrieved and extracted the German sources
  and prepared proposals 01–10. The reviewer used no subagents and made no
  repository edits.
- Read-only integration checks (three GPT-5.6-terra agents, not Sol): one
  checked policy, naming and document collisions; one reopened the core pilot
  sources and tested claim strength; one checked ADR numbering, checklist,
  selection-record and build-log structure. Model token and cost telemetry were
  not exposed, so both are recorded as unavailable.

### Multi-agent architecture

Delegation was used only for independent, read-only checks while the main agent
integrated the proposal pack. The policy lane found stale selection-record
claims and naming risks; the source lane confirmed that C-014 must not be
labelled delayed and that C-019's street address is an HKW site anchor rather
than a project-specific address; the structural lane found the unresolved
prior build-log hash and the required two-commit procedure. The main agent
accepted those findings, rejected one lane's recommendation to keep the C-019
pump station inside scope because it contradicted the owner's later ruling, and
checked the integrated result against the proposal README, current repository
and original URLs.

### Work performed

- Added two standing retrieval rules, ADR-009 and ADR-010 as accepted decisions,
  and ADR-011 as a proposal only.
- Added glossary 1.1 seed rows, recorded C-010's milestone-type structural risk,
  and added the evidence source ladder, parliamentary URL patterns, reference
  sources and retrieval playbook.
- Replaced the C-014 dossier and created C-010 and C-019 dossiers. C-010's
  `107.300.000 €` remains quarantined; C-014's `1.900.000 €` causal reading
  remains unresolved; C-019's pump station is a linked measure outside the
  owner-ruled boundary.
- Reconciled the candidate ledger and pilot-selection record with the completed
  evidence pass, including medium-high difficulty for C-014 and C-010, low for
  C-019, and the superseded C-019 boundary declaration.
- Repaired the existing C-014 build-log entry's reachable commit hash and
  advanced the project-checklist handoff.

### Decisions

- The source ladder is documented as an observed and relevant-family sequence,
  not a universal requirement that every project has parliamentary records.
- C-014 is described as having passed an expected target window with completion
  unverified, not as delayed.
- C-019's address is explicitly a cross-source HKW site anchor; no precise
  Power-to-Heat parcel or project-only street address is asserted.
- Source-described organization relationships are retained without normalizing
  them into commissioner, financer or contractor fields while the role
  vocabulary remains blocked.
- PDF metadata stripping remains proposed. The playbook does not make ADR-011
  operational before the owner rules.

### Verification

- Reopened all 18 registered dossier URLs with a full browser User-Agent. Every
  URL returned HTTP 200, including both PARDOK and Hauptausschuss direct-PDF
  patterns.
- Recomputed SHA-256 over raw response bytes: 15 hashes matched exactly. The two
  Entwicklungsstadt pages and HOWOGE page had changed bytes while still
  resolving and retaining their cited content; their current hashes and the
  revalidation finding are recorded.
- Confirmed 15 matching sources included all official Berlin, parliamentary,
  BEW, meinBerlin and reference-PDF artifacts in the registries.
- Checked the repository for unresolved placeholder ADR references, stale
  inside-scope instructions, overstrong C-014 delay wording and newly introduced
  natural-person names.
- Verified that no proposal-scaffolding file is tracked or staged.

### Course correction

**Course correction** — The reviewer reported PARDOK as unreachable after HTTP
403 responses and recommended a manual human pass. The project owner acted on
that recommendation before directing a browser attempt. A full browser
User-Agent retrieved both parliamentary document families. Cost: one
misdirected owner instruction and delayed access to C-010's quarantined cost and
C-014's financial structure. The standing retrieval rule now requires both
User-Agent and browser-tool attempts before escalation.

**Course correction** — The reviewer used regex-over-decompressed-streams PDF
extraction that produced superficially readable but mangled spacing and nearly
entered C-019's site address as a verbatim span. It was caught before recording.
The Störfall PDF remains explicitly extraction-unreliable and cannot supply a
string-comparison span until re-extracted with a proper parser.

**Course correction** — The reviewer initially treated
`zum Schuljahresbeginn 2026/27` as a German-reading judgment. The Berlin
Ferienordnung supplies the first teaching day after the summer break,
2026-08-24. The source anchor remains canonical, the resolved date carries its
authority, and the owner's “within one week” interpretation remains separately
tagged as owner judgment.

**Course correction** — The preceding C-014 dossier commit was left in the
build log as `Commit: Pending` even though reachable commit `efe0227` existed.
The structural integration check caught it. Cost: no repository rework beyond
repairing the entry in this work commit.

### Failures and limitations

- C-014 completion status and the causal explanation for its `1.900.000 €`
  field remain open.
- C-010's sports-hall scope conflict and formal meaning of
  `Schuljahresbeginn` remain open; the 31 August expected milestone requires a
  later official check.
- C-019 has no public change history found, no source-confirmed Bezirk and no
  project-specific street address.
- Native-speaker glossary verification and every golden-set value remain future
  human work.

### Evidence

- `AGENTS.md`; `docs/decision-log.md`; `docs/glossary.md`;
  `docs/methodology.md`; `docs/research/source-ecosystem.md`
- `docs/research/evidence-retrieval-playbook.md`
- `docs/research/dossiers/C-014-europaplatz-sued.md`
- `docs/research/dossiers/C-010-heinrich-hertz-gymnasium.md`
- `docs/research/dossiers/C-019-power-to-heat-hkw-mitte.md`
- `docs/research/candidate-ledger.md`;
  `docs/research/pilot-selection-record.md`;
  `docs/project-checklist.md`


## 2026-08-06 — Verified C-014 dossier evidence and change history

**Status:** Complete

**Commit:** `efe0227` — `docs(research): record verified C-014 dossier evidence and change history`

### Goal

Record the first verified dossier evidence for C-014, including the superseded completion target, the current completion field, the reported Baubeginn chain, source metadata and the remaining verification boundary.

### Participants and scopes

- Project owner: confirmed the four C-014 source spans directly on 2026-08-06.
- Main agent (Codex): independently reopened the official and secondary pages, captured content hashes and recorded the evidence without assigning organization roles.
- Secondary-source tracing agent (GPT-5.6-terra, high): located the missing official 2023 citation trail and returned the exact German span; it did not edit files.

### Work performed

- Verified `Die Fertigstellung der anspruchsvollen Bauaufgabe ist bis Ende 2025 vorgesehen.` in the 2023-10-12 Senate press release, preserving `bis` and `vorgesehen`.
- Verified the current `Fertigstellung: 2026` field and recorded the pair as supersession, not correction.
- Recorded the official planning statement, competition result, observed organizations and absence of a cost figure.
- Recorded the two Entwicklungsstadt Baubeginn reports with `Reported` labels and preserved the excluded whole-Bahnhofsumfeld speculation.
- Captured URL, publication date, retrieval date and SHA-256 content hash for four sources.

### Decisions and limitations

- No commissioner, financer or contractor roles were assigned; role vocabulary is blocked on the pending ADR.
- The current record can preserve both date spans but cannot yet type source date, as-of date, modal qualifier and supersession relation as a structured historical milestone. This is a Phase 2 schema finding.
- C-014 remains open on current status, the official basis of the 2026 field, exact boundary, Bezirk and Senate wording for the two later reported Baubeginn points.

### Verification

- Official primary span resolved at the supplied URL and matched verbatim.
- Current official page resolved and `Fertigstellung: 2026` matched.
- Both secondary pages resolved; their attribution chains were retained as reported, not promoted to primary evidence.
- Hashes and retrieval metadata are recorded in the dossier.

### Evidence

- `docs/research/dossiers/C-014-europaplatz-sued.md`
- `docs/research/candidate-ledger.md`
- `docs/research/pilot-selection-record.md`
- `docs/research/glossary-verification.md`

## 2026-08-06 — Owner-confirmed pilot selection and handoff

**Status:** Complete

**Commit:** `9acacfa` — `docs(process): close pilot-selection checklist items and update handoff`

### Goal

Record the project owner's confirmation of the four hard-gate candidates, select three pilots and a reserve, close only the evidenced Phase 1 selection items, and hand off manual dossier research.

### Participants and scopes

- Project owner: confirmed all four shortlisted identities, boundaries and exact German end-date wording against the original sources on 2026-08-06; made the final selection and accepted the documented process deviations.
- Main agent (Codex): corrected four flagged modal framings, recorded the selection, updated the checklist and maintained the single-writer repository.
- Native-speaker review: not performed in this pass; the glossary verification report's native-speaker column remains empty.

### Work performed

- Corrected C-002, C-004, C-009 and C-019 so their milestone framing preserves `sollen` and `vorgesehen` rather than collapsing them into stronger or different planning language.
- Recorded selected pilots C-014, C-010 and C-019, with C-003 as reserve, in `docs/research/pilot-selection-record.md`.
- Recorded the owner confirmation, C-010's requirement for both cited sources, the per-project boundaries and aliases, exact German date wording, milestone types, source/as-of dates, difficulty notes, unresolved gates, rationale and verification links.
- Set the C-010 checkpoint to 2026-08-25 for its 2026-08-31 milestone.

### Decisions and disclosures

- The frozen weighted rubric was not applied and no dimension scores were assigned. This was deliberate: 26 days remained to first release, the shortlist had passed the hard gates, and portfolio complementarity was the deciding factor even though the rubric weights it at only 10 of 100. Retrospective scores would be post-hoc rationalisation.
- The difficulty-control conflict is resolved by owner override, not satisfaction. All three pilots are low-to-medium difficulty, so the frozen requirement for at least one fragmented or difficult-evidence project is not met. The owner accepted this as a known first-release gap.
- C-010 resolves one day before first release. A met promise and a slip are both publishable; the risk is discovering the answer late.

### Verification

- Re-read the four ledger rows and confirmed the quoted German spans were not changed.
- Confirmed the three selected IDs and reserve match the owner decision record.
- Confirmed only the three evidenced checklist items were closed; the controlled glossary remains open because native-speaker review is pending.
- Commits in this sequence: `0dbe0e7` (modal framing), `bfcc45d` (selection record), and this commit (checklist and handoff).

### Evidence

- `docs/research/candidate-ledger.md`
- `docs/research/glossary-verification.md`
- `docs/research/pilot-selection-record.md`
- `docs/project-checklist.md`

- **Course correction** — 2026-08-06 — Project owner and Codex: corrected an orphaned build-log hash, made the two-commit hash procedure executable, and recorded the false German-language assumption as the course correction it was. Verified: every backticked build-log hash resolves through `git log`; ADR-008 and the disclosure entry state the actual and counterfactual costs. `16f997c`

## 2026-08-06 — Disclose the German-language constraint and verification boundary

**Course correction**

**Status:** Complete; course correction recorded; native-speaker review pending

**Commit:** `7173758` — `docs(process): disclose German-language constraint and mitigations`

### Goal

State that the project owner does not read German, show what that means for the
evidence chain, and measure the first verification pass over the vocabulary on
which glossary-derived golden values will depend.

### Participants and scopes

- Project owner: confirmed the language constraint, required human rather than
  owner authorship of ground truth, set the authority boundary and requested the
  full-glossary verification run.
- Main agent (OpenAI Codex, `/research` skill and web research): integrated the
  policy, audited all glossary and candidate rows, ran back-translation,
  independently reopened primary sources, wrote the report and made all
  repository changes and commits.
- External reviewer (Claude): identified that the original rule assigned German
  ground-truth work to an owner who does not read German, before construction of
  the golden set began.
- Glossary-authorities subagent (OpenAI Codex, `/research` skill): read-only
  retrieval lane for Duden, DWDS, specialist primary authorities and official
  English publications. It returned a cited proposal and did not edit the tree.

### Multi-agent architecture

- Specialized delegation was used because the research skill requires a
  background primary-source lane while the main agent continued the ledger audit
  and policy work. The lane was limited to retrieval and divergence detection;
  the main agent remained the single writer and authority integrator.
- The subagent identified Duden's multiple senses for `Bauabnahme` and
  `Finanzierung`, the general-language overlap between `Kosten` and `Ausgaben`,
  specialist public-finance sources, three Berlin.de English publication paths,
  and DB/BVG English-site gaps. Its DWDS retrieval was blocked by robots policy.
- Accepted after independent reopening: the lexical ambiguities, specialist
  sources, Berlin.de pairs and the DWDS limitation. Modified: its pre-change
  74-row scope was expanded to the version-1.0 glossary's 88 rows, and English
  absence was reported as “not found in this pass,” not proof of nonexistence.
  Rejected: treating general dictionary synonymy, search-result agreement or an
  official-hosted machine translation as contextual validation.
- Independent check: the main agent reopened the cited Duden, Berlin.de,
  Destatis, Bundestag, Federal Ministry of Finance, DB and BVG sources; then
  recomputed report row, status, span and parallel-pair counts from the file.

### Work performed

- Added glossary version 1.0 and a date-qualifier/modal section that preserves
  bounds, direction, precision, confidence and as-of wording.
- Audited all 29 candidate rows against those qualifiers without editing the
  discovery ledger. No direct contradiction was found between quoted wording
  and a row's recorded milestone/date characterization; the ledger still lacks
  a typed qualifier field.
- Replaced owner authorship with human authorship as the golden-set invariant,
  added per-value provenance and recorded ADR-008.
- Checked 88 glossary rows, representing 87 distinct row labels because
  `geschätzt` appears in two sections. Results: 77 `agreed`, 6 `flagged` and 5
  `unresolved`. “Agreed” means only that consulted authorities did not diverge.
- Inspected 29 candidate rows. Twenty-eight contained a quoted German
  expected-end span group and were back-translated; C-026 had no quoted German
  expected-end span. Four of the 28 showed a material modal divergence.
- Found three project-specific German/English Berlin.de publication pairs
  (C-001, C-014 and C-019). No pair was found for the other 26 candidate rows;
  DB and BVG English sites existed but did not expose counterparts for the
  checked C-003, C-004 and C-005 publications.
- Added the verified-vocabulary premise to the README without claiming that the
  constraint has been overcome.

### Decisions

- The native-speaker queue is `Baubeginn`, `Bauabnahme`, `Kosten`,
  `Finanzierung`, `vorgesehen` and `soll`. No flagged glossary row was edited.
- Five terms remain `unresolved` because this pass retrieved no adequate
  authority for the complete term: `Ergänzungsunterlage zur Finanzierung`,
  `haushalterische Grundlage`, `finanziert aus dem Plätzeprogramm`,
  `Realisierungsverträge` and `Einbringungsverträge`.
- Back-translation and official-hosted English text are divergence detectors,
  not authorities. Three Berlin.de English pages were credited to automated
  translation and were not promoted to controlled glossary sources.
- Multiple model passes remain ineligible as golden-set validation regardless of
  agreement.

### Course correction

The original rule required the project owner to build the golden truth set by
hand from German source documents. It encoded the unexamined assumption that the
project owner could read German, which was never true. The assumption survived
21 commits and was caught in reviewer critique before any golden values were
constructed. The actual cost was documentation rework: the rule, role table,
ADR, README premise, verification report and build record had to be aligned.

Had the contradiction surfaced after golden-set construction, the
counterfactual cost would have been rebuilding affected values and invalidating
evaluation results derived from them. That did not happen; there was no golden
set or evaluation to rebuild. The controlled glossary and provenance design
bound the remaining risk but do not solve the owner's lack of German
comprehension.

### Verification

- Confirmed the glossary report has exactly 88 term rows: 77 `agreed`, 6
  `flagged` and 5 `unresolved`.
- Confirmed the back-translation appendix has 29 candidate rows, 28 completed
  span-group passes and one explicit source gap.
- Confirmed the parallel-text appendix has three German/English pairs and labels
  the remaining 26 as not found in this pass.
- Confirmed native-speaker review cells are empty and `docs/glossary.md` was not
  modified by the verification-report commit.
- Confirmed all five requested commits are focused and ordered:
  `309363d`, `32888b6`, `1a5ce5b`, `ba3de76`, then this disclosure commit.

### Failures and limitations

- The project owner cannot independently verify contextual German meaning.
  Project identity, boundary, applicable sense and disagreements between
  authorities remain outside the owner's comprehension.
- No native speaker has reviewed the glossary. Version 1.0 is therefore not
  eligible as a verified layer for `glossary-derived` golden values.
- DWDS pages could not be retrieved because of robots restrictions. Duden is a
  general-language dictionary and does not establish every domain-specific
  financial, planning or procurement sense.
- Back-translation used a model and is correlated with the system being bounded;
  agreement is not evidence of correctness.
- Official parallel English was sparse—3 pairs found, 26 absent in this pass—and
  the found English pages were official-hosted automated translations rather
  than controlled terminology.
- The ledger discrepancy—28 stored German span groups across 29 rows—must be
  resolved before claiming complete candidate-span coverage.

### Evidence

- `309363d` — glossary version and qualifier section
- `32888b6` — golden-set rule, provenance tags, ADR-008 and policy log
- `1a5ce5b` — 88-row glossary verification report and measured appendices
- `ba3de76` — public verified-vocabulary premise
- `docs/research/glossary-verification.md`
- `docs/project-checklist.md`, current handoff

## 2026-08-06 — Scope golden-set authorship and value provenance

**Status:** Complete

**Commit:** `32888b6` — `docs(process): scope golden-set authorship and add value provenance tags`

### Goal

Resolve the contradiction between owner-owned ground truth and the requirement
that a human understand the German source, while preserving the prohibition on
model-generated evaluation authority.

### Participants and scopes

- Project owner: disclosed the language constraint, chose human authorship rather
  than owner authorship as the invariant, and specified the permitted and
  prohibited operations.
- Main agent (OpenAI Codex): integrated the rule, role definition, ADR and public
  accountability record.
- Subagents: none contributed to this policy decision.

### Work performed

- Replaced owner authorship with human authorship as the binding golden-set rule.
- Added per-value provenance tags and prohibited `model-assisted` golden values.
- Defined the versioned, human-verified controlled glossary as the reusable layer.
- Separated agent operation of an authority from being the authority.
- Recorded the rejected multi-pass-AI option and the residual need for German
  comprehension in ADR-008.

### Decisions

- Accepted a human-verified glossary layer because recurring controlled terms can
  be versioned and audited without pretending that model agreement is validation.
- Rejected multiple AI passes as an independence mechanism because correlated
  systems reduce variance but do not remove shared bias.
- Retained German-speaking human review for contextual sense, project boundary,
  identity, disagreement and out-of-vocabulary decisions.

### Verification

- Cross-checked the role table, rule 1 and ADR-008 for the same authority boundary.
- Confirmed that the permitted operations are retrieval, divergence detection and
  verbatim matching, not contextual judgment.
- Confirmed that no golden value or candidate-ledger row was changed.

### Failures and limitations

- The glossary is not yet human-verified, so no value is currently eligible as
  `glossary-derived` ground truth.
- Provenance tags are policy only until the golden-set schema is implemented.
- The project owner still cannot independently resolve German contextual disputes.

### Evidence

- `AGENTS.md`, rule 1 and the roles table
- `docs/decision-log.md`, ADR-008
- `docs/glossary.md`, version 1.0

- 2026-08-06 — Codex: flipped the build log to newest-first and extracted its conventions. Verified: entry order follows Git commit order, the entry count is preserved, and moved prose is unchanged. `a00a129`
- 2026-08-06 — Codex: separated the candidate data ledger, frozen record specification and category coverage map. Verified: moved sections retain their prose and cross-references resolve. `356238f`
- 2026-08-06 — Codex: assigned stable candidate IDs C-001–C-029 to the discovery longlist, shortlist and provenance tables. Verified: 29 IDs, no gaps or duplicates, and ledger/trail names match. `e572bcf`
- **Course correction** -- 2026-08-06 — Claude review recomputed the final end-date gate column from the candidate ledger and caught a lane gate count that did not reconcile against its own source ledger. Corrected housing/mixed-use from 1 to 0 and total from 17 to 16; no repository rework, but the error was live in two commits. `a0baace`
- 2026-08-06 — Codex (skills CLI): ignored vendored third-party agent skills and retained `skills-lock.json` as the reproducibility record. Verified: a disposable fresh-clone simulation restored all 35 skill directories from the lockfile and matched the local `.agents/skills/` tree byte-for-byte. `681e9fc`

## 2026-08-06 — Named pilot-candidate discovery and end-date filter

**Status:** Complete; awaiting project-owner confirmation and selection

**Commit:** `3e70ad7` — `docs(research): name and filter pilot candidates`

### Goal

Replace the candidate ledger's category placeholders with named, geographically
bounded Berlin project leads, preserve the full discovery trail, and apply only
the cheapest hard finalist question: whether an official project-level expected
end date exists and what the exact German wording and milestone type are.

### Participants and scopes

- Project owner: froze the four discovery lanes, prohibited agent scoring and
  finalist selection, required full query/access trails and retains confirmation
  of project identity, German end wording and final-three selection.
- Main agent (Codex, web research and integration): froze the record, ran the
  utilities/environment lane, reopened all core identity links, deduplicated,
  applied eligibility/end-date gates, wrote the longlist, shortlist, glossary
  seeds and accountability record.
- Transport subagent (GPT-5.6-terra, high; Chrome fallback): roads, bridges,
  rail and transport infrastructure.
- Public subagent (GPT-5.6-terra, high): schools, public buildings, cultural
  facilities and public space.
- Development subagent (GPT-5.6-terra, high): housing, commercial redevelopment,
  demolition and mixed-use.
- Three initial GPT-5.6-sol/high subagent invocations were interrupted at the
  project owner's request before their output was accepted.

### Multi-agent architecture

- Delegation was used because the four category lanes were independent and the
  project owner explicitly requested multiple scouts with a research trail per
  lane. Each completed subagent was read-only and returned a proposal; only the
  main agent wrote the repository.
- Transport returned six leads and correctly rejected a bridge-closure date as
  project completion. Public returned eight leads and separated whole-project,
  phase-only and planning-stage milestones. Development returned eight leads
  and exposed that most official dates were phase-only, relative, stale or not
  typed as completion. The main agent returned seven utility/environment leads
  and separated duration wording from calendar end dates.
- Accepted: all 29 named identity leads, their source/access trails, explicit
  gaps and German terminology. Modified: confidence and eligibility were
  normalized against the frozen fields; linked subprojects were kept separate.
  Rejected: closure-only dates, programme-level dates presented as project ends,
  non-official developer dates, completed comparators, unbounded candidates for
  final eligibility and any inferred calendar date from a duration.
- Independent check: the main agent reopened all 29 core identity links. The DB
  Wollankstraße PDF that timed out in the lane opened during integration, but
  its date still described a closure rather than project completion.

### Work performed

- Froze the discovery record and the `found` / `not found` / `not checked`
  expected-end vocabulary before lane results were integrated.
- Named and bounded 29 candidates across four lanes with plausible official
  identity sources, explicit read-versus-inferred fields and one next check.
- Preserved every query, opened URL outcome, dead end, skipped source family,
  access barrier and cross-lane link in a dedicated research-trail document.
- Applied identity, construction-substance, geographic-boundary and end-date
  gates without assigning scores.
- Produced a four-project owner-review shortlist and retained every failed gate
  in the longlist with its reason.
- Added discovery seed rows for every consequential German milestone and
  financial term encountered. The glossary remains unconfirmed and is not
  marked complete.

### Lane performance

`Survived discovery gates` means identity, construction substance, an official
evidence path and a usable geographic boundary. `Survived final end-date gate`
also requires current project-level end wording; phase-only, programme-level,
closure-only and untyped period endpoints do not pass cleanly.

| Lane | Leads returned / requested | Core links open and identify project | Cited page did not support claim / project nonexistent | Survived discovery gates | Duplicates across lanes | Findable end-date evidence | Survived final end-date gate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Transport | 6 / 5–8 | 6 / 6 | 0 | 6 | 0 | 5 | 5 |
| Public buildings / culture / space | 8 / 5–8 | 8 / 8 | 0 | 6 | 0 | 8 | 6 |
| Utilities / energy / water / environment | 7 / 5–8 | 7 / 7 | 0 | 7 | 0 | 6 | 5 |
| Housing / commercial / mixed-use | 8 / 5–8 | 8 / 8 | 0 | 7 | 0 | 4 | 0 |
| **Total** | **29 / 20–32** | **29 / 29** | **0** | **26** | **0** | **23** | **16** |

Eight access-barrier paths were retained as source-registry seeds: a moved
Senate directory, CAPTCHA, an initial DB PDF timeout, an internal-error school
PDF, a timed-out legacy school page, a BWB PDF redirect to 404, a BEW PDF fetch
error and an internal-error Senate press page.

### What was surprising

The housing/mixed-use lane had abundant official identity and planning material
but almost no clean whole-project completion evidence. By contrast, operator
and transport pages often named `Inbetriebnahme`, `Bauende` or
`Gesamtfertigstellung` directly. The end-date-first filter therefore changed the
portfolio shape before any scoring: no development candidate entered the four,
even though several remain strong public-interest backlog items.

### Course correction

The first three delegated lanes were launched on GPT-5.6-sol/high. The project
owner stopped that choice because of credit use and asked that sol not be used
moving forward. Those invocations were interrupted, their partial work was not
accepted, and the same lanes were rerun on GPT-5.6-terra/high. Exact tokens and
cost are unavailable because the agent runtime exposes neither; no estimate was
invented. The correction cost was the aborted model usage and restart latency,
not repository rework. Browser fallback was then permitted for access failures.

### Decisions

- Shortlisted U3 to Mexikoplatz, Heinrich-Hertz-Gymnasium at Ostbahnhof, the
  HKW Mitte Power-to-Heat plant and Europaplatz Süd for owner review; no score
  was assigned.
- Kept a year-only public-space milestone as the spare despite weaker precision,
  because it is still official and project-level and adds a distinct public
  consequence.
- Did not force category balance by admitting a development lead that failed
  the frozen end-date or phase-boundary gate.
- Kept all non-shortlisted candidates and failed paths visible.

### Verification

- Reopened all 29 core identity links and confirmed that each names the claimed
  project; zero core citations failed the identity claim.
- Checked aliases and linked phases for overlaps; no returned rows were merged.
  Adjacent or linked projects are explicitly separated in the research trail.
- Confirmed no natural person is named in the candidate records or shortlist.
- Confirmed no closure notice is a candidate and no closure duration is stored
  as a project end date.
- Confirmed no score or golden-truth value was written.

### Failures and limitations

- Exact token and cost telemetry was unavailable for every lane. This remains
  an instrumentation gap before the first extraction run.
- A core identity page opening does not make every field current or
  authoritative. The project owner still needs to confirm the four identities,
  boundaries and exact German end wording before scoring.
- Source licensing, quote/retention rights, financial measures, organization
  roles, date history and dossier claims were intentionally not researched.

### Evidence

- `docs/research/candidate-ledger.md`
- `docs/research/candidate-record-spec.md`
- `docs/research/candidate-discovery-trail.md`
- `docs/glossary.md`
- `docs/project-checklist.md`
- **Course correction** — 2026-08-06 — Project owner and Codex: added skill/tool attribution and course-correction conventions, marked the ADR-006 stage mismatch, and gitignored private working notes. Verified: `notes/learning.md` is ignored and absent from Git status; diff check passes. `4d4e215`
- 2026-08-05 — Project owner: raised the bar for full build-log entries; documentation and planning work now gets a short entry. Recorded as ADR-007. `39be832`
- 2026-08-06 — Project owner and Codex: made spawned-agent orchestration mandatory in the build record, including failed, redundant and rejected lanes; preserved single-writer synthesis and verification. `39be832`

## 2026-08-06 — Rescope ADR-006 from candidate discovery to selected-project research

**Status:** Complete

**Commit:** `39be832` — `docs(process): raise build-log bar and rescope agent research`

### Goal

Correct the stage that the six-lane research workflow applies to. ADR-006 was drafted and recorded as covering candidate research and project intake generally, but the immediate task — turning category rows in the candidate ledger into named, addressed projects — needs a single identity lookup, not six lanes with claim extraction and cross-source synthesis.

### Participants and scopes

- Project owner: identified that the recorded ADR did not match what was intended by "six agents", and that approval was given to a build that was not the one needed.
- External reviewer (Claude): reviewed the three research artifacts and ADR-006,
  initially recommended deferring the ADR to Phase 5, then drafted the rescope
  separating lightweight candidate naming from six-lane selected-project
  dossier research after the project owner clarified the immediate need.
- Main agent (OpenAI Codex): reviewed the proposed rescope against the original
  ADR, corrected the remaining scope inconsistency and integrated the process
  documentation.
- Subagents: none used for this task.

### Multi-agent architecture

- This was sequential collaboration between the project owner, Claude as an
  external reviewer and Codex as the integrating main agent; no parallel
  subagents were spawned.
- Claude supplied an uncommitted working-tree draft of the rescope and amendment
  rationale. Codex inspected the full diff against the candidate ledger, prior
  orchestration record and repository policy, then corrected the stale context
  wording and dates before any commit.
- The project owner directed the scope correction and retains final acceptance
  of the integrated wording.

### Work performed

- Retitled ADR-006 from "per project intake" to "to research selected projects".
- Changed status from `Proposed for review` to `Accepted, rescoped`.
- Narrowed the scope statement to projects whose identity is already established, explicitly excluding candidate discovery and naming.
- Changed "Decision proposed" to "Decision" and reworded the opening line to apply after selection.
- Added an `Amended 6 August 2026` note recording what moved and why.

### Decisions

- Rejected the reviewer's initial recommendation to defer ADR-006 to Phase 5.
  The workflow belongs in Phase 1 dossier research once pilots are named, not
  in the preceding candidate-naming pass.
- Kept the six lanes themselves unchanged. Only the stage they apply to moved.
- Candidate naming will use a separate lightweight single-pass lookup rather than the full lane workflow.
- Retained the existing rule that agent output is a lead until the project owner verifies it against the original German source.

### Course correction

An agent produced a well-designed six-lane research system aimed at candidate
discovery and project intake generally. The project owner caught that the
workflow was aimed at the wrong pipeline stage: candidate naming needs a
lightweight identity lookup, while the six specialized lanes belong after a
project has been named and selected for dossier research. The mismatch was
caught before implementation. Its cost was one decision-log section and the
review time needed to rescope it; no pipeline code had to be discarded.

### Verification

- Re-read ADR-006 end to end after editing to confirm the title, status, scope, decision wording and amendment note agree with each other.
- Confirmed the lanes, consequences and reconsideration conditions were not altered.
- Confirmed the public record describes only project architecture,
  accountability and verification rationale.

### Failures and limitations

- The original ADR was recorded at a scope the project owner had not intended, and approved before that mismatch was noticed. Cost was one decision-log section, caught before any implementation work followed from it.
- The lightweight candidate-naming pass is not yet specified or run; the candidate ledger still contains category rows rather than named projects.
- Claude edited the shared working tree directly, which crossed the repository's
  reviewer/single-writer convention. No concurrent edit or commit occurred;
  Codex reviewed and integrated the complete diff. Future reviewer changes
  should be proposed for the main agent to apply.

### Evidence

- `docs/decision-log.md`, ADR-006
- 2026-08-05 — Claude: backfilled build-log entries for `e029383` and `f5fb60b` (both previously un-logged or left `Commit: Pending`), added `**Amended**` notes to ADR-003 and ADR-004, and added a "log at commit time, not after" rule to `AGENTS.md`. Verified: reviewed and approved by the project owner. `03e9deb`

## 2026-08-05 — Clarify evaluation-gate and 3D-sequencing wording

**Status:** Complete

**Commit:** `f5fb60b` — docs(decisions): clarify evaluation gates and 3D sequencing

### Goal

Close two review findings against the newly recorded ADR-003 and ADR-004: the 99% evaluation targets read as firm commitments rather than provisional release hypotheses, and ADR-004's reconsideration clause had no floor, meaning a persuasive argument could pull 3D work into the first release ahead of its fixed date.

### Participants and scopes

- Project owner: reviewed both findings and asked for the wording fixed without a commit.
- External reviewer (Claude): identified the two findings during a decision-log review, drafted the replacement wording for ADR-003 and ADR-004 in place.
- Main agent (OpenAI Codex): committed the reviewed wording.
- Subagents: none used for this task.

### Work performed

- ADR-003: reworded the three 99% figures as targets rather than fixed thresholds, called out the unsupported-claims rule as the one true zero-tolerance invariant, and added that the release publishes its real measured numbers, including below-target ones, rather than withholding launch until targets are hit.
- ADR-004: added a floor to the reconsideration clause — the trigger conditions may be noted before the first release, but do not pull 3D work forward into it regardless of how compelling they look mid-sprint.

### Decisions

- Accepted both wording changes as drafted; the underlying decisions in ADR-003 and ADR-004 did not change, only their precision.
- Treated this as a clarification of the existing ADRs rather than a new ADR, since no decision reversed.

### Verification

- Re-read both ADRs end to end after editing to confirm the Decision and Reconsider-when sections no longer contradict the Context section's hedging language.
- Confirmed via `git diff` that no other ADR content was touched.

### Failures and limitations

- This edit was not recorded in this log at the time it was committed; it is being backfilled now. See the entry above for the same gap on `e029383`.

### Evidence

- `docs/decision-log.md`
- 2026-08-05 — Claude: drafted `docs/methodology.md` (evidence labels, financial-measure and milestone definitions, publication thresholds, status rules, correction process), cross-referencing the existing ADRs rather than duplicating them. Verified: reviewed against README, decision log and feature register for consistency; approved by the project owner. `af0e412`

## 2026-08-05 — Research plan: source availability as a product differentiator

**Status:** In progress

**Commit:** `1accf13` — `docs(research): define source discovery orchestration`

### Goal

Design the first research pass for selecting three pilot projects while preserving the complexity of finding and verifying fragmented public information.

### Participants and scopes

- Project owner: reviewed the initial orchestration results and decided that source availability and discovery difficulty should be treated as core product value, not merely a research obstacle.
- Main agent (OpenAI Codex): coordinated six bounded, read-only Luna research tasks and synthesized their outputs.
- Luna research agents: one selection-rubric task, one official-source ecosystem map, three category-specific candidate scans, and one adversarial bias review.
- Claude: reserved for deeper finalist dossier review after the candidate pool and rubric are frozen.

### Decisions

- Agents will produce a broad candidate pool; they will not independently select the final three projects.
- The scoring rubric will be frozen before candidates are scored.
- Source availability and researchability will be scored separately from public value and research importance.
- The candidate pool will deliberately include projects whose public evidence is fragmented, difficult to discover, scanned, moved, or distributed across agencies and document types.
- The first three projects should form a balanced set: at least one bounded case, one complex multi-source case, and one hard-to-discover public-information case.
- The source-ecosystem map is a first-class research output. It should show where project identity, dates, budgets, procurement, planning, contracts, geometry and updates are actually found.
- Every candidate, exclusion reason, failed search path, dead or inaccessible source and unresolved gap should be retained in the research record.
- A candidate will not be rejected merely because its information is difficult to find; it will be rejected when the evidence cannot be recovered or verified within the release scope and rules.

### Verification

- Six Luna reports were returned as research proposals; no agent edited files, committed, or selected the final projects.
- The reports identified official-source families including Berlin Senate and district pages, procurement platforms, TED, budget and parliamentary records, operator pages, Geoportal/Open Data and planning records.
- The adversarial review identified famous-project, source-availability, survivorship, authority and selection-leakage biases.
- Candidate examples were treated as preliminary discovery leads, not verified project dossiers.

### Failures and limitations

- Agent-reported dates, budgets and URLs still require direct source verification.
- The candidate pool is not yet frozen and no pilot project has been selected.
- The methodology draft was approved by the project owner and pushed as `af0e412`; the research plan itself remains uncommitted.

### Next step

Freeze the scoring rubric and source-discovery record before conducting deeper finalist research.
## 2026-08-05 — Pilot-selection and source-ecosystem research artifacts

**Status:** Proposed for project-owner review

**Commit:** `bdafec9` — `docs(research): add pilot selection and source ecosystem artifacts`

### Goal

Turn the preliminary multi-agent research outputs into reviewable Phase 0
artifacts for selecting three pilots without treating agent-reported facts as
verified research.

### Participants and scopes

- Project owner: supplied the scope, retained final selection and
  golden-truth authority, and must review the proposed artifacts.
- Main agent (OpenAI Codex): inspected the repository and existing policy
  documents, checked a limited set of official source entry points, and drafted
  the three research files and this proposed log entry.
- Prior multi-agent research outputs: preliminary leads only; no agent selected
  a winner, edited the golden truth set or verified candidate claims.

### Work performed

- Drafted hard eligibility and final-selection gates for project-owner review,
  intended to freeze the pilot process once accepted.
- Drafted a weighted 0–100 rubric with expected end-date evidence as the largest
  user-facing dimension.
- Separated source availability from public usefulness and recorded controls for
  source-availability, famous-project and public-usefulness bias.
- Mapped official Berlin source families across identity, dates, finance,
  procurement, planning, geospatial data, updates and oversight.
- Created a cross-category candidate ledger without selecting final projects.

### Decisions

- Proposed retaining difficult-to-research candidates rather than excluding
  them automatically.
- Proposed requiring a supported expected end date, or a supported statement
  that no expected end date is published, before final selection.
- Proposed treating official entry-point checks as source-family verification,
  not as verification of candidate-level facts or licensing permissions.

### Verification

- Confirmed the repository was clean on `main` before editing.
- Read `README.md`, `AGENTS.md`, `docs/project-checklist.md`,
  `docs/decision-log.md` and `docs/methodology.md`.
- Confirmed that `docs/research/source-discovery-orchestration.md` is absent;
  its available content is represented only by prior build-log and decision-log
  entries and was not reconstructed as if it were a verified file.
- Opened a limited set of official Berlin entry points for procurement, budget,
  parliamentary, planning, geospatial and Open Data discovery. Candidate-level
  claims remain unverified.

### Failures and limitations

- The prior multi-agent reports were not present as standalone files in the
  repository, so the ledger uses their recorded source families and preliminary
  leads without asserting their reported facts.
- No candidate has a manually verified dossier, final score or selection
  decision.
- Source retention, quotation, database rights, personal-data handling and
  machine-access conditions still require project- and dataset-specific review.

### Project-owner feedback incorporated for review

- Missing expected-end-date evidence remains exactly 0 in the rubric, but an
  undated observation can remain in a separate research backlog instead of
  being discarded.
- Public usefulness is framed around affected-place context and disruption,
  not an artificial exact headcount.
- Road closures and lane restrictions were added as a distinct candidate
  category because they directly affect residents and traffic users.
- Research-agent discoveries are proposed to flow into a human-owned backlog;
  agents still do not select pilots or edit the golden truth set.

### Evidence

- `docs/research/pilot-selection-criteria.md`
- `docs/research/source-ecosystem.md`
- `docs/research/candidate-ledger.md`
- `docs/research/candidate-record-spec.md`
- Existing research record in this document and proposed source-specialization
  workflow in `docs/decision-log.md`, ADR-006.
## 2026-08-05 — Project-level multi-agent source discovery

**Status:** Superseded

**Commit:** `1accf13` — `docs(research): define source discovery orchestration`

### Goal

Define how the system researches a project after it is proposed by the system, selected from the candidate pool, or added by the project owner or a future user.

### Decision proposed

Each project intake should trigger five or six lightweight, read-only research lanes with distinct source responsibilities:

1. Official project identity, authority and current project pages.
2. Procurement, tender, award and contract-lot records from Berlin and TED.
3. Budgets, investment plans, parliamentary records and oversight documents.
4. Planning, approvals, environmental records and geospatial sources.
5. Operator, district, construction-update and disruption sources.
6. Independent corroboration, contradiction and missing-source discovery.

Each lane returns structured source candidates, extracted claims, exact evidence spans, dates, source metadata, confidence and unresolved gaps. Agents do not publish, edit the golden truth set, or select the final project. A stronger review model handles ambiguity and cross-source synthesis after the lanes finish; lightweight models handle bounded discovery, extraction and deduplication.

### Project-intake inputs

- Candidate name and aliases.
- Address, district, coordinates or affected route.
- Organizations and known roles.
- Category and lifecycle hypothesis.
- User-submitted text, sign details or external identifiers where available.
- Discovery timestamp and origin: system candidate, owner-selected or user-submitted.

### Verification

- All lane outputs are proposals until checked against the original source.
- The system preserves failed searches, dead links, inaccessible documents, contradictions and duplicate sources.
- Claims are deduplicated by source identity and content hash before synthesis.
- The project owner establishes the golden truth values from the German source material.
- Human review is required before a project or consequential claim becomes public.

### Consequences and open questions

- Source discovery becomes repeatable across selected and user-submitted projects.
- Six lanes reduce blind spots caused by relying on a single agency or source type.
- The workflow increases model calls, so cost per project and diminishing returns must be measured.
- Source lanes may overlap; the schema must preserve provenance while deduplicating claims.
- We still need to define the exact structured output schema, stop conditions, retry policy and whether all six lanes run for every project or whether simple projects can use fewer lanes.

**Superseded 6 August 2026** — the lane design remains accepted for named,
selected-project dossier research, but no longer applies to candidate naming.
See “Rescope ADR-006 from candidate discovery to selected-project research.”
## 2026-08-05 — Record initial architecture and policy decisions

**Status:** Complete

**Commit:** `e029383` — docs(decisions): record initial architecture and policy ADRs

### Goal

Record the five decisions needed to begin implementation without leaving architecture and publication rules implicit.

### Participants and scopes

- Project owner: confirmed that implementation should begin collaboratively and approved the decision-log step.
- Main agent (OpenAI Codex): drafted and cross-checked the ADRs against `AGENTS.md`, `README.md` and the project checklist.
- External reviewer (Claude): supplied the release-sequencing, German-first, naming-policy and evaluation recommendations that informed the decisions.
- Subagents: none used for this task.

### Decisions

- Preserve German source wording and translate only at the display layer.
- Name organizations by documented role and exclude natural persons from v0.
- Separate precision-critical quality gates from recall and report human review.
- Ship the accessible 2D public product before advanced 3D.
- Use the small typed v0 stack already specified in `AGENTS.md`, with the pipeline running locally until the first release.

### Verification

- Confirmed each ADR has context, decision, consequences and reconsideration conditions.
- Confirmed the stack matches `AGENTS.md`.
- Confirmed the checklist next action advances to methodology.

### Failures and limitations

- Metric thresholds remain proposals until the manually verified pilot set exists.
- Legal and privacy requirements still require authoritative review before launch.

### Evidence

- `docs/decision-log.md`
- `docs/project-checklist.md`
- 2026-08-05 — Codex: extracted the complete feature register, moved the blueprint binary to `~/Documents/berlin-blueprint-private`, removed recruitment framing and replaced the public history. Verified: one commit, no DOCX in history and no recruitment-framing hits. `6a84726`

## 2026-08-05 — Initialize local Git repository

**Status:** Complete

**Commit:** `6a84726` — docs: establish project foundation

### Goal

Place the project under local version control and prevent machine-specific or sensitive local files from entering the first commit.

### Participants and scopes

- Project owner: authorized connecting the workspace to Git.
- Main agent (OpenAI Codex): initialized the repository, reviewed untracked files and added ignore rules.
- Subagents: none used for this task.

### Work performed

- Initialized a Git repository with `main` as the initial branch.
- Added `.gitignore` rules for macOS metadata, local AI-tool settings, environment files, dependencies, generated output, logs and editor settings.
- Preserved the project blueprint as an untracked project file pending the first-commit decision.
- Updated the project checklist.

### Decisions

- Kept `.claude/settings.local.json` out of version control because it is machine-specific configuration.
- Kept `.DS_Store` out of version control.
- Did not create a GitHub remote or make a commit because those are separate steps and Git author identity is not currently configured in this repository.

### Verification

- Confirmed the repository is on `main` with no commits.
- Confirmed ignored local files no longer appear as commit candidates.

### Failures and limitations

- No Git remote is configured.
- Git author name and email still need to be configured before the first commit.

### Evidence

- `.git/`
- `.gitignore`
- `docs/project-checklist.md`
- `docs/how-this-was-built.md`
## 2026-08-05 — Product planning and release sequencing

**Status:** Complete

**Commit:** `6a84726` — docs: establish project foundation

### Goal

Turn the product blueprint into an honest README and an operational build sequence suitable for a first public release.

### Participants and scopes

- Project owner: provided the blueprint, established the expected-end-date priority, requested a persistent checklist and approved revising the delivery strategy.
- Main agent (OpenAI Codex): reviewed the blueprint, drafted the README and checklist, integrated review feedback and maintained the workspace documents.
- External reviewer (Claude): reviewed the initial plan for delivery risk, release timing, German terminology, publication precision, legal-risk boundaries and AI-development disclosure.
- Subagents: none used for this task.

### Work performed

- Created the initial project README from the blueprint.
- Made expected completion date a primary user-facing question.
- Created a living project checklist.
- Reframed the initial release around three verified projects, bounded AI evaluation and a 2D map.
- Deferred advanced 3D work to a distinct later milestone.
- Added a transparent process for recording AI-agent assistance.

### Decisions

- Accepted the recommendation to target a small public vertical slice before expanding coverage.
- Accepted German-first extraction with controlled translation at the display layer.
- Accepted separate precision and recall measures instead of one blended accuracy score.
- Accepted deterministic evidence-span enforcement for published claims.
- Accepted organization-by-role naming and exclusion of natural persons for v0 as a cautious product policy.
- Modified the ten-project starting scope to three projects for the first release, expanding toward ten afterward.
- Treated legal assertions from the review as research leads requiring authoritative verification before launch.

### Verification

- Compared the review feedback with the original blueprint, README and checklist.
- Checked that planned features remain described as future work rather than completed implementation.
- Checked that the revised order preserves the evidence-first product thesis.

### Failures and limitations

- The repository has not yet been initialized as Git, so no commit hash exists.
- Technology choices and metric thresholds remain proposals until prototypes and pilot data provide evidence.
- German legal, privacy and source-reuse requirements have not yet been verified against authoritative guidance.

### Evidence

- `README.md`
- `docs/project-checklist.md`
- `docs/how-this-was-built.md`
