# Mobile readthrough — 9 September 2026

Scope: local checkpoint 8483760 at 390 × 844 in the Browser tool. This is a
phone-sized browser viewport, not physical-device touch or network testing.
No implementation changes were made. Screenshots are local review artifacts.

- Homepage: navigation/footer text is very small; area chooser wraps; open project
  list occupies much of the map. Mouse-specific instructions remain visible.
  Screenshot: `/private/tmp/berlin-mobile-home.png`.
- C-014 card: title/status/date hierarchy is readable and the full-overview action
  is visible. Description source arrow wraps to a separate line; supporting text
  and source targets are small. Screenshot: `/private/tmp/berlin-mobile-card.png`.
- Expanded overview: project name repeats; not-applicable freshness/date fields
  consume the first screen. Opening details, returning to the brief, and closing
  the project succeeded. Screenshot: `/private/tmp/berlin-mobile-overview.png`.
- Project index: readable body text, but the first screen contains implementation
  and provider-call disclosures instead of projects. Move this material to the
  method/context section and prioritize the project list.
  Screenshot: `/private/tmp/berlin-mobile-index.png`.
- Method: prose and metrics fit the viewport; header navigation remains tiny.
  Screenshot: `/private/tmp/berlin-mobile-method.png`.

Next: simplify the mobile map controls and project chooser; enlarge navigation,
footer and source targets; prioritize project content on the index and expanded
record. Keep detailed evidence available. Then check real touch interactions,
small-screen landscape, keyboard access, source disclosure scrolling and loading
on a real mobile connection. No full mobile acceptance is claimed.
