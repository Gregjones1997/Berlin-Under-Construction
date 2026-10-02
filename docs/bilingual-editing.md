# Maintaining the German and English site

Tell Codex the change in English. The builder updates both languages in the same
reviewable diff and previews the affected screens in each locale. No CMS or
translation-provider account is needed. German source facts are never rewritten
as an editorial shortcut.

## Shared implementation and copy

German uses existing URLs; English uses `/en/` equivalents. English route files
wrap the same Astro components. `web/src/lib/i18n.ts` owns message lookup, explicit
state labels, display explanations and supported source-date formatting.

The paired catalogs are in `web/src/i18n/`:

| File | Scope |
| --- | --- |
| `messages.json` | Navigation, pages, legal/privacy copy, accessibility, map states and structural labels |
| `facts.json` | English explanations of the 20 existing published facts; original German and source revision retained |
| `listings.json` | Explanatory English titles for 150 basic register listings; official German titles retained |
| `terms.json` | Proposed contextual domain mappings, glossary version/revision and review status |
| `revisions.json` | Acknowledged hashes of both language values; synchronization evidence, not semantic certification |

Keep existing IDs stable. New wording gets a paired entry and a shared component
reference. Do not put visitor copy directly into Astro text or public attributes.
The public-copy check detects literal Astro wording; dynamic atlas messages must
also use the catalog. Original quotations, proper names and identifiers retain
their source form. English descriptive titles do not imply official English names.

After updating both values, acknowledge only the changed IDs:

```sh
cd web
npm run i18n:sync -- messages:translation.note
npm run i18n:check
npm run typecheck
node --test scripts/i18n.test.mjs
npm run build
```

Use the actual affected IDs. For a punctuation/idiom edit whose other language is
already equivalent, the sync command requires `--equivalent-reason "reason"`.
That exception must explain equivalence; it never establishes independent review.
Never regenerate every revision to conceal an untranslated change.

Source changes also invalidate the full fact/listing fingerprint. Update the
explanation against the changed source, reset confirmation, and preserve original
source data and publication boundaries. A glossary change invalidates term
mappings for renewed review. No withheld value belongs in a translation catalog.

## Review and release

Current domain entries are `editorial_unverified`. The public terminology page
shows their context and status; it does not claim they are confirmed. Neither
build success nor agreement between models verifies meaning. A qualified human
must assess consequential German wording in context, especially contested types.

For a confirmed entry, record `reviewerId`, review `date`, precise `scope` and
`meaningRevision` in `review`, and set `verification` to `confirmed`. Use a
non-identifying reviewer reference linked to the retained review evidence, not
personal data. The meaning revision is the `digest` exported by
`web/scripts/check-i18n.mjs`, over these objects:

- Facts/listings: `{de, en, sourceRevision}`.
- Terms: `{de, en, context: messages[contextMessage], glossaryRevision}`.

The fingerprint ensures changed meaning or context cannot retain an old
confirmation. It does not authenticate a reviewer. The builder must verify the
independent review evidence before accepting metadata. Confirmation of a passage
does not resolve a contested stored type or verify the entire glossary. Keep the
previous review in Git history. Golden values still require separate human
authority under AGENTS.md.

`npm run i18n:release-check` and the standard `npm run package:vercel` reject
unreviewed domain entries. Do not bypass this by calling the packaging script
for a public release. `npm run package:preview` permits a draft preview package,
still enforcing existing postal-address, privacy and package checks. The same
build contains both languages; there is no mixed-language fallback release.

Verify both routes, original evidence, conflict/withheld presentations, keyboard
navigation, phone layouts and map view switching. Run the export privacy scans
across both locales and assets. Follow `public-deployment.md` only after review
and the release checks pass; updating copy is not deployment authorization.
