# Batch research queue

The queue expands preparation beyond the three published dossiers. It is an
internal research tool, not an automatic publication path or an accuracy evaluator.
It runs locally and makes no model-provider calls. No recurring scheduler is set up.

## Run

From the repository root with the documented Python environment installed:

```sh
.venv/bin/python -m pipeline.research_queue \
  --screening docs/research/findings/2026-09-08-seven-candidate-screening.json \
  --locations docs/research/findings/2026-09-09-candidate-location-proposals.json \
  --refresh
```

Omit `--refresh` to check the original retained artifacts without network requests.
Private artifacts must be present for that mode; a clean clone reports missing
artifacts instead of treating their sources as verified. Output is always in
ignored `build/research-queue/`: JSON queue, Markdown review report and a linked
HTML map. Serve that directory locally to inspect it. Never deploy this directory.
The public website and its three accepted dossiers are untouched.

## What scales

Add screened candidate entries with stable IDs, canonical German names, source
URLs, dates, hashes, exact excerpts, scope notes and review questions. One command
rechecks the entire batch. Shared URLs are fetched once per successful batch;
retained artifacts are content-addressed. HTML inline formatting does not split
words; block boundaries become spaces. Exact passage matching is not interpretation.

Existing retrieval controls enforce HTTPS, host allowlists, redirect limits, byte
limits and User-Agent retry. Browser-required results remain explicit follow-ups;
the queue never labels them human-only or silently drops a failed project. Hosts
for the already-screened BVG and DB sources are now allowed transport destinations.
That allowlist is not an endorsement of every claim on those hosts.

A changed hash with intact excerpts still routes to changed-document review.
Missing excerpts and transport failures remain visible. Location coordinates must
match an exact retained marker tag and its content hash. Coordinates are proposals,
not approvals. The location preview does not infer construction boundaries from
map centers or school-campus coordinates.

## Publication path

1. Check current evidence and project scope in the generated queue.
2. Resolve map geometry scope: a bridge map center, a campus, a station and a route
   are different geographic claims.
3. Prepare reviewed identity, category and location facts plus correction links.
   Schedule/status claims continue through the existing fact publication gates.
4. Apply actual human review decisions through the existing approval process.
5. Add eligible facts/geometry to the public projection and map; verify the export.

A later research-pending public layer can show reviewed identity/category/location
while full dossier research continues. It must not present unreviewed coordinates,
a model's interpretation or research progress as construction status. The current
queue intentionally emits no public records and grants no publication decisions.
