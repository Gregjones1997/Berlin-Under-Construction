/** Offline mesh compiler. No source text, addresses or names enter the runtime model. */
import {
  readFileSync,
  writeFileSync,
  mkdirSync,
  readdirSync,
  appendFileSync,
  rmSync,
} from "node:fs";
import { createHash } from "node:crypto";
import { gzipSync } from "node:zlib";
import { ShapeUtils, Vector2 } from "three";
import proj4 from "proj4";
const [buildingPath, osmPath] = process.argv.slice(2);
if (!buildingPath || !osmPath)
  throw new Error(
    "Usage: node scripts/build-atlas.mjs building-pages-directory context.json",
  );
const UTM = "+proj=utm +zone=33 +ellps=GRS80 +units=m +no_defs";
const origin = [391000, 5820000];
const project = (lon, lat) => {
  const [e, n] = proj4("EPSG:4326", UTM, [lon, lat]);
  return [e - origin[0], origin[1] - n];
};
const surface = [],
  edges = [];
const output = "site-public/atlas";
mkdirSync(output, { recursive: true });
const spool = `${buildingPath}/mesh-spool`;
rmSync(spool, { recursive: true, force: true });
mkdirSync(spool, { recursive: true });
const bounds = [Infinity, Infinity, -Infinity, -Infinity];
let count = 0,
  missing = 0,
  invalid = 0,
  sourceFeatures = 0,
  expected;
const inputHashes = [];
const ids = new Set();
const overview = [];
const manifestTiles = [];
function pack(surfaces, lines, offset = [0, 0], quantization = 2) {
  const packed = new Int16Array(surfaces.length + lines.length);
  for (let i = 0; i < packed.length; i++) {
    const value =
      i < surfaces.length ? surfaces[i] : lines[i - surfaces.length];
    const q = Math.round(
      (value - (i % 3 === 0 ? offset[0] : i % 3 === 2 ? offset[1] : 0)) *
        quantization,
    );
    if (!Number.isFinite(q) || q < -32768 || q > 32767)
      throw new Error("Geometry exceeds packed coordinate range");
    packed[i] = q;
  }
  const gzip = gzipSync(new Uint8Array(packed.buffer), { level: 9 });
  const hash = createHash("sha256").update(gzip).digest("hex");
  const filename = `berlin-${hash.slice(0, 12)}.bin.gz`;
  writeFileSync(`${output}/${filename}`, gzip);
  return {
    geometry: `/atlas/${filename}`,
    sha256: `sha256:${hash}`,
    bytes: gzip.length,
    surfaceFloats: surfaces.length,
    edgeFloats: lines.length,
    offset,
    quantization,
  };
}
function cleaned(ring) {
  const pts = ring.map(([e, n]) => [
    Math.round((e - origin[0]) * 10) / 10,
    Math.round((origin[1] - n) * 10) / 10,
  ]);
  if (
    pts.length > 1 &&
    pts[0][0] === pts.at(-1)[0] &&
    pts[0][1] === pts.at(-1)[1]
  )
    pts.pop();
  return pts.filter(
    (p, i) =>
      i === 0 || Math.hypot(p[0] - pts[i - 1][0], p[1] - pts[i - 1][1]) > 0.15,
  );
}
// Reduce nearly collinear vertices only in the zoomed-out footprint layer.
function overviewRing(ring) {
  let result = ring;
  for (let pass = 0; pass < 3; pass++) {
    const next = [];
    for (let i = 0; i < result.length; i++) {
      const a = next.at(-1) ?? result.at(-1),
        b = result[i],
        c = result[(i + 1) % result.length];
      const length = Math.hypot(c[0] - a[0], c[1] - a[1]);
      const distance = length
        ? Math.abs(
            (c[0] - a[0]) * (a[1] - b[1]) - (a[0] - b[0]) * (c[1] - a[1]),
          ) / length
        : Infinity;
      if (distance >= 2 || next.length + result.length - i <= 3) next.push(b);
    }
    if (next.length >= 3) result = next;
  }
  return result;
}
function polygonMesh(rings, height, positions, linePositions, base = 0) {
  if (rings[0].length < 3) return;
  const outer = rings[0].map((p) => new Vector2(...p));
  const holes = rings
    .slice(1)
    .filter((r) => r.length >= 3)
    .map((r) => r.map((p) => new Vector2(...p)));
  const all = [outer, ...holes].flat();
  const triangles = ShapeUtils.triangulateShape(outer, holes);
  for (const triangle of triangles) {
    for (const i of [...triangle].reverse()) {
      const p = all[i];
      positions.push(p.x, height, p.y);
    }
  }
  if (height > base) {
    for (const ring of rings) {
      for (let i = 0; i < ring.length; i++) {
        const a = ring[i],
          b = ring[(i + 1) % ring.length];
        positions.push(
          a[0],
          base,
          a[1],
          b[0],
          base,
          b[1],
          b[0],
          height,
          b[1],
          a[0],
          base,
          a[1],
          b[0],
          height,
          b[1],
          a[0],
          height,
          a[1],
        );
        if (linePositions) {
          linePositions.push(
            a[0],
            height + 0.04,
            a[1],
            b[0],
            height + 0.04,
            b[1],
            a[0],
            base,
            a[1],
            a[0],
            height,
            a[1],
          );
        }
      }
    }
  }
}
// Partition source pages before triangulation, keeping peak compiler memory bounded.
for (const name of readdirSync(buildingPath)
  .filter((n) => /^buildings-.*\.json$/.test(n))
  .sort()) {
  const raw = readFileSync(`${buildingPath}/${name}`);
  const data = JSON.parse(raw);
  expected ??= data.numberMatched;
  if (expected !== data.numberMatched)
    throw new Error("Source count changed during pagination");
  inputHashes.push({
    file: name,
    sha256: "sha256:" + createHash("sha256").update(raw).digest("hex"),
    features: data.features.length,
  });
  sourceFeatures += data.features.length;
  const groups = new Map();
  for (const f of data.features) {
    if (ids.has(f.properties.gisid))
      throw new Error("Duplicate source feature across pages");
    ids.add(f.properties.gisid);
    const h = f.properties.hoehe;
    if (typeof h !== "number" || !Number.isFinite(h) || h <= 0) {
      missing++;
      continue;
    }
    if (!f.geometry || f.geometry.type !== "MultiPolygon") {
      invalid++;
      continue;
    }
    if (f.properties.shape_area < 50) continue;
    count++;
    for (const polygon of f.geometry.coordinates) {
      const rings = polygon.map(cleaned);
      if (rings[0].length < 3) continue;
      const p = rings[0][0];
      const key = `${Math.floor(p[0] / 2000)}_${Math.floor(p[1] / 2000)}`;
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key).push({ rings, h, area: f.properties.shape_area });
      for (const [x, z] of rings[0]) {
        bounds[0] = Math.min(bounds[0], x);
        bounds[1] = Math.min(bounds[1], z);
        bounds[2] = Math.max(bounds[2], x);
        bounds[3] = Math.max(bounds[3], z);
      }
    }
  }
  for (const [key, features] of groups)
    appendFileSync(
      `${spool}/${key}.jsonl`,
      features.map((f) => JSON.stringify(f)).join("\n") + "\n",
    );
  console.log(`Partitioned ${sourceFeatures}/${expected} features`);
}
if (!expected || sourceFeatures !== expected)
  throw new Error(`Incomplete city export: ${sourceFeatures}/${expected}`);
for (const file of readdirSync(spool).sort()) {
  const key = file.replace(".jsonl", "");
  const [tx, tz] = key.split("_").map(Number);
  const offset = [tx * 2000 + 1000, tz * 2000 + 1000];
  const ts = [],
    te = [],
    tb = [Infinity, Infinity, -Infinity, -Infinity];
  let buildings = 0,
    maxHeight = 0;
  for (const line of readFileSync(`${spool}/${file}`, "utf8")
    .trim()
    .split("\n")) {
    const { rings, h, area } = JSON.parse(line);
    polygonMesh(rings, h, ts, te);
    // Overview is explicitly a flat footprint layer, not a substitute height model.
    if (area >= 500)
      polygonMesh(rings.map(overviewRing), 0.4, overview, null, 0.4);
    buildings++;
    maxHeight = Math.max(maxHeight, h);
    for (const [x, z] of rings[0]) {
      tb[0] = Math.min(tb[0], x);
      tb[1] = Math.min(tb[1], z);
      tb[2] = Math.max(tb[2], x);
      tb[3] = Math.max(tb[3], z);
    }
  }
  manifestTiles.push({
    id: key,
    bounds: tb,
    maxHeight,
    buildings,
    ...pack(ts, te, offset),
  });
}
console.log(`Buildings: ${count}, streamed tiles: ${manifestTiles.length}`);
// Retain geometry only from the public OpenStreetMap export.
const nodes = new Map(),
  ways = new Map(),
  relations = [];
if (osmPath.endsWith(".json")) {
  const context = JSON.parse(readFileSync(osmPath, "utf8"));
  if (context.remark) throw new Error(context.remark);
  let synthetic = -1;
  const insert = (element) => {
    if (!element.geometry) return null;
    const refs = element.geometry.map((p) => {
      const id = synthetic--;
      nodes.set(id, [p.lon, p.lat]);
      return id;
    });
    if (element.geometry.length > 2) {
      const a = element.geometry[0],
        b = element.geometry.at(-1);
      if (a.lon === b.lon && a.lat === b.lat) refs[refs.length - 1] = refs[0];
    }
    ways.set(element.id, { refs, tags: element.tags ?? {} });
    return refs;
  };
  for (const e of context.elements) {
    if (e.type === "way") insert(e);
  }
  for (const e of context.elements) {
    if (e.type !== "relation") continue;
    const type = kind(e.tags);
    if (!type) continue;
    const members = e.members
      .filter((m) => m.type === "way" && m.geometry)
      .map((m) => {
        if (!ways.has(m.ref)) insert({ ...m, id: m.ref });
        return { id: m.ref, type: "way", role: m.role };
      });
    relations.push({ members, tags: e.tags });
  }
  // Share equal coordinates between relation members to preserve connected rings.
  const canonical = new Map();
  for (const w of ways.values())
    w.refs = w.refs.map((id) => {
      const n = nodes.get(id);
      const key = n.join(",");
      if (!canonical.has(key)) canonical.set(key, id);
      return canonical.get(key);
    });
} else {
  throw new Error("Context must be an Overpass JSON export");
}

console.log(
  `OSM context: ${nodes.size} nodes, ${ways.size} ways, ${relations.length} area relations`,
);
const water = [],
  parks = [],
  roads = [],
  rail = [];
const used = new Set();
const projected = new Map();
const coord = (id) => {
  if (!projected.has(id)) {
    const n = nodes.get(id);
    if (!n) return null;
    projected.set(id, project(...n));
  }
  return projected.get(id);
};
function kind(tags) {
  return tags.natural === "water" || tags.water || tags.waterway === "riverbank"
    ? "water"
    : ["park", "garden"].includes(tags.leisure) ||
        ["forest", "grass", "meadow"].includes(tags.landuse) ||
        tags.natural === "wood"
      ? "park"
      : null;
}
function area(refs, type, holes = []) {
  const outer = refs.map(coord);
  if (outer.some((p) => !p)) return;
  const hs = holes.map((r) => r.map(coord)).filter((r) => r.every(Boolean));
  const points = outer.slice(0, -1);
  polygonMesh(
    [points, ...hs.map((r) => r.slice(0, -1))],
    type === "water" ? 0.15 : 0.1,
    type === "water" ? water : parks,
    null,
    type === "water" ? 0.15 : 0.1,
  );
}
function join(parts) {
  const rings = [];
  let remaining = parts.map((r) => [...r]);
  while (remaining.length) {
    let ring = remaining.pop();
    let changed = true;
    while (ring[0] !== ring.at(-1) && changed) {
      changed = false;
      for (let i = 0; i < remaining.length; i++) {
        const r = remaining[i];
        if (r[0] === ring.at(-1)) {
          ring.push(...r.slice(1));
          remaining.splice(i, 1);
          changed = true;
          break;
        }
        if (r.at(-1) === ring.at(-1)) {
          ring.push(...r.slice(0, -1).reverse());
          remaining.splice(i, 1);
          changed = true;
          break;
        }
      }
    }
    if (ring[0] === ring.at(-1)) rings.push(ring);
  }
  return rings;
}
function inside(ref, ring) {
  const p = coord(ref);
  if (!p) return false;
  let inside = false;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const a = coord(ring[i]),
      b = coord(ring[j]);
    if (!a || !b) return false;
    if (
      a[1] > p[1] !== b[1] > p[1] &&
      p[0] < ((b[0] - a[0]) * (p[1] - a[1])) / (b[1] - a[1]) + a[0]
    )
      inside = !inside;
  }
  return inside;
}
for (const r of relations) {
  const type = kind(r.tags);
  if (!type) continue;
  const members = r.members.filter((m) => m.type === "way" && ways.has(m.id));
  const outer = join(
    members.filter((m) => m.role !== "inner").map((m) => ways.get(m.id).refs),
  );
  const inner = join(
    members.filter((m) => m.role === "inner").map((m) => ways.get(m.id).refs),
  );
  for (const ring of outer) {
    area(
      ring,
      type,
      inner.filter((h) => inside(h[0], ring)),
    );
  }
  members.forEach((m) => used.add(m.id));
}
const widths = {
  motorway: 18,
  trunk: 14,
  primary: 12,
  secondary: 10,
  tertiary: 8,
  residential: 6,
  unclassified: 6,
  living_street: 4,
  pedestrian: 6,
  service: 3,
};
for (const [id, w] of ways) {
  const type = kind(w.tags);
  if (type && !used.has(id) && w.refs[0] === w.refs.at(-1)) area(w.refs, type);
  if (w.tags.tunnel === "yes") continue;
  const width = widths[w.tags.highway];
  const railWay = w.tags.railway === "rail";
  if (!width && !railWay) continue;
  const points = w.refs.map(coord);
  for (let i = 1; i < points.length; i++) {
    const a = points[i - 1],
      b = points[i];
    if (!a || !b) continue;
    if (railWay) {
      rail.push(a[0], 0.5, a[1], b[0], 0.5, b[1]);
      continue;
    }
    const len = Math.hypot(b[0] - a[0], b[1] - a[1]);
    if (len < 0.01) continue;
    const dx = ((b[1] - a[1]) * width) / len / 2,
      dz = (-(b[0] - a[0]) * width) / len / 2;
    const y = w.tags.bridge === "yes" ? 3 : 0.3;
    roads.push(
      a[0] + dx,
      y,
      a[1] + dz,
      b[0] + dx,
      y,
      b[1] + dz,
      b[0] - dx,
      y,
      b[1] - dz,
      a[0] + dx,
      y,
      a[1] + dz,
      b[0] - dx,
      y,
      b[1] - dz,
      a[0] - dx,
      y,
      a[1] - dz,
    );
  }
}
function append(target, values) {
  const s = { start: target.length, count: values.length };
  for (const n of values) target.push(n);
  return s;
}
const overviewSeg = append(surface, overview),
  waterSeg = append(surface, water),
  parkSeg = append(surface, parks),
  roadSeg = append(surface, roads),
  railSeg = append(edges, rail);
// Whole-city coordinates use metre precision; detailed tiles retain half metres.
const base = pack(surface, edges, [0, 0], 1);
const manifest = {
  version: 2,
  ...base,
  buildings: count,
  missingHeights: missing,
  invalidGeometry: invalid,
  tiles: manifestTiles,
  overview: overviewSeg,
  water: waterSeg,
  parks: parkSeg,
  roads: roadSeg,
  rail: railSeg,
  bounds,
};
writeFileSync(`${output}/model.json`, JSON.stringify(manifest));
const provenance = {
  retrievedOn: new Date().toISOString().slice(0, 10),
  buildingSource: "https://gdi.berlin.de/services/wfs/ua_gebaeudehoehen",
  buildingDataset: "Gebäudehöhen 2022 (Umweltatlas)",
  buildingLicense: "dl-de-zero-2.0",
  sourceCrs: "EPSG:25833",
  origin,
  contextSource: "https://overpass-api.de/api/interpreter",
  contextLicense: "ODbL-1.0",
  contextAttribution: "© OpenStreetMap contributors",
  contextInputSha256:
    "sha256:" +
    createHash("sha256").update(readFileSync(osmPath)).digest("hex"),
  contextTimestamp: JSON.parse(readFileSync(osmPath, "utf8")).osm3s
    ?.timestamp_osm_base,
  buildingInputs: inputHashes,
  modelSha256: base.sha256,
  transformation:
    "Numeric geometry only; detailed buildings smaller than 50 m² and unknown/nonpositive heights omitted; detailed tile coordinates quantized to 0.5 m, city overview to 1 m; overview shows flat footprints of shapes at least 500 m² with simplified outlines; flat roof extrusions at source ridge heights; no vertical exaggeration; ground plane, road widths and bridge elevations are illustrative. Context reprojected from WGS84 to EPSG:25833. No building names, addresses or contributor details retained.",
  buildings: count,
  sourceFeatures,
  missingHeights: missing,
  bounds,
  compressedBytes: base.bytes + manifestTiles.reduce((n, t) => n + t.bytes, 0),
};
writeFileSync(`${output}/provenance.json`, JSON.stringify(provenance, null, 2));
console.log(
  JSON.stringify({
    buildings: count,
    tiles: manifestTiles.length,
    overviewMB: base.bytes / 1e6,
    totalMB: provenance.compressedBytes / 1e6,
    bounds,
  }),
);
