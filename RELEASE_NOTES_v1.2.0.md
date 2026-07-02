# kcii-audit-suite v1.2.0 Development Draft

`kcii-audit-suite v1.2.0` is currently a development draft on `dev/v1.2.0`. No `v1.2.0` tag or GitHub Release has been created.

The baseline final release remains `v1.1.0`, fixed at commit `31f624e`. The `v1.0.0`, `v1.0.0rc2`, and `v1.0.0rc1` tags also remain fixed and must not be moved.

## Summary

This draft documents the Juniper Junos parser MVP completed after `v1.1.0`:

- Network profile now has a second vendor MVP for Juniper Junos.
- The Junos MVP supports sanitized `show configuration | display set` style input only.
- `--vendor junos` and `--vendor juniper_junos` are accepted.
- Network `N-01` to `N-38` full result emission is preserved.
- Ambiguous, unsupported, default-dependent, policy-dependent, or unexpanded configuration remains `MANUAL_REQUIRED`.

## Changes Since v1.1.0

- Added a Junos display-set parser that normalizes selected `set ...` configuration lines into the existing Network evidence contract.
- Added Junos fixture coverage for a sanitized good display-set sample, a sanitized vulnerable display-set sample, and an unsupported brace-style sample.
- Added Junos vendor mapping to the Network `kcii-2025-12` manifest and rulepack.
- Added CLI support for `--vendor junos` and `--vendor juniper_junos`.
- Updated Network coverage documentation and sanitization guidance for Junos display-set input.

## Juniper Junos MVP Scope

Supported input:

- `show configuration | display set`
- Equivalent sanitized display-set text where active configuration appears as one `set ...` statement per line

Explicitly unsupported in this MVP:

- brace-style Junos configuration such as `system { services { ssh; } }`
- XML configuration
- JSON configuration
- complete `groups`, `apply-groups`, and inheritance expansion
- direct device connection or live collection

Brace-style input is not parsed as if it were complete evidence. It is reported as `needs_display_set` and each Network item remains `MANUAL_REQUIRED`.

## Network Output

The Network profile continues to emit all `N-01` to `N-38` items. The Junos display-set smoke result currently produces:

- `GOOD`: 14
- `MANUAL_REQUIRED`: 24
- `VULNERABLE`: 0 for the sanitized good fixture

This distribution is expected for the MVP because missing Junos lines and default-dependent settings are not treated as safe by default.

## Output Files

Default classification still creates:

- `evidence.jsonl`
- `results.json`
- `detail.xlsx`
- `summary.xlsx`
- `report.md`
- `security_advisory.md`
- `security_advisory.xlsx`

`--no-advisory` continues to create only the first five files.

## Validation

Validation completed before this draft was written:

- full `python -m pytest`: `166 passed`
- release readiness tests: `9 passed`
- Junos fixture smoke: 38 results and seven output files
- Junos good fixture status distribution: `GOOD 14`, `MANUAL_REQUIRED 24`
- root and packaged Network rulepack resources: synchronized
- high-confidence secret pattern scan: no hits

Run the current validation gate in `docs/V1_2_0_READINESS.md` before any `v1.2.0` tag or private GitHub Release is considered.

## Security Notes

- Fixtures must stay synthetic and sanitized.
- Do not include real customer configuration exports, live output, raw configs, `.env`, `out/`, `raw/`, `tmp/`, `dist/`, commercial device images, CML images, Junos images, VM disks, or license files in source control or release assets.
- Do not include hostnames, IP addresses, usernames, SNMP communities, serial numbers, domains, config paths, banner text, keys, tokens, password hashes, or passwords in fixtures.
- GNS3, CML, Containerlab, approved lab, and actual device output must be sanitized before it can become a fixture.
- PyPI and TestPyPI publishing remain deferred.
- Public repository conversion remains out of scope.

## Known Limitations

- Junos support is display-set parsing, not a complete Junos configuration interpreter.
- Junos configuration groups and inheritance are not expanded.
- XML, JSON, and brace-style Junos configuration parsing remain future work.
- Direct device access, NETCONF, and live collection are out of scope.
- Many official Network items still require assessor review and remain `MANUAL_REQUIRED`.

## Upgrade Notes

No migration is expected for existing offline evidence flows. Existing Cisco IOS commands and output bundles remain compatible with `v1.1.0`.

## Next Steps

- Keep `v1.2.0` untagged until release readiness, package version update, build, checksum, installed-wheel smoke, and explicit release approval are complete.
- Compare sanitized real Junos display-set output from approved labs against the synthetic fixture.
- Consider inheritance-aware Junos fixture expansion only as a later scoped task.
