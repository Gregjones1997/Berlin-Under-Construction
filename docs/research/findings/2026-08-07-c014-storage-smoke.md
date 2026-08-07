# C-014 storage reconstruction smoke — 2026-08-07

This is a neutral integration observation, not a golden evaluation and not an
accuracy measurement. The committed dossier was read only after the frozen
prompt, storage implementation and generated fragment existed. Neither the
dossier nor `evaluation/` was changed.

- Live retrieval reproduced the configured response hash:
  `sha256:36d47e13604b30115339bd75090a452296d9ebd1f8919bf9cf2440299070f4f5`.
- A retrieval record, retained artifact and one milestone proposal survived a
  close/reopen cycle in the ignored private SQLite store.
- Storage-only reconstruction withheld the proposal because it is unreviewed,
  unverified and lacks complete supporting evidence. This is the intended
  fail-closed result; it is not evidence that the stored claim is correct.
- Smoke status: `differences_observed`.
- Committed dossier observation:
  `sha256:97fe870dc32277a6afaf262056de312567603a9ece617580259f9d9aed2ccdc9`.
- Generated fragment observation:
  `sha256:f15498da78f9b3d2b121973b1b57f28cf7c98f7afd128c46b4ab80fe8061b5b1`.

The raw retained bytes, generated fragment and unified diff remain under ignored
private paths. No percentage or scored comparison was computed. A complete
dossier reconstruction remains blocked on the first real metered extraction and
human review of any resulting claim.
