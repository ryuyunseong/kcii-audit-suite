# Network Output Sanitization

This document defines how Cisco IOS, GNS3, CML, and approved lab command output can be converted into repository-safe fixtures for the Network profile. The repository must never store real customer configuration exports, commercial device images, CML or IOS images, license files, raw credentials, or unredacted live output.

## Scope

The Network profile remains an offline parser and reporting helper. `kcii-netlab-sim` is a command-response simulator for parser and rulepack tests; it is not a Packet Tracer, GNS3, CML, routing, or packet-forwarding emulator.

Allowed fixture sources:

- Synthetic `kcii-netlab-sim` output.
- GNS3 or CML lab output after sanitization.
- Actual device command output only after sanitization and only when the source is approved for local test use.

Excluded material:

- Customer config exports in raw form.
- Device images, IOS images, CML images, VM disks, or license files.
- Hostnames, domains, public or private IP addresses, usernames, SNMP communities, serial numbers, object names, backup paths, banner text, keys, tokens, hashes, and passwords.

## Required Replacements

Apply these replacements before adding a fixture:

| Source value | Replacement |
| --- | --- |
| Hostname or prompt name | `[HOST_1]` |
| IP address | `[IP_1]` |
| Username | `[USER_1]` |
| SNMP community | `[COMMUNITY_1]` |
| Serial number | `[SERIAL_1]` |
| Domain | `[DOMAIN_1]` |
| Path or config backup path | `[PATH_1]` |
| Banner text | `[BANNER_1]` |
| Key, token, hash, or password | `[SECRET_1]` |

Use numbered placeholders such as `[IP_2]` only when multiple distinct values are required for parser behavior. Do not use real-looking private addresses as examples.

## Supported Command Set

Realistic Cisco IOS fixtures should focus on the same offline command set used by the parser:

- `show running-config` or `show run`
- `show startup-config`
- `show version`
- `show ip ssh`
- `show users`
- `show line`
- `show logging`
- `show ntp status`
- `show snmp`
- `show access-lists`
- `show ip interface brief`

Unknown command output, separators, prompts, blank lines, and vendor-specific noise should not make parsing fail. Unsupported evidence should be ignored or should leave the item as `MANUAL_REQUIRED`.

## Parser Output Rules

The parser must keep only normalized evidence such as booleans, enums, counts, warnings, and `raw_evidence_hash`. It must not store full command output, config sections, account names, IP addresses, SNMP communities, serial numbers, paths, banner text, or secret material in:

- `evidence.jsonl`
- `results.json`
- `report.md`
- `security_advisory.md`
- `detail.xlsx`
- `summary.xlsx`
- `security_advisory.xlsx`

## Fixture Review Checklist

Before committing a realistic fixture:

1. Search for raw IP addresses, hostnames, usernames, communities, serials, domains, paths, passwords, keys, tokens, and hashes.
2. Run `kcii-audit classify-file --profile network --vendor cisco_ios` against the fixture.
3. Confirm `N-01` to `N-38` all appear in `results.json`.
4. Confirm the seven-file output bundle is created.
5. Search text and workbook outputs for fixture placeholders.
6. Run `python -m pytest`.
