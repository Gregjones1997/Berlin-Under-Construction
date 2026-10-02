import type { MapView } from "./renderer";
export type AtlasViewState = {
  camera: MapView;
  plan: boolean;
  expanded: boolean;
  filter: string;
  area: string;
  labels: Record<"projects" | "basic" | "water" | "parks", boolean>;
};
export function decodeViewState(
  raw: string | null,
): AtlasViewState | undefined {
  if (!raw || raw.length > 1000) return undefined;
  try {
    const value = JSON.parse(raw);
    const vector = (v: unknown) =>
      Array.isArray(v) &&
      v.length === 3 &&
      v.every(
        (n) =>
          typeof n === "number" && Number.isFinite(n) && Math.abs(n) <= 250000,
      );
    if (
      !vector(value.camera?.target) ||
      !vector(value.camera?.offset) ||
      typeof value.camera.zoom !== "number" ||
      !Number.isFinite(value.camera.zoom) ||
      value.camera.zoom < 0.01 ||
      value.camera.zoom > 100 ||
      typeof value.plan !== "boolean" ||
      typeof value.expanded !== "boolean" ||
      typeof value.filter !== "string" ||
      value.filter.length > 60 ||
      typeof value.area !== "string" ||
      value.area.length > 60
    )
      return undefined;
    if (
      !["projects", "basic", "water", "parks"].every(
        (key) => typeof value.labels?.[key] === "boolean",
      )
    )
      return undefined;
    if (Math.hypot(...value.camera.offset) < 1) return undefined;
    return {
      camera: {
        target: value.camera.target,
        offset: value.camera.offset,
        zoom: value.camera.zoom,
      },
      plan: value.plan,
      expanded: value.expanded,
      filter: value.filter,
      area: value.area,
      labels: {
        projects: value.labels.projects,
        basic: value.labels.basic,
        water: value.labels.water,
        parks: value.labels.parks,
      },
    };
  } catch {
    return undefined;
  }
}
export function encodeViewState(value: AtlasViewState): string {
  const text = JSON.stringify(value);
  if (!decodeViewState(text)) throw new Error("Invalid atlas view");
  return text;
}
