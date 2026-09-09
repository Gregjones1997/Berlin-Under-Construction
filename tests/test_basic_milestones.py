"""Publication failures must be visible before any basic date reaches the atlas."""
import subprocess
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]

@pytest.mark.parametrize('mutation', ['none', 'tamper', 'empty_span', 'invented_day', 'excluded'])
def test_basic_milestone_publication_gate(mutation):
    script = r'''
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {validateBasicMilestones} from './web/src/lib/basic-milestones.mjs';
const json=p=>JSON.parse(readFileSync(p,'utf8'));
const payload=json('web/src/atlas/basic-milestones.json');
const release=json('public/data/basic-milestone-release.json');
const research=json('docs/research/findings/2026-09-09-milestone-enrichment.json');
const ids=json('web/src/atlas/basic-listings.json').records.map(x=>x.id);
const mutation=process.argv[1];
if(mutation==='empty_span') { research.candidates[0].sources[0].spans[0]=''; release.researchSha256='sha256:'+createHash('sha256').update(JSON.stringify(research)).digest('hex'); }
if(mutation==='invented_day') payload.facts[0].valueDe='2028-12-31';
if(mutation==='excluded') payload.facts.push({...payload.facts[0],projectId:'MB-2023-00716'});
let raw=mutation==='none'||mutation==='tamper'?readFileSync('web/src/atlas/basic-milestones.json','utf8'):JSON.stringify(payload);
// Exercise evidence/scope checks independently from the payload fingerprint.
if(mutation!=='none'&&mutation!=='tamper') release.payloadSha256='sha256:'+createHash('sha256').update(raw).digest('hex');
if(mutation==='tamper')raw+=' ';
try {
 const rows=validateBasicMilestones(raw,release,research,ids);
 if(mutation!=='none'||rows.length!==6||new Set(rows.map(x=>x.projectId)).size!==5)process.exit(2);
} catch(e) {if(mutation==='none')throw e;}
'''
    result = subprocess.run(['node', '--input-type=module', '-e', script, mutation], cwd=ROOT, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
