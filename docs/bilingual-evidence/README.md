# Bilingual candidate verification — 2 October 2026

Local candidate only. No translation is independently confirmed and no bilingual
production deployment is claimed. Browser checks used the in-app Browser skill
against a same-origin static preview at `http://localhost:4321`.

## Automated checks

- TypeScript passed.
- Eight Node regression checks passed: paired revisions, placeholders, bounded
  map view state, real catalog/source scope, locale route identity, public-copy
  catalog enforcement and the pending review gate.
- 212 Python tests passed, including the complete Astro build, equal published
  fact IDs/evidence/conflicts and withheld treatment across both languages,
  JavaScript-free reading routes, both-language privacy scans and package checks.
- Current-date draft package: 34 routes and 271 static assets. Full privacy scan
  passed across 305 generated files. The prior approved address was reused without
  printing it. No server functions or source artifacts were packaged.
- 34 HTML routes built: 17 German and 17 English, including terminology and 404.
- Release review check fails as intended: 20 facts, 150 listing titles and 14
  contextual term mappings await independent review. This is not a build defect.

The Python fixture builds with a test-only legal address and a frozen 25 August
publication date. The phone screenshots are layout evidence, not proof of a fresh
source retrieval; desktop captures show the current-date preview. A subsequent draft preview package uses the already approved
address and 2 October build date; the public-source dates remain unchanged.

## Browser checks and screenshots

Desktop at 1280 × 720 and simulated phone widths 390 and 320 showed no document
horizontal overflow in the checked atlas, dossier, correction and terminology
screens. Both language controls remain visible. This is viewport simulation,
not physical-phone acceptance.

The German atlas's Mitte place filter retained the same 25 basic entries/pins,
selected C-014, camera and expanded history through EN and DE switches. The
English atlas → dossier → original Evidence → German dossier → C-014 correction
→ English correction journey retained identity and localized internal links.
Reading pages had no client script. The terminology table retained all 14 proposed
mappings with unverified status and contextual notes.

- [German desktop atlas](atlas-de-desktop.jpg)
- [English desktop atlas](atlas-en-desktop.jpg)
- [German phone atlas](atlas-de-phone.jpg)
- [English phone atlas](atlas-en-phone.jpg)
- [German phone dossier](dossier-de-phone.jpg)
- [English phone dossier with original evidence](dossier-en-phone.jpg)

## Limits

No physical-device, exact 195 px failure fixture, reduced-motion or production
check was performed in this session. The localized loading/error paths are
covered by the catalog/build scan; no new network-failure or WebGL-disabled
browser fixture was injected. Translation completeness and synchronized revisions
do not prove semantic equivalence. Original German remains canonical, and
contested stored types remain unresolved.
