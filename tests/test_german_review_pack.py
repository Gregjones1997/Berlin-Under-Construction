import runpy
from pathlib import Path

PACK = runpy.run_path(str(Path(__file__).parents[1] / "scripts/build_german_review_pack.py"))


def test_literal_matching_preserves_word_boundaries_and_german_case():
    assert PACK["matches"]("Übergabe", "technische Übergabe")
    assert PACK["matches"]("geplant", "Geplant für 2028")
    assert not PACK["matches"]("Kosten", "Gesamtkosten")
    assert not PACK["matches"]("ab", "abgeschlossen")


def test_withheld_detail_never_enters_inventory_even_if_present():
    projection = {"projects": [{"projectId": "C-000", "conflicts": [], "facts": [
        {"factId": "withheld", "state": "withheld", "reasonCode": "pending",
         "valueDe": "PRIVATE SENTINEL", "evidence": {"exactTextDe": "PRIVATE SENTINEL"}}
    ]}]}
    passages, excluded = PACK["inventory"](projection, [])
    assert passages == []
    assert excluded == [{"fact_id": "withheld", "reason": "pending"}]
    assert "PRIVATE SENTINEL" not in repr((passages, excluded))


def test_same_passage_keeps_all_app_fields_and_conflict_routing():
    fact = {"factId": "a", "factType": "milestone", "state": "published",
            "translationState": "german_canonical", "evidence": {
                "sourceUrl": "https://example.org", "sourceId": "source",
                "publicationDate": {"state": "not_stated"}, "exactTextDe": "Baubeginn 2026"}}
    projection = {"projects": [{"projectId": "C-000",
        "conflicts": [{"memberFactIds": ["b"]}],
        "facts": [fact, dict(fact, factId="b", factType="status")]}]}
    passages, _ = PACK["inventory"](projection, [{"id": "G1", "aliases": ["Baubeginn"]}])
    assert len(passages) == 1
    assert [f["fact_id"] for f in passages[0]["facts"]] == ["a", "b"]
    assert passages[0]["exception_reasons"] == ["existing_conflict_member"]
    assert passages[0]["glossary_ids"] == ["G1"]
