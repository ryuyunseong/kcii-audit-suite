# Profile Coverage

This document summarizes the release-candidate coverage for the `kcii-2025-12` rulepack baseline. The tool is an offline assessment helper and not an official KISA tool.

## Summary

| Profile | Registered items | Auto | Partial | Manual | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| Windows Server | 64 | 7 | 2 | 55 | Full Windows manifest, selected automatic judgment |
| Linux Server | 8 | 0 | 8 | 0 | MVP-only rulepack, not full official Linux coverage |
| Unix Server | 67 | 0 | 28 | 39 | AIX, Solaris, HP-UX, Linux fixture-based parser |
| DBMS | 26 | 0 | 12 | 14 | PostgreSQL, MySQL, MariaDB offline parser and Docker live verification |
| Network | 38 | 9 | 0 | 29 | Cisco IOS simulator/parser MVP |
| Security Appliance | 23 | 0 | 23 | 0 | Questionnaire-centered evidence flow |

## Windows Server

- Scope: `W-01` to `W-64`
- Status: full item registration, partial automatic judgment
- Known limits:
  - Many account, service, share, audit, and IIS-related items require manual review.
  - English and Korean command output coverage needs continued expansion.
- Next automation candidates:
  - Password policy details
  - Audit policy
  - Unnecessary services
  - Share and anonymous access checks

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
- Status: offline parser plus Docker Compose live SQL verification
- Known limits:
  - Oracle, MSSQL, Tibero, Altibase, and Cubrid are not implemented.
  - Password policy, audit, role, and remote restriction evidence remains conservative.
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
  - Cisco IOS parser coverage is intentionally narrow.
  - Juniper, FortiGate, and other network OS support remains future work.
  - Configuration context often requires manual review.
- Next automation candidates:
  - AAA and management access policy
  - SNMP hardening
  - Logging/NTP policy
  - Additional vendor fixture sets

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
