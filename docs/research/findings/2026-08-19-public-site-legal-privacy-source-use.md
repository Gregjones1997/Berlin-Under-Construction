# Public-site legal, privacy and source-use evidence

**Checked:** 2026-08-19  
**Scope:** Gate 6 pre-deployment evidence for the static public portfolio  
**Status:** **Public deployment is blocked; use an access-restricted preview.**

This is a primary-source compliance record, not a substitute for legal advice.
It records what the present product can rely on, what the public site must show,
and which owner/hosting facts remain unresolved. No unresolved requirement may
be worked around by weakening the public wording.

## Decision table

| Area | Basis checked | Required implementation | Present status |
| --- | --- | --- | --- |
| Short `berlin.de` evidence spans | Statutory quotation right, not an open licence | Quote only short, exact German spans for a genuine evidentiary purpose; identify the source and link its HTTPS URL | Conditionally satisfiable by the current evidence model; span-by-span purpose and attribution remain mandatory |
| Short `parlament-berlin.de` evidence spans | Statutory quotation right; a narrower official-work basis exists for identified Drucksachen and Plenarprotokolle | Keep exact wording, identify the source and link its HTTPS URL; do not assume every committee paper is a Drucksache | Conditionally satisfiable; C-014's committee paper uses the quotation basis, not an unverified official-work classification |
| BKG Berlin boundary | `dl-de/by-2-0` plus BKG's product-specific source-note rules | Put the prescribed, linked attribution visibly with the map and mark the transformed data as changed | **Not yet satisfied:** no map presentation exists and the recorded attribution omits the change notice |
| Cookies and analytics | TDDDG § 25, GDPR Article 13 and Berlin DPA guidance | Ship no product analytics, tracking, cookie/local-storage access or external embeds; separately disclose host/CDN request processing | Product-side position is implementable; **host facts and privacy notice remain unresolved** |
| Provider identity and corrections | MStV §§ 18–20; DDG § 5 where applicable; project publication policy | Publish the legally required provider/editorial identity and address, a monitored contact, and working contextual correction routes | **Not yet satisfied:** operator details are not approved and `/corrections` is not implemented |

## 1. Short German evidence spans

### Controlling use rule

The public pages do not receive a blanket licence to republish source text.
[UrhG § 51](https://www.gesetze-im-internet.de/urhg/__51.html) permits quotation
from a published work only where the quotation purpose and extent justify the
use. [UrhG § 63](https://www.gesetze-im-internet.de/urhg/__63.html) requires a
clear source identification and, for public communication under § 51, the
author where possible. [UrhG § 62](https://www.gesetze-im-internet.de/urhg/__62.html)
preserves the no-alteration rule, subject to its limited exceptions.

For this product, the defensible quotation purpose is narrow: each exact German
span is displayed so the reader can inspect the official wording supporting a
specific factual value, uncertainty or conflict. The implementation therefore
must:

- keep the quote short and proportionate to that evidentiary purpose;
- reproduce the German span exactly, visibly as source evidence rather than as
  the site's own prose;
- name the source authority and link the exact HTTPS source URL adjacent to the
  claim or its evidence presentation;
- avoid photographs, graphics, logos and third-party passages unless a separate
  right is established; and
- seek permission or remain an access-restricted preview if a longer extract is
  needed or the quotation purpose is not genuine.

### `berlin.de`

The [central Berlin.de imprint](https://www.berlin.de/wir-ueber-uns/impressum/)
says the portal's text and other content are copyright protected and usable only
within statutory provisions. More specifically, the
[Senate department imprint governing the project sources](https://www.berlin.de/sen/bauen/impressum/)
allows private copying but says public distribution is not allowed. It supplies
no open or express reuse licence for these Senate project pages or press
releases. The current short evidence spans therefore rely on §§ 51 and 63, not
on a `berlin.de` licence.

The statutory basis is adequate only while the spans remain short, exact,
attributed and necessary to the dossier's explanatory/evidentiary purpose. If
that boundary cannot be maintained, public deployment is blocked pending
permission or legal review.

### `parlament-berlin.de`

The [Abgeordnetenhaus imprint](https://www.parlament-berlin.de/impressum) says:

- ordinary site content requires permission beyond the stated personal-use
  allowance;
- press releases and speeches may be reprinted/evaluated with source
  attribution; and
- identified parliamentary Drucksachen and plenary protocols are official
  works under [UrhG § 5(2)](https://www.gesetze-im-internet.de/urhg/__5.html),
  while remaining subject to §§ 62 and 63 and possible third-party rights.

The C-014 `h19-2449-v.pdf` committee paper is not clearly classified by that
notice as a Drucksache or plenary protocol. The repository must not make that
classification itself. Its short exact spans use the same § 51 quotation basis
as above. A source explicitly identified as a Drucksache may use the narrower
official-work basis, still without alteration and with attribution.

## 2. BKG boundary attribution and placement

The bundled geometry is recorded as BKG's *Verwaltungsgebiete 1:250 000, Stand
01.01.2026 (VG250 01.01.)*, retrieved 2026-08-19. Its source CRS is EPSG:25832;
the WFS response was requested in EPSG:4326 and non-geometry attributes were
removed. The exact provenance and geometry digest are in
[`public/data/map/berlin-boundary.provenance.json`](../../../public/data/map/berlin-boundary.provenance.json).

The [BKG product page](https://gdz.bkg.bund.de/index.php/default/open-data/verwaltungsgebiete-1-250-000-stand-01-01-vg250-01-01.html)
requires a **clearly visible** source note for every public presentation and
specifies that, on a website, `BKG` and `dl-de/by-2-0` are links. The
[general `dl-de/by-2-0` text](https://www.govdata.de/dl-de/by-2-0) requires the
provider, linked licence notation, dataset URI and identification of changes.
The [BKG source-note guidance](https://gdz.bkg.bund.de/index.php/default/hinweise-zu-nutzungsbedingungen-und-quellenvermerken/)
expressly uses `(Daten verändert)` when source data have been changed.

The required visible map-associated source line is:

> © [BKG](https://www.bkg.bund.de) 2026 [dl-de/by-2-0](https://www.govdata.de/dl-de/by-2-0) (Daten verändert), Datenquellen: https://sgx.geodatenzentrum.de/web_public/gdz/datenquellen/datenquellen_vg_nuts.pdf

Placement requirement: show that line as an always-visible caption or source
line directly associated with the map/boundary presentation. A legal page may
repeat it, but metadata or a legal page alone does not meet the product-specific
"deutlich sichtbar" instruction. This is a compliance placement rule, not a
typography or layout decision.

The public build is blocked until Gate 4 supplies that visible linked line. The
current provenance string also omits `(Daten verändert)` and must be corrected
when the map implementation consumes it.

## 3. No analytics, no cookies, and hosting privacy

[TDDDG § 25](https://www.gesetze-im-internet.de/ttdsg/__25.html) generally
requires informed consent before storing information on, or accessing
information from, an end user's device, except for transmission-only or strictly
necessary operations. The
[Berlin data-protection authority's cookie guidance](https://www.datenschutz-berlin.de/themen/internet/cookies)
likewise says tracking normally requires consent and that the exception is for
strictly necessary access.

The v0 public application therefore has this bounded position:

- no client-side or product analytics;
- no analytics script, tracking pixel, cookie, `localStorage`, fingerprinting
  or consent-management code;
- no external embed, tile request or other third-party runtime request; and
- no cookie banner, because the verified application performs no device
  storage/access operation for which consent would be requested.

That is **not** a claim that the hosting provider processes no request data.
Static delivery exposes at least request metadata such as an IP address to the
host/CDN; GDPR recital 30 identifies IP addresses as online identifiers.
[GDPR Article 13](https://eur-lex.europa.eu/eli/reg/2016/679/oj) requires the
privacy notice to disclose the controller/contact, purposes and legal basis,
recipients/processors, applicable transfers and safeguards, retention period or
criteria, and data-subject rights.

The planned host's current
[Data Processing Addendum](https://vercel.com/legal/dpa) distinguishes customer
data from service-generated data, covers service-generated personal data,
identifies subprocessors, and contemplates processing/transfers outside the EEA.
The actual account plan, applicable contract/DPA, request-log and observability
behavior, retention, subprocessor locations, transfer safeguards, and disabled
optional analytics state have not been verified for the production deployment.
Do not state a retention period or transfer basis until those account-specific
facts are checked.

Consequently, Gate 6 must keep the deployment access-restricted until it has:

1. inspected the production account and network behavior;
2. confirmed optional Web Analytics and all product tracking are disabled;
3. recorded operational request/log processing, retention and transfers; and
4. published an Article 13 notice matching those facts.

If “no analytics” is intended to mean literally no host operational request
telemetry, the planned host is not presently established as compatible. Use the
restricted-preview fallback or select a host whose behavior can be verified;
do not recast operational telemetry as zero collection.

## 4. Provider identity and correction route

The correction route is both a project trust requirement and an intake path for
legal/privacy requests; it is not described here as a universal statutory
requirement in exactly the project's UI form.

[MStV § 18](https://www.gesetze-bayern.de/Content/Document/MStV-18) requires a
non-personal/family telemedia provider's name and address to be easily
recognizable, directly reachable and permanently available. For a
journalistically/editorially designed offer it additionally requires a named
responsible person and address, subject to the section's eligibility rules.
[MStV § 19](https://www.gesetze-bayern.de/Content/Document/MStV-19) applies
journalistic care duties to the covered services. [MStV § 20](https://www.gesetze-bayern.de/Content/Document/MStV-20)
creates a formal right of reply for its narrower class of covered offers; a
generic correction form would not replace that procedure if it applies.
[DDG § 5](https://www.gesetze-im-internet.de/ddg/__5.html) adds contact and
other information for businesslike services generally offered for remuneration.

The project's stricter publication policy requires every project and every
named organization to carry a visible correction path. Gate 6 verification must
prove:

- a stable public correction route exists and retains the affected project or
  organization context;
- every project and named-organization presentation links to it;
- the route reaches an actionable, monitored channel suitable for a static
  no-JavaScript site;
- the public instructions distinguish ordinary evidence corrections from
  formal rights of reply and data-protection requests; and
- the provider identity, postal address, electronic contact and any required
  editorially responsible person are approved and published.

The current projection contains `/corrections?project=...` paths, but no
`/corrections` route exists. The owner/operator identity, publishable address,
monitored channel and § 18(2) responsible-person decision are also unresolved.
These are public-deployment blockers. The repository's ban on naming source
natural persons does not authorize hiding a legally required operator identity.
If the identity/address cannot be published or applicability cannot be cleared,
the named fallback is an **access-restricted preview**, not a public release.

## Gate 6 pre-public checklist derived from this evidence

- [ ] Keep all source spans short, exact, purpose-bound, visibly quoted and
  linked to their exact HTTPS source.
- [ ] Add the visible, linked BKG attribution with `(Daten verändert)` directly
  to the map presentation.
- [ ] Verify the production host/account, optional analytics state, cookies,
  storage, network requests, operational logs, retention, subprocessors and
  transfer safeguards.
- [ ] Publish an accurate privacy notice and provider/editorial identity.
- [ ] Implement and production-test contextual correction routes and the
  monitored intake channel.
- [ ] Keep the deployment access-restricted until every item above is evidenced.

## Research method and source quality

Codex checked the statutes, authority imprints, regulator guidance, BKG product
and source-note instructions, licence text, and the planned host's current DPA.
A read-only legal-research subagent independently searched the same primary
sources and identified two refinements that were accepted after direct recheck:
the C-014 committee paper must not be self-classified as a parliamentary
Drucksache, and the no-analytics claim must distinguish product tracking from
host operational telemetry. No subagent edited the repository. Secondary
summaries were not used as controlling authority.
