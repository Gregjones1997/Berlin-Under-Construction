import type { Locale } from "./locales";
/** Only exact-day source forms become numeric dates. Partial dates return undefined. */
export function numericCardDate(
  value: string,
  locale: Locale,
): string | undefined {
  const months = [
    "Januar",
    "Februar",
    "März",
    "April",
    "Mai",
    "Juni",
    "Juli",
    "August",
    "September",
    "Oktober",
    "November",
    "Dezember",
  ];
  const named = value.match(/^(\d{1,2})\. ([A-Za-zÄä]+) (\d{4})$/);
  const numeric = value.match(/^(\d{1,2})\.(\d{1,2})\.(\d{4})$/);
  const iso = value.match(/^(\d{4})-(\d{2})-(\d{2})$/);
  const month = named ? months.indexOf(named[2]) + 1 : 0;
  const parts =
    named && month
      ? [named[1], String(month), named[3]]
      : numeric
        ? [numeric[1], numeric[2], numeric[3]]
        : iso
          ? [iso[3], iso[2], iso[1]]
          : null;
  return parts
    ?.map((n, i) => (i < 2 ? n.padStart(2, "0") : n))
    .join(locale === "de" ? "." : "/");
}
