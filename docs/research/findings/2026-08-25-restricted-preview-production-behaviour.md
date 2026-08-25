# Restricted-preview production behavior

**Checkpoint:** 2026-08-25
**Scope:** Gate 6 live-delivery, privacy and operational evidence
**Status:** **Incomplete — no live deployment URL or account-specific evidence was available in this lane.**

This record is deliberately observation-first. It does not replace missing live
facts with a hosting provider's general product or marketing pages. The project
owner is handling the Astro deployment in a separate session. Until the exact
deployment and its account configuration are supplied and observed, this file
backs no claim about host/CDN request processing, operational logs, retention,
subprocessors or transfers.

Do not record authentication secrets, cookie values, reviewer IP addresses,
raw request headers containing credentials or unnecessary account personal data
in this repository.

## Evidence identity required for the live pass

- Deployment URL: `[LIVE EVIDENCE REQUIRED]`
- Deployment ID: `[LIVE EVIDENCE REQUIRED]`
- Deployed Git commit: `[LIVE EVIDENCE REQUIRED]`
- Observation time in UTC: `[LIVE EVIDENCE REQUIRED]`
- Browser and version: `[LIVE EVIDENCE REQUIRED]`
- Fresh-profile and empty-cache confirmation: `[LIVE EVIDENCE REQUIRED]`
- Deployment/access-protection mode: `[LIVE EVIDENCE REQUIRED]`

## Observation matrix

| Area | Observation required | Evidence to retain | Current result |
| --- | --- | --- | --- |
| Outbound requests | Preserve the fresh-profile network log through first load, any access step, all static routes and one reload. Separate automatic requests from user-initiated source-link navigation. | Sanitized origin, method, resource type and initiator table; sanitized HAR only if it contains no credentials or personal identifiers. | Not observed. |
| Cookies | Inspect `Set-Cookie` response headers and the cookie jar before access, after access and after route traversal. Record names and attributes, never values. | Host, path, session/expiry, `Secure`, `HttpOnly` and `SameSite` for each cookie, with whether it belongs to the application, host or access layer. | The repository export contains no application cookie code; live delivery not observed. |
| Browser storage | Inspect local storage, session storage, IndexedDB, Cache Storage and service-worker registrations before and after route traversal. | Empty/non-empty state for each mechanism and any observed access initiator. | The repository export contains no application storage code or service worker; live delivery not observed. |
| Analytics | Inspect delivered HTML and network traffic for analytics, pixels, beacons, Web Analytics and Speed Insights. Inspect project settings and installed integrations. | Sanitized network evidence plus account-setting screenshots or exports showing the actual enabled/disabled state. | The repository contains no analytics dependency or client JavaScript; account state not observed. |
| Operational logging | Generate a synthetic, non-personal request and locate the correlated event in project logs/observability. Record which fields are stored without publishing IP or authentication material. | Sanitized correlated event, log/drain configuration and the actual recipients. | Not observed. |
| Retention | Inspect account/project retention controls for request logs, observability, access/protection events and any configured drain. The oldest visible event does not prove deletion. | Account-bound setting, contract term or provider support confirmation that establishes a period or deletion criterion. | Unresolved. No period is asserted. |
| Subprocessors | Match the account's operative DPA/subprocessor schedule to the services and integrations actually enabled for this deployment. | Applicable agreement/version, enabled services and relevant subprocessor entries. | Unresolved. Browser traffic alone cannot establish this. |
| Transfers and safeguards | Inspect processing-region controls and match each relevant non-EEA processing location to its operative safeguard. | Account-bound agreement, actual service/region configuration and safeguard applicability. | Unresolved. No transfer or safeguard is inferred. |

## Three layers that must remain distinct

1. **Static application behavior.** The committed export can establish the
   absence of application JavaScript, analytics dependencies, external embeds
   and application storage calls.
2. **Deployment/access-layer behavior.** The live platform may add a challenge,
   cookie, script or request that does not exist in the repository export.
3. **Host/CDN operational processing.** Server-side request logs, retention,
   recipients, subprocessors and transfers cannot be inferred from a quiet
   browser trace.

## Local evidence available at this checkpoint

- `npm run build` generated 12 static pages after the legal-draft routes were
  added and emitted no client JavaScript.
- The Python suite passed 173 tests after this work.
- `web/package.json` contains Astro as its only application dependency and
  disables Astro build telemetry.
- The real-export tests reject scripts, JavaScript files, copied JSON/data and
  known-withheld or sentinel values.
- A local fresh-origin browser reload made one same-origin HTML request, set no
  cookie, and left local/session storage, IndexedDB, Cache Storage and service
  workers empty. All 12 routes fit at 320 CSS pixels and were keyboard
  reachable. The detailed evidence is in
  `2026-08-25-local-route-accessibility-verification.md`.

These are build observations, not production-host observations. They support
the application-layer statements in the draft Article 13 route only.

## Completion criterion

This finding becomes complete only after every row above contains evidence from
the exact deployed artifact and its actual account configuration. The final
Article 13 notice must cite this completed record and must not contain any live
placeholder.

## Research orchestration

A read-only research subagent was used because the repository research skill
requires a bounded background evidence lane. It inspected the existing Gate 6
finding, plan, decisions, tests and static architecture without editing files or
making an external/provider call. Its useful output was the three-layer model
and the observation matrix above. The main agent accepted that structure,
rewrote it as an incomplete evidence record, and independently checked every
repository path and claim. No live-host conclusion from the lane was accepted
because no deployment or account evidence existed.
