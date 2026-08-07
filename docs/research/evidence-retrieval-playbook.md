# Evidence retrieval playbook

**Status:** Operational research guidance. Derived from the 2026-08-06 pilot evidence pass.
**Audience:** Any agent or person doing source research for this project.

This is a map of where evidence actually lives in the Berlin public record and
how to get it out intact. It is not a log of one session. Everything here was
established by retrieval, and the failures are recorded alongside the
techniques because the failures are what generated most of the rules.

---

## 1. Before anything: what you are and are not

You may **operate** any authority. You may not **be** the authority.

Retrieving a dictionary entry, a statutory holiday order, an official parallel
text, or a parliamentary answer is permitted and encouraged. Deciding which
dictionary sense applies, assigning a milestone type that enters the golden
set, or resolving a disagreement between two authorities is not. Divergence you
detect is a question for a human, never an answer.

Practical consequence: when you hit something that looks like a judgment call,
check first whether an authority publishes the answer. Often one does, and the
question dissolves. `Schuljahresbeginn 2026/27` looked like a German-reading
judgment; it is set statutorily and took one retrieval.

---

## 2. The source ladder

The 2026-08-06 evidence pass found projects published at up to five depths.
The most exact financial evidence in the cases tested lived at 4 and 5.

| Depth | Source | Gives you | Watch for |
| --- | --- | --- | --- |
| 1 | Project page | Status label, fact box, headline date | Undated fields; mislabelled fields |
| 2 | Press release | Narrative, rounded figures, organizations | `rund`; no budget reference |
| 3 | Programme index `Aktuelles` | A different text, often extra figures | Volatile |
| 4 | Schriftliche Anfrage | Status, cost tables, "is it on time" | Split tables |
| 5 | Hauptausschuss-Vorlage | Exact figures, tax basis, budget titles, approval dates | Length; typos |

**Rule: before recording a financial measure or `not found` for a date or
cost, check whether depths 4 and 5 cover the project. Search them when relevant;
otherwise record that the depth is inapplicable or unavailable.**

In the 2026-08-06 pass, depths 4 and 5 supplied C-010's quarantined construction
cost, C-014's three funding sources and approved total, and C-014's official
planning-approval date. They did not resolve every open field or every project.

---

## 3. Where things are

### Senate and district

- Press releases are **mirrored at two paths** and serve byte-identical
  content: `/sen/sbw/presse/pressemeldungen/…` and
  `/sen/stadt/presse/pressemeldungen/…`. Dedupe by hash, not URL.
- Programme index pages (`…/berliner-plaetzeprogramm/`) carry an `Aktuelles`
  block of dated items that are **separate publications** from the press
  releases and sometimes carry figures the press release omits.
- Always look for the release *before* the one you were given. In this pass a
  2023-06-26 release predated the known 2023-10-12 one and moved the change
  history back six months.

### Parliament

- Schriftliche Anfragen:
  `pardok.parlament-berlin.de/starweb/adis/citat/VT/{WP}/SchrAnfr/S{WP}-{nr}.pdf`
- Hauptausschuss papers:
  `parlament-berlin.de/adosservice/{WP}/Haupt/vorgang/h{WP}-{nr}-v.pdf`
- Both are directly fetchable. Neither needs a session. Both are signed by
  named officials — **cite the document, never the signatory.**
- The PARDOK STARWEB search UI is hostile to automation. Finding document
  numbers via a domain-restricted web search and then fetching the PDF directly
  is faster and more reliable than driving the search form.

### Delivery bodies

- Operator and Bauherr pages (HOWOGE, BEW, BVG, BWB, DB) carry fact boxes with
  `Bauzeit`, `Bauherr`, addresses, and timeline sections. Primary for their own
  project where the body is the documented Bauherr.
- Host splits are common: `www.howoge.de` and `unternehmen.howoge.de` serve
  overlapping paths, and the press URL that search engines return may 404 while
  the project page resolves.

### Participation and planning

- `mein.berlin.de/vorhaben/{id}/` gives boundary, participation history and a
  cost field that is frequently `offen` — a real "not published" datapoint, not
  a blank to fill.

### Reference sources

- Statutory instruments resolve relative anchors. The Ferienordnung resolves
  `Schuljahresbeginn`. Register these by the term they resolve, not by project,
  and reuse them across dossiers.

### Journalism

- Useful as a finding aid and nothing else. It points at primary documents
  reliably and cannot carry a figure: in this pass, two articles about the same
  project gave construction costs 34 million euros apart.
- Beware machine-translated agency copy on official domains. A `berlin.de/en/`
  news page carried the byline `Author: dpa/deepl.com`. It looks like official
  parallel English text and is not — it is agency copy, machine-translated,
  hosted by the city. It does **not** qualify as authority-published parallel
  text.

---

## 4. Getting the bytes out intact

**Fetch raw, extract yourself.** A summarizing fetch paraphrases German.
Verbatim spans must be extracted from raw HTML or PDF text, or string
comparison against the source is meaningless.

**Treat HTTP 403 as a possible User-Agent block.** Retry with a full browser
User-Agent; if that fails use a browser tool. Never escalate a 403 to a human
as a manual task without trying both. PARDOK and `berlin.de/suche` behaved
this way during the evidence pass.

**Use a real PDF parser.** A regex-over-decompressed-streams approach produces
mangled spacing that looks like text and is not quotable. If you cannot use a
proper parser, mark the extraction unreliable and say so in the dossier.

**Read PDF metadata — carefully.**
- `/CreationDate` and `/ModDate` resolve disputed publication dates. In this
  pass a document with letterhead `6. Oktober 2026` had `/CreationDate`
  `D:20251014…`, confirming a year typo.
- `/Author` may contain a named official's email address. Rule 3 has no
  exceptions. Do not record or display it. ADR-011 requires object-graph-aware
  metadata stripping and a successful post-strip re-parse before retention.
- Metadata timestamps are **provenance, not publication**. A creation timestamp
  corroborates a date; it does not publish one.

**Keep the two hash roles separate.** Frozen dossier registries record SHA-256
over raw response bytes (`pre_transform_response_hash`) for historical chain of
custody. Retained artifact identity and deduplication use only SHA-256 over the
post-transform bytes (`stored_content_hash`). For HTML the recorded transform is
the identity transform, so the two values are equal. For stripped PDFs they are
expected to differ. Never reconcile one into the other silently.

**An empty Wayback CDX result is a finding.** No archive of a page means its
undated fields are unverifiable by any member of the public. That is
publishable, not a dead end.

---

## 5. Reading a source without breaking it

**Reunite tables with their headers and footnotes.** A number in a table cell
is meaningless without its column header and can be actively misleading without
its footnote. In this pass, `107.300.000` needed the header `Gesamtkosten (€)`
to be typed at all, and needed the footnote stating that sports-hall costs are
included to reveal that it cannot be attached to the project as bounded.

**One document can contain several statements of the same milestone at
different force and precision.** A single Hauptausschuss paper stated
completion three times: `Fertigstellung geplant für Sommer 2026`, then
`Die Baumaßnahme wird im Sommer 2026 abgeschlossen werden`, then
`Die Fertigstellung der Baumaßnahme wird voraussichtlich in 2026 erfolgen`.
Picking "the" date from such a document is arbitrary. Record all of them.

**A source's own field label can contradict its own value.** A project page
labelled a field `Gesamtkosten:` and gave the value
`finanziert aus dem Plätzeprogramm: 1.900.000 €` — a total-cost label over a
funding-share value. Storing that as `Gesamtkosten` introduces a type error
that came from the source's layout, not from the data.

**A source can contradict itself on roles.** One page's fact box read
`Bauherr:` / `ZECH Hochbau AG` while its body called the same firm
`der beauftragte Generalübernehmer`.

**Scope words are load-bearing.** `Teilbereich`, `Das Vorhaben umfasst`,
`Ergänzend`, `mit Sporthalle`, `perspektivisch` each redrew a project boundary
in this pass. `Ergänzend` in particular marks something as adjacent to an
enumerated scope, not inside it.

**Match exact figures across documents.** Exact-string matching is a cheap,
deterministic diagnostic. A `1.900.000 €` on a project page matching a
`Verpflichtungsermächtigungen 2026 (Entwurf): 1.900.000,00 €` line in a budget
paper is not a coincidence — it is a hypothesis worth flagging, without
asserting the causal claim.

**Verify publication dates; never read them off the letterhead.**

**Never accept a summarizer's factual claim about a date.** In this pass a
search summary asserted the Berlin 2026/27 school year begins 31 August. The
statutory Ferienordnung gives 24 August. The wrong answer happened to match the
project's current target date and would have erased a one-week movement in the
change history entirely. **Confirmation-shaped errors are the dangerous ones**
because nothing in the output looks wrong.

---

## 6. Recording

- `found` / `not found` / `not checked` are three different states. A
  `not found` is only worth recording if it names what was searched. C-019's
  absent change history is evidence because BEW, 50Hertz, PARDOK and open web
  were each checked and named.
- Preserve failed paths, dead links and access barriers. They are part of the
  record.
- Mark every value read-from-source versus inferred.
- Never sum. Never infer "over budget". Never infer contractor responsibility
  for a delay.
- Never name a natural person, including in a span you would otherwise quote
  verbatim, and including in file metadata.
- Nothing an agent produces is a golden-set value.

---

## 7. The thing worth internalising

The project's thesis shows up in the evidence, not in the framing, and both
times it did so in this pass it took going one rung deeper than felt necessary.

One pilot has a completion year on a public page that no member of the public
can date, next to a cost figure that appears to be a programme-wide commitment
authorization displayed as a single project's total. Another has an official
cost figure that cannot be attached to the project because its scope silently
includes a sports hall built elsewhere by someone else.

Neither is a researcher's mistake. Both are what the public record actually
looks like. An agent optimising for a filled-in field would have recorded both
numbers, confidently, with a citation, and been wrong twice.

The discipline that catches this is not general skepticism about sources. It is
refusing to let a field label, a table cell, or a rounded press figure stand in
for the document that generated it.
