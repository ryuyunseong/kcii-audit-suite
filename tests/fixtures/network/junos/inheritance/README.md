# Junos Inheritance Fixture Plan

This directory is reserved for synthetic or sanitized Junos `display inheritance` fixtures.

No real customer configuration, raw live output, Junos image, CML image, VM disk, license file, key, token, password hash, certificate body, or credential material may be stored here.

## Intended Evidence Pair

Fixtures should model offline evidence collected as:

```text
show configuration | display set
show configuration | display inheritance
```

The display-set fixture remains the primary active configuration evidence. The display-inheritance fixture is supplemental evidence used to understand how `apply-groups` affects effective settings.

## Sanitization

Replace sensitive values with stable placeholders:

| Sensitive value | Placeholder |
| --- | --- |
| hostname | `[HOST_1]` |
| IP address or network prefix | `[IP_1]` |
| username | `[USER_1]` |
| SNMP community | `[COMMUNITY_1]` |
| configuration group name | `[GROUP_1]` |
| firewall filter or prefix-list name | `[FILTER_1]`, `[PREFIX_LIST_1]` |
| serial number | `[SERIAL_1]` |
| domain | `[DOMAIN_1]` |
| file path or backup path | `[PATH_1]` |
| banner text | `[BANNER_1]` |
| key, token, hash, password, or credential value | `[SECRET_1]` |

## Merge Rules Under Design

- Local active display-set statements take precedence over inherited evidence.
- Inactive or deactivated inherited statements must not become active evidence.
- Conflicting inherited values must remain `MANUAL_REQUIRED`.
- Missing source group data must remain `MANUAL_REQUIRED`.
- `apply-groups-except` must remain `MANUAL_REQUIRED` until explicitly supported.

## Automation Candidates

The first parser implementation may consider deterministic handling only for explicit inherited evidence related to SSH, Telnet, web management, syslog, NTP, SNMP, and management ACL references.

All other inherited evidence should remain manual-review evidence until tests prove a narrower safe rule.
