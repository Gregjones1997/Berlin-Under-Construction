export type Locale = "de" | "en";
export const locales: Locale[] = ["de", "en"];
export function localeFromPath(path: string): Locale {
  return /^\/en(?:\/|[?#]|$)/.test(path) ? "en" : "de";
}
export function unlocalizedPath(path: string): string {
  const clean = path.replace(/^\/en(?=\/|[?#]|$)/, "");
  return !clean || /^[?#]/.test(clean) ? "/" + clean : clean;
}
export function localizePath(path: string, locale: Locale): string {
  if (!path.startsWith("/") || path.startsWith("//")) return path;
  const clean = unlocalizedPath(path);
  if (/^\/404(?:\/|\.html)(?=[?#]|$)/.test(clean)) {
    const suffix = clean.replace(/^\/404(?:\/|\.html)/, "");
    return (locale === "en" ? "/en/404/" : "/404.html") + suffix;
  }
  return locale === "en" ? "/en" + clean : clean;
}
