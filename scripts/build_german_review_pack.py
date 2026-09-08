"""Build an unverified review inventory from public facts; never read private data."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/research/glossary-review/app-v1"


def words(text: str) -> int:
    """Count whitespace tokens containing a Unicode letter or digit."""
    return sum(any(c.isalnum() for c in token) for token in text.split())


def glossary_rows(text: str) -> list[dict]:
    rows = []
    section = ""
    for line in text.splitlines():
        if line.startswith("## "):
            section = line[3:]
        if not line.startswith("| `"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        rows.append(dict(id=f"G{len(rows) + 1:03}", section=section,
                         german=cells[0], proposed_english=cells[1],
                         distinction=cells[2], aliases=re.findall(r"`([^`]+)`", cells[0])))
    return rows


def matches(alias: str, text: str) -> bool:
    return re.search(r"(?<!\w)" + re.escape(alias) + r"(?!\w)", text, re.I) is not None


def inventory(projection: dict, glossary: list[dict]) -> tuple[list[dict], list[dict]]:
    passages = {}
    excluded = []
    for project in projection["projects"]:
        conflicts = {fid for c in project["conflicts"] for fid in c["memberFactIds"]}
        for fact in project["facts"]:
            if fact["state"] != "published":
                excluded.append({"fact_id": fact["factId"], "reason": fact["reasonCode"]})
                continue
            evidence = fact["evidence"]
            key = (project["projectId"], evidence["sourceUrl"], evidence["exactTextDe"])
            if key not in passages:
                passages[key] = dict(
                    id=f"P{len(passages) + 1:03}", project_id=key[0], source_url=key[1],
                    exact_text_de=key[2], source_id=evidence["sourceId"],
                    publication_date=evidence["publicationDate"], facts=[],
                    glossary_ids=[g["id"] for g in glossary if any(matches(a, key[2]) for a in g["aliases"])],
                    exception_reasons=[], word_count=words(key[2]),
                )
            row = passages[key]
            row["facts"].append({"fact_id": fact["factId"], "app_field": fact["factType"],
                                 "translation_state": fact["translationState"]})
            if fact["factId"] in conflicts:
                row["exception_reasons"].append("existing_conflict_member")
            if project["projectId"] == "C-010" and fact["factType"] == "milestone":
                row["exception_reasons"].append("documented_c010_milestone_context_question")
    return list(passages.values()), excluded


def csv_text(rows: list[dict], fields: list[str]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fields)
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def main() -> None:
    projection_path = ROOT / "public/data/projects.json"
    glossary_path = ROOT / "docs/glossary.md"
    glossary = glossary_rows(glossary_path.read_text())
    passages, excluded = inventory(json.loads(projection_path.read_text()), glossary)
    used_ids = {gid for p in passages for gid in p["glossary_ids"]}
    used = [g for g in glossary if g["id"] in used_ids]
    exceptions = sum(bool(p["exception_reasons"]) for p in passages)
    routine = len(passages) - exceptions
    counts = dict(projects=len({p["project_id"] for p in passages}),
                  published_facts=sum(len(p["facts"]) for p in passages),
                  withheld_facts_excluded=len(excluded), passages=len(passages),
                  source_words=sum(p["word_count"] for p in passages),
                  distinct_text_words=sum(words(s) for s in {p["exact_text_de"] for p in passages}),
                  glossary_rows_total=len(glossary), matched_glossary_rows=len(used),
                  matched_german_term_words=sum(words(" ".join(g["aliases"])) for g in used),
                  passages_with_literal_match=sum(bool(p["glossary_ids"]) for p in passages),
                  routine_passages=routine, exception_passages=exceptions)
    # Planning assumptions only; a timed human review must establish actual rates.
    low = 10 + len(used) * 1 + routine * 2 + exceptions * 5
    high = 20 + len(used) * 3 + routine * 5 + exceptions * 15
    payload = dict(status="unverified-review-preparation", glossary_version="1.1",
                   inputs={str(p.relative_to(ROOT)): "sha256:" + hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (projection_path, glossary_path)},
                   counts=counts, assumed_minutes_range=[low, high],
                   glossary=used, passages=passages, withheld=excluded)
    outputs = {"inventory.json": json.dumps(payload, ensure_ascii=False, indent=2) + "\n"}
    review = [dict(passage_id=p["id"], project_id=p["project_id"],
                   fact_ids=";".join(f["fact_id"] for f in p["facts"]),
                   source_url=p["source_url"], exact_text_de=p["exact_text_de"],
                   review_category="exception" if p["exception_reasons"] else "routine",
                   REVIEW_english="", REVIEW_milestone_or_measure="", REVIEW_scope="",
                   REVIEW_date_and_qualifiers="", REVIEW_verdict="", REVIEW_notes="",
                   REVIEW_minutes="") for p in passages]
    outputs["passage-review.csv"] = csv_text(review, list(review[0]))
    terms = [dict(glossary_id=g["id"], german=g["german"],
                  passage_ids=";".join(p["id"] for p in passages if g["id"] in p["glossary_ids"]),
                  REVIEW_english="", REVIEW_scope_of_reuse="", REVIEW_verdict="",
                  REVIEW_notes="", REVIEW_minutes="") for g in used]
    outputs["term-review.csv"] = csv_text(terms, list(terms[0]))
    OUT.mkdir(parents=True, exist_ok=True)
    # Never overwrite a reviewer's answers, including partially completed files.
    for name, content in outputs.items():
        path = OUT / name
        if path.exists() and path.read_bytes() != content.encode():
            raise SystemExit(f"Refusing to overwrite changed review pack: {path}")
    for name, content in outputs.items():
        (OUT / name).write_bytes(content.encode())
    print(json.dumps({"counts": counts, "assumed_minutes_range": [low, high]}, indent=2))


if __name__ == "__main__":
    main()
