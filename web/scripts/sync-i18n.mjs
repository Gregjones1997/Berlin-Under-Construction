// Explicit editorial acknowledgment; never establishes independent language verification.
import { readFileSync, writeFileSync } from "node:fs";
import { digest, validatePair } from "./check-i18n.mjs";
const args = process.argv.slice(2),
  reasonIndex = args.indexOf("--equivalent-reason");
const reason = reasonIndex < 0 ? null : args[reasonIndex + 1];
if (reasonIndex >= 0) args.splice(reasonIndex, 2);
if (!args.length)
  throw Error(
    "Provide explicit catalog:id pairs; blanket synchronization is not supported",
  );
const lock = JSON.parse(readFileSync("src/i18n/revisions.json", "utf8"));
for (const key of args) {
  const [file, ...rest] = key.split(":");
  if (!["messages", "facts", "listings", "terms"].includes(file))
    throw Error("Unknown catalog");
  const pair = JSON.parse(readFileSync(`src/i18n/${file}.json`, "utf8"))[
    rest.join(":")
  ];
  if (!pair) throw Error(`Unknown pair: ${key}`);
  const hashes = { de: digest(pair.de), en: digest(pair.en) };
  validatePair(key, pair, hashes);
  const previous = lock[key];
  if (
    previous &&
    (previous.de === hashes.de || previous.en === hashes.en) &&
    !reason
  )
    throw Error(
      `One language unchanged: ${key}; update its counterpart or provide --equivalent-reason`,
    );
  lock[key] = {
    ...hashes,
    editorialAcknowledgment:
      "Codex paired update; independent verification not established",
    ...(reason ? { equivalentReason: reason } : {}),
  };
}
writeFileSync("src/i18n/revisions.json", JSON.stringify(lock, null, 2) + "\n");
