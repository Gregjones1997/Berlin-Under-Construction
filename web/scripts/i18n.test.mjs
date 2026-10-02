import { test } from "node:test";
import assert from "node:assert/strict";
import { digest, validatePair, checkTranslations } from "./check-i18n.mjs";
import { decodeViewState, encodeViewState } from "../src/atlas/view-state.ts";

test("English copy edits cannot pass with an old German counterpart revision", () => {
  const pair = { de: "Beleg ansehen", en: "View evidence" };
  const revision = { de: digest(pair.de), en: digest(pair.en) };
  assert.doesNotThrow(() => validatePair("evidence", pair, revision));
  assert.throws(
    () =>
      validatePair("evidence", { ...pair, en: "Read the evidence" }, revision),
    /synchronization/,
  );
  assert.throws(
    () => validatePair("evidence", { ...pair, de: "" }, revision),
    /Missing de/,
  );
});
test("placeholders remain compatible across both languages", () => {
  const pair = { en: "Selected {name}", de: "{project} ausgewählt" };
  assert.throws(
    () =>
      validatePair("selected", pair, {
        en: digest(pair.en),
        de: digest(pair.de),
      }),
    /Placeholder mismatch/,
  );
});
test("selected map view roundtrips with filter, perspective and layer visibility", () => {
  const view = {
    camera: { target: [1000, 0, -100], offset: [1400, 2600, 2800], zoom: 2.2 },
    plan: true,
    expanded: true,
    folder: "budget",
    filter: "13.38886,52.517",
    area: "overview",
    labels: { projects: true, basic: false, water: true, parks: false },
  };
  assert.deepEqual(decodeViewState(encodeViewState(view)), view);
});
test("malformed or unbounded map state is ignored", () => {
  assert.equal(decodeViewState("not json"), undefined);
  assert.equal(decodeViewState("x".repeat(1001)), undefined);
  assert.equal(
    decodeViewState(
      JSON.stringify({
        camera: { target: [0, 0, 0], offset: [0, 0, 0], zoom: Infinity },
      }),
    ),
    undefined,
  );
});
test("the real public catalogs retain source and paired revision links", () => {
  const result = checkTranslations();
  assert.equal(result.facts, 20);
  assert.equal(result.listings, 150);
  assert.equal(result.terms, 14);
  assert.ok(result.messages > 400);
});

import { localizePath, localeFromPath } from "../src/lib/locales.ts";
test("language URLs keep dossier identity, query and evidence fragment", () => {
  assert.equal(
    localizePath("/en/projects/europaplatz-sued/?mode=history#evidence", "de"),
    "/projects/europaplatz-sued/?mode=history#evidence",
  );
  assert.equal(
    localizePath("/projects/europaplatz-sued/#history-heading", "en"),
    "/en/projects/europaplatz-sued/#history-heading",
  );
  assert.equal(localizePath("/404/", "en"), "/en/404/");
  assert.equal(localizePath("/en?view=one", "de"), "/?view=one");
  assert.equal(
    localizePath("https://mein.berlin.de/vorhaben/2026-01441/", "en"),
    "https://mein.berlin.de/vorhaben/2026-01441/",
  );
  assert.equal(localeFromPath("/energy/"), "de");
});

import { checkPublicCopy } from "./check-public-copy.mjs";
import { translationReadiness } from "./check-i18n.mjs";
test("static public copy stays in paired catalogs or labelled originals", async () => {
  assert.match(await checkPublicCopy(), /paired catalog/);
});
test("unverified model explanations cannot pass the release review gate", () => {
  const report = translationReadiness();
  assert.equal(report.ready, false);
  assert.equal(report.pending.facts.length, 20);
  assert.equal(report.pending.listings.length, 150);
  assert.equal(report.pending.terms.length, 14);
});

import { numericCardDate } from "../src/lib/card-dates.ts";
test("numeric card dates retain exact-day and partial-date precision", () => {
  assert.equal(numericCardDate("2. Februar 2026", "en"), "02/02/2026");
  assert.equal(numericCardDate("2. Februar 2026", "de"), "02.02.2026");
  assert.equal(numericCardDate("31.08.2026", "en"), "31/08/2026");
  assert.equal(numericCardDate("2026", "en"), undefined);
  assert.equal(numericCardDate("Sommer 2026", "en"), undefined);
  assert.equal(numericCardDate("bis Ende 2028", "en"), undefined);
});

test('old map links default to Schedule and arbitrary folder IDs are ignored',()=>{
 const old={camera:{target:[0,0,0],offset:[100,100,100],zoom:1},plan:false,expanded:true,filter:'',area:'overview',labels:{projects:true,basic:true,water:false,parks:false}};
 assert.equal(decodeViewState(JSON.stringify(old)).folder,'schedule');
 assert.equal(decodeViewState(JSON.stringify({...old,folder:'untrusted-id'})),undefined);
});
