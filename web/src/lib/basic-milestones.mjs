import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

// This gate publishes the explicitly scoped release only. It never grants
// golden-set provenance or promotes arbitrary research candidates.
export function validateBasicMilestones(raw, release, research, listingIds) {
  if (release.version !== 1 || release.decisionId !== 'ADR-026' ||
      release.researchSha256 !== 'sha256:' + createHash('sha256').update(JSON.stringify(research)).digest('hex') ||
      release.payloadSha256 !== 'sha256:' + createHash('sha256').update(raw).digest('hex'))
    throw new Error('Basic milestone release does not match its checked payload');
  const payload = JSON.parse(raw);
  if (payload.version !== 1 || !Array.isArray(payload.facts)) throw new Error('Invalid milestone payload');
  const seen = new Set();
  return payload.facts.map(fact => {
    if (Object.keys(fact).sort().join(',') !== 'kind,projectId,sourceIndex,spanIndex,valueDe')
      throw new Error('Unexpected milestone fields');
    const key = fact.projectId + ':' + fact.kind;
    if (seen.has(key) || !listingIds.includes(fact.projectId) ||
        !['planned_completion', 'planned_end', 'reported_start'].includes(fact.kind) ||
        release.excludedFacts.some(x => x.projectId === fact.projectId &&
          (x.kind === fact.kind || x.kind === 'all_milestones')))
      throw new Error('Milestone is duplicate, excluded or outside scope');
    seen.add(key);
    const candidate = research.candidates.find(x => x.project_id === fact.projectId);
    const source = candidate?.sources[fact.sourceIndex];
    const span = source?.spans[fact.spanIndex];
    const recheck = research.independent_retained_artifact_recheck.find(x => x.project_id === fact.projectId);
    if (!source?.span_match || recheck?.status !== 'screened_spans_present' ||
        typeof span !== 'string' || !span.trim() || typeof fact.valueDe !== 'string' ||
        !fact.valueDe.trim() || !span.includes(fact.valueDe) ||
        !/^sha256:[a-f0-9]{64}$/.test(source.content_hash) ||
        !/^https:\/\/mein\.berlin\.de\/vorhaben\/\d{4}-\d+\/$/.test(source.url))
      throw new Error('Milestone lacks checked source evidence');
    return { ...fact, exactTextDe: span, sourceUrl: source.url,
      sourceModifiedDateDe: source.source_modified_date_de,
      retrievedOn: source.retrieved_on, contentHash: source.content_hash,
      label: fact.kind === 'reported_start' ? 'Start (reported)' : 'Planned finish' };
  });
}

export function loadBasicMilestones(listingIds) {
  const read = path => readFileSync(resolve(path), 'utf8');
  return validateBasicMilestones(read('src/atlas/basic-milestones.json'),
    JSON.parse(read('../public/data/basic-milestone-release.json')),
    JSON.parse(read('../docs/research/findings/2026-09-09-milestone-enrichment.json')), listingIds);
}
