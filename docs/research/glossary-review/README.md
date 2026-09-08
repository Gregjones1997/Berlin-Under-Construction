# German glossary review package v1.0

**8 September follow-up:** The [app-linked pack](app-v1/README.md) narrows initial
review to the current public facts, with reproducible counts, blank answer sheets
and an explicitly assumed time estimate. This broader 95-row package remains
unverified; the reviewer description below is a template, not evidence that a
reviewer has been recruited or has completed work.

## Project in three sentences

Berlin, Under Construction is an independent, source-backed map explaining what is being built across Berlin, who is responsible, what was promised, and what changed. Source claims are extracted and stored in German, with short evidence spans and links back to the publishing authority. English is a display layer only: this review checks whether the proposed display wording preserves distinctions in the German rather than replacing it.

## Reviewer record

- **Reviewer ID and role:** Reviewer A, native German speaker
- **Relevant qualification:** REVIEWER TO COMPLETE — qualification only; do not provide a name
- **Review date:** REVIEWER TO COMPLETE as `YYYY-MM-DD`

This public repository never records the reviewer's name. Please keep that name out of the CSV, filename, notes, comments, and returned email subject; the pseudonymous record above is the complete public identity.

## Review workflow — avoid anchoring on our proposal

The `our_proposed_english` column is supplied for audit, but reading it first can anchor the answer. Please use this two-pass workflow:

1. In your spreadsheet, hide column D (`our_proposed_english`) before reading any data rows.
2. Read `german_term`, `context_source`, and `distinction_we_are_trying_to_preserve`. Write your own English wording in `REVIEW_better_english` first. If the context does not support one answer, record that rather than guessing.
3. Unhide column D, compare our proposal with your independently written wording, and then complete `REVIEW_verdict`, `REVIEW_notes`, and `REVIEW_confidence`.

`correct` means the proposal loses no material distinction in the supplied context; it does not merely mean that the English sounds plausible. `ambiguous-in-context` and `needs-more-context` are useful, first-class results. Ambiguity is evidence about the source and schema, not a review failure; flagging it is more useful than guessing.

## C-010 priority question

Filter `id` for `PRIORITY-C010`. Five source formulations describe what may or may not be one event: `Fertigstellung und Übergabe`, `Fertigstellung`, `technische Übergabe`, `bauliche Fertigstellung` together with `Übergabe an den Bezirk`, and `Endfertigstellung`. Review both each row and the cluster as a whole: do these denote one completion event, several distinct milestones, or is the relationship ambiguous from the supplied contexts?

This adjudication blocks C-010 milestone typing. Until a qualified human resolves it, the project will not assert one English milestone type for these German terms. Two priority rows—`technische Übergabe` and `Endfertigstellung`—postdate the glossary v1.0 verification table and therefore show `not in glossary v1.0 verification pass`; that is a missing check, not a negative dictionary finding.

## Columns

| Column | Meaning |
| --- | --- |
| `id` | Stable row identifier. Values beginning `PRIORITY-C010` should be reviewed first. |
| `german_term` | Canonical German glossary term. |
| `context_source` | Source context or the repository records that supplied the row. A “not found” statement is scoped to the documented verification pass. |
| `our_proposed_english` | Project's unverified display proposal. Hide this during the first review pass. |
| `distinction_we_are_trying_to_preserve` | Descriptive statement of distinctions the German separates from neighbouring terms or events. It is not a requested verdict. |
| `duden_dwds_status` | What the existing glossary v1.0 authority-retrieval pass established. `D` means a standalone Duden article; `S` means exact search or component evidence without a standalone article for the complete phrase; `A` means a specialist primary authority. `DWDS blocked` means the retrieval service's robots policy blocked the page, not that the entry is absent. |
| `REVIEW_verdict` | Choose exactly one: `correct`, `wrong`, `ambiguous-in-context`, or `needs-more-context`. |
| `REVIEW_better_english` | Your independent English display wording. Complete this before revealing our proposal; it may remain empty if no wording is supportable. |
| `REVIEW_notes` | Explain lost distinctions, ambiguity, or missing context. Ambiguity is a valid and useful result. |
| `REVIEW_confidence` | Your confidence in the contextual judgment; use a consistent scale and define it in the first note where used. |

## Package scope and return check

The CSV contains all 95 rows in `docs/glossary.md` version 1.1, including both section-specific occurrences of `geschätzt`. It is left-joined to all 88 rows in the version 1.0 term table at `docs/research/glossary-verification.md:96`; the seven later glossary rows are retained with an explicit missing-pass marker rather than dropped or assigned an invented status. The filename is the reviewer-package version requested for this round; it does not rename either source document's version.

Before returning the file, confirm that every non-empty verdict is one of the four allowed values and that no natural person's name appears anywhere. Preserve UTF-8 and the header row. The distributed CSV uses a UTF-8 byte-order mark, CRLF line endings, and quoting on every field for broad spreadsheet compatibility.
