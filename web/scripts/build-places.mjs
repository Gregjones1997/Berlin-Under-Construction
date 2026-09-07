/** Compile source-backed navigation anchors; these are not project positions. */
import { readFileSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
const raw = readFileSync(process.argv[2]);
const data = JSON.parse(raw);
if (data.remark) throw new Error(data.remark);
const ids = new Set([
  29336704, 31451386, 33790061, 129875262, 151013231, 162012321, 288659908,
  331139102, 560483804, 1583388419, 1775453665,
]);
const places = data.elements
  .filter((e) => ids.has(e.id))
  .map((e) => ({
    name: e.tags.name,
    longitude: e.lon,
    latitude: e.lat,
    sourceUrl: `https://www.openstreetmap.org/node/${e.id}`,
  }))
  .sort((a, b) => a.name.localeCompare(b.name, "de"));
if (places.length !== ids.size) throw new Error("Missing navigation source");
writeFileSync(
  "src/atlas/places.json",
  JSON.stringify(
    {
      sourceTimestamp: data.osm3s.timestamp_osm_base,
      inputSha256: "sha256:" + createHash("sha256").update(raw).digest("hex"),
      license: "ODbL-1.0",
      places,
    },
    null,
    2,
  ) + "\n",
);
