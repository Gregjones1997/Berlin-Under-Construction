/** Offline mesh compiler. No source text, addresses or names enter the runtime model. */
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { createHash } from "node:crypto";
import { gzipSync } from "node:zlib";
import { ShapeUtils, Vector2 } from "three";
import proj4 from "proj4";
const [buildingPath, osmPath] = process.argv.slice(2);
if (!buildingPath || !osmPath)
  throw new Error(
    "Usage: node scripts/build-atlas.mjs buildings.json context.json",
  );
const UTM = "+proj=utm +zone=33 +ellps=GRS80 +units=m +no_defs";
const origin = [391000, 5820000];
const project = (lon, lat) => {
  const [e, n] = proj4("EPSG:4326", UTM, [lon, lat]);
  return [e - origin[0], origin[1] - n];
};
const raw = readFileSync(buildingPath);
const data = JSON.parse(raw);
if (!Array.isArray(data.features) || !data.features.length)
  throw new Error("No building features");
if (data.numberMatched > data.features.length)
  throw new Error(
    `Truncated export: ${data.features.length}/${data.numberMatched}`,
  );
const surface = [],
  edges = [],
  tiles = new Map();
let count = 0,
  missing = 0,
  invalid = 0;
const bounds = [Infinity, Infinity, -Infinity, -Infinity];
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
for (const f of data.features) {
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
  const polygons = f.geometry.coordinates.map((p) => p.map(cleaned));
  for (const rings of polygons) {
    if (rings[0].length < 3) continue;
    const p = rings[0][0];
    const key = `${Math.floor(p[0] / 750)}:${Math.floor(p[1] / 750)}`;
    if (!tiles.has(key)) tiles.set(key, { surface: [], edges: [] });
    const tile = tiles.get(key);
    polygonMesh(rings, h, tile.surface, tile.edges);
    for (const [x, z] of rings[0]) {
      bounds[0] = Math.min(bounds[0], x);
      bounds[1] = Math.min(bounds[1], z);
      bounds[2] = Math.max(bounds[2], x);
      bounds[3] = Math.max(bounds[3], z);
    }
  }
  count++;
}
const manifestTiles = [];
for (const t of tiles.values()) {
  const s = { start: surface.length, count: t.surface.length },
    e = { start: edges.length, count: t.edges.length };
  for (const n of t.surface) surface.push(n);
  for (const n of t.edges) edges.push(n);
  manifestTiles.push({ surface: s, edges: e });
}
console.log(
  `Buildings: ${count}, tiles: ${tiles.size}, missing heights: ${missing}`,
);
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
const waterSeg = append(surface, water),
  parkSeg = append(surface, parks),
  roadSeg = append(surface, roads),
  railSeg = append(edges, rail);
const maxCoordinate = Math.max(
  ...bounds.map(Math.abs),
  ...surface.filter((_, i) => i % 10000 === 0).map(Math.abs),
);
const quantization = maxCoordinate < 16000 ? 2 : 1;
const packed = new Int16Array(surface.length + edges.length);
for (let i = 0; i < surface.length + edges.length; i++) {
  const value = i < surface.length ? surface[i] : edges[i - surface.length];
  const q = Math.round(value * quantization);
  if (!Number.isFinite(q) || q < -32768 || q > 32767)
    throw new Error("Geometry exceeds packed coordinate range");
  packed[i] = q;
}
const gzip = gzipSync(new Uint8Array(packed.buffer), { level: 9 });
const hash = createHash("sha256").update(gzip).digest("hex");
const output = "site-public/atlas";
mkdirSync(output, { recursive: true });
const filename = `berlin-${hash.slice(0, 12)}.bin.gz`;
writeFileSync(`${output}/${filename}`, gzip);
const manifest = {
  version: 1,
  quantization,
  buildings: count,
  missingHeights: missing,
  invalidGeometry: invalid,
  tiles: manifestTiles,
  water: waterSeg,
  parks: parkSeg,
  roads: roadSeg,
  rail: railSeg,
  bounds,
  surfaceFloats: surface.length,
  edgeFloats: edges.length,
  geometry: `/atlas/${filename}`,
};
writeFileSync(`${output}/model.json`, JSON.stringify(manifest));
writeFileSync(
  `${output}/provenance.json`,
  JSON.stringify(
    {
      retrievedOn: "2026-09-07",
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
      buildingInputSha256:
        "sha256:" + createHash("sha256").update(raw).digest("hex"),
      modelSha256: "sha256:" + hash,
      transformation:
        "Numeric geometry only; buildings smaller than 50 m² and unknown/nonpositive heights omitted; Coordinates quantized to the packed model precision (see model manifest); flat roof extrusions at source ridge heights; no vertical exaggeration; ground plane, road widths and bridge elevations are illustrative. Context is reprojected from WGS84 into EPSG:25833. No building names, addresses, or contributor details retained.",
      buildings: count,
      sourceFeatures: data.features.length,
      missingHeights: missing,
      bounds,
    },
    null,
    2,
  ),
);
console.log(
  JSON.stringify({
    buildings: count,
    triangles: surface.length / 9,
    edges: edges.length / 6,
    gzipMB: gzip.length / 1e6,
    bounds,
  }),
);
