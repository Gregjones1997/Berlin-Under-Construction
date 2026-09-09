import hashlib
from pathlib import Path

import pytest

from pipeline.research_queue import build_queue, check_source, normalized_text


def source(tmp_path, body=b'<p>Baubeginn <strong>2026</strong></p>'):
    digest = hashlib.sha256(body).hexdigest()
    (tmp_path / (digest + '.html')).write_bytes(body)
    return dict(url='https://www.berlin.de/project', content_hash='sha256:'+digest,
                spans=['Baubeginn 2026'], publication_date=None, retrieved_on='2026-09-08')


def candidate(src):
    return dict(project_id='C-001', name_de='Projekt', sources=[src],
                location_assessment='Unchecked', review_questions=['Scope?'])


def test_inline_markup_and_block_boundaries_do_not_create_false_changes():
    assert normalized_text(b'<p>Mexikopla<strong>tz</strong></p><p>2026</p>') == 'Mexikoplatz 2026'
    assert 'hidden' not in normalized_text(b'<script>hidden</script><p>shown</p>')


def test_tampered_artifact_fails_closed(tmp_path):
    src = source(tmp_path)
    (tmp_path / (src['content_hash'][7:]+'.html')).write_bytes(b'wrong')
    assert check_source(src,tmp_path)['status'] == 'artifact_hash_mismatch'


def test_missing_span_and_missing_artifact_remain_visible(tmp_path):
    src = source(tmp_path)
    src['spans'] = ['Actual completion']
    assert check_source(src,tmp_path)['status'] == 'evidence_changed'
    (tmp_path / (src['content_hash'][7:]+'.html')).unlink()
    assert check_source(src,tmp_path)['status'] == 'retrieval_failed'


def test_repeated_sources_deduplicate_without_promoting_to_publication(tmp_path):
    src = source(tmp_path)
    one = candidate(src)
    two = dict(one, project_id='C-002')
    q = build_queue({'candidates':[one,two]},tmp_path)
    assert q['summary'] == {'candidates':2,'map_eligible':0,'source_followups':0}
    assert all(c['state']=='research_pending' and not c['map_eligible'] for c in q['candidates'])
    assert q == build_queue({'candidates':[one,two]},tmp_path)


def test_duplicate_candidate_rejected(tmp_path):
    c = candidate(source(tmp_path))
    with pytest.raises(ValueError,match='duplicate'):
        build_queue({'candidates':[c,c]},tmp_path)


def test_coordinates_must_match_retained_marker_and_never_approve(tmp_path):
    from pipeline.research_queue import attach_locations
    tag = '<div data-marker-long="13.4" data-marker-lat="52.5">'
    src = source(tmp_path,tag.encode())
    q = build_queue({'candidates':[candidate(src)]},tmp_path)
    loc = dict(project_id='C-001',content_hash=src['content_hash'],
               exact_location_tag=tag,longitude=13.4,latitude=52.5,
               source_url=src['url'],scope='project_map_center')
    attach_locations(q,{'locations':[loc]},tmp_path)
    assert q['summary']['source_located_proposals'] == 1
    assert not q['candidates'][0]['map_eligible']
    assert 'location_scope_review_needed' in q['candidates'][0]['blockers']
    with pytest.raises(ValueError,match='coordinate'):
        attach_locations(build_queue({'candidates':[candidate(src)]},tmp_path),
                         {'locations':[dict(loc,longitude=13.6)]},tmp_path)


def test_non_https_source_is_rejected_before_rendering(tmp_path):
    src = dict(source(tmp_path),url='javascript:alert(1)')
    with pytest.raises(ValueError,match='HTTPS'):
        check_source(src,tmp_path)
