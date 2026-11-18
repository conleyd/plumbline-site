# plumbline-site

The public marketing and compliance site for Plumbline. It is plain HTML and CSS: no framework, no JavaScript, no cookies, no tracking, and no third-party requests (fonts are system fonts).

## Layout

| Path | What it is |
| --- | --- |
| `src/` | The site: every page, `styles.css`, `favicon.svg`, `robots.txt`, `sitemap.xml` |
| `site.config` | The two values to edit: `CONTACT_EMAIL` and `BASE_URL` |
| `scripts/render.py` | Copies `src/` to `_site/` and fills in `__CONTACT_EMAIL__` and `__BASE_URL__`. A string substitution, nothing more |
| `scripts/check_links.py` | Crawls a running copy and fails on broken links, missing `#anchors`, unfilled placeholders, or any page of 100 KB or more |
| `.github/workflows/pages.yml` | On push to `main`: render, link-check, deploy to GitHub Pages |

## Config

- **Contact address:** edit `CONTACT_EMAIL` in `site.config`. Every mailto link uses it.
- **Base URL:** used only for canonical links, `sitemap.xml`, `robots.txt` and the 404 page; every other link is relative. Leave `BASE_URL` empty and it resolves to `https://<owner>.github.io/plumbline-site` in Actions. To move to a custom domain, add a `CNAME` file at the repository root containing the domain (for example `www.example.com`): the base URL becomes `https://<domain>` and the file is copied into the published site. Also set the domain under Settings, Pages, and add the DNS record.

## Local preview

```
python3 scripts/render.py --base-url http://127.0.0.1:8765
python3 -m http.server 8765 --bind 127.0.0.1 --directory _site
python3 scripts/check_links.py http://127.0.0.1:8765/
```

## Pages

| Page | File | Content |
| --- | --- | --- |
| Home | `index.html` | One-sentence description; what sponsors see; what portfolio companies connect; how data is protected; link to Integrations |
| Product | `product.html` | Onboarding in three steps (invite, connect tools, heatmap) with SVG diagrams. The heatmap diagram is labelled illustrative and holds no data |
| Integrations and data use | `integrations.html` | Rules for every source; Salesforce, Microsoft Entra ID, Ramp: reads, never reads, scopes, not requested, read-only, upload alternative; "other sources are planned" |
| Security | `security.html` | Design only; states that no SOC 2 report or other certification has been issued |
| Privacy policy | `privacy.html` | Marked "Draft, pending legal review" |
| Terms | `terms.html` | Marked "Draft, pending legal review" |
| Contact | `contact.html` | mailto link only |
| Not found | `404.html` | GitHub Pages 404 |

## Where each claim comes from

All sources are in the `nativeops` repository. Line references are to the files as of 2026-11-18.

| Claim on the site | Source |
| --- | --- |
| One-sentence description, "see, steer and prove", "measure itself, follow a prescribed roadmap, show results in financial terms", "Agents collect, people confirm, every number shows its evidence" | `README.md` |
| "In development" notice | `README.md` "Status" |
| Sponsors see only aggregates, at company and function level, only while a data agreement is in force; nothing below five people; no ranking | `SECURITY_AND_COMPLIANCE.md` Summary, data classification table, Visibility matrix, Decisions 2 |
| Email invitations: single use, bound to the invited email, 72-hour expiry; SSO through Entra or Google; SSO can be required | `SECURITY_AND_COMPLIANCE.md` "Authentication" |
| Data agreement acceptance is audited | `SECURITY_AND_COMPLIANCE.md` "What is logged" |
| Five-step connect panel; panel generated from the registry; missing scopes shown; preview of at most 20 rows, not stored; upload alternative on every source | `INTEGRATIONS.md` Summary, 1.2, 1.4, 1.10 |
| Agents never handle passwords; OAuth, app install or pasted key | `INTEGRATIONS.md` 1.5; `SECURITY_AND_COMPLIANCE.md` principle 2 |
| 90-day backfill, newest first; Salesforce reads open plus TTM-closed opportunities | `INTEGRATIONS.md` 1.8, decision I-D4 |
| Revoke: vendor revoke endpoint, credential deleted, queued work stopped, history kept | `INTEGRATIONS.md` 1.2 "Revoke" |
| Attested, Verified, Stale, Not connected; last good value kept; never zero | `INTEGRATIONS.md` 1.4 (`confidence_gain`), 1.6 steps 2 to 6 |
| AI output is a proposal until a named person approves | `SECURITY_AND_COMPLIANCE.md` principle 7 |
| Read-only guard test; the four allowed writes | `INTEGRATIONS.md` 1.3; `SECURITY_AND_COMPLIANCE.md` principle 1 |
| Credentials AES-256-GCM under the tenant data key, decrypted only in the connector task, no human sees them | `INTEGRATIONS.md` 1.5, 6.1 "Secret storage"; `SECURITY_AND_COMPLIANCE.md` data classification |
| Rate-limit headroom | `INTEGRATIONS.md` 1.7 |
| Salesforce reads, never reads, objects, `api` and `refresh_token`, PKCE, integration user, not requested, Bulk API query jobs, 5% API cap, purposes | `INTEGRATIONS.md` INT-04, 1.3, 1.7, 6.1 row INT-04 |
| Salesforce data processed in Plumbline's cloud; package stores only config, license state, OAuth linkage; no write on standard objects; change events are pointers re-read through REST | `ADR-003`; `INTEGRATIONS.md` INT-04 "Managed package path", 1.3 |
| Entra reads, never reads, `User.Read.All`, `Group.Read.All`, `AuditLog.Read.All`, `Directory.Read.All`, P1/P2 licence note, SCIM inbound only, purposes, upload alternative | `INTEGRATIONS.md` INT-11, 6.1 row INT-11; `SECURITY_AND_COMPLIANCE.md` scopes table row INT-11 |
| Ramp reads, never reads, `transactions:read`, `users:read`, Developer API permission, not requested, daily, purposes, statement upload with memo dropped | `INTEGRATIONS.md` INT-10, 6.1 row INT-10 |
| Per-tenant data key, KMS, encryption context, AAD binding, annual rotation, at-rest encryption, TLS 1.2 | `SECURITY_AND_COMPLIANCE.md` "Secrets and keys", "Infrastructure security" |
| Row-level security, guard tests, roles enforced in the data layer, anti-differencing | `SECURITY_AND_COMPLIANCE.md` Summary, principle 3, "Suppression and anti-differencing", Decisions 1 |
| Append-only evidence, nightly hash-chain check that pages, Object Lock, 7 years | `SECURITY_AND_COMPLIANCE.md` principle 5, "Audit logging", data classification |
| Prompt content never collected; allowlisted usage schema; no leaderboards; raw-access log visible to admin | `SECURITY_AND_COMPLIANCE.md` data classification, "Data minimisation", "Visibility matrix", principle 4 |
| Export and close: revoke, delete, destroy keys, backups gone by day 28, certificate on day 30, residual items | `SECURITY_AND_COMPLIANCE.md` "Crypto-shredding and deletion certificate" |
| No SOC 2 report issued | `SECURITY_AND_COMPLIANCE.md` "SOC 2 path" (a target, not a result) and `README.md` status |
| Controller and processor roles; employee access and erasure through the company admin | `SECURITY_AND_COMPLIANCE.md` "GDPR and EU considerations" |
| What data is collected | `SECURITY_AND_COMPLIANCE.md` data classification; EXIF stripping from "Application security controls" |
| Service providers list | `SECURITY_AND_COMPLIANCE.md` "Sub-processor list" |
| Retention table | `SECURITY_AND_COMPLIANCE.md` data classification, "Audit logging", "Infrastructure security", Decisions 14; `INTEGRATIONS.md` 1.2 (webhook payloads) |
| Export-and-close overrides 7-year retention | `SECURITY_AND_COMPLIANCE.md` FLAG-4 (resolved O-01, subject to counsel) |
| Governance features are not legal advice | `SECURITY_AND_COMPLIANCE.md` "Compliance scope boundaries" |
| Support access through a grant the admin can see | `SECURITY_AND_COMPLIANCE.md` Decisions 10, 13 |

## Needs the owner's review

1. **Legal text.** Privacy policy and Terms are drafts written from the architecture documents, not by counsel. The Terms leave fees, liability, warranties, acceptable use, governing law and the DPA unwritten. Export-and-close overriding evidence retention is itself "subject to counsel" (O-01).
2. **"Shared with: none".** The brief asks for "none". The privacy policy says none for third parties' own use, then lists the service providers (sub-processors) from SECURITY_AND_COMPLIANCE.md, which also requires the policy to name them. Confirm the list is still current.
3. **Anthropic and ZDR.** The sub-processor list says "Anthropic (AI processing, ZDR)", but open question 7 (O-08) says ZDR is not signed. The site says "AI processing" only.
4. **Contact address.** `conley.dylan@gmail.com` is a personal address; it is used for general, security and privacy contact. Change `CONTACT_EMAIL` when a company address exists.
5. **Domain.** The site publishes to `github.io`. A custom domain needs a `CNAME` file, the Pages setting and DNS.
6. **Hosting note.** The privacy policy says GitHub Pages receives request details such as IP address. That is a fact about the host, not from the nativeops docs.
7. **Onboarding words from the brief.** "AI-adoption heatmap" and "invite" come from the brief, not the docs; the heatmap description uses only the confidence states the docs define. The diagram is illustrative, with placeholder labels.
8. **Status.** The site says Plumbline is in development, per the nativeops README ("Architecture phase. No application code yet."). Update the notice when that changes.
9. **Vendor facts marked unverified in INTEGRATIONS.md.** Ramp scope names are "verified in part" and the grant type is unverified; Salesforce connected app versus External Client App is unconfirmed. The site lists the scopes as the docs give them.
10. **Brand.** The mark and the accent colour were drawn for this site; the brand files in `nativeops/design/` and `web/public/brand/` were out of scope and were not read.

## Left out because the source docs do not support it

- **Microsoft 365 usage reports.** The brief asks for it under identity and usage, but none of the source sections describe a Microsoft 365 usage-reports connector or its scopes, so the Integrations page has no section for it.
- Phase and timing of each connector, pricing, customers, team, address, and any certification.
