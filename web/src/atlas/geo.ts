import proj4 from "proj4";
// Same metric reference frame is used by preprocessing and camera/marker placement.
export const UTM = "+proj=utm +zone=33 +ellps=GRS80 +units=m +no_defs";
export const ORIGIN = [391000, 5820000] as const;
export function cityPoint(lon: number, lat: number): [number, number] {
  const [e, n] = proj4("EPSG:4326", UTM, [lon, lat]);
  return [e - ORIGIN[0], ORIGIN[1] - n];
}
