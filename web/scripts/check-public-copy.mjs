import { parse } from "@astrojs/compiler";
import { readFileSync, readdirSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
const root = resolve(dirname(fileURLToPath(import.meta.url)), "../src");
const walk = (dir) =>
  readdirSync(dir, { withFileTypes: true }).flatMap((e) =>
    e.isDirectory() ? walk(resolve(dir, e.name)) : [resolve(dir, e.name)],
  );
const originals = new Set([
  "BERLIN",
  "UNDER CONSTRUCTION",
  "B",
  "N",
  "BKG",
  "Gregory Anthony Jones",
  "jonesg158@gmail.com",
  "50Hertz",
  "(Daten verändert), Datenquellen:",
]);
export async function checkPublicCopy() {
  const failures = [];
  for (const file of walk(root).filter((f) => f.endsWith(".astro"))) {
    const { ast } = await parse(readFileSync(file, "utf8"));
    function visit(node, parent, protectedValue = false) {
      const skip =
        protectedValue ||
        ["code", "script", "style"].includes(node.name) ||
        node.attributes?.some(
          (a) =>
            (a.name === "lang" && a.value === "de") ||
            (a.name === "aria-hidden" && a.value === "true"),
        );
      if (node.type === "text" && parent?.type !== "expression" && !skip) {
        const value = node.value.trim();
        if (
          /[A-Za-zÄÖÜäöüß]/.test(value) &&
          !originals.has(value) &&
          !/^C-\d{3}(?:\s*—)?$/.test(value) &&
          !value.startsWith("--")
        )
          failures.push(`${file}: literal public copy: ${value}`);
      }
      for (const attr of node.attributes ?? []) {
        const publicAttribute =
          [
            "title",
            "heading",
            "subtitle",
            "aria-label",
            "placeholder",
          ].includes(attr.name) ||
          (attr.name === "content" &&
            node.attributes.some(
              (a) => a.name === "name" && a.value === "description",
            ));
        if (
          publicAttribute &&
          attr.kind === "quoted" &&
          /[A-Za-zÄÖÜäöüß]/.test(attr.value) &&
          !originals.has(attr.value)
        )
          failures.push(`${file}: literal ${attr.name}: ${attr.value}`);
        if (
          publicAttribute &&
          attr.kind === "expression" &&
          /^`[A-Za-z][^`]*\$\{/.test(attr.value)
        )
          failures.push(`${file}: unlocalized ${attr.name} template`);
      }
      if (node.type !== "frontmatter")
        for (const child of node.children ?? []) visit(child, node, skip);
    }
    visit(ast, null);
  }
  if (failures.length) throw Error(failures.join("\n"));
  return "Public Astro copy uses the paired catalog or labelled original values.";
}
if (process.argv[1] === fileURLToPath(import.meta.url))
  console.log(await checkPublicCopy());
