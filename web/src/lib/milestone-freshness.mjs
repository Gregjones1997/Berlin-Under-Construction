function exactGermanDate(canonicalDe) {
  const match = /^(\d{2})\.(\d{2})\.(\d{4})$/.exec(canonicalDe ?? "");
  if (!match) {
    return undefined;
  }
  const [, day, month, year] = match;
  return `${year}-${month}-${day}`;
}

export function publicationAsOfDate(explicitDate) {
  if (!explicitDate) {
    throw new Error("PUBLICATION_AS_OF_DATE is required");
  }
  if (!/^\d{4}-\d{2}-\d{2}$/.test(explicitDate)) {
    throw new Error("PUBLICATION_AS_OF_DATE must use YYYY-MM-DD");
  }
  return explicitDate;
}

export function milestoneDisplayWarnings(fact, explicitBuildDate) {
  if (
    fact.factType !== "milestone" ||
    fact.freshness?.state !== "unassessed" ||
    fact.dateValue?.precision !== "exact_day" ||
    !fact.qualifiers?.some(
      (qualifier) =>
        qualifier.qualifierClass === "modal_intent" &&
        qualifier.appliesTo === "date",
    )
  ) {
    return [];
  }

  const plannedDate = exactGermanDate(fact.dateValue.canonicalDe);
  if (!plannedDate) {
    return [];
  }

  const sourceDate = fact.asOfDate?.value ?? "an unstated source date";
  if (publicationAsOfDate(explicitBuildDate) > plannedDate) {
    return [
      `The source planned this milestone for ${fact.dateValue.canonicalDe} as of ${sourceDate}. ` +
        "That date has passed, but no confirming source is recorded. Completion is not asserted.",
    ];
  }

  return [
    `The source planned this milestone for ${fact.dateValue.canonicalDe} as of ${sourceDate}. ` +
      "This is not evidence that the milestone has happened.",
  ];
}
