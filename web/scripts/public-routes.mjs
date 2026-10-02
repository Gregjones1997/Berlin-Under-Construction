// The public route contract is shared by packaging and the localization audit.
export const germanPages = [
  "index.html",
  "404.html",
  "impressum/index.html",
  "privacy/index.html",
  "method/index.html",
  "records/index.html",
  "style-guide/index.html",
  "terminology/index.html",
  "projects/europaplatz-sued/index.html",
  "projects/heinrich-hertz-gymnasium-ostbahnhof/index.html",
  "projects/power-to-heat-heizkraftwerk-mitte/index.html",
  "corrections/index.html",
  "corrections/projects/C-014/index.html",
  "corrections/projects/C-010/index.html",
  "corrections/projects/C-019/index.html",
  "corrections/organizations/50hertz/index.html",
  "corrections/organizations/senatsverwaltung-stadtentwicklung-bauen-wohnen/index.html",
];
export const publicPages = [
  ...germanPages,
  ...germanPages.map((path) =>
    path === "404.html" ? "en/404/index.html" : "en/" + path,
  ),
];
