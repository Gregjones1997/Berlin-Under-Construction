# Feature Register

This register preserves the complete product vision for Berlin, Under Construction. Feature IDs are stable references; implementation sequencing lives in [`project-checklist.md`](project-checklist.md). A feature is not deleted from this register merely because it is outside the current delivery phase.

The source blueprint contains 68 feature IDs across ten groups. AI-12 and OPS-01
are scoped for Phase 2; implementation remains not started. All other features
are currently marked `Not started`.

## Phase 2 local admin surface

AI-12 and OPS-01 jointly define the local-only review dashboard required for
the trustworthy data core. It is an operator tool, is not part of the public
Vercel deployment, and does not introduce authentication to v0. Its registered
minimum scope is retrieval health and failures; hashes and detected changes;
extraction model, token, cost, duration and validation data; exact German spans
beside proposed claims; qualifiers and public marker states; supersession,
conflict and scope quarantine; reviewer actions and decision history; and each
claim's publication eligibility with the exact blocking gate.

## Map (`MAP`)

| ID | Feature | Full-vision behaviour | Status |
| --- | --- | --- | --- |
| MAP-01 | All-construction city map | Display every known construction site and major work in Berlin, with status, category and confidence. | Not started |
| MAP-02 | Technical 3D Berlin | Render open city geometry as clean white forms with black hidden-line outlines. | Not started |
| MAP-03 | 2D fallback map | Provide a performant and accessible conventional map with equivalent information. | Not started |
| MAP-04 | Filters | Filter by status, type, duration, responsible body, financing, contractor, budget range, district and confidence. | Not started |
| MAP-05 | Time slider | Explore announced, active, delayed and completed projects at any historical or future planning date. | Not started |
| MAP-06 | Address and nearby search | Search an address, use current location or draw a neighborhood radius. | Not started |
| MAP-07 | Construction density and impact layers | Visualize concentrations, long-running sites, closures and overlapping works. | Not started |
| MAP-08 | Street-level entry | Link a physical sign, QR concept or geolocated report to the digital dossier. | Not started |

## Project dossiers (`DOS`)

| ID | Feature | Full-vision behaviour | Status |
| --- | --- | --- | --- |
| DOS-01 | Project overview | Plain-language purpose, current state, location, owner, financer and responsible organizations. | Not started |
| DOS-02 | Versioned timeline | Preserve every supported milestone and estimate with effective date and source. | Not started |
| DOS-03 | Budget history | Separate original estimate, approved budget, current estimate, awards, amendments, expenditure and final cost. | Not started |
| DOS-04 | Contract and lot ledger | Show procurement stages, awarded suppliers, lot values, amendments and source notices. | Not started |
| DOS-05 | Funding view | Show city, district, federal, EU, utility, company and private financing when disclosed. | Not started |
| DOS-06 | Organization graph | Connect commissioners, owners, designers, contractors, consortia and repeat relationships. | Not started |
| DOS-07 | Source evidence record | Display source metadata, retrieval dates, hashes, short evidence spans and original links; retained full artifacts remain private. | Not started |
| DOS-08 | Change log | Show exactly what changed, when it changed and which new source caused the update. | Not started |
| DOS-09 | Confidence and freshness | Display evidence level, last checked time, contradictions and stale-source warnings. | Not started |
| DOS-10 | Project comparison | Compare like-for-like fields while preserving differences in budget and date definitions. | Not started |
| DOS-11 | Photos and progress evidence | Display official, licensed and resident-contributed visual progress with dates and moderation. | Not started |
| DOS-12 | Downloads | Export source list, timeline, machine-readable data and printable project brief. | Not started |

## 3D experience (`3D`)

| ID | Feature | Full-vision behaviour | Status |
| --- | --- | --- | --- |
| 3D-01 | Exploded flagship models | Create detailed interactive anatomy for selected projects. | Not started |
| 3D-02 | Construction-step animation | Animate planned project phases and reveal where progress currently sits. | Not started |
| 3D-03 | Planned vs. current geometry | Compare existing site, published plan and observed or reported state. | Not started |
| 3D-04 | Infrastructure connections | Visualize rail, road, utility and neighborhood dependencies when data permits. | Not started |
| 3D-05 | Illustrative reconstruction workflow | Build simplified models from public plans with explicit provenance and accuracy labels. | Not started |

## AI (`AI`)

| ID | Feature | Full-vision behaviour | Status |
| --- | --- | --- | --- |
| AI-01 | Document classification | Identify project pages, tenders, awards, amendments, budgets, planning documents and updates. | Not started |
| AI-02 | Structured extraction | Extract names, amounts, definitions, dates, organizations, addresses, phases and quoted evidence. | Not started |
| AI-03 | Entity resolution | Match aliases, notices, contract lots, organizations and sites to canonical records. | Not started |
| AI-04 | Change detection | Identify material differences between versions and assess whether public records should update. | Not started |
| AI-05 | Contradiction detection | Surface conflicting claims without silently selecting the most convenient one. | Not started |
| AI-06 | Grounded project Q&A | Answer user questions only from retrievable evidence with citations and uncertainty. | Not started |
| AI-07 | Plain-language explanation | Translate bureaucratic language while retaining the exact financial/date definition. | Not started |
| AI-08 | German-English support | Support bilingual ingestion, interface summaries and source-aware translation. | Not started |
| AI-09 | Sign and photo intake | Read project signs and user images to create leads, not automatic facts. | Not started |
| AI-10 | Delay-risk research | Offer experimental, clearly labelled inference about schedule risk based on patterns and known dependencies. | Not started |
| AI-11 | Model routing and cost control | Use fit-for-purpose models, caching and escalation based on ambiguity. | Not started |
| AI-12 | Evaluation and extraction-run dashboard | Locally inspect extraction runs, model/cost/latency, validation outcomes and smoke/evaluation reports; public reporting is a separate release output. | Phase 2 scoped; not started |

## Community (`COM`)

| ID | Feature | Full-vision behaviour | Status |
| --- | --- | --- | --- |
| COM-01 | Report missing construction | Drop a pin, choose a type, add sign details/photos and submit a lead. | Not started |
| COM-02 | Correction request | Challenge a claim, attach evidence and track the review outcome. | Not started |
| COM-03 | Observation updates | Report visible activity, inactivity, changed signage or apparent completion. | Not started |
| COM-04 | Contributor reputation | Weight submissions using history, evidence quality and moderation rather than popularity. | Not started |
| COM-05 | Public discussion context | Allow restrained, evidence-focused annotations without becoming an unmoderated accusation forum. | Not started |
| COM-06 | Organization response | Allow responsible bodies to provide source-backed clarifications without controlling the record. | Not started |

## Monitoring (`MON`)

| ID | Feature | Full-vision behaviour | Status |
| --- | --- | --- | --- |
| MON-01 | Follow a project | Receive alerts for material budget, date, status, contract or source changes. | Not started |
| MON-02 | Follow an area or route | Monitor a radius, commute or district for new and changed work. | Not started |
| MON-03 | Weekly change digest | Summarize the most meaningful verified changes across Berlin. | Not started |
| MON-04 | Source health alerts | Notify operators when a source disappears, changes structure or becomes stale. | Not started |

## Analytics (`ANA`)

| ID | Feature | Full-vision behaviour | Status |
| --- | --- | --- | --- |
| ANA-01 | Citywide analytics | Analyze durations, disclosure quality, budget history and construction density. | Not started |
| ANA-02 | Disclosure score | Measure how complete, current and source-backed a project's public information is. | Not started |
| ANA-03 | Contractor and authority profiles | Aggregate projects and contracts without turning correlation into allegations. | Not started |
| ANA-04 | Cross-project benchmarking | Compare only compatible project categories and financial definitions. | Not started |
| ANA-05 | Research workspace | Save projects, annotations, source collections and comparisons. | Not started |

## Operations (`OPS`)

| ID | Feature | Full-vision behaviour | Status |
| --- | --- | --- | --- |
| OPS-01 | Review queue | Local-only v0 queue to accept, reject, correct or defer extracted claims with immutable decision history and explicit publication gates. | Phase 2 scoped; not started |
| OPS-02 | Source registry | Track authoritative sources, update schedules, licenses, parsers and failure states. | Not started |
| OPS-03 | Claim editor and audit trail | Edit structured claims while preserving original extraction and reviewer decision. | Not started |
| OPS-04 | Organization and alias manager | Merge, split and disambiguate project and company entities safely. | Not started |
| OPS-05 | Moderation console | Review photos, reports, disputes, abuse and personally identifying information. | Not started |
| OPS-06 | Public methodology page | Explain definitions, evidence hierarchy, limitations, corrections and model performance. | Not started |

## Platform (`PLAT`)

| ID | Feature | Full-vision behaviour | Status |
| --- | --- | --- | --- |
| PLAT-01 | Public API | Provide documented access to projects, claims, sources, events and geometry where licenses permit. | Not started |
| PLAT-02 | Embeddable project cards | Let publications and neighborhood sites embed current, source-backed status. | Not started |
| PLAT-03 | Open data exports | Release reusable datasets with provenance, update timestamps and license metadata. | Not started |
| PLAT-04 | Multi-city architecture | Keep geography, authority and source connectors configurable for later expansion. | Not started |

## Scope (`SCP`)

| ID | Feature | Full-vision behaviour | Status |
| --- | --- | --- | --- |
| SCP-01 | Public infrastructure and buildings | Cover roads, bridges, transit, schools, hospitals, cultural and government works. | Not started |
| SCP-02 | Utilities and street works | Cover water, energy, telecommunications, excavation and restoration work. | Not started |
| SCP-03 | Commercial and institutional development | Cover offices, campuses, retail, hotels, data centers and major institutional works. | Not started |
| SCP-04 | Private residential development | Cover new housing and major private developments when publicly observable and documentable. | Not started |
| SCP-05 | Apartment-building upgrades | Eventually cover facade, roof, energy, lift and substantial building renovations with careful privacy boundaries. | Not started |
| SCP-06 | Resident-discovered unknown sites | Maintain an explicit unknown/unverified site state until authoritative information is found. | Not started |

## Construction scope and taxonomy

The initial focus is visible construction that shapes daily life and raises public questions: transport, roads, utilities, schools, public buildings, institutional developments, large commercial works, major private projects and long-running sites. The complete vision retains a path for new private residences and substantial apartment-building upgrades, with appropriate discovery thresholds and privacy boundaries.

### Project categories

| Category | Examples | Typical information availability |
| --- | --- | --- |
| Transport | Rail, stations, tram, U-Bahn, roads, bridges, cycle infrastructure | Often strong public documentation, but fragmented across authorities and contractors. |
| Utilities | Water, wastewater, district heating, electricity, telecom | Operational information may exist without full budget or project history. |
| Public buildings | Schools, hospitals, administration, culture, sports | Investment plans and procurement can provide strong records. |
| Public realm | Squares, parks, streetscapes and accessibility works | Often split across district programmes and individual contracts. |
| Institutional | Universities, research campuses, foundations and major nonprofit works | Mixed public and organizational disclosure. |
| Commercial | Offices, retail, hotels, industrial and data centers | Planning information may be public; financing and contract detail may be private. |
| Private residential | New apartment buildings and housing developments | Planning and developer information may exist; cost detail is usually limited. |
| Building upgrades | Facade, roof, heating, lift, energy and major structural renovation | Hardest to discover comprehensively; privacy and threshold rules are necessary. |
| Unknown observed work | A resident-visible site not yet matched to a project | Published as a lead or unknown site, never as verified fact. |

### Lifecycle states

- Proposed or announced
- Planning or consultation
- Approved but not tendered
- Tendering
- Awarded or mobilizing
- Enabling works
- Under construction
- Partially operational
- Paused or dormant
- Delayed relative to a defined milestone
- Completed physically
- Opened or commissioned
- Cancelled or superseded
- Unknown or awaiting verification

Status must always be "as of" a date and tied to evidence. "Delayed" requires comparison against a specific previously supported milestone, not merely a resident's impression that a site has taken too long.
