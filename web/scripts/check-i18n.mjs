import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";
import { resolve, dirname } from "node:path";
const web = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const read = (p) => JSON.parse(readFileSync(resolve(web, p), "utf8"));
const stable = (v) =>
  Array.isArray(v)
    ? "[" + v.map(stable).join(",") + "]"
    : v && typeof v === "object"
      ? "{" +
        Object.keys(v)
          .sort()
          .map((k) => JSON.stringify(k) + ":" + stable(v[k]))
          .join(",") +
        "}"
      : JSON.stringify(v);
export const digest = (v) =>
  createHash("sha256")
    .update(typeof v === "string" ? v : stable(v))
    .digest("hex");
export function validatePair(id, pair, revision) {
  for (const locale of ["de", "en"])
    if (typeof pair[locale] !== "string" || !pair[locale].trim())
      throw Error(`Missing ${locale} translation: ${id}`);
  const placeholders = (s) =>
    [...s.matchAll(/\{([a-zA-Z]\w*)\}/g)]
      .map((m) => m[1])
      .sort()
      .join(",");
  if (placeholders(pair.de) !== placeholders(pair.en))
    throw Error(`Placeholder mismatch: ${id}`);
  if (
    !revision ||
    revision.de !== digest(pair.de) ||
    revision.en !== digest(pair.en)
  )
    throw Error(`Translation pair needs synchronization: ${id}`);
}
export function checkTranslations() {
  const lock = read("src/i18n/revisions.json");
  for (const file of ["messages", "facts", "listings", "terms"]) {
    const entries = read(`src/i18n/${file}.json`);
    for (const [id, pair] of Object.entries(entries))
      validatePair(`${file}:${id}`, pair, lock[`${file}:${id}`]);
    for (const [id, pair] of Object.entries(entries)) {
      if (file === "facts" || file === "listings") {
        if (!["editorial_unverified", "confirmed"].includes(pair.verification))
          throw Error(`Invalid translation verification: ${id}`);
        if (
          pair.verification === "confirmed" &&
          (!pair.review?.reviewerId ||
            !pair.review?.date ||
            !pair.review?.scope ||
            pair.review?.meaningRevision !==
              digest({
                de: pair.de,
                en: pair.en,
                sourceRevision: pair.sourceRevision,
              }))
        )
          throw Error(`Confirmed translation lacks scoped review: ${id}`);
      }
    }
    if (
      Object.keys(lock).some(
        (id) =>
          id.startsWith(file + ":") && !(id.slice(file.length + 1) in entries),
      )
    )
      throw Error(`Orphan translation revision in ${file}`);
  }
  const facts = read("src/i18n/facts.json");
  const publicFacts = read("../public/data/projects.json")
    .projects.flatMap((p) => p.facts)
    .filter((f) => f.state === "published");
  if (Object.keys(facts).length !== publicFacts.length)
    throw Error("Fact translation scope differs from published scope");
  for (const fact of publicFacts)
    if (
      facts[fact.factId]?.sourceRevision !== digest(fact) ||
      facts[fact.factId]?.de !== fact.valueDe
    )
      throw Error(`Changed source invalidates explanation: ${fact.factId}`);
  const listings = read("src/i18n/listings.json");
  const records = read("src/atlas/basic-listings.json").records;
  if (Object.keys(listings).length !== records.length)
    throw Error("Listing translation scope mismatch");
  for (const record of records)
    if (
      listings[record.id]?.sourceRevision !== digest(record) ||
      listings[record.id]?.de !== record.nameDe
    )
      throw Error(
        `Changed register title invalidates explanation: ${record.id}`,
      );
  for (const [id, term] of Object.entries(read("src/i18n/terms.json"))) {
    if (
      term.glossaryRevision !==
      digest(readFileSync(resolve(web, "../docs/glossary.md"), "utf8"))
    )
      throw Error(`Changed glossary invalidates term mapping: ${id}`);
    if (
      term.verification === "confirmed" &&
      (!term.review?.reviewerId ||
        !term.review?.date ||
        !term.review?.scope ||
        term.review?.meaningRevision !==
          digest({
            de: term.de,
            en: term.en,
            context: read("src/i18n/messages.json")[term.contextMessage],
            glossaryRevision: term.glossaryRevision,
          }))
    )
      throw Error(`Term confirmation lacks scoped review: ${id}`);
    if (!["editorial_unverified", "confirmed"].includes(term.verification))
      throw Error(`Invalid term review status: ${id}`);
  }
  return {
    messages: Object.keys(read("src/i18n/messages.json")).length,
    facts: publicFacts.length,
    listings: records.length,
    terms: Object.keys(read("src/i18n/terms.json")).length,
  };
}
export function translationReadiness() {
  const pending = {};
  for (const file of ["facts", "listings", "terms"])
    pending[file] = Object.entries(read(`src/i18n/${file}.json`))
      .filter(([, entry]) => entry.verification !== "confirmed")
      .map(([id]) => id);
  return {
    ready: Object.values(pending).every((ids) => ids.length === 0),
    pending,
  };
}
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  console.log(JSON.stringify(checkTranslations()));
  if (process.argv.includes("--release")) {
    const report = translationReadiness();
    if (!report.ready)
      throw Error(
        "Bilingual release needs scoped independent translation review: " +
          Object.entries(report.pending)
            .map(([kind, ids]) => kind + "=" + ids.length)
            .join(", "),
      );
  }
}
