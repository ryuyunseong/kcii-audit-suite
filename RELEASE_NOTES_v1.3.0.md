# kcii-audit-suite v1.3.0

`kcii-audit-suite v1.3.0` is the final private GitHub Release for the `dev/v1.3.0` branch. The release tag is `v1.3.0` and points to commit `30490b4`.

The latest fixed final release remains `v1.2.0`, fixed at commit `9296245`. The `v1.1.0`, `v1.0.0`, `v1.0.0rc2`, and `v1.0.0rc1` tags also remain fixed and must not be moved.

## Summary

This release documents the Junos realistic display-set compatibility work completed after `v1.2.0`:

- Junos display-set support continues to build on the `v1.2.0` parser MVP.
- A sanitized realistic Junos display-set fixture was added.
- Parser normalization now handles prompt lines, blank lines, spacing variants, inactive or deactivated statements, `apply-groups` evidence, and unsupported XML/JSON inputs more conservatively.
- Package version metadata is prepared as `1.3.0` for release smoke, build, checksum, and installed-wheel validation.
- Cisco IOS and Junos common Network regression coverage continues to verify full `N-01` to `N-38` result emission.
- `apply-groups` and inheritance-dependent evidence remains `MANUAL_REQUIRED` or partial evidence until a separate inheritance-expansion task is approved.

## Changes Since v1.2.0

- Added `tests/fixtures/network/junos/realistic/display_set_realistic_sanitized.txt` as a synthetic sanitized fixture for realistic display-set output shape.
- Updated the Junos parser to strip CLI prompt prefixes before evaluating `set ...` lines.
- Kept inactive and deactivated Junos statements out of deterministic good evidence.
- Added evidence markers for unexpanded inheritance when `apply-groups` appears.
- Failed closed for XML and JSON Junos config input by preserving `MANUAL_REQUIRED` behavior instead of treating missing lines as safe.
- Extended Network vendor regression tests for Cisco IOS and Junos.
- Updated Network profile and realistic-lab documentation for Junos sanitization and inheritance limits.

## Junos Realistic Display-Set Scope

Supported input remains:

- `show configuration | display set`
- Equivalent sanitized display-set text where active configuration appears as `set ...` statements
- Prompt-prefixed display-set output where command echoes or shell prompts appear before valid `set ...` lines

Explicitly unsupported or manual-review input remains:

- brace-style Junos configuration
- XML configuration
- JSON configuration
- complete `groups`, `apply-groups`, and inheritance expansion
- direct device connection, NETCONF, SSH collection, or live collection

Unsupported formats must not be treated as safe. They must continue to emit all Network items and keep ambiguous results as `MANUAL_REQUIRED`.

## Network Output

The Network profile continues to emit all `N-01` to `N-38` items. The Junos realistic display-set smoke result currently produces:

- `GOOD`: 14
- `MANUAL_REQUIRED`: 24
- `VULNERABLE`: 0

This distribution is expected for `v1.3.0` because default-dependent, policy-dependent, unsupported, and inheritance-dependent evidence is not treated as safe by default.

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

Validation completed before this release was created:

- targeted Network tests: `11 passed`
- release readiness tests: `9 passed`
- full `python -m pytest`: `171 passed`
- Junos realistic fixture smoke: 38 results and seven output files
- Junos realistic fixture status distribution: `GOOD 14`, `MANUAL_REQUIRED 24`
- high-confidence secret pattern scan: no hits
- forbidden staged path scan: no hits
- generated output placeholder scan for the Junos realistic smoke: no hits
- `git diff --check`: no whitespace errors after fixture cleanup
- build: wheel and source distribution generated successfully for `1.3.0`
- release checksum file: `SHA256SUMS.txt` generated for wheel and source distribution
- installed-wheel smoke from a clean non-repository working directory: OK
- `v1.2.0` tag remained fixed at `9296245`

The `docs/V1_3_0_READINESS.md` checklist records the validation gate used before the `v1.3.0` tag and private GitHub Release were created.

## Security Notes

- Fixtures must stay synthetic and sanitized.
- Do not include real customer configuration exports, raw live output, `.env`, `out/`, `raw/`, `tmp/`, `dist/`, commercial device images, CML images, Junos images, VM disks, or license files in source control or release assets.
- Do not include hostnames, IP addresses, usernames, SNMP communities, serial numbers, domains, config paths, banner text, keys, tokens, password hashes, or passwords in fixtures.
- GNS3, CML, Containerlab, approved lab, and actual device output must be sanitized before it can become a fixture.
- PyPI and TestPyPI publishing remain deferred.
- Public repository conversion remains out of scope.

## Known Limitations

- Junos support is still display-set parsing, not a complete Junos configuration interpreter.
- Junos configuration groups and inheritance are not expanded.
- XML, JSON, and brace-style Junos configuration parsing remain future work.
- Direct device access, NETCONF, and live collection are out of scope.
- Many official Network items still require assessor review and remain `MANUAL_REQUIRED`.

## Upgrade Notes

No migration is expected for existing offline evidence flows. Existing Cisco IOS and Junos display-set evidence flows remain compatible with `v1.2.0`.

## Next Steps

- Do not move the `v1.3.0` tag or replace release assets.
- Treat `display inheritance`, brace-style parsing, XML/JSON parsing, and broader Junos semantics as later scoped work.
