from pipeline.bulk_discovery import category, make_record, select_records


def row(**kwargs):
    return dict(title='Neubau Testschule',url='/vorhaben/2026-12345/',status=0,
                district='Mitte',topics=['EDU'],created_or_modified='2026-09-09T12:00:00+02:00',
                point={'geometry':{'type':'Point','coordinates':[13.4,52.5]}},
                point_label='School campus') | kwargs


def test_selection_keeps_auditable_dispositions_and_original_json_indices():
    rows=[row(title='Handlungsleitfaden zum Neubau'),row(),row(status=2,url='/vorhaben/2026-99999/')]
    chosen,excluded=select_records(rows,150)
    assert len(chosen)==1 and chosen[0]['index']==1
    assert {x['reason'] for x in excluded}=={'guidance_or_study_not_bounded_works','register_archived_not_current_research_priority'}
    rec=make_record(chosen[0],'sha256:'+'a'*64)
    assert rec['evidence']['title_pointer']=='/1/title'
    assert rec['publication_state']=='not_approved'
    assert 'construction progress' in rec['status_caveat']


def test_bad_locations_and_external_paths_cannot_become_pins():
    chosen,excluded=select_records([row(point=None),row(url='https://evil.test/'),row(point={'geometry':{'type':'Point','coordinates':[52.5,13.4]}})],150)
    assert chosen==[]
    assert len(excluded)==3


def test_duplicate_urls_and_batch_reserves_are_not_silently_dropped():
    chosen,excluded=select_records([row(),row(),row(url='/vorhaben/2026-11111/')],1)
    assert len(chosen)==1
    assert [x['reason'] for x in excluded]==['duplicate_source_url','reserve_after_batch_limit']


def test_project_object_beats_street_address_in_category_proposals():
    assert category('Erneuerung Spielplatz Germaniastraße')[0]=='public_space'
    assert category('Neubau Schule mit Sporthalle')[0]=='education'
    assert category('Sanierung Sportanlage Musterstraße')[0]=='civic_sport'
    assert category('Ersatzneubau Musterbrücke')[0]=='transport'


def test_short_description_is_only_a_source_excerpt_not_a_status_claim():
    from pipeline.bulk_discovery import scope_excerpt
    result=scope_excerpt(b'<div class="item-detail__basic-content ck-content"><p>Der Neubau ist geplant.</p></div>')
    assert result['exact_text_de']=='Der Neubau ist geplant.'
    assert result['state']=='unreviewed_source_excerpt'
    assert not result['truncated']


def test_contact_like_description_is_quarantined():
    from pipeline.bulk_discovery import scope_excerpt
    assert scope_excerpt(b'<div class="item-detail__basic-content ck-content">Kontakt Frau Example</div>')=={'state':'review_required'}
