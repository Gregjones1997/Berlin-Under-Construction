# Recruiter-ready proof of concept

Owner direction, 9 September 2026: finish the existing three-case release for a
personal portfolio, check repository hygiene and credentials, and consider a
separate pending-research layer. This takes priority over preparing the next
full dossier. The live product is a prototype; scored AI accuracy is not established.

## Finish order

1. **Repository and release hygiene.** Check reachable commit history for
   credentials without printing values; check ignored private inputs, dependencies,
   tests, type checking and build-log hashes. Preserve coherent historical commits
   and attribution. If credentials are found, revoke/rotate before any separately
   coordinated history rewrite. Check deployment output separately from Git.
2. **Three-case presentation walkthrough.** The owner already verified the original
   source wording for the three frozen dossiers; do not repeat that acceptance task.
   Evidence: owner confirmations in `docs/research/dossiers/`, the completed Phase 1
   checklist items, and `public/data/accepted-review-decisions.json` (including the
   later C-014 publication decisions). Check that deployed C-014 Europaplatz,
   C-010 Heinrich-Hertz school and C-019 Power-to-Heat correctly present the accepted
   records, evidence links, conflicts, withheld values and correction routes.
   Two located projects and
   three records is the current contract; do not invent a third map position.
   Recheck time-sensitive source wording before updating publication freshness.
   The separate `evaluation/golden-set.json` still contains placeholders; that
   deferred accuracy-evaluation work does not invalidate completed dossier review
   or block this portfolio release.
3. **AI proof.** Make the existing source-to-extraction-to-validation example easy
   to find. Use recorded metering and actual rejection behavior. Distinguish
   deterministic checks from independently measured extraction accuracy.
4. **Portfolio story.** Prepare concise problem, role, architecture, tradeoffs,
   measured results and limitations, with app/repository links and a two-minute
   walkthrough. Explain preserving German evidence as a response to the author's
   language barrier. In a business application, translation/terminology review
   fits existing internal review; temporary review labels may be removed after
   approval while evidence and approval history remain. This business application
   is proposed, not implemented departmental workflow.
5. **Mobile and desktop acceptance.** Test map controls, project selection,
   navigation, evidence expansion and keyboard access. Capture readable screenshots
   and measure loading; the 390 × 844 preview shows crowded atlas controls.
6. **Release verification.** Build with real deployment configuration, deploy the
   checked candidate, verify public routes/assets/private-path exclusion, and link
   the accepted version from the personal portfolio. Test addresses must never
   enter the deployed artifact. Capture the source commit and verification scope.

## Optional pending-research layer

This is a follow-on enhancement, not a prerequisite for showing the three-case
proof of concept. The owner proposed approximately 40 additional projects across
three or four categories. The existing ledger has 33 rows total, including the
pilots; seven expansion candidates have a recent source screening. None of those
seven has approved coordinates. A count target is not evidence of coverage.

- Use a separate `Research pending` filter/tab and visually distinct markers.
- Require source-backed identity, category and geometry before publishing a marker.
- Show the canonical project name, supported category, source link and exactly what
  review remains. Keep research status separate from construction status.
- Support tap and keyboard activation as well as hover; users on phones cannot hover.
- Keep candidates lacking supported geometry in a list until located.
- Do not describe a candidate as awaiting automation unless an actual processing
  queue exists. Do not imply departmental or authority approval of the project.
- Existing evidence, naming, correction and German-language rules still apply.

Start with the source-supported subset rather than fabricating 40 markers. Category
choices should follow the evidence; the recently screened subset covers bridges,
rail and schools. Housing needs its own source and location checks.

## Initial audit evidence, 9 September

- Clean working tree before audit; 146 commits on HEAD history.
- All 92 recorded build-log hashes validated against reachable history.
- 187 tests passed in 22.45 seconds; TypeScript check passed.
- Targeted credential-format scan of 848 blobs across locally reachable refs found
  no matches. Checked private-key headers, selected provider tokens and credentialed
  database URLs. This does not cover every secret format, remote-only refs, ignored
  files, deployment settings or provider access logs.
- `.env.example` is tracked; the checked credential/key/artifact filename patterns
  returned no other tracked entries. Retained artifacts are ignored.
- Initial npm audit reported four affected packages: Astro, js-yaml, sharp and
  svgo. Installed-package advisories are not proof of an exploitable production
  endpoint: this deployment uses static output. Updated Astro to 7.3.2 and refreshed
  compatible transitive dependencies; npm audit fix then reported zero vulnerabilities.
  TypeScript passed after the update. Production has not been redeployed with it.
  Post-update regression suite: 187 passed in 23.94 seconds.
  Regression builds use a test-only legal address and are not deployment artifacts.

Remaining checks above are open unless independently recorded as completed.
