import { readFileSync } from "node:fs";
import { resolve } from "node:path";

export type PublicFact = {
  factId: string;
  factType: string;
  state: "published" | "withheld";
  valueDe?: string;
  reasonCode?: string;
  evidence?: {
    exactTextDe: string;
    sourceUrl: string;
    [key: string]: unknown;
  };
  [key: string]: unknown;
};

export const EVIDENCE_LABEL_GLOSSARY: Record<string, string> = {
  Verified:
    "The displayed wording is faithfully supported by the cited source. It does not mean the value is current, the only official value, or that a conflicting value is resolved.",
  Corroborated: "More than one reliable source supports the displayed claim.",
  Reported: "A reputable secondary source reports the displayed claim.",
  Observed: "A dated observation supports visible conditions, not cause.",
  Disputed: "Relevant counterevidence exists and review remains open.",
};

type PublicConflict = {
  conflictId: string;
  memberFactIds: string[];
  [key: string]: unknown;
};

type ProjectRecord = {
  projectId: string;
  slug: string;
  correctionPath: string;
  facts: PublicFact[];
  conflicts: PublicConflict[];
};

export type PublicProjectPage = {
  projectId: string;
  slug: string;
  correctionPath: string;
  publishedFacts: PublicFact[];
  withheldFacts: PublicFact[];
  conflicts: Array<PublicConflict & { facts: PublicFact[] }>;
};

const projectionPath = resolve(process.cwd(), "../public/data/projects.json");

function fail(message: string): never {
  throw new Error(`Public projection cannot build: ${message}`);
}

function pageRecord(project: ProjectRecord): PublicProjectPage {
  const factsById = new Map(project.facts.map((fact) => [fact.factId, fact]));
  const conflictMemberIds = new Set(
    project.conflicts.flatMap((conflict) => conflict.memberFactIds),
  );

  for (const fact of project.facts) {
    if (fact.state === "published") {
      if (!fact.valueDe?.trim() || !fact.evidence?.exactTextDe.trim()) {
        fail(`published fact ${fact.factId} has no value or exact German span`);
      }
      if (!fact.evidence.sourceUrl.startsWith("https://")) {
        fail(`published fact ${fact.factId} has no HTTPS source URL`);
      }
    } else if (
      !fact.reasonCode ||
      "valueDe" in fact ||
      "evidence" in fact
    ) {
      fail(`withheld fact ${fact.factId} contains display data or no reason code`);
    }
  }

  const conflicts = project.conflicts.map((conflict) => ({
    ...conflict,
    facts: conflict.memberFactIds.map((factId) => {
      const fact = factsById.get(factId);
      if (!fact || fact.state !== "published") {
        return fail(`conflict ${conflict.conflictId} has an invalid member`);
      }
      return fact;
    }),
  }));

  return {
    projectId: project.projectId,
    slug: project.slug,
    correctionPath: project.correctionPath,
    publishedFacts: project.facts.filter(
      (fact) => fact.state === "published" && !conflictMemberIds.has(fact.factId),
    ),
    withheldFacts: project.facts.filter((fact) => fact.state === "withheld"),
    conflicts,
  };
}

export function loadPublicProjectPages(): PublicProjectPage[] {
  const projection = JSON.parse(readFileSync(projectionPath, "utf8")) as {
    projects?: ProjectRecord[];
  };
  if (!Array.isArray(projection.projects)) {
    fail("projects list is missing");
  }
  return projection.projects.map(pageRecord);
}
