# kcii-audit-suite v1.4.0

`kcii-audit-suite v1.4.0` is the final private GitHub Release for the current baseline offline workflow. It is fixed at commit `178369b`.

The `v1.4.0`, `v1.3.0`, `v1.2.0`, `v1.1.0`, `v1.0.0`, `v1.0.0rc2`, and `v1.0.0rc1` tags are fixed and must not be moved.

## Summary

This release records the Junos display-inheritance parser skeleton completed after `v1.3.0` and marks the private baseline product completion point:

- Junos display-set parsing continues to emit all Network `N-01` to `N-38` items.
- Synthetic display-inheritance fixtures cover clear inherited evidence, conflicting inherited values, and incomplete source context.
- The parser distinguishes display-set, display-inheritance, and combined display-set plus display-inheritance input.
- Clear inherited evidence is mapped only to limited partial evidence fields.
- Conflicting or incomplete inheritance remains `MANUAL_REQUIRED`.
- Source group names, hostnames, IP addresses, usernames, communities, serials, keys, tokens, and license text are not stored in normal output evidence.
- Package version metadata is prepared as `1.4.0`.
- The private offline workflow is treated as baseline-complete for maintenance planning.

## Changes Since v1.3.0

- Added four synthetic Junos inheritance fixtures under `tests/fixtures/network/junos/inheritance/`.
- Added a conservative display-inheritance parser skeleton for sanitized fixture lines.
- Added inheritance evidence fields such as `inheritance_required`, `inheritance_available`, `inheritance_conflict`, `inheritance_incomplete`, `inheritance_source_count`, and `automation_scope`.
- Added tests for apply-groups without inheritance context, clear inherited evidence, combined evidence, and conflict or incomplete inheritance.
- Updated Network profile documentation to describe the limited inheritance skeleton.

## Supported v1.4.0 Scope

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

Validation completed for the release implementation:

- targeted Junos and Network vendor tests: passed
- release readiness tests: passed
- full `python -m pytest`: `176 passed`
- full profile smoke: passed
- Junos inheritance smoke: seven output files generated
- Junos inheritance smoke distribution: `GOOD 4`, `MANUAL_REQUIRED 34`
- build: wheel and source distribution generated successfully for `1.4.0`
- release checksum file: `SHA256SUMS.txt` generated for wheel and source distribution
- installed-wheel smoke from a clean non-repository working directory: OK
- high-confidence secret pattern scan: no hits
- forbidden path scan: no hits
- `git diff --check`: no whitespace errors; Windows LF to CRLF warnings may appear
- `v1.3.0` tag remained fixed at `30490b4`
- `v1.4.0` tag fixed at `178369b`
- private GitHub Release created as a final release, not a pre-release

## Security Notes

- Fixtures must stay synthetic and sanitized.
- Do not include real customer configuration exports, raw live output, `.env`, `out/`, `raw/`, `tmp/`, `dist/`, commercial device images, CML images, Junos images, VM disks, or license files in source control or release assets.
- Do not include hostnames, IP addresses, usernames, SNMP communities, serial numbers, domains, config paths, banner text, keys, tokens, password hashes, or passwords in fixtures.
- Public repository conversion, PyPI publishing, and TestPyPI publishing remain out of scope.

## Maintenance Split

- Patch-only fixes should use `dev/v1.4.1`.
- New compatible feature work should use `dev/v1.5.0` or later.
- Public repository conversion requires separate approval and review.
