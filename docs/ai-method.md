# AI method: recorded run, failed attempt and limits

**Evidence checked:** 2026-08-19  
**Scope:** Public Gate 5 prose and figures; no accuracy claim

The retained private store contains one completed extraction run for one C-014
source document. This is a record of one stored run, not a count of every
historical provider request. The repository does not establish a total
provider-call count, so none is published here.

## Completed run

The completed run used `gpt-5.6-luna` and produced a proposed milestone that was
routed to human review rather than directly to publication.

| Recorded measure | Value |
| --- | ---: |
| Uncached input tokens | 3 |
| Cached input tokens | 17,682 |
| Output tokens | 1,053 |
| Recorded cost | USD 0.00161784 |
| Recorded latency | 10,017 ms |

The stored input total is 17,685 tokens: 3 uncached plus 17,682 read from cache.
Cache-write input tokens are recorded as zero. The cache read demonstrates that
a prefix was reused. It does **not** establish which earlier request primed that
cache. That priming request is unestablished, and no origin or total historical
request count is inferred from it.

These are provider-accounting and elapsed-time observations from the stored
run. They are not measures of extraction quality.

## Failed attempt on 13 August 2026

A later authorized request on 13 August returned an incomplete response. The
adapter rejected it as `provider_response_incomplete`. The attempt produced no
stored extraction run and no stored claim, and it is not counted or described
as a successful run.

The response was discarded before that version of the adapter captured safe
usage and latency. Its token use, cost, latency and incomplete cause therefore
cannot be recovered from the repository. The 2,000-output-token cap then in
force was a plausible diagnosis candidate, not an established cause. No retry
was made without fresh authorization.

The adapter was subsequently corrected so a future authorized call can preserve
content-free usage, cost, latency, incomplete reason and rejection details even
when the provider response is incomplete or has an invalid output shape. Such a
response still exits nonzero and is not written to the append-only extraction
run or claim tables. The correction is prospective: it does not reconstruct the
missing 13 August accounting, establish that attempt's cause, or turn a failed
attempt into a completed run.

## What has and has not been demonstrated

As of 19 August 2026, the current repository suite passes **164 tests**. Those
tests cover schemas, storage, evidence and publication gates, adapter behavior,
the public projection, static export, and leak scans. A passing engineering test
suite does not evaluate whether model extractions are correct.

No accuracy, precision or recall result exists. The scored golden set is empty,
so the project has no basis for any extraction-quality percentage or comparative
model claim. Human review of a proposed claim establishes that claim's
publication decision; it does not create a model-level accuracy measurement.

## Evidence trail

- The completed-run figures are reproduced from the append-only private
  `extraction_runs` record for C-014. The artifact and provider response remain
  private.
- The 13 August incomplete-response record and the later adapter correction are
  documented in [`how-this-was-built.md`](how-this-was-built.md#2026-08-13--attempt-the-authorized-c-014-one-shot)
  and
  [`how-this-was-built.md`](how-this-was-built.md#2026-08-13--preserve-accounting-from-failed-extraction-calls).
- The adapter's fail-closed behavior is implemented in
  [`pipeline/openai_provider.py`](../pipeline/openai_provider.py) and exercised
  by `tests/pipeline/test_openai_provider.py` and
  `tests/pipeline/test_extract_once.py`.
- The 164-test figure is the full local `pytest` result on 2026-08-19 before
  this prose-only change; it is rechecked at the session close.
