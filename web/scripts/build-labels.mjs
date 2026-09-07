/** Compile source-linked geographic labels from the retained OSM export. */
import { readFileSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
const path = process.argv[2];
if (!path) throw new Error("Usage: node scripts/build-labels.mjs context.json");
const raw = readFileSync(path);
const context = JSON.parse(raw);
// Cartographic selection; never a source of construction-project claims.
const selected = new Set([
  "way/4317997",
  "way/4436463",
  "way/4469529",
  "way/4685998",
  "way/277545599",
  "way/815670035",
  "relation/3410",
  "relation/451908",
  "relation/7643526",
  "relation/3099987",
  "relation/14524667",
  "relation/15803725",
  "relation/8676818",
  "relation/3582343",
  "way/737280675",
  "way/340138573",
  "way/16000014",
  "way/176696872",
  "way/15740772",
  "way/4638994",
  "way/52189421",
  "way/4778261",
  "way/4686373",
  "way/10295991",
  "way/23381024",
  "relation/26993",
]);
const labels = context.elements
  .filter((e) => selected.has(`${e.type}/${e.id}`))
  .map((e) => {
    const kind =
      e.tags.leisure === "park" || e.tags.landuse === "forest"
        ? "parks"
        : e.tags.natural === "water"
          ? "water"
          : null;
    if (!kind || !e.tags.name)
      throw new Error(`Missing source name/type: ${e.id}`);
    const geometry =
      e.geometry ??
      e.members
        .filter((m) => m.role === "outer")
        .flatMap((m) => m.geometry ?? []);
    if (!geometry.length) throw new Error(`Missing geometry: ${e.id}`);
    const longitude =
      (Math.min(...geometry.map((p) => p.lon)) +
        Math.max(...geometry.map((p) => p.lon))) /
      2;
    const latitude =
      (Math.min(...geometry.map((p) => p.lat)) +
        Math.max(...geometry.map((p) => p.lat))) /
      2;
    return {
      name: e.tags.name,
      minZoom: [4436463, 277545599, 3410, 451908].includes(e.id) ? 0.055 : 0.55,
      kind,
      longitude,
      latitude,
      sourceUrl: `https://www.openstreetmap.org/${e.type}/${e.id}`,
    };
  });
if (labels.length !== selected.size)
  throw new Error("Selected label sources are missing");
writeFileSync(
  "src/atlas/context-labels.json",
  JSON.stringify(
    {
      sourceTimestamp: context.osm3s.timestamp_osm_base,
      inputSha256: "sha256:" + createHash("sha256").update(raw).digest("hex"),
      license: "ODbL-1.0",
      anchorMethod:
        "Feature bounding-box center for cartographic placement; not a project location.",
      labels,
    },
    null,
    2,
  ) + "\n",
);
console.log(`Compiled ${labels.length} source-linked geographic labels.`);
