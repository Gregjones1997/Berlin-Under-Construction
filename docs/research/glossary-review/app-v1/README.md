# App-linked German review pack

Prepared 8 September 2026 from the committed public projection and glossary 1.1.
This is an unverified inventory, not a golden set or a new source-verification pass.
It supplements the broader 95-row pack in the parent directory.

## Measured inventory

| Item | Count |
| --- | ---: |
| Existing projects | 3 |
| Published facts / distinct source-linked passages | 20 / 20 |
| Words in supplied German excerpts | 184 |
| Glossary rows with literal evidence matches | 16 of 95 |
| German words in those row aliases | 25 |
| Passages with at least one literal glossary match | 13 of 20 |
| Routine / exception passages | 17 / 3 |
| Withheld facts excluded from passage review | 6 |

Words are whitespace tokens containing a letter or digit; numbers count and
punctuation-only tokens do not. Distinct excerpt texts also total 184 words.
The 25 term words are a separate task count, not additional unique source words.
Matching is case-insensitive with word boundaries, preserving overlapping glossary
rows and separate senses. There is no stemming, translation or contextual inference.
Seven unmatched passages remain in the review pack; a match never approves a meaning.

Each inventory passage links its source URL, source publication date, app fact ID,
field type and current translation state. Proposed English glossary text is copied
unchanged into `inventory.json` and remains unverified. Current public acceptance
does not establish independent semantic verification for evaluation.

## Review procedure

1. Work on copies of `term-review.csv` and `passage-review.csv`. Record a pseudonymous
   reviewer ID, relevant language/domain competence, glossary version and review
   date in an accompanying note; do not supply a personal name.
2. Start with the blank answer sheets. Use passage IDs to find source context.
   Write independent English wording and interpretations before inspecting the
   proposed mappings in `inventory.json`. The pack is not held-out evaluation data.
3. Check scope, dates and qualifiers as well as wording. Use `correct`, `wrong`,
   `ambiguous-in-context` or `needs-more-context` when comparing an explicit proposal;
   identify that proposal in notes. Blank responses are pending, not approvals.
4. For a glossary decision, state the permitted scope of reuse. For passage review,
   assess that actual context; dictionary or glossary matching alone is insufficient.
5. Log time separately for setup, term decisions, routine passages, exception
   passages and additional source reading. Keep ambiguous cases unresolved.

**Context limit:** These are the short excerpts already approved for public
display, not complete documents. Open the linked source when a fragment is
insufficient; record additional reading time and request context when unavailable.
The pack does not cover private withheld details or all historical dossier text.
In particular, the full C-010 five-term question remains in the parent review pack.
No retained source document has been copied into this package.

The three initial exception passages are the two existing C-014 financial conflict
members and C-010's milestone passage, based on the documented contextual question.
This routes attention without resolving either issue. The other 17 passages are
not known to be easy or correct; reviewers can reclassify them as exceptions.

## Unvalidated planning estimate

| Non-overlapping task | Count | Assumed minutes each | Subtotal minutes |
| --- | ---: | ---: | ---: |
| Setup | 1 | 10–20 | 10–20 |
| Glossary decisions | 16 | 1–3 | 16–48 |
| Routine contextual checks | 17 | 2–5 | 34–85 |
| Exception contextual checks | 3 | 5–15 | 15–45 |
| Initial pack total | | | **75–198** |

These rates are deliberately explicit planning inputs, not observed reviewer
speeds or sourced industry benchmarks. The estimate is roughly **1¼–3⅓ hours**
for this pack under those assumptions. Additional source retrieval/reading,
uncovered historical questions and newly discovered exceptions are outside that
range and must be added. This is not an estimate for verifying all three dossiers,
the entire glossary or seven new projects. Repeated wording still needs contextual
assessment; no review-time saving or accuracy result has been demonstrated.

Time a small sample spanning the categories, revise the rates and count remaining
work before relying on the estimate. Glossary decisions and contextual checks are
different tasks; do not charge the same review interval to both.

## Reproduction and boundaries

Run `python3 scripts/build_german_review_pack.py` from the repository. Input hashes
are recorded in the inventory. Output is deterministic; the script refuses to
overwrite changed files so reviewer answers cannot be silently erased. Changed
inputs require a deliberately versioned new pack after preserving review returns.

The generator reads only `public/data/projects.json` and `docs/glossary.md`.
Withheld facts contribute only IDs and public reason codes. It changes no app
facts, review decisions, glossary meanings or golden answers and makes no provider
or network calls. Verification tests cover withheld-data exclusion, literal-match
boundaries and preservation of multiple app references to one passage.
