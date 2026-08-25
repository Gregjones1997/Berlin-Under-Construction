# C-010 milestone recheck

**Checked:** 2026-08-25
**Fact:** `c010-technical-handover-current`
**Status:** The recorded date is still a plan; no completion is asserted.

## Sources checked

1. The [19 June 2026 parliamentary answer](https://pardok.parlament-berlin.de/starweb/adis/citat/VT/19/SchrAnfr/S19-26230.pdf)
   still states: `Die technische Übergabe des Neubaus an den Bezirk ist für den
   31.08.2026 geplant.` It also states that the implementation was on schedule
   as of that answer. Neither sentence confirms a later outcome.
2. The [6 July 2026 district update](https://www.berlin.de/ba-friedrichshain-kreuzberg/aktuelles/pressemitteilungen/2026/pressemitteilung.1689904.php)
   still states: `In Abstimmung mit allen Beteiligten ist die bauliche
   Fertigstellung am Ostbahnhof und die Übergabe an den Bezirk zum 31. August
   2026 geplant.` It separates later equipment and the move/teaching schedule.
3. The [current HOWOGE project page](https://unternehmen.howoge.de/schulbau/heinrich-hertz-gymnasium-projektuebersicht),
   observed 2026-08-25, still presents the project as `Im Bau`, gives `Bauzeit
   2024 bis 2026`, and says `Die Endfertigstellung ist für 2026 vorgesehen.` It
   does not confirm the 31 August technical handover as completed.

The recheck found no newer checked source that confirms or supersedes the
31 August technical-handover plan. This is an absence in the checked source set,
not evidence that the handover failed or occurred.

## Display decision

Keep the exact German planned claim and its `geplant` qualifier. Do not convert
it into a completion, current status or delay claim.

The unstyled Astro display adds a build-time warning:

- through 31 August 2026: the source planned the milestone for that date, but
  the plan is not evidence that it happened;
- after 31 August 2026: the planned date has passed, no confirming source is
  recorded, and completion is not asserted.

The build date can be pinned with `PUBLICATION_AS_OF_DATE=YYYY-MM-DD` so the
static artifact is reproducible and the passed-date treatment is testable. The
canonical German value, evidence span, milestone qualifier and accepted review
decision are unchanged.

## Next check

Recheck official district, parliamentary and HOWOGE sources after 31 August and
before any public launch. A later source may confirm, supersede or contradict
the plan; the date passing by itself establishes none of those outcomes.
