# Approved Phase 2 typed schemas

**Status:** Approved by the project owner 2026-08-07; Python types not yet implemented
**Date:** 2026-08-07
**Scope:** Claim, source and extraction-run boundaries for the three pilot projects

This proposal preserves the source's German wording, separates source tier from
organization role, and makes every publication decision reproducible without a
model at render time. It does not assign organization roles and does not turn the
frozen dossiers into golden truth.

## Shared identifiers and versioning

- IDs are opaque stable strings: `project_id`, `source_id`, `artifact_id`,
  `claim_id`, `extraction_run_id` and `review_decision_id`.
- Every stored record carries `schema_version`, `created_at` and an immutable
  content or record version. Corrections append; they do not overwrite history.
- Dates use ISO 8601 only when the source supports that precision. Year, season,
  month, range and relative anchor remain distinct typed values.
- German source wording is canonical. English display text is derived later from
  a named, human-verified glossary version.

## Claim schema

Every claim has this common envelope:

```text
Claim
  claim_id, project_id, schema_version
  claim_kind: milestone | financial | status | scope | organization_observation
  canonical_value_de
  source_id, artifact_id
  evidence_spans[]
  qualifiers[]
  confidence
    score: decimal 0.0..1.0
    source: extractor
    threshold_config_version
  extraction_run_id?          # absent for manually entered claims
  review_state
  validation_results[]
  relations[]                 # confirms | contradicts | supersedes
  publication_eligibility: eligible | blocked | review_required | quarantined
  verification_state: verified | unverified
  created_at
```

`evidence_spans` contain exact German text plus a stable locator: page and
bounding box for PDF, or selector plus character offsets for HTML. The saved
span is checked against the retained private artifact. High-confidence personal
data fails validation; a possible name that is not a known organization or
toponym routes to review. A forbidden span is rejected rather than silently
redacted because redaction would no longer preserve an exact evidence span.

`qualifiers` is a stored list, not display formatting. It uses closed classes:
`upper_bound`, `lower_bound`, `approximation`, `range`, `modal_intent`,
`source_stated_unreliability`, and `as_of_hedge`, retaining the exact German
token. Every qualifier also carries `applies_to: amount | date | scope | status`
so `bis zu` on an amount cannot be confused with `bis` on a date. This is
sufficient to compute ADR-009's precision marker without a model.

`confidence.score` is the extractor's declared probability on a closed 0.0–1.0
scale, recorded with the threshold-configuration version used for routing. It
can route a claim to review but can never make a claim publishable by itself.
Missing, malformed or below-threshold confidence routes to review; no default is
guessed.

`relations` never chooses a winner for an unreconciled conflict. Supersession
requires evidence for ordering; different values alone do not establish it.

### Milestone claim

```text
MilestoneClaim extends Claim
  claim_kind: milestone
  milestone_type              # mandatory; no default
  milestone_term_de           # exact source noun or phrase
  object_scope                 # what reaches the milestone
  date_value
    precision: exact_day | month | season | half_year | year | range | relative_anchor
    canonical                 # source wording, including anchor/qualifier
    normalized_start: EvidenceField<Date>
    normalized_end: EvidenceField<Date>
    relative_anchor?
      wording_de
      resolved_date: EvidenceField<Date>
      resolution_authority_source_id: EvidenceField<SourceId>
```

Any claim carrying a `date_value` is invalid unless `milestone_type` is present.
Resolution never replaces a relative anchor; it adds a derived date and the
authority that resolves it. Terms such as `Fertigstellung`, `technische
Übergabe`, `bauliche Fertigstellung` and `Inbetriebnahme` remain distinct.

### Financial claim

```text
FinancialClaim = ActiveFinancialClaim | QuarantinedFinancialClaim

FinancialClaimBase extends Claim
  claim_kind: financial
  measure_type                # mandatory; no generic cost default
  amount
    value, currency
    lower_bound?, upper_bound?
  scope                       # mandatory non-empty German scope string
  tax_treatment: EvidenceField<gross | net>
  price_basis: EvidenceField<string>
  as_of_date: EvidenceField<Date>
  budget_reference: EvidenceField<string>

ActiveFinancialClaim extends FinancialClaimBase
  publication_eligibility: eligible | blocked | review_required
  quarantine: forbidden

QuarantinedFinancialClaim extends FinancialClaimBase
  publication_eligibility: quarantined
  verification_state: unverified
  quarantine
    reason
    scope_relation: superset | subset | overlapping | disjoint | unknown
    assigned_by_review_decision_id
```

The initial measure vocabulary distinguishes original estimate, approved
budget/cost, current forecast, awarded contract value, contract amendment,
expenditure to date, final cost and financing commitment. Unknown or conflicting
scope first routes to review. A reviewer may then quarantine a correctly
extracted figure that does not describe the project's cost. A quarantined claim
retains its exact evidence span, German scope string and source; remains
`unverified`; is never rendered as the project's cost; is never dropped; and is
shown on the dossier as an explicitly excluded figure.

`scope_relation` describes the source-published scope relative to the project
boundary. It is assigned by a human during review and is stored but not rendered.
It must never be model-derived. A source-published approximation or upper bound
is a qualifier, not quarantine. An exact value with incompatible scope is not
converted into an inferred approximation or derived bound.

Financial claims are never summed unless an independent human-reviewed
relationship establishes non-overlap; v0 stores no inferred sum.

### Status, scope and organization observations

- Status claims require `as_of_date: EvidenceField<Date>` and an evidence span.
  `delayed` additionally requires a relation to the previously
  supported milestone or a source's own explicit delay statement.
- Scope claims retain the exact boundary wording and included/excluded/linked
  object. A different scope produces ADR-009's `scope-divergent` state.
- Organization observations store the organization and the source's exact
  relationship wording only. They contain no normalized role until the role
  vocabulary ADR is accepted. Source tier is stored on the source record and is
  never reused as an organization role. A source's publisher is not an
  organization observation; it exists only on the `Source` record.

## Conflict schema

```text
Conflict = SupersededConflict | UnreconciledConflict | ScopeDivergentConflict

ConflictBase
  conflict_id, project_id, schema_version
  key
    project_id
    measure_type
    scope_normalized
  member_claim_ids[]          # at least 2
  resolved_by_review_decision_id?

SupersededConflict extends ConflictBase
  state: superseded
  promoted_claim_id           # required
  supersession_evidence       # required

UnreconciledConflict extends ConflictBase
  state: unreconciled
  promoted_claim_id: forbidden
  supersession_evidence: forbidden

ScopeDivergentConflict extends ConflictBase
  state: scope_divergent
  promoted_claim_id: forbidden
  supersession_evidence: forbidden
```

The conflict record, rather than pairwise claim relations alone, computes
ADR-009's marker for two or more members. The tagged union makes promotion
structurally impossible in `unreconciled` and `scope_divergent` states.

## Optional evidence-bearing fields

Every optional field whose value would require evidence uses the same wrapper:

```text
EvidenceField<T>
  status: not_checked | verified | not_stated | unresolved
  value?: T                   # present only when verified
  provenance[]
```

`not_checked` is the default initial state. It remains distinct from
`not_stated`, which means the relevant evidence was checked and the source did
not state a value.

## Source and artifact schema

```text
Source
  source_id, schema_version
  artifact_id
  canonical_url, observed_urls[]
  publisher_name
  source_tier
  publication_date: EvidenceField<Date>
  retrievals[]
  access_barriers[]

Retrieval
  retrieved_at, request_url, final_url
  http_status?, outcome
  user_agent_class: default | browser
  retry_number, failure_detail?
  artifact_id?

Artifact
  artifact_id, media_type, byte_length
  retained_private: true
  hash_algorithm: sha256
  pre_transform_response_hash # private chain of custody only
  stored_content_hash         # the only identity and dedupe key
  transform_rule_version      # recorded per artifact
  transform_verification
  extracted_pdf_timestamps: EvidenceField<PdfTimestamps>
```

Publication date is a verified field with its own provenance. Letterhead text
may be retained as evidence but cannot populate the verified value by itself.
`not_checked`, `not_stated` and `unresolved` remain distinct. Retrieval failures,
redirects, 403 responses and browser-User-Agent retries remain data.

Source merging is triggered by equality of `stored_content_hash`, never by URL
normalization. `canonical_url` and `observed_urls[]` are descriptive and are not
identity keys. `request_url` and `final_url` preserve redirects without claiming
that a redirect demonstrates content-hash deduplication.

ADR-011 is accepted. PDFs are rewritten with an object-graph-aware tool,
re-parsed, and retained only if forbidden metadata is no longer reachable. The
transform must be idempotent. For HTML and media with no metadata transform, an
identity transform and rule version are still recorded; both hashes then exist
and are equal. `pre_transform_response_hash` is never displayed or used as a
foreign key. `ExtractionRun.artifact_hash` and all content addressing use
`stored_content_hash`.

## Extraction schema

```text
ExtractionRun
  extraction_run_id, schema_version
  source_id, artifact_id, artifact_hash # stored_content_hash only
  provider, model, model_version
  prompt_version, extraction_schema_version
  started_at, completed_at, duration_ms
  input_tokens, output_tokens, cached_tokens?
  cost_amount, cost_currency, pricing_reference
  raw_output_private
  parse_status: valid | malformed
  proposed_claims[]
  validation_results[]
```

Malformed output is rejected as a whole; missing types or scopes are not
defaulted. Each proposed claim preserves its exact German span next to the
normalized value. The first extraction run records tokens, cost and duration per
document. Prompt/model output is untrusted data and cannot alter configuration,
validation rules or publication state.

## Deterministic publication and review states

Validation produces stable codes rather than free-text-only outcomes:

- `missing_evidence_span` → fail, cannot publish
- `personal_data_high_confidence` → hard fail, cannot publish; deterministic
  patterns include email addresses, honorific plus capitalized token, `gez.` and
  `i. V.`
- `possible_personal_name` → route to review and never publish unreviewed; a
  capitalized bigram matching the organization/toponym allowlist does not fire
- `missing_milestone_type` → fail, route to review
- `unresolved_financial_scope` → fail, route to review; a reviewer may apply
  `quarantine`
- `claim_conflict` → route to review; preserve every claim
- `below_confidence_threshold` → route to review; never drop
- `missing_or_invalid_confidence` → route to review; never default
- `malformed_extraction_output` → reject run

Publication eligibility is `eligible` only when every blocking validation passes
and an accepted reviewer decision exists where review was required. The review
history is append-only and records `accept`, `reject`, `correct`, `defer` or
`quarantine`, the actor class, timestamp, prior state and rationale. Quarantine
is terminal publication eligibility: the claim remains visible as an explicitly
excluded figure but cannot render as the project's value. Review records do not
store a natural person's name.
