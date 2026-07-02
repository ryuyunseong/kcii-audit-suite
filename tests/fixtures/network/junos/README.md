# Junos Fixture Sanitization

This directory contains synthetic or sanitized Juniper Junos fixtures for the Network profile.

## Supported MVP Input

The current parser accepts only display-set style configuration:

```text
set system services ssh
set system login user [USER_1] class read-only
set snmp community [COMMUNITY_1] authorization read-only
```

Use output collected with `show configuration | display set`, or an equivalent offline text file where each active configuration statement is represented as one `set ...` line.

## Unsupported Input

The following formats must stay unsupported unless a separate parser task is approved:

- brace-style configuration such as `system { services { ssh; } }`
- XML configuration
- JSON configuration
- unexpanded `groups`, `apply-groups`, or inherited configuration
- direct device sessions or live collection transcripts

Unsupported input must lead to `MANUAL_REQUIRED` or `needs_display_set`. It must not be interpreted as safe evidence.

## Sanitization Rules

Before adding a lab or device-derived fixture, replace sensitive values with stable placeholders:

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
| file path or config backup path | `[PATH_1]` |
| banner text | `[BANNER_1]` |
| key, token, hash, or password | `[SECRET_1]` |

Do not store customer configuration exports, live output, commercial images, VM disks, licenses, keys, tokens, password hashes, or certificate bodies in this directory.

## Fixture Review Checklist

- The fixture contains no real hostnames, IP addresses, account names, communities, serials, domains, paths, keys, tokens, password hashes, or license text.
- Active evidence appears as `set ...` lines.
- Inactive or deactivated statements are preserved only when the test intentionally validates that they are ignored.
- `apply-groups` or inherited configuration must remain a manual-review signal until inheritance expansion is explicitly implemented.
- Every fixture is synthetic or sanitized before commit.
- `python -m pytest tests/test_network_junos.py tests/test_network_vendor_regression.py` passes.
