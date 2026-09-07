/** Package the checked static export only. Never upload the repository or retained artifacts. */
import {
  cpSync,
  existsSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { join, relative } from "node:path";
const root = "dist";
const out = ".vercel/output";
if (!existsSync(join(root, "index.html")))
  throw new Error("Build the site first");
const walk = (dir) =>
  readdirSync(dir, { withFileTypes: true }).flatMap((e) =>
    e.isDirectory() ? walk(join(dir, e.name)) : [join(dir, e.name)],
  );
const address = process.env.LEGAL_ADDRESS;
const date = process.env.PUBLICATION_AS_OF_DATE;
if (!address || !date)
  throw new Error(
    "LEGAL_ADDRESS and PUBLICATION_AS_OF_DATE are required when packaging",
  );
for (const route of ["impressum", "privacy"])
  if (!readFileSync(join(root, route, "index.html"), "utf8").includes(address))
    throw new Error("The export does not match the supplied legal address");
const files = walk(root);
const pages = files.filter((p) => p.endsWith(".html"));
if (pages.length !== 14) throw new Error("Unexpected route count");
for (const file of files) {
  if (/\.(?:pdf|sqlite3?|py|env)$/i.test(file))
    throw new Error(`Private artifact in static output: ${file}`);
  if (
    file.endsWith(".html") &&
    !readFileSync(file, "utf8").includes(`This page was generated on ${date}.`)
  )
    throw new Error("The export does not match the publication date");
  if (
    file.endsWith(".html") &&
    /test-only|\[\[ANSCHRIFT\]\]/i.test(readFileSync(file, "utf8"))
  )
    throw new Error("Test address or placeholder in deployment");
}
const csp =
  "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; font-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'none'";
const routes = [
  {
    src: "/(.*)",
    headers: {
      "Content-Security-Policy": csp,
      "Referrer-Policy": "no-referrer",
      "X-Content-Type-Options": "nosniff",
    },
    continue: true,
  },
  {
    src: "/_astro/(.*)",
    headers: { "Cache-Control": "public, max-age=31536000, immutable" },
    continue: true,
  },
  {
    src: "/atlas/berlin-(.*)\\.bin\\.gz",
    headers: { "Cache-Control": "public, max-age=31536000, immutable" },
    continue: true,
  },
  ...pages.map((p) => {
    const file = relative(root, p);
    if (file === "index.html") return { src: "^/$", dest: "/index.html" };
    const path = "/" + file.slice(0, -11);
    return { src: "^" + path + "/?$", dest: "/" + file };
  }),
  { handle: "filesystem" },
];
const model = JSON.parse(readFileSync(join(root, "atlas/model.json"), "utf8"));
const config = {
  version: 3,
  routes,
  overrides: { [model.geometry.slice(1)]: { contentType: "application/gzip" } },
  framework: {
    version: JSON.parse(readFileSync("package.json", "utf8")).dependencies
      .astro,
  },
};
rmSync(out, { recursive: true, force: true });
mkdirSync(out, { recursive: true });
cpSync(root, join(out, "static"), { recursive: true });
writeFileSync(join(out, "config.json"), JSON.stringify(config, null, 2) + "\n");
console.log(
  `Packaged ${pages.length} HTML routes and ${files.length - pages.length} static assets. No source files or server functions.`,
);
