"""Batch source checks for candidate research; never publishes facts or calls a model.

The screening ledger is input, not a set of approvals. Rechecks are deterministic
against retained bytes. A successful exact-span check is not semantic validation.
"""
from __future__ import annotations

import argparse
import hashlib
import html
from html.parser import HTMLParser
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable
from urllib.parse import urlsplit

from pipeline.retrieval import retrieve_artifact, RetrievalError, BrowserToolRequired
from pipeline.artifacts import ArtifactPreparationError
from pipeline.retrieval_config import load_retrieval_config

ROOT = Path(__file__).resolve().parents[1]


def normalized_text(raw: bytes) -> str:
    class Text(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.parts = []
            self.hidden = 0
        def handle_starttag(self, tag, attrs):
            if tag in {"script", "style"}: self.hidden += 1
            if tag in {"p", "div", "br", "li", "td", "h1", "h2", "h3"}: self.parts.append(" ")
        def handle_endtag(self, tag):
            if tag in {"script", "style"}: self.hidden = max(0, self.hidden - 1)
            if tag in {"p", "div", "li", "td", "h1", "h2", "h3"}: self.parts.append(" ")
        def handle_data(self, data):
            if not self.hidden: self.parts.append(data)
    parser = Text()
    parser.feed(raw.decode("utf-8"))
    return " ".join("".join(parser.parts).split())


def check_source(source: dict, artifact_dir: Path, fetch: Callable | None = None) -> dict:
    url = urlsplit(source["url"])
    if url.scheme != "https" or not url.hostname or url.username or url.password:
        raise ValueError("source URL must be public HTTPS")
    expected = source["content_hash"]
    if not re.fullmatch(r"sha256:[a-f0-9]{64}", expected):
        raise ValueError("invalid source content hash")
    result = {"url": source["url"], "screened_hash": expected,
              "publication_date": source["publication_date"], "screened_on": source["retrieved_on"]}
    try:
        if fetch:
            retrieved = fetch(source["url"])
            if retrieved.artifact.media_type != "text/html":
                return dict(result, status="unsupported_screening_format", spans=[])
            raw = retrieved.artifact.stored_bytes
            digest = hashlib.sha256(raw).hexdigest()
            artifact_dir.mkdir(parents=True, exist_ok=True)
            (artifact_dir / (digest + ".html")).write_bytes(raw)
            result["retrieved_at"] = datetime.now(timezone.utc).isoformat()
            result["attempts"] = [dict(status=a.status_code, outcome=a.outcome,
                                       user_agent=a.user_agent_class) for a in retrieved.attempts]
        else:
            raw = (artifact_dir / (expected[7:] + ".html")).read_bytes()
            digest = hashlib.sha256(raw).hexdigest()
            if "sha256:" + digest != expected:
                return dict(result, status="artifact_hash_mismatch", spans=[])
        text = normalized_text(raw)
        spans = [{"exact_text_de": span, "present": " ".join(span.split()) in text}
                 for span in source["spans"]]
        if not spans or not all(s["present"] for s in spans):
            status = "evidence_changed"
        elif "sha256:" + digest != expected:
            status = "source_changed_spans_present"
        else:
            status = "screened_spans_present"
        return dict(result, status=status, content_hash="sha256:" + digest, spans=spans)
    except BrowserToolRequired:
        return dict(result, status="browser_followup_required", spans=[])
    except (OSError, UnicodeError, RetrievalError, ArtifactPreparationError) as exc:
        return dict(result, status="retrieval_failed", failure_type=type(exc).__name__, spans=[])


def build_queue(screening: dict, artifact_dir: Path, fetch: Callable | None = None) -> dict:
    seen = set()
    sources = {}
    candidates = []
    for candidate in screening["candidates"]:
        pid = candidate["project_id"]
        if not re.fullmatch(r"C-\d{3}", pid) or pid in seen:
            raise ValueError("invalid or duplicate candidate id")
        seen.add(pid)
        if not candidate["sources"]:
            raise ValueError("candidate must cite a screened source")
        checks = []
        for source in candidate["sources"]:
            key = (source["url"], source["content_hash"], tuple(source["spans"]))
            if key not in sources:
                sources[key] = check_source(source, artifact_dir, fetch)
            checks.append(sources[key])
        blockers = ["location_evidence_needed", "scope_and_publication_review_needed"]
        if any(s["status"] not in {"screened_spans_present", "source_changed_spans_present"} for s in checks):
            blockers.insert(0, "source_followup_needed")
        if any(s["status"] == "source_changed_spans_present" for s in checks):
            blockers.insert(0, "changed_document_review_needed")
        candidates.append({"project_id": pid, "name_de": candidate["name_de"],
                           "state": "research_pending", "map_eligible": False,
                           "blockers": blockers, "location_assessment": candidate["location_assessment"],
                           "review_questions": candidate["review_questions"], "sources": checks})
    return {"schema_version": 1, "purpose": "internal-research-queue-not-publication",
            "mode": "live_refresh" if fetch else "retained_artifact_check",
            "summary": {"candidates": len(candidates), "map_eligible": 0,
                        "source_followups": sum("source_followup_needed" in c["blockers"] for c in candidates)},
            "candidates": candidates}


def attach_locations(queue: dict, proposals: dict, artifact_dir: Path) -> None:
    by_id = {c["project_id"]: c for c in queue["candidates"]}
    seen = set()
    for location in proposals["locations"]:
        url = urlsplit(location["source_url"])
        if url.scheme != "https" or not url.hostname or url.username or url.password:
            raise ValueError("location URL must be public HTTPS")
        pid = location["project_id"]
        if pid not in by_id or pid in seen:
            raise ValueError("unknown or duplicate location candidate")
        seen.add(pid)
        digest = location["content_hash"]
        if not re.fullmatch(r"sha256:[a-f0-9]{64}", digest):
            raise ValueError("invalid location hash")
        raw = (artifact_dir / (digest[7:] + ".html")).read_bytes()
        if hashlib.sha256(raw).hexdigest() != digest[7:]:
            raise ValueError("location artifact hash mismatch")
        tag = location["exact_location_tag"]
        if tag not in raw.decode("utf-8"):
            raise ValueError("location evidence missing")
        for field, attr in [("longitude", "long"), ("latitude", "lat")]:
            match = re.search(r'data-marker-' + attr + r'="([0-9.]+)"', tag)
            if not match or float(match[1]) != location[field]:
                raise ValueError("coordinate does not match evidence")
        if not 13.0 < location["longitude"] < 14.0 or not 52.3 < location["latitude"] < 52.8:
            raise ValueError("location outside Berlin review extent")
        c = by_id[pid]
        c["location_proposal"] = location
        c["blockers"].remove("location_evidence_needed")
        c["blockers"].append("location_scope_review_needed")
    queue["summary"]["source_located_proposals"] = len(seen)


def render_map(queue: dict, boundary: dict, provenance: dict) -> str:
    rings = [ring for f in boundary["features"] for polygon in f["geometry"]["coordinates"] for ring in polygon]
    coords = [p for ring in rings for p in ring]
    lo, hi = min(p[0] for p in coords), max(p[0] for p in coords)
    bottom, top = min(p[1] for p in coords), max(p[1] for p in coords)
    def point(lon, lat):
        return (30 + (lon-lo)/(hi-lo)*740, 30 + (top-lat)/(top-bottom)*540)
    paths = []
    for ring in rings:
        paths.append('<path d="M' + ' L'.join(f'{x:.2f},{y:.2f}' for x,y in [point(*p[:2]) for p in ring]) + ' Z"/>')
    markers, cards = [], []
    for c in queue["candidates"]:
        pid, name = html.escape(c["project_id"]), html.escape(c["name_de"])
        loc = c.get("location_proposal")
        if loc:
            x,y = point(loc["longitude"],loc["latitude"])
            markers.append(f'<a href="#{pid}" aria-label="Review {name}"><circle cx="{x}" cy="{y}" r="15"/><text x="{x+20}" y="{y+5}">{pid}</text></a>')
            location = html.escape(loc["scope"].replace("_", " "))
        else:
            location = 'Location still needed — not drawn'
        sources = ''.join(f'<li><a href="{html.escape(s["url"],quote=True)}">Source</a> · {html.escape(s["status"])}</li>' for s in c["sources"])
        if loc:
            sources += f'<li><a href="{html.escape(loc["source_url"],quote=True)}">Location source</a></li>'
        questions = ''.join(f'<li>{html.escape(q)}</li>' for q in c['review_questions'])
        cards.append(f'<article id="{pid}"><small>RESEARCH PENDING · {pid}</small><h2>{name}</h2><p>{location}</p><ul>{sources}</ul><details><summary>Review questions</summary><ul>{questions}</ul></details></article>')
    return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Berlin research queue</title><style>body{background:#f3f1eb;color:#28332e;font:16px/1.6 system-ui;margin:0;padding:24px;max-width:1100px;margin:auto}h1{font:44px Georgia}a{color:#8c431e}svg{width:100%;height:auto;max-height:60vh}path{fill:#e2e5db;stroke:#859282;stroke-width:1}circle{fill:#f3f1eb;stroke:#c56635;stroke-width:3;stroke-dasharray:4 2}text{font:16px monospace;fill:#28332e}article{padding:22px;border-top:1px solid #b9c0b4;scroll-margin-top:20px}article:target{background:#f5e4d5}small{letter-spacing:1px}summary{cursor:pointer;min-height:44px}h2{font:25px Georgia}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}</style><h1>Berlin · research queue</h1><p>'+str(len(queue['candidates']))+' candidates. '+str(sum('location_proposal' in c for c in queue['candidates']))+' source-located proposals. None newly approved for publication.</p><p>Dashed markers are research locations, not construction-status claims. C-009 is only an approximate campus reference.</p><svg viewBox="0 0 800 600" role="img" aria-label="Candidate location proposals within Berlin">'+''.join(paths+markers)+'</svg><p><a href="'+html.escape(provenance['datasetUrl'],quote=True)+'">'+html.escape(provenance['license']['attribution'])+'</a></p><div class="grid">'+''.join(cards)+'</div></html>'


def render_report(queue: dict) -> str:
    lines = ["# Candidate research queue", "", "Internal preparation only. No publication approvals or model calls.", "",
             "| Candidate | Source checks | Next steps |", "| --- | --- | --- |"]
    for c in queue["candidates"]:
        checks = ", ".join(sorted({s["status"] for s in c["sources"]}))
        lines.append(f'| {c["project_id"]} — {c["name_de"]} | {checks} | {", ".join(c["blockers"])} |')
    for c in queue["candidates"]:
        lines += ["", f'## {c["project_id"]} — {c["name_de"]}', "", c["location_assessment"], ""]
        lines += ["- " + q for q in c["review_questions"]]
        lines += [f'- [Source]({s["url"]}): {s["status"]}' for s in c["sources"]]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--screening", type=Path, required=True)
    parser.add_argument("--locations", type=Path, help="Source-backed proposals, never approval decisions")
    parser.add_argument("--refresh", action="store_true", help="Fetch current sources; no model calls")
    args = parser.parse_args()
    screening = json.loads(args.screening.read_text())
    config, _ = load_retrieval_config(ROOT / "pipeline/config/retrieval.v1.toml")
    # Fetch each distinct URL once per batch, even when projects share a source.
    cache = {}
    def fetch(url):
        if url not in cache:
            cache[url] = retrieve_artifact(url, config)
        return cache[url]
    queue = build_queue(screening, ROOT / "data/artifacts", fetch if args.refresh else None)
    if args.locations:
        attach_locations(queue, json.loads(args.locations.read_text()), ROOT / "data/artifacts")
    output = ROOT / "build/research-queue"
    output.mkdir(parents=True, exist_ok=True)
    (output / "queue.json").write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n")
    (output / "queue.md").write_text(render_report(queue))
    (output / "index.html").write_text(render_map(queue, json.loads((ROOT / "public/data/map/berlin-boundary.geojson").read_text()), json.loads((ROOT / "public/data/map/berlin-boundary.provenance.json").read_text())))
    print(json.dumps(queue["summary"]))
    print("Internal report: build/research-queue/queue.md")


if __name__ == "__main__":
    main()
