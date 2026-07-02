# Junos Display Inheritance Design

This document records the `dev/v1.4.0` design boundary for Junos `display inheritance` support. It is a planning document, not a parser implementation.

## Goal

Use sanitized offline Junos evidence to decide when inherited configuration can safely improve Network profile judgment while preserving conservative `MANUAL_REQUIRED` behavior for ambiguous cases.

The target evidence pair is:

```text
show configuration | display set
show configuration | display inheritance
```

The parser must not connect to devices, collect live data, or store raw customer configuration.

## Non-Goals

- Full Junos configuration interpreter behavior
- Brace-style configuration parser
- XML or JSON parser
- NETCONF, SSH, or live collection
- Complete `apply-groups` semantics
- Automatic good or vulnerable judgment from incomplete inherited evidence

## Evidence Model

Display-set evidence remains the primary active configuration source. Display-inheritance evidence is supplemental and should be normalized into an inheritance map.

Suggested normalized fields:

- `input_format`: `junos_display_set_with_inheritance`
- `inheritance_present`: boolean
- `inheritance_sources`: masked group count or stable placeholder list
- `inheritance_conflict_detected`: boolean
- `inheritance_incomplete`: boolean
- `inherited_paths`: sanitized path summary
- `manual_required_reason`: enum or short sanitized text

The normal output contract must still avoid raw config text. Store booleans, enums, counts, masked identifiers, and `raw_evidence_hash`.

## Merge Strategy

1. Parse active display-set lines first.
2. Parse display-inheritance evidence into sanitized path summaries.
3. Match inherited evidence to active paths only when path and semantic meaning are clear.
4. Prefer explicit local active statements over inherited statements when both are present.
5. Treat inactive or deactivated inherited statements as non-active evidence.
6. Treat conflicting inherited values as `MANUAL_REQUIRED`.
7. Treat missing group source context as `MANUAL_REQUIRED`.

## Automation Candidates

The following may become deterministic only when inherited evidence is explicit and not contradicted:

- SSH enabled and Telnet disabled evidence
- web management disabled evidence
- syslog host presence
- NTP server or peer presence
- SNMP read-only community and access restriction evidence
- management ACL or filter reference evidence

## Manual-Required Cases

Keep the item as `MANUAL_REQUIRED` when:

- multiple groups define conflicting values
- `apply-groups-except` changes applicability
- inheritance source details are omitted
- only brace-style, XML, or JSON config is supplied
- inactive statements are the only evidence
- a platform default must be assumed
- policy context or assessor judgment is required

## Fixture Plan

Fixture work should start under `tests/fixtures/network/junos/inheritance/`.

Initial files should be synthetic and sanitized:

- `display_set_with_apply_groups.txt`
- `display_inheritance_effective_good.txt`
- `display_inheritance_conflict.txt`
- `display_inheritance_incomplete.txt`

Each fixture must avoid real hostnames, IP addresses, usernames, SNMP communities, serials, domains, paths, keys, tokens, hashes, passwords, and license text.

## Test Plan

Initial tests should verify:

- display-set only behavior remains unchanged
- inheritance evidence can be parsed without storing raw lines
- explicit inherited safe evidence can become partial evidence only for selected fields
- conflicts and incomplete inheritance remain `MANUAL_REQUIRED`
- all `N-01` to `N-38` items continue to be emitted
- sensitive placeholders do not leak into normal outputs

## Release Boundary

`v1.4.0` should not claim complete Junos inheritance support unless parser tests prove the supported evidence shapes. The first implementation can remain a design and fixture skeleton if deterministic merge rules are not yet narrow enough.
