# Profile Coverage

This document summarizes the release-candidate coverage for the `kcii-2025-12` rulepack baseline. The tool is an offline assessment helper and not an official KISA tool.

## Summary

| Profile | Registered items | Auto | Partial | Manual | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| Windows Server | 64 | 8 | 7 | 49 | Full Windows manifest, expanded rc2 automatic and partial judgment |
| Linux Server | 8 | 0 | 8 | 0 | MVP-only rulepack, not full official Linux coverage |
| Unix Server | 67 | 0 | 28 | 39 | AIX, Solaris, HP-UX, Linux fixture-based parser |
| DBMS | 26 | 0 | 12 | 14 | PostgreSQL, MySQL, MariaDB offline parser with JSON and key/value fixture coverage |
| Network | 38 | 27 | 0 | 11 | Cisco IOS simulator/parser with expanded command-response checks |
| Security Appliance | 23 | 0 | 23 | 0 | Questionnaire-centered evidence flow |

## Windows Server

- Scope: `W-01` to `W-64`
- Status: full item registration, partial automatic judgment
- Known limits:
  - Many account, service, share, audit, and IIS-related items require manual review.
  - English and Korean command output coverage needs continued expansion.
- Next automation candidates:
  - Password policy edge cases
  - Audit policy
  - Unnecessary services
  - Share and anonymous access checks
  - Event log retention policy

## Linux Server

- Scope: `L-01` to `L-08` MVP
- Status: MVP deterministic checks
- Known limits:
  - This is not a full official Linux item set.
  - Container results cannot replace VM or real host evidence for PAM, audit, and service-manager behavior.
- Next automation candidates:
  - Expand from MVP items to full official Linux/Unix alignment where appropriate.
  - Add more distro-specific fixture coverage.

## Unix Server

- Scope: `U-01` to `U-67`
- Supported offline fixture flavors: AIX, Solaris, HP-UX, Linux-compatible output
- Status: full item registration with conservative parser coverage
- Known limits:
  - Real AIX, Solaris, and HP-UX command output varies by version and vendor configuration.
  - Unsupported or ambiguous output remains `MANUAL_REQUIRED`.
- Next automation candidates:
  - Real-world sanitized AIX/Solaris/HP-UX output normalization
  - Service and log policy evidence expansion

## DBMS

- Scope: `D-01` to `D-26`
- Supported MVP DBMS: PostgreSQL, MySQL, MariaDB
- Status: offline parser MVP with JSON and key/value fixture coverage; Docker Compose remains a development verification lab
- Known limits:
  - Oracle, MSSQL, Tibero, Altibase, and Cubrid are not implemented.
  - Password policy, audit, role, and remote restriction evidence remains conservative.
  - Permission-denied and unsupported outputs remain `MANUAL_REQUIRED` rather than runtime failures.
- Next automation candidates:
  - Password policy evidence expansion
  - Audit/log setting checks
  - Remote access restriction checks
  - Additional DBMS engines

## Network

- Scope: `N-01` to `N-38`
- Supported MVP vendor: Cisco IOS
- Status: simulator/parser MVP
- Known limits:
  - Cisco IOS parser coverage is limited to deterministic command-response evidence.
  - Juniper, FortiGate, and other network OS support remains future work.
  - Configuration context often requires manual review.
- Next automation candidates:
  - AAA and management access policy
  - Real Cisco IOS, GNS3, CML, and lab output normalization
  - Additional vendor fixture sets

## v1.1.0 Development Scope

The `dev/v1.1.0` branch starts after the private `v1.0.0` release. The first development slice expands Cisco IOS automatic judgment only where sanitized command output can be interpreted deterministically.

`v1.1.0` is not tagged or released yet; see `RELEASE_NOTES_v1.1.0.md` and `docs/V1_1_0_READINESS.md` for the current draft release notes and readiness checklist.

Included in this slice:

- Preserve the published `v1.0.0`, `v1.0.0rc1`, and `v1.0.0rc2` tags.
- Keep `kcii-netlab-sim` as a command-response simulator, not a packet or routing emulator.
- Expand Cisco IOS checks for timestamp logging, SNMP ACL and authorization, TFTP, TCP keepalives, management web service, small services, Bootp, CDP, directed-broadcast, source-route, proxy ARP, ICMP control messages, identd, domain lookup, pad, and mask-reply indicators.
- Add sanitized realistic Cisco IOS fixture coverage for common `show run`, multi-`line vty`, SNMP, logging, NTP, and service-hardening output variants.
- Leave policy-dependent items such as password complexity, AAA lockout, user privilege design, auxiliary port review, patch status, logging policy completeness, SNMP necessity, spoofing controls, DDoS controls, and unused interface judgment as `MANUAL_REQUIRED`.
- Keep fixtures synthetic and sanitized; do not store customer configuration exports or live device output.

## Security Appliance

- Scope: `S-01` to `S-23`
- Supported MVP appliance types:
  - Firewall
  - IPS/IDS
  - WAF
  - VPN
  - Anti-DDoS
  - FortiGate
  - Palo Alto PAN-OS
  - Cisco ASA
  - F5 BIG-IP
- Status: questionnaire Excel export/import and sanitized config-summary parser
- Known limits:
  - Vendor-specific config parsers are wrappers around the common sanitized parser.
  - Policy review, monitoring, backup, and operational process evidence often requires interviews.
- Next automation candidates:
  - FortiGate config summary parser
  - PAN-OS config summary parser
  - Cisco ASA config summary parser
  - F5 BIG-IP config summary parser

## Common Interpretation

`GOOD` means the supplied sanitized evidence matched the rulepack's good condition.

`VULNERABLE` means the supplied sanitized evidence matched the rulepack's vulnerable condition.

`MANUAL_REQUIRED` means the item remains in scope but needs additional evidence, interview confirmation, compensating-control review, or assessor judgment. It is not a runtime failure.

## Automation Levels

- `auto`: deterministic judgment is possible from the sanitized evidence shape currently supported by the parser.
- `partial`: the item has one or more deterministic checks, but additional operating-context review may still be required.
- `manual`: the item is registered and intentionally emitted as `MANUAL_REQUIRED` unless reviewed evidence is supplied by an assessor.
- `unsupported`: the item or platform is out of the current parser scope and must remain a documented future candidate.

## v1.0.0rc2 Scope

The `dev/v1.0.0rc2` branch is for release-candidate hardening after the private `v1.0.0rc1` pre-release. The rc2 goal is practical completeness, not full automation.

Targets:

- Preserve full registered manifests for Windows Server, Unix Server, DBMS, Network, and Security Appliance.
- Keep Linux Server as the current MVP unless a separately scoped Linux expansion is approved.
- Increase automatic judgment only where sanitized evidence can be interpreted deterministically.
- Ensure every registered item still produces `GOOD`, `VULNERABLE`, or `MANUAL_REQUIRED`.
- Include vulnerable and manual-check items in `security_advisory.md` and `security_advisory.xlsx`.
- Keep the seven-file output bundle stable for every supported profile.
- Document profile-level auto, partial, manual, and unsupported coverage before each release candidate.

## v1.0.0rc2 Exclusions

The following are excluded from rc2 unless separately approved:

- Moving, deleting, or reusing the published `v1.0.0rc1` tag.
- Public repository publication.
- PyPI or TestPyPI publishing.
- Production remote collection from customer targets.
- Storing raw customer evidence in normal report, advisory, workbook, or fixture outputs.
- Broad parser rewrites unrelated to a scoped profile improvement.
- New secret, token, credential, certificate, or license material in samples, fixtures, docs, or release assets.

## Official Guide Reflection Procedure

Rulepack changes must stay tied to the local `kcii-2025-12` baseline used by this project.

When updating manifest or rulepack content:

1. Check the item ID, title, severity, and domain against the approved local guide source.
2. Do not invent item names.
3. Do not copy long guide passages into the repository.
4. Add every official item to both the profile manifest and profile rulepack.
5. Mark deterministic checks as `auto` or `partial` only when the parser evidence is sufficient.
6. Leave ambiguous or policy-dependent items as `manual`.
7. Keep source notes concise and avoid customer-specific examples.

## Sensitive Evidence Handling

- Fixtures must remain synthetic and sanitized.
- Do not commit customer evidence, raw config exports, `.env` files, passwords, hashes, tokens, keys, certificate bodies, hostnames, domains, account names, serial numbers, policy names, object names, internal URLs, or IP addresses.
- Store boolean, integer, enum, count, masked identifier, warning, and `raw_evidence_hash` values rather than raw evidence text.
- Treat parser failures, unsupported output, and permission-denied collection as classification evidence that can lead to `MANUAL_REQUIRED`, not as a reason to drop the item from results.
