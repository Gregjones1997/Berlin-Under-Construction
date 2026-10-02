import messages from "../i18n/messages.json";

import {
  locales,
  localeFromPath,
  localizePath,
  unlocalizedPath,
  type Locale,
} from "./locales";
export { locales, localeFromPath, localizePath, unlocalizedPath, type Locale };
export function forLocale(locale: Locale) {
  return (id: string, values: Record<string, string | number> = {}): string => {
    const entry = (messages as Record<string, { en: string; de: string }>)[id];
    if (!entry?.[locale]?.trim())
      throw new Error(`Missing ${locale} message: ${id}`);
    return entry[locale].replace(/\{([a-zA-Z]\w*)\}/g, (_, key: string) => {
      if (!(key in values))
        throw new Error(`Missing placeholder ${key} in ${id}`);
      return String(values[key]);
    });
  };
}
export function enumLabel(value: unknown, locale: Locale): string {
  if (typeof value !== "string") return forLocale(locale)("state.not_stated");
  return forLocale(locale)(`state.${value}`);
}
export const formatNumber = (value: number, locale: Locale) =>
  new Intl.NumberFormat(locale === "de" ? "de-DE" : "en-GB", {
    maximumFractionDigits: 8,
  }).format(value);

import factTranslations from "../i18n/facts.json";
import listingTranslations from "../i18n/listings.json";
import type { PublicFact } from "./public-projects";
export function factText(fact: PublicFact, locale: Locale): string {
  if (fact.state !== "published" || !fact.valueDe || !fact.evidence)
    throw new Error("Cannot translate a withheld fact");
  const entry = (
    factTranslations as Record<string, { de: string; en: string }>
  )[fact.factId];
  if (!entry || entry.de !== fact.valueDe)
    throw new Error(`Stale fact translation: ${fact.factId}`);
  return locale === "de" ? fact.valueDe : entry.en;
}
export function projectName(
  project: { publishedFacts: PublicFact[] },
  locale: Locale,
): string {
  const fact = project.publishedFacts.find(
    (f) => f.factType === "project_name",
  );
  if (!fact) throw new Error("Missing project name");
  return factText(fact, locale);
}
export function listingName(
  project: { id: string; nameDe: string },
  locale: Locale,
): string {
  const entry = (
    listingTranslations as Record<string, { de: string; en: string }>
  )[project.id];
  if (!entry || entry.de !== project.nameDe)
    throw new Error(`Stale listing translation: ${project.id}`);
  return entry[locale];
}
export function dateText(value: string, locale: Locale): string {
  if (locale === "de" || /^\d{4}(?:-\d{2}-\d{2})?$/.test(value)) return value;
  const map: Record<string, string> = Object.fromEntries(
    Object.entries(messages)
      .filter(([id]) => id.startsWith("date."))
      .map(([id, pair]) => [pair.de, id]),
  );
  if (!map[value]) throw new Error(`Unmapped source date: ${value}`);
  return forLocale(locale)(map[value]);
}
export function qualifierText(value: string, locale: Locale): string {
  const map: Record<string, string> = Object.fromEntries(
    Object.entries(messages)
      .filter(([id]) => id.startsWith("qualifier."))
      .map(([id, pair]) => [pair.de, id]),
  );
  if (!map[value]) throw new Error(`Unmapped qualifier: ${value}`);
  return forLocale(locale)(map[value]);
}
export function factWarning(fact: PublicFact, locale: Locale): string {
  const date = (fact.dateValue as { canonicalDe?: string })?.canonicalDe;
  if (!date) throw new Error("Warning requires a source date");
  const sourceDate =
    (fact.asOfDate as { value?: string })?.value ??
    forLocale(locale)("state.not_stated");
  // The publication decision is already computed by the existing freshness gate.
  const warning = (fact.displayWarnings as string[])[0] ?? "";
  return forLocale(locale)(
    warning.includes("has passed") ? "warning.passed" : "warning.planned",
    { date: dateText(date, locale), sourceDate },
  );
}
