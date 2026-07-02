# kcii-audit-suite v1.4.0 Draft

`kcii-audit-suite v1.4.0` is a development release candidate draft for the `dev/v1.4.0` branch. No `v1.4.0` tag or GitHub Release has been created.

The latest fixed final release remains `v1.3.0`, fixed at commit `30490b4`. The `v1.2.0`, `v1.1.0`, `v1.0.0`, `v1.0.0rc2`, and `v1.0.0rc1` tags also remain fixed and must not be moved.

## Summary

This draft records the Junos display-inheritance parser skeleton completed after `v1.3.0`:

- Junos display-set parsing continues to emit all Network `N-01` to `N-38` items.
- Synthetic display-inheritance fixtures cover clear inherited evidence, conflicting inherited values, and incomplete source context.
- The parser distinguishes display-set, display-inheritance, and combined display-set plus display-inheritance input.
- Clear inherited evidence is mapped only to limited partial evidence fields.
- Conflicting or incomplete inheritance remains `MANUAL_REQUIRED`.
- Source group names, hostnames, IP addresses, usernames, communities, serials, keys, tokens, and license text are not stored in normal output evidence.

## Changes Since v1.3.0

- Added four synthetic Junos inheritance fixtures under `tests/fixtures/network/junos/inheritance/`.
- Added a conservative display-inheritance parser skeleton for sanitized fixture lines.
- Added inheritance evidence fields such as `inheritance_required`, `inheritance_available`, `inheritance_conflict`, `inheritance_incomplete`, `inheritance_source_count`, and `automation_scope`.
- Added tests for apply-groups without inheritance context, clear inherited evidence, combined evidence, and conflict or incomplete inheritance.
- Updated Network profile documentation to describe the limited inheritance skeleton.

## Supported v1.4.0 Draft Scope

Supported input for this draft:

- sanitized `show configuration | display set`
- sanitized `show configuration | display inheritance`
- combined display-set and display-inheritance text
- synthetic `effective-statement` inheritance lines used by the fixture contract

Clear inherited evidence may be used only for a narrow set of fields, including SSH/Telnet safety, remote syslog presence, NTP presence, and SNMP read-only authorization.

## Known Limitations

- This is not a complete Junos inheritance interpreter.
- Brace-style, XML, JSON, NETCONF, and full Junos configuration tree parsing remain out of scope.
- `apply-groups-except`, omitted source context, inactive inheritance, and conflicting inherited values remain manual-review cases.
- The current skeleton is validated against synthetic fixtures, not raw customer exports or unsanitized live output.
- Many official Network items still require assessor review and remain `MANUAL_REQUIRED`.

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

Validation completed for the current draft implementation:

- targeted Junos and Network vendor tests: passed
- release readiness tests: passed
- full `python -m pytest`: `176 passed`
- Junos inheritance smoke: seven output files generated
- Junos inheritance smoke distribution: `GOOD 4`, `MANUAL_REQUIRED 34`
- high-confidence secret pattern scan: no hits
- forbidden path scan: no hits
- `git diff --check`: no whitespace errors; Windows LF to CRLF warnings may appear
- `v1.3.0` tag remained fixed at `30490b4`
- `v1.4.0` tag: not created

## Security Notes

- Fixtures must stay synthetic and sanitized.
- Do not include real customer configuration exports, raw live output, `.env`, `out/`, `raw/`, `tmp/`, `dist/`, commercial device images, CML images, Junos images, VM disks, or license files in source control or release assets.
- Do not include hostnames, IP addresses, usernames, SNMP communities, serial numbers, domains, config paths, banner text, keys, tokens, password hashes, or passwords in fixtures.
- Public repository conversion, PyPI publishing, and TestPyPI publishing remain out of scope.

## Next Steps

- Update package version metadata to `1.4.0` only after release smoke is approved.
- Re-run full profile smoke, build, checksum generation, and installed-wheel validation before creating a tag.
- Create `v1.4.0` annotated tag and private GitHub Release only after separate approval.
