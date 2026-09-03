# Vercel Hobby privacy evidence and unresolved processor terms

**Checked:** 25 August 2026

**Scope:** Official Vercel legal and product documentation for the planned
public static deployment. This is documentary research, not a substitute for
observing the deployed site or authenticated project settings.

## Question

What can the Article 13 notice state about Vercel request processing,
retention, analytics, recipients and transfers without relying on a marketing
page or inferring account-specific behavior?

## Official sources checked

- [Vercel Terms of Service, effective 1 June 2026](https://vercel.com/legal/terms)
- [Vercel Data Processing Addendum, effective 31 March 2026](https://vercel.com/legal/dpa)
- [DPA PDF linked by the current Terms of Service, dated 29 March 2023](https://assets.vercel.com/image/upload/v1682696728/front/legal/terms/Vercel_Customer_DPA__032923.pdf)
- [Vercel Privacy Notice, effective 1 June 2026](https://vercel.com/legal/privacy-notice)
- [Vercel Runtime Logs documentation](https://vercel.com/docs/logs/runtime)
- [Vercel Observability documentation](https://vercel.com/docs/observability)
- [Vercel Web Analytics quickstart](https://vercel.com/docs/analytics/quickstart)

## Findings

### Request and operational data

Vercel's Privacy Notice says it receives traffic information from customer
websites including an end-user IP address, location derived from that address
and system-configuration information. It separately lists log files, IP
address, IP-derived city/country, proxy server, diagnostics, capacity and usage,
server performance, data settings and system configuration as
service-generated information. The Terms define traffic data, telemetry,
service-generated logs and usage statistics as System Data.

This supports disclosing that the host processes request data including the IP
address for delivery and operational purposes. It does not establish which
fields appear in the owner-visible logs for this particular deployment.

### Retention

Vercel documents a one-hour Hobby retention window for customer-visible runtime
logs and a 12-hour Hobby window for base Observability events. The planned site
is a static export and has no serverless function runtime. These documented
dashboard windows must not be restated as deletion periods for all Vercel
systems. The Privacy Notice gives only a criterion for Vercel-controlled data:
minimum necessary for legal, contractual and legitimate purposes, followed by
deletion or anonymization when there is no ongoing legitimate business need;
backups may remain securely stored where deletion is not possible.

### Analytics and application behavior

Vercel's Astro and Web Analytics documentation requires an explicit package,
component, adapter setting or script integration. Repository inspection and the
real-export test establish that this application contains none of them and
ships no script or JavaScript asset. That supports “Web Analytics is not
integrated in the application.” It does not establish whether an account-level
feature or other platform telemetry is active; the dashboard and live network
trace still need inspection.

### Recipient, processor and DPA conflict

Vercel Inc. identifies itself at 440 N Barranca Avenue #4133, Covina, CA 91723,
United States. The current Terms say personal information is processed as
controller or processor as applicable and incorporate a linked DPA. That link
currently resolves to the 29 March 2023 DPA PDF, which can supplement an “other
agreement executed” between Vercel and the customer and describes Vercel as
processor for Customer Data.

The newer canonical DPA, however, expressly says its processor terms apply to
Enterprise and Pro customers. It does not include Hobby. Public official
documents therefore do not provide one unambiguous basis for claiming that the
current canonical DPA governs a Hobby deployment. The notice may link both the
host's Terms and current DPA and disclose the conflict; it must not claim that
current-DPA coverage has been established. Resolution requires an authoritative
account-specific answer from Vercel or a change of plan/provider.

### Transfers and subprocessors

Vercel's Privacy Notice says information can be processed in the United States
and other jurisdictions and says that, where required, it uses Standard
Contractual Clauses or other appropriate mechanisms. It also states that Vercel
participates in the EU–U.S. Data Privacy Framework. The canonical DPA contains
subprocessor and transfer clauses, but its applicability to Hobby is the
unresolved issue above. A service-wide subprocessor list does not establish
which named entities process this deployment. Deployment-specific
subprocessors and the operative transfer mechanism remain unverified.

## Claims permitted in the draft notice

- The host is Vercel Inc. and receives request information including IP address
  and IP-derived location.
- The controller's basis for the necessary delivery and security processing is
  Art. 6(1)(f) GDPR, with operation, troubleshooting, abuse prevention and
  security as the stated legitimate interests.
- The application contains no cookies, analytics, tracking, third-party runtime
  requests, client JavaScript, accounts or forms; user-selected source links are
  navigations rather than embeds.
- The documented one-hour and 12-hour windows are customer-visible product
  windows, not asserted global deletion periods.
- The Hobby DPA applicability, exact applicable subprocessors and exact
  transfer safeguard remain unverified.

## Live checks still required

Against the exact production URL and commit, from a fresh browser profile:

1. Preserve a network trace for the landing page, every generated route and a
   reload; separate automatic requests from clicked source-link navigations.
2. Inspect response headers, cookies, local/session storage, IndexedDB, Cache
   Storage, service workers and delivered JavaScript assets.
3. Inspect project settings for Web Analytics, Speed Insights, integrations and
   log drains.
4. Correlate a synthetic request with owner-visible Observability/log entries
   and record the fields exposed, without retaining the visitor IP or cookie
   values.
5. Record the exact plan, project, deployment ID, commit, UTC observation time
   and applicable account terms.

Until those checks exist, the repository can describe the static application
and the provider's official documentary position, but not actual production
network behavior or account configuration.

## Method and limitations

The main agent checked the official pages above and independently reconciled a
read-only research subagent's source list. No model/extraction-provider call was
made. The subagent did not edit the repository. This finding is not legal advice
and does not resolve the contradiction in Vercel's official documents.
