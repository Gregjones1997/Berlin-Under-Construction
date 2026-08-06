# Candidate discovery research trail

**Run date:** 2026-08-06
**Scope:** shallow identity, geographic boundary, official-source lead and one
project-level expected-end-date question. No scoring, finalist selection,
dossier research or golden-set writes.
**Safety:** fetched pages were treated as untrusted data. Natural-person names
encountered in source pages were not retained in the research output.

The frozen candidate record is in [`candidate-ledger.md`](candidate-ledger.md).
The ledger contains the integrated 29-lead longlist and the exact source-read
end wording. This file preserves how the four lanes searched, including failed
paths and access barriers. Search-result snippets were navigation leads, not
claim evidence. A URL is marked `loaded` only when the page itself opened.

## Orchestration and usage

Three initial GPT-5.6-sol/high lane calls were stopped when the project owner
asked not to use sol. They produced no accepted lane result. The same bounded
transport, public and development lanes were restarted on GPT-5.6-terra/high.
The main agent handled utilities and independently reopened every core identity
link from all four completed lanes.

| Invocation / lane | Model | Outcome | Tokens | Cost |
| --- | --- | --- | --- | --- |
| Transport, initial | GPT-5.6-sol, high | Interrupted; no output accepted | Unavailable — runtime exposes no lane token telemetry | Unavailable; not estimated |
| Public, initial | GPT-5.6-sol, high | Interrupted; no output accepted | Unavailable | Unavailable; not estimated |
| Development, initial | GPT-5.6-sol, high | Interrupted; no output accepted | Unavailable | Unavailable; not estimated |
| Transport, completed | GPT-5.6-terra, high | 6 leads and full trail | Unavailable | Unavailable; not estimated |
| Public, completed | GPT-5.6-terra, high | 8 leads and full trail | Unavailable | Unavailable; not estimated |
| Development, completed | GPT-5.6-terra, high | 8 leads and full trail | Unavailable | Unavailable; not estimated |
| Utilities, completed by main agent | Primary Codex runtime; model identifier not exposed | 7 leads and full trail | Unavailable | Unavailable; not estimated |

The unavailable values are instrumentation gaps, not zero usage. No price or
token count was invented.

## Transport lane

### Queries, verbatim

```text
site:berlin.de "Straßenbahn Adlershof II"
site:berlin.de "Straßenbahn Adlershof II"
site:deutschebahn.com Berlin "Bahnhof Köpenick" "2027"
site:deutschebahn.com Berlin Wollankstraße Brücke "2027"
site:autobahn.de "Rudolf-Wissell-Brücke" Bau
site:berlin.de Elsenbrücke Neubau Fertigstellung
site:berlin.de "Mühlendammbrücke" "Fertigstellung"
site:deutschebahn.com Siemensbahn 2029 Berlin
site:bvg.de U3 Mexikoplatz 2030
site:berlin.de "Straßenbahn Mahlsdorf" "Inbetriebnahme"
```

The duplicate Adlershof query is intentional: the first used Google and the
second retried through Bing.

### Source families chosen and skipped

- **Project identity, scope and current project pages:** Senate bridge pages,
  BVG and DB. Chosen for official names, route/boundary and project/phase
  distinctions.
- **Construction updates and disruptions:** Senate and DB updates. Chosen only
  for current completion or commissioning wording. A closure date was rejected
  when it did not state the project end.
- **State investment:** one GRW publication was consulted because it contained
  the current Mühlendamm construction-completion phrase. No amount was retained.
- **Skipped deliberately:** Berlin Vergabeplattform/TED, broader budgets,
  PARDOK, audits, legal notices, plan-approval files and Geoportal. They belong
  after selection or to a boundary follow-up; tenders risk becoming false
  project identities.

### URLs opened and outcomes

| URL | Outcome |
| --- | --- |
| `https://www.google.com/search?q=site%3Aberlin.de+%22Stra%C3%9Fenbahn+Adlershof+II%22` | Loaded; no usable official result |
| `https://www.bing.com/search?q=site%3Aberlin.de+%22Stra%C3%9Fenbahn+Adlershof+II%22` | CAPTCHA; not bypassed |
| `https://www.berlin.de/sen/uvk/mobilitaet-und-verkehr/verkehrsplanung/oeffentlicher-personennahverkehr/strassenbahn/neubaustrecken/` | 404 / moved |
| `https://www.berlin.de/sen/uvk/mobilitaet-und-verkehr/infrastruktur/brueckenbau/elsenbruecke/` | Loaded; identity/boundary/end evidence |
| `https://www.berlin.de/sen/uvk/mobilitaet-und-verkehr/infrastruktur/brueckenbau/muehlendammbruecke/` | Loaded; identity/boundary |
| `https://www.berlin.de/rbmskzl/aktuelles/pressemitteilungen/2026/ausgewaehlte-grw-projekte.pdf` | Loaded through search retrieval; end wording |
| `https://www.bvg.de/de/unternehmen/herzensprojekte/u3-verlaengerung` | Loaded; identity/route/end evidence |
| `https://www.deutschebahn.com/de/presse/presse-regional/pr-berlin-de/aktuell/presseinformationen/Meilenstein-fuer-die-Siemensbahn-Allianz-Partner-fuer-die-Reaktivierung-stehen-fest-13569054` | Loaded; identity/route |
| `https://bauprojekte.deutschebahn.com/p/siemensbahn-reaktivierung/pdf` | Loaded through search retrieval; end evidence |
| `https://www.deutschebahn.com/de/presse/presse-regional/pr-berlin-de/aktuell/presseinformationen/Zeitplan-fuer-Ausbauprojekt-Berlin-Frankfurt-Oder-angepasst--13508236` | Loaded; station/wider-project distinction and end evidence |
| `https://bauprojekte.deutschebahn.com/p/berlin-nord/pdf` | Timed out in the lane; later loaded in main-agent verification. Closure wording still failed the end-date test. |

### Per-lead provenance, confidence and next confidence-changing check

| Lead | Source-read fields | Inferred / not established | Confidence and decisive next check |
| --- | --- | --- | --- |
| Elsenbrücke | Name, endpoints, two districts, work and public consequence, construction-period/end wording | Likely budget/procurement trail only | High; rises if the remaining-works page repeats 2028 `Gesamtfertigstellung`, falls if it is revised |
| Mühlendammbrücke | Name, boundary, district, work/consequence, 2029 completion wording | Likely source trail | High; compare current page and GRW wording and retain older 2028 as history |
| U3 to Mexikoplatz | Name, endpoints, work/consequence, 2030 `Fertigstellung`/`Inbetriebnahme` | District and exact approved underground perimeter | High; approval record confirms or changes the boundary |
| Siemensbahn | Name, endpoints, work/consequence, 2029 `Inbetriebnahme` | Districts and present phase boundary | High; DB plan/approval map confirms current construction limits |
| Bahnhof Köpenick | Station identity, parent-project relation, service-start and wider-project dates | District | Medium-high; selecting station or corridor as the candidate raises it, conflating them lowers it |
| Wollankstraße bridge | Bridge identity, underlying work, closure wording | District boundary; project end | Medium; a DB project milestone raises it, another closure-only notice does not |

**Scope check:** stayed inside transport. Adlershof II, Rudolf-Wissell-Brücke
and Mahlsdorf were retained as dead ends. No closure notice became a candidate.

## Public buildings, culture and public-space lane

### Queries, verbatim

```text
site:berlin.de Schulneubau Berlin Fertigstellung 2026
site:berlin.de Berlin Schulbau Fertigstellung 2027 Neubau
site:berlin.de Berlin Kultur Bauarbeiten Fertigstellung 2026
site:berlin.de Berlin Platz Umgestaltung Baubeginn Fertigstellung 2026
site:berlin.de "Neue Integrierte Sekundarschule am Ostpreußendamm" "Fertigstellung"
site:berlin.de "Grundschule am Weißen See" "Fertigstellung"
site:berlin.de "Rubensstraße 63" "Fertigstellung"
site:berlin.de "Heinrich-Hertz-Gymnasium" Ostbahnhof "Fertigstellung"
site:berlin.de "Grundschule am Wasserturm" "Fertigstellung"
site:berlin.de "Hochmeisterplatz" "Bauabschnitt" "Herbst 2026"
site:berlin.de "Checkpoint Charlie" "Baumaßnahme abgeschlossen" 2030
site:berlin.de "Europaplatz Süd" Fertigstellung Umgestaltung
```

### Source families chosen and skipped

- **Project identity/current updates:** district and Senate project/press pages.
- **Official participation:** meinBerlin for bounded project/competition records.
- **Skipped deliberately:** tenders, TED, budgets, parliamentary oversight,
  formal approvals, geospatial layers, legal notices and audits. Identity,
  boundary and the one end-date question were sufficient for discovery.

### URLs opened and outcomes

| URL | Outcome |
| --- | --- |
| `https://www.berlin.de/ba-steglitz-zehlendorf/aktuelles/pressemitteilungen/2026/pressemitteilung.1693735.php` | Loaded |
| `https://www.berlin.de/ba-pankow/aktuelles/pressemitteilungen/2026/pressemitteilung.1663498.php` | Loaded |
| `https://www.berlin.de/ba-marzahn-hellersdorf/politik-und-verwaltung/aemter/schul-und-sportamt/schule/informationsveranstaltung-neubauschule-auerbacher-ring-20012026.pdf?ts=1773247066` | Internal error; Auerbacher Ring excluded |
| `https://www.berlin.de/ba-tempelhof-schoeneberg/aktuelles/pressemitteilungen/2026/pressemitteilung.1689531.php` | Loaded |
| `https://www.berlin.de/ba-friedrichshain-kreuzberg/aktuelles/pressemitteilungen/2026/pressemitteilung.1689904.php` | Loaded |
| `https://mein.berlin.de/vorhaben/2022-00630/` | Loaded |
| `https://www.berlin.de/ba-charlottenburg-wilmersdorf/aktuelles/pressemitteilungen/2026/pressemitteilung.1673494.php` | Loaded |
| `https://mein.berlin.de/vorhaben/2026-01353/` | Loaded |
| `https://www.berlin.de/sen/bauen/baukultur/berliner-plaetzeprogramm/` | Loaded |
| `https://www.berlin.de/sen/bauen/baukultur/berliner-plaetzeprogramm/europaplatz-sued-1567894.php` | Loaded |
| `https://www.berlin.de/ba-pankow/aktuelles/pressemitteilungen/2026/pressemitteilung.1646183.php` | Loaded |
| `https://www.berlin.de/ba-treptow-koepenick/aktuelles/pressemitteilungen/2026/pressemitteilung.1690128.php` | Loaded; school already delivered and excluded |
| `https://www.berlin.de/ba-marzahn-hellersdorf/aktuelles/pressemitteilungen/2026/` | Loaded; listing did not confirm Auerbacher Ring |
| `https://www.berlin.de/ba-pankow/politik-und-verwaltung/aemter/schul-und-sportamt/schulbauoffensive/grundschule-am-weissen-see-03g17-1195738.php` | Timeout; current district update retained as the core source |

### Per-lead provenance, confidence and next confidence-changing check

| Lead | Source-read fields | Inferred / not established | Confidence and decisive next check |
| --- | --- | --- | --- |
| New ISS Ostpreußendamm | Name, road-level place, authority context, consequence, 2028 `Fertigstellung` | Exact parcel/address; detailed project boundary | Medium-high identity but insufficient geography; a parcel/current project page raises it |
| Grundschule am Weißen See | Name, current status and uncertain completion wording; address read in official record | No fixed reliable day | High identity / medium schedule; post-summer 2026 update decides |
| DFK 2.0 Friedenauer Gemeinschaftsschule | Name/aliases, address, added rooms, full completion wording | Whether the system name represents the whole permanent project | High; project/contract boundary confirms or narrows it |
| Heinrich-Hertz-Gymnasium | Name, route boundary, district, construction/hand-over and later move milestones | Likely later source families | High; an update after 31 August confirms or supersedes the date |
| Grundschule am Wasserturm, remaining phases | Name, address, completed phase 1, remaining scope and forecast | Authorization and identifiers for phases 2–4 | Medium-high; phase IDs raise it, lack of authorized future phases lowers it |
| Hochmeisterplatz phase 1 | Name, square, phase-one works/consequence and autumn end | Whole-project later phases | High for phase 1 / low for whole project; later-phase page decides candidate boundary |
| Checkpoint Charlie education/memory place | Name, crossing boundary, proposed use and 2030 construction wording | District; construction implementation decision | Medium and currently ineligible; post-competition authorization raises it |
| Europaplatz Süd | Name/aliases, station-forecourt boundary, current 2026 field, scope | District from geography; month/day | High identity / medium schedule; a current 2026 milestone update raises it |

**Scope check:** stayed inside lane. Europaplatz's adjacent S21 works were
explicitly excluded. Auerbacher Ring and the delivered Adlershof school remain
dead-end/source-registry seeds.

## Utilities, energy, water, environment and climate-adaptation lane

### Queries, verbatim

```text
site:bwb.de Berlin Bauprojekt Fertigstellung Klärwerk Ruhleben Ausbau
site:berlin.de Berlin Wasserwerk Neubau Fertigstellung Projekt
site:bew.berlin Projekt Bau Inbetriebnahme Berlin Wärmepumpe Reuter West
site:stromnetz.berlin Bauprojekt Umspannwerk Berlin Fertigstellung
site:bwb.de/de Bauprojekt Berlin "Fertigstellung" 2026
site:bwb.de/de "Baumaßnahme" Berlin "bis" 2027
site:berlin.de "Klärwerk Ruhleben" Ausbau Fertigstellung
site:berlin.de "Stauraumkanal" Berlin Fertigstellung Wasserbetriebe
site:bwb.de/de "Klärwerk Ruhleben" "Fertigstellung"
site:bwb.de/de "Abwasserhauptpumpwerk Charlottenburg" Fertigstellung
site:bwb.de/de "Cité Foch" "Mitte 2027"
site:bwb.de/de "Gneisenaustraße" Fertigstellung
site:berlin.de Panke Renaturierung Baumaßnahme Fertigstellung Berlin
site:berlin.de Gewässerausbau Berlin "Fertigstellung" 2027
site:berlin.de Klimaanpassung Bauprojekt Berlin "Fertigstellung"
site:berlin.de Regenwasser Projekt Berlin "Fertigstellung" 2028
site:berlin.de/ba-pankow "Renaturierung des Wilhelmsruher Sees" Fertigstellung
site:berlin.de "Ausbau der Panke" "Fertigstellung"
site:berlin.de "Energiedreieck Ruhleben" Inbetriebnahme
site:bew.berlin "Abwasserwärmepumpenanlage" "Inbetriebnahme"
site:bwb.de/de Berliner Wasserbetriebe "Ende 2028" Baumaßnahme Berlin
site:bwb.de/de Berliner Wasserbetriebe "Ende 2027" Baumaßnahme Berlin
site:bwb.de/de Berliner Wasserbetriebe "bis 2030" Bau Berlin Projekt
site:bwb.de/de Berliner Wasserbetriebe "anvisiert" Fertigstellung Berlin
site:bew.berlin/aktuelles-und-presse Energiedreieck Ruhleben Abwasserwärmepumpe Inbetriebnahme 2027
site:bew.berlin/aktuelles-und-presse "Abwasserwärmepumpe" Reuter West Fertigstellung
site:bew.berlin "Dampfturbine" Reuter West Inbetriebnahme
site:bew.berlin Heizkraftwerk Mitte Adresse Berlin Michaelkirchstraße
```

### Source families chosen and skipped

- **Operator project/current works pages:** Berliner Wasserbetriebe and BEW;
  chosen for named infrastructure, route/site and project-level milestones.
- **Senate/district environmental and water-construction pages:** chosen for
  approval-backed river/environment project identity and phase boundary.
- **Official operator environmental/financing publications:** consulted only
  to test whether a plant-specific date existed; no financial amount became a
  candidate claim.
- **Skipped deliberately:** tenders/TED, PARDOK, audits, general budget research,
  geospatial services and legal notices. The operator pages answered the frozen
  discovery fields. Procurement and money remain trail leads only.

### URLs opened and outcomes

| URL | Outcome |
| --- | --- |
| `https://www.bwb.de/de/landsberger-allee.php` | Loaded |
| `https://www.bwb.de/de/baustelleninformationen.php` | Loaded; Cité Foch and linked works |
| `https://www.bwb.de/de/assets/downloads/2023_rahmenwerk-fuer-einen-gruenen-schuldschein.pdf` | Redirected to 404/error page |
| `https://www.bew.berlin/fernwaermesystem/waermewende/energiedreieck-ruhleben/` | Loaded |
| `https://www.bew.berlin/fernwaermesystem/waermewende/abwaerme-und-grosswaermepumpen/` | Loaded |
| `https://www.bew.berlin/aktuelles-und-presse/bauvorhaben-hindenburgdamm/` | Loaded |
| `https://www.bew.berlin/aktuelles-und-presse/2026/120-megawatt-am-heizkraftwerk-berlin-mitte/` | Loaded |
| `https://www.bew.berlin/binaries/content/assets/website/erzeugungsanlagen/information-der-offentlichkeit-storfallv---hkw-mitte.pdf` | Loaded; site address |
| `https://www.bwb.de/de/assets/downloads/Umwelterklaerung-2025.pdf` | Loaded PDF |
| `https://www.berlin.de/sen/uvk/mobilitaet-und-verkehr/infrastruktur/wasserbau/ausbau-von-gewaessern/panke/` | Loaded |
| `https://www.berlin.de/ba-pankow/aktuelles/pressemitteilungen/2023/pressemitteilung.1391124.php` | Loaded; Wilhelmsruher See old/finished-stage comparator |
| `https://www.bwb.de/de/29097_29096.php` | Loaded; Gneisenaustraße identified as cross-lane combined work and not returned |
| `https://www.bew.berlin/binaries/content/assets/website/erzeugungsanlagen/information-der-offentlichkeit---hkw-reuter-und-hkw-reuter-west.pdf` | Internal fetch error |
| `https://www.bew.berlin/binaries/content/assets/website/newsroom/pressemappe/campus-reuter/infoblatt-energiepark-reuter.pdf` | Loaded PDF |
| `https://www.bew.berlin/binaries/content/assets/website/uber-uns/geschaftsbericht/bericht-uber-das-geschaftsjahr-2025.pdf/` | Loaded PDF |

### Per-lead provenance, confidence and next confidence-changing check

| Lead | Source-read fields | Inferred / not established | Confidence and decisive next check |
| --- | --- | --- | --- |
| Landsberger Allee | Name, route endpoints, line-renewal scope/consequence and whole-measure end wording | District and later procurement trail | High; district/lot map confirms geography without splitting the project |
| Cité Foch utilities | Name, three streets/phases, Wittenau/Reinickendorf, scope/consequence and infrastructure end wording | Detailed contract identifiers | High; development agreement confirms exact overall-versus-utility boundary |
| Hindenburgdamm heat-network reinforcement | Name, route, district, project length/phase count and `Bauende` | Procurement trail | High; a current phase table confirms end-2026 remains current |
| Energiedreieck Ruhleben | Name, component works/consequence, 2027 heat-pump `Inbetriebnahme` | Exact site address in directly opened identity page; turbine end | Medium-high; official site record and component schedule decide one-vs-two project boundary |
| HKW Mitte Power-to-Heat | Name, site address, plant scope/consequence and end-2028 `Inbetriebnahme` | Procurement trail only | High; construction update confirms current status and keeps later river-water heat pump separate |
| Ruhleben fourth treatment stage | Plant/component identity and programme-level 2028 wording | Exact plant address and plant-specific end date | Medium; a plant project page raises it, another all-plants programme statement does not |
| Panke Phase II, Buch/Pölnitzwiesen | Name, bounded river section, district, work/consequence and 24-month duration | Calendar end date | High identity / low end-date confidence; a dated Senate milestone raises it |

**Scope check:** stayed inside utilities/environment. Gneisenaustraße was
flagged as a combined transport/utility work and not returned; Wilhelmsruher See
and Abwasserhauptpumpwerk Charlottenburg were already-completed comparators.

## Housing, commercial redevelopment, demolition and mixed-use lane

### Queries, verbatim

```text
site:berlin.de "Buckower Felder" Fertigstellung
site:berlin.de "Schumacher Quartier" Fertigstellung
site:berlin.de "Haus der Statistik" Fertigstellung
site:berlin.de "Molkenmarkt" Fertigstellung
site:berlin.de "Buckower Felder" "Fertigstellung" OR "bezugsfertig"
site:berlin.de "Haus der Statistik" "Fertigstellung" OR "Eröffnung"
site:berlin.de "Rathausblock" "Fertigstellung"
site:berlin.de "Blankenburger Süden" "Fertigstellung"
site:berlin.de "Pankower Tor" "Fertigstellung"
site:berlin.de "Siemensstadt Square" "Fertigstellung"
site:berlin.de "Urbane Mitte" "Fertigstellung"
site:berlin.de "Behrens-Ufer" OR "Behrens Ufer"
"Haus der Statistik" "Fertigstellung" Berlin 2027
site:berlin.de "Haus der Statistik" "bis 202"
site:berlin.de "Buckower Felder" "2026" Wohnungen
site:berlin.de "Insel Gartenfeld" "Fertigstellung"
"Buckower Felder" "Fertigstellung"
"Insel Gartenfeld" "Fertigstellung"
site:berlin.de "Neue Mitte Tempelhof" "Fertigstellung"
site:berlin.de "Schöneberger Linse" "Fertigstellung"
"Das Neue Gartenfeld" "Fertigstellung" -linkedin
site:berlin.de "Das Neue Gartenfeld"
site:gewobag.de "Gartenfeld" "Fertigstellung"
site:berlin.de "Quartier Heidestraße" "Fertigstellung"
site:berlin.de "Lichterfelde Süd" "Fertigstellung"
site:berlin.de "Ehemaliger Güterbahnhof Köpenick" "Fertigstellung"
site:berlin.de "Michelangelostraße" "Fertigstellung" Wohnungsbau
site:berlin.de "Siemensstadt Square" "Fertigstellung" OR "Bezugsfertig"
site:berlin.de/sen/stadtentwicklung/neue-stadtquartiere "Lichterfelde Süd" "zwischen"
site:berlin.de/sen/stadtentwicklung/neue-stadtquartiere "Ehemaliger Güterbahnhof Köpenick" "zwischen"
site:berlin.de "Rathausblock" "Mehringdamm" "Yorckstraße"
site:berlin.de "Pankower Tor" "Mühlenstraße" "Prenzlauer Promenade"
```

### Source families chosen and skipped

- **Senate/district planning and project pages:** main identity, boundary and
  status family.
- **Official participation/B-Plan pages:** phase and perimeter disambiguation.
- **Public owner/operator pages:** used for leads only where a public operator
  published a project page.
- **Budget:** one district PDF was opened while testing a cross-lane component;
  no amount or whole-development date was retained.
- **Skipped deliberately:** procurement/TED, oversight, Geoportal, closure
  notices and private developer/contractor dates. The latter were deliberately
  not promoted into authoritative end evidence.

### URLs opened and outcomes

| URL | Outcome |
| --- | --- |
| `https://mein.berlin.de/vorhaben/2025-01091/` | Loaded |
| `https://www.berlin.de/sen/stadt/presse/pressemeldungen/pressemitteilung.1526943.php` | Loaded |
| `https://www.berlin.de/rbmskzl/aktuelles/pressemitteilungen/2024/pressemitteilung.1481553.php` | Loaded |
| `https://www.berlin.de/ba-treptow-koepenick/aktuelles/pressemitteilungen/2021/pressemitteilung.1092646.php` | Loaded |
| `https://www.berlin.de/sen/stadtentwicklung/neue-stadtquartiere/buckower-felder/` | Loaded |
| `https://stadtundland.de/unternehmen/presse/2026/stadt-und-land-feiert-quartiersfertigstellung-auf-den-buckower-feldern` | Loaded; completed comparator |
| `https://stadtundland.de/bauen/neubau/neukoelln/im-bau/buckower-felder` | Loaded |
| `https://berlinerstadtwerke.de/energieprojekte/quartier-haus-der-statistik/` | Loaded; utilities subproject only |
| `https://www.berlin.de/rathausblock-fk/aktuelles/newsletter/newsletter.1684158.php` | Loaded |
| `https://www.berlin.de/ba-pankow/politik-und-verwaltung/bezirksamt/cornelius-bechtler/artikel.1488504.php` | Loaded |
| `https://www.berlin.de/sen/stadtentwicklung/neue-stadtquartiere/blankenburger-sueden/planungsprozess/` | Loaded; planning only |
| `https://www.berlin.de/ba-spandau/aktuelles/pressemitteilungen/2026/pressemitteilung.1644735.php` | Loaded |
| `https://www.berlin.de/sen/finanzen/haushalt/downloads/haushaltsplaene-der-bezirke/37_ba_tempelhof-schoeneberg_26_27.pdf` | Loaded/searchable; cross-lane component only |
| `https://www.berlin.de/sen/stadtentwicklung/neue-stadtquartiere/das-neue-gartenfeld/` | Loaded |
| `https://www.berlin.de/sen/stadt/ueber-uns/berliner-perspektiven/norden/` | Loaded |
| `https://www.berlin.de/sen/uvk/mobilitaet-und-verkehr/infrastruktur/brueckenbau/rhenaniabruecke/` | Loaded; linked transport project, not development lead |
| `https://www.berlin.de/ba-spandau/aktuelles/pressemitteilungen/2024/pressemitteilung.1483858.php` | Loaded |
| `https://www.berlin.de/ba-mitte/politik-und-verwaltung/aemter/strassen-und-gruenflaechenamt/planung-entwurf-neubau/quartier-heidestrasse-westlich-heidestrasse-1032342.php` | Loaded |
| `https://www.berlin.de/rbmskzl/aktuelles/pressemitteilungen/2022/pressemitteilung.1193638.php` | Loaded |
| `https://www.berlin.de/ba-steglitz-zehlendorf/aktuelles/pressemitteilungen/2024/pressemitteilung.1490757.php` | Loaded |
| `https://www.berlin.de/sen/stadtentwicklung/neue-stadtquartiere/ehemaliger-gueterbahnhof-koepenick/gebietsbeirat/` | Loaded |
| `https://www.berlin.de/sen/stadt/presse/pressemeldungen/2023/pressemitteilung.1331463.php` | Internal error; not relied upon |
| `https://www.berlin.de/ba-treptow-koepenick/politik-und-verwaltung/service-und-organisationseinheiten/sozialraumorientierte-planungskoordination/archiv-dammvorstadt/artikel.1527748.php` | Loaded |
| `https://www.berlin.de/ba-pankow/politik-und-verwaltung/aemter/stadtentwicklungsamt/stadtplanung/artikel.487200.php` | Loaded |
| `https://www.berlin.de/rathausblock-fk/gebiet/` | Loaded |
| `https://www.berlin.de/rathausblock-fk/aktuelles/artikel.1550846.php` | Loaded |
| `https://www.berlin.de/sen/stadtentwicklung/neue-stadtquartiere/ehemaliger-gueterbahnhof-koepenick/` | Loaded |

### Per-lead provenance, confidence and next confidence-changing check

| Lead | Source-read fields | Inferred / not established | Confidence and decisive next check |
| --- | --- | --- | --- |
| Schumacher Quartier | Name/alias, whole boundary, district, scope/consequence, first-buildings date | Geographic boundary of those first buildings | High whole identity / insufficient phase boundary; phase map raises it |
| Behrens-Ufer | Name/aliases, riverfront industrial-site identity, district, scope/consequence and old development-end phrase | Street endpoints; current validity; milestone type | Medium; a current B-Plan/update can raise or lower it materially |
| Das Neue Gartenfeld | Name/aliases, canal boundary, district, scope/consequence and rail-component date | Whole-quarter completion | High identity / no end evidence; implementation plan could raise it |
| Quartier Heidestraße public works | Name, named spaces/streets, district, public-works scope and project period | Explicit completion milestone; map geometry | Medium-high; mapped unfinished sections and a typed end raise it |
| Pankower Tor | Name/alias, yard/B-Plan boundaries, district and intended uses | Construction/end milestone | Medium; phase implementation contract raises it |
| Rathausblock / Dragonerareal | Name/alias, street boundary, district and intended uses | Integrated completion date | High identity / no end evidence; programme schedule could raise it |
| Lichterfelde Süd | Name, near-station place, district, scope/consequence and preparatory duration | Exact perimeter and project completion | Medium and geographically ineligible; official perimeter is the first check |
| Ehemaliger Güterbahnhof Köpenick | Name/aliases, mapped boundary, district, scope/consequence and relative completion phrase | Textual endpoints; calendar date | Medium; dated implementation plan raises it, treating 15 years as a calendar date lowers it |

**Scope check:** stayed inside development. Rhenaniabrücke, Gartenfeld school,
Haus der Statistik energy system and Neue Mitte Tempelhof cultural building were
flagged and not returned in this lane. Buckower Felder was already complete;
Blankenburger Süden was planning-only.

## Integration observations and access-barrier seeds

- No two returned rows were deduplicated as the same project. Several linked or
  adjacent works were deliberately kept distinct: Europaplatz/S21;
  Gartenfeld/Rhenaniabrücke/school; Köpenick station/wider corridor;
  Energiedreieck/Ruhleben treatment; Hindenburgdamm heat/water/electric works.
- The discovery run produced no case where a core opened identity page failed
  to describe the named project. The failures were access paths, stale dates,
  phase mismatch, closure-only dates or insufficient geography.
- Seed access failures for OPS-02/MON-04: one moved Senate tram directory (404),
  Bing CAPTCHA, initial DB PDF timeout, Auerbacher PDF internal error, Weißen
  See legacy-page timeout, BWB green-finance PDF redirect to 404, BEW Reuter
  site-PDF internal error and one GBK Senate press-page internal error.
- Browser fallback was useful in the transport lane after its scrape runtime
  was unavailable. The other lanes did not need Chrome fallback.
