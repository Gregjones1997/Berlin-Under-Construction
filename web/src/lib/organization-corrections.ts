export interface OrganizationCorrection {
  name: string;
  path: string;
}

const CORRECTIONS_BY_FACT_ID: Record<string, OrganizationCorrection> = {
  "c014-approved-total-cost": {
    name: "Senatsverwaltung für Stadtentwicklung, Bauen und Wohnen",
    path: "/corrections/organizations/senatsverwaltung-stadtentwicklung-bauen-wohnen/",
  },
  "c019-financing-commitment": {
    name: "50Hertz",
    path: "/corrections/organizations/50hertz/",
  },
};

export function organizationCorrectionForFact(
  factId: string,
): OrganizationCorrection | undefined {
  return CORRECTIONS_BY_FACT_ID[factId];
}
