from __future__ import annotations

import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "web" / "src" / "lib" / "milestone-freshness.mjs"


def _warnings(as_of: str) -> list[str]:
    fact = {
        "factType": "milestone",
        "qualifiers": [
            {
                "qualifierClass": "modal_intent",
                "appliesTo": "date",
                "tokenDe": "geplant",
            }
        ],
        "asOfDate": {"state": "verified", "value": "2026-06-19"},
        "freshness": {"state": "unassessed"},
        "dateValue": {
            "precision": "exact_day",
            "canonicalDe": "31.08.2026",
        },
    }
    script = (
        f'import {{ milestoneDisplayWarnings }} from "{MODULE.as_uri()}"; '
        "const fact = JSON.parse(process.argv[1]); "
        "console.log(JSON.stringify(milestoneDisplayWarnings(fact, process.argv[2])));"
    )
    result = subprocess.run(
        ["node", "--input-type=module", "--eval", script, json.dumps(fact), as_of],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)


def test_planned_milestone_never_implies_completion_before_its_date() -> None:
    assert _warnings("2026-08-25") == [
        "The source planned this milestone for 31.08.2026 as of 2026-06-19. "
        "This is not evidence that the milestone has happened."
    ]


def test_passed_planned_milestone_requires_confirmation() -> None:
    assert _warnings("2026-09-01") == [
        "The source planned this milestone for 31.08.2026 as of 2026-06-19. "
        "That date has passed, but no confirming source is recorded. "
        "Completion is not asserted."
    ]
