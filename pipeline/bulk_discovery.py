"""Reproducible, source-cited discovery from the official meinBerlin plan register.

No model calls, status inference, translation, golden authorship or publication.
The output is a research catalog; categories are explicit lexical review proposals.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
from datetime import datetime, timezone
import hashlib
from html import unescape
import json
from pathlib import Path
import re
import time
import urllib.request
from urllib.parse import urljoin

from pipeline.retrieval import retrieve_artifact
from pipeline.retrieval_config import load_retrieval_config
from pipeline.research_queue import normalized_text, render_map

ROOT = Path(__file__).resolve().parents[1]
API = 'https://mein.berlin.de/api/plans/'
WORK = re.compile(r'Neubau|Sanierung|Umbau|Ausbau|Erneuerung|Umgestaltung|Ersatzneubau|Instandsetzung|Errichtung|Baumaßnahme|Neugestaltung|Modernisierung|Reaktivierung|Verlängerung',re.I)
EXCLUSIONS = [
 (r'Handlungsleitfaden|Machbarkeitsstudie|Freiraumplanerischer Wettbewerb', 'guidance_or_study_not_bounded_works'),
 (r'^Kunst am Bau|^Beteiligungsveranstaltung|^Beteiligung', 'participation_or_art_process_not_construction_record'),
 (r'^Sanierungsgebiet|^Rahmenkonzept', 'area_programme_not_bounded_project'),
 (r'Heinrich-Hertz', 'existing_pilot_C-010'),
]
# Structural category proposals, not verified contextual glossary meanings.
CATEGORY_RULES = [
 ('energy',r'Umspannwerk|Netzausbau|Netzsanierung|Kabelsanierung'),
 ('housing',r'Wohnungsneubau|Wohnungsbau'),
 ('education',r'Schule|Schul|Gymnasium|Kita|Kindertages|ISS|Förderzentrum'),
 ('civic_sport',r'Sport|Spielfeld|Ballfangzaun|Bibliothek|Jugend|Begegnung|Beratung|Amtshaus|Gebäude|Kloster|Zilleklub|Otawitreff|Kindervilla|Bootshaus'),
 ('transport',r'Brücke|brücke'),
 ('public_space',r'Grün|Park|park|Spielplatz|Spielplätze|Kinderspiel|Bolzplatz|Ufer|Promenade|Dorfteich|Rosengarten|Freifläche|platz|Platz|Gartendenkmal|Wegeverbindung|Außenanlagen|Dorfanger|See|Höfe'),
 ('transport',r'Straße|Strasse|straße|strasse|Tunnel|bahn|Gehweg|Radverkehr'),
]


def category(title: str) -> tuple[str,str]:
    for name, pattern in CATEGORY_RULES:
        match = re.search(pattern,title,re.I)
        if match: return name,match[0]
    return 'scope_review',''


def select_records(plans: list, limit: int) -> tuple[list, list]:
    selected, disposition, seen = [], [], set()
    for index, row in enumerate(plans):
        title = row.get('title','')
        path = row.get('url','')
        reason = None
        if not re.fullmatch(r'/vorhaben/\d{4}-\d+/',path): reason='invalid_canonical_url'
        elif path in seen: reason='duplicate_source_url'
        elif row.get('status') == 2: reason='register_archived_not_current_research_priority'
        elif not WORK.search(title): reason='no_explicit_work_term_in_title'
        elif row.get('district') == 'Gesamtstädtisch': reason='citywide_programme_not_site'
        else:
            for pattern, why in EXCLUSIONS:
                if re.search(pattern,title,re.I): reason=why; break
        point = (row.get('point') or {}).get('geometry',{})
        xy = point.get('coordinates',[])
        if not reason and (point.get('type')!='Point' or len(xy)!=2 or not all(type(v) in (int,float) for v in xy) or not 13.0<xy[0]<14.0 or not 52.3<xy[1]<52.8):
            reason='missing_or_outside_location'
        if not reason and len(selected)>=limit: reason='reserve_after_batch_limit'
        if reason:
            disposition.append({'source_pointer':f'/{index}','source_path':path,'reason':reason})
            continue
        seen.add(path)
        group, trigger = category(title)
        selected.append({'index':index,'row':row,'category':group,'category_trigger':trigger})
    return selected, disposition


def make_record(item: dict, source_hash: str) -> dict:
    r = item['row']; path=r['url']; i=item['index']
    return {
      'candidate_id':'MB-'+path.strip('/').split('/')[-1],
      'name_de':r['title'], 'source_url':urljoin(API,path),
      'district_de':r['district'], 'source_topics':r['topics'],
      'category_proposal':item['category'], 'category_basis':item['category_trigger'],
      'category_review':'unreviewed_lexical_rule',
      'record_depth':'basic_listing_research', 'publication_state':'not_approved',
      'source_modified_at':r['created_or_modified'],
      'register_status_code':r['status'],
      'status_caveat':'Register workflow status is not construction progress.',
      'location':{'type':'Point','coordinates':r['point']['geometry']['coordinates'],
                  'label_de':r.get('point_label',''), 'scope':'official_register_navigation_point_not_footprint'},
      'evidence':{'inventory_url':API,'artifact_hash':source_hash,
                  'title_pointer':f'/{i}/title','exact_title_de':r['title'],
                  'location_pointer':f'/{i}/point/geometry/coordinates',
                  'location_label_pointer':f'/{i}/point_label'},
      'review_required':['identity_and_scope','location_scope','category','publication_decision'],
    }


def scope_excerpt(body: bytes) -> dict:
    block=re.search(rb'<div class="item-detail__basic-content ck-content"[^>]*>(.*?)</div>',body,re.S)
    if not block: return {'state':'not_extracted'}
    text=normalized_text(block[1])
    excerpt=' '.join(text.split()[:25])
    if not excerpt or re.search(r'@|\b(?:Herr|Frau|Dr\.|Prof\.)\s',excerpt):
        return {'state':'review_required'}
    return {'state':'unreviewed_source_excerpt','selector':'.item-detail__basic-content',
            'exact_text_de':excerpt,'truncated':len(excerpt)<len(text)}


def verify_page(record: dict, config, artifact_dir: Path) -> dict:
    try:
        result=retrieve_artifact(record['source_url'],config)
        raw=result.artifact.stored_bytes
        digest=hashlib.sha256(raw).hexdigest()
        (artifact_dir/(digest+'.html')).write_bytes(raw)
        if result.artifact.media_type!='text/html': raise ValueError('unexpected_media_type')
        h1=re.search(rb'<h1\b[^>]*>(.*?)</h1>',raw,re.S|re.I)
        heading=normalized_text(h1[1]) if h1 else ''
        matched=heading==' '.join(record['name_de'].split())
        return {'status':'title_matched' if matched else 'title_review_needed',
                'artifact_hash':'sha256:'+digest, 'retrieved_at':datetime.now(timezone.utc).isoformat(),
                'evidence_selector':'h1','exact_heading_de':heading,'scope_excerpt':scope_excerpt(raw),
                'http_attempts':[{'status':a.status_code,'outcome':a.outcome,'user_agent':a.user_agent_class} for a in result.attempts]}
    except Exception as exc:
        # Keep failures in the batch without exposing response content or credentials.
        return {'status':'retrieval_followup_required','failure_type':type(exc).__name__}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--inventory',type=Path)
    ap.add_argument('--fetch-inventory',action='store_true')
    ap.add_argument('--limit',type=int,default=150)
    ap.add_argument('--output-dir',type=Path,default=ROOT/('docs/research/findings/'+datetime.now(timezone.utc).date().isoformat()+'-bulk-discovery'))
    ap.add_argument('--verify-pages',action='store_true')
    ap.add_argument('--page-cache',type=Path,help='Recheck previously retained page artifacts without network')
    args=ap.parse_args()
    if args.limit<1: ap.error('limit must be positive')
    started=time.monotonic()
    if args.fetch_inventory:
        with urllib.request.urlopen(urllib.request.Request(API,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/127.0 Safari/537.36'}),timeout=30) as response:
            if response.url != API: raise ValueError('unexpected inventory redirect')
            raw=response.read(20_000_001)
        if len(raw)>20_000_000: raise ValueError('inventory too large')
        artifact=ROOT/'data/artifacts'/(hashlib.sha256(raw).hexdigest()+'.json')
        artifact.write_bytes(raw)
    elif args.inventory:
        raw=args.inventory.read_bytes()
    else: ap.error('--inventory or --fetch-inventory is required')
    source_hash='sha256:'+hashlib.sha256(raw).hexdigest()
    plans=json.loads(raw)
    selected,excluded=select_records(plans,args.limit)
    records=[make_record(x,source_hash) for x in selected]
    config,_=load_retrieval_config(ROOT/'pipeline/config/retrieval.v1.toml')
    if args.verify_pages:
        # At most two concurrent same-host requests; no retry beyond the existing policy.
        with ThreadPoolExecutor(max_workers=2) as pool:
            results=list(pool.map(lambda r:verify_page(r,config,ROOT/'data/artifacts'),records))
        for record,result in zip(records,results):record['page_check']=result
    if args.page_cache and not args.verify_pages:
        old={r['source_url']:r for r in json.loads(args.page_cache.read_text())['records']}
        for record in records:
            prior=old.get(record['source_url'],{}).get('page_check',{})
            digest=prior.get('artifact_hash','')
            try:
                if not re.fullmatch(r'sha256:[a-f0-9]{64}',digest): raise ValueError('missing_hash')
                body=(ROOT/'data/artifacts'/(digest[7:]+'.html')).read_bytes()
                if hashlib.sha256(body).hexdigest()!=digest[7:]: raise ValueError('hash_mismatch')
                h1=re.search(rb'<h1\b[^>]*>(.*?)</h1>',body,re.S|re.I)
                heading=normalized_text(h1[1]) if h1 else ''
                record['page_check']=dict(prior,status='title_matched' if heading==' '.join(record['name_de'].split()) else 'title_review_needed',check_mode='retained_artifact_recheck',scope_excerpt=scope_excerpt(body))
            except (OSError,ValueError):
                record['page_check']={'status':'retained_artifact_followup_required'}
    duplicate_flags=[]
    from difflib import SequenceMatcher
    for i,left in enumerate(records):
        for right in records[i+1:]:
            same_point=left['location']['coordinates']==right['location']['coordinates']
            similar=SequenceMatcher(None,left['name_de'].casefold(),right['name_de'].casefold()).ratio()>=0.90
            if same_point or similar:
                duplicate_flags.append({'left':left['candidate_id'],'right':right['candidate_id'],
                                        'reason':'shared_navigation_point' if same_point else 'similar_title',
                                        'disposition':'scope_review_not_automatic_merge'})
    from collections import Counter
    summary={'inventory_records':len(plans),'selected_candidates':len(records),
             'located_candidates':len(records),'published_new_records':0,'possible_duplicate_pairs':len(duplicate_flags),
             'categories_proposed':dict(Counter(r['category_proposal'] for r in records)),
             'page_checks':dict(Counter(r.get('page_check',{}).get('status','not_checked') for r in records)),
             'dispositions':dict(Counter(x['reason'] for x in excluded))}
    catalog={'schema_version':1,'checked_on':datetime.now(timezone.utc).date().isoformat(),'inventory_url':API,
             'inventory_hash':source_hash,'elapsed_seconds':round(time.monotonic()-started,3),'model_provider_calls':0,'summary':summary,'records':records,'excluded':excluded,'possible_duplicates':duplicate_flags}
    out=args.output_dir
    out.mkdir(parents=True,exist_ok=True)
    (out/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
    lines=['# Bulk construction candidate register','',
      'Research only. Every location is an official register navigation point, not a checked building footprint. No new construction-status or publication claim.','',
      '| Candidate | Proposed group | District | Original source | Page check |','| --- | --- | --- | --- | --- |']
    for r in records:
        title=r['name_de'].replace('|','\\|')
        lines.append(f"| {r['candidate_id']} — {title} | {r['category_proposal']} | {r['district_de']} | [Official project]({r['source_url']}) | {r.get('page_check',{}).get('status','not_checked')} |")
    (out/'register.md').write_text('\n'.join(lines)+'\n')
    details=['# Individual research records', '', 'All excerpts are unreviewed source wording; no current construction progress is inferred. Coordinates are official register navigation points, not project footprints.', '']
    for r in records:
        check=r.get('page_check',{}); excerpt=check.get('scope_excerpt',{})
        details += [f"## {r['candidate_id']} — {r['name_de']}", '',
          f"[Official project page]({r['source_url']}) · [Inventory]({API})", '',
          f"District: {r['district_de']}. Category proposal: {r['category_proposal']} (unreviewed).", '',
          f"Source coordinates [longitude, latitude]: {r['location']['coordinates']}. Location label: {r['location']['label_de']}", '',
          f"Evidence: JSON pointers `{r['evidence']['title_pointer']}` and `{r['evidence']['location_pointer']}`; page heading `h1`. Inventory hash `{source_hash}`.", '']
        if excerpt.get('exact_text_de'):
            details += ['> '+excerpt['exact_text_de']+(' …' if excerpt['truncated'] else ''),'',
                        f"Excerpt selector: `{excerpt['selector']}`. Retained page hash `{check['artifact_hash']}`.", '']
        details += ['Review remains: identity/scope, category, location scope, publication decision.', '']
    (out/'records.md').write_text('\n'.join(details)+'\n')

    with (out/'review.csv').open('w',newline='') as f:
        fields=['candidate_id','name_de','source_url','category_proposal','location_scope','reviewer_verdict','review_notes']
        w=csv.DictWriter(f,fields,lineterminator='\n');w.writeheader()
        for r in records:w.writerow({k:r.get(k,'') for k in fields}|{'location_scope':r['location']['scope']})
    queue={'candidates':[{'project_id':r['candidate_id'],'name_de':r['name_de'],
          'location_proposal':{'longitude':r['location']['coordinates'][0],'latitude':r['location']['coordinates'][1],'scope':r['location']['scope'],'source_url':r['source_url']},
          'sources':[{'url':r['source_url'],'status':r.get('page_check',{}).get('status','not_checked')}],
          'review_questions':r['review_required']} for r in records]}
    preview=ROOT/'build/bulk-research';preview.mkdir(parents=True,exist_ok=True)
    rendered=render_map(queue,json.loads((ROOT/'public/data/map/berlin-boundary.geojson').read_text()),json.loads((ROOT/'public/data/map/berlin-boundary.provenance.json').read_text()))
    rendered=rendered.replace('C-009 is only an approximate campus reference.','Locations are register navigation references; project boundaries remain to be checked.')
    rendered=re.sub(r'<text\b[^>]*>.*?</text>','',rendered)
    rendered=rendered.replace('r="15"','r="6"')
    (preview/'index.html').write_text(rendered)
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
