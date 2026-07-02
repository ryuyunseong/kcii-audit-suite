# kcii-audit-suite v1.1.0 Draft

`kcii-audit-suite v1.1.0` is currently a draft for the `dev/v1.1.0` development branch. No `v1.1.0` tag or GitHub Release has been created yet.

The baseline final release remains `v1.0.0`, fixed at commit `31983bd`. The `v1.0.0rc1` and `v1.0.0rc2` tags also remain fixed and must not be moved.

## Summary

This draft documents the v1.1.0 Network profile improvements completed after `v1.0.0`:

- Cisco IOS automatic judgment coverage expands from 9 items to 27 items.
- Network `N-01` to `N-38` full result emission is preserved.
- Realistic sanitized Cisco IOS command output compatibility is improved.
- Default seven-file output generation remains unchanged.
- Ambiguous or policy-dependent checks still return `MANUAL_REQUIRED`.

## Changes Since v1.0.0

- Added deterministic Cisco IOS evidence checks for additional hardening indicators such as timestamp logging, SNMP ACL and read-only authorization, TFTP, TCP keepalives, HTTP/HTTPS management service, small services, Bootp, CDP, directed-broadcast, source-route, proxy ARP, ICMP control messages, identd, domain lookup, pad, and mask-reply.
- Added realistic sanitized Cisco IOS fixture coverage for common `show run`, `show startup-config`, multi-`line vty`, logging, NTP, SNMP, and service-hardening output variants.
- Added network output sanitization guidance for GNS3, CML, approved lab, and actual device output before it can become a fixture.

## Network Cisco IOS Improvements

The Network profile continues to register all `N-01` to `N-38` items. Cisco IOS automation now covers 27 deterministic checks. The remaining 11 items stay manual because they require password-complexity policy, AAA lockout policy, user privilege design, auxiliary port review, patch baseline review, logging policy completeness, SNMP necessity review, anti-spoofing design, DDoS controls, or inventory context for unused interfaces.

The parser keeps raw command output out of normal outputs. It stores only normalized evidence summaries and `raw_evidence_hash`.

## kcii-netlab-sim And Realistic Fixture Compatibility

`kcii-netlab-sim` remains a command-response simulator for parser and rulepack testing. It is not a Packet Tracer, GNS3, CML, routing, or packet-forwarding emulator.

For GNS3, CML, or approved lab output, only sanitized fixtures are allowed in the repository. Real customer configs, live output, commercial IOS or CML images, VM disks, and license files remain excluded.

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

Latest `dev/v1.1.0` validation for this draft:

- targeted Network tests: `13 passed`
- full `python -m pytest`: `161 passed`
- realistic Cisco IOS fixture smoke: 38 results and seven output files
- realistic fixture status distribution: `GOOD 27`, `MANUAL_REQUIRED 11`
- sensitive placeholder search over text and Excel outputs: no hits

Before any `v1.1.0` tag or private GitHub Release is created, rerun the readiness checks in `docs/V1_1_0_READINESS.md`.

## Security Notes

- Do not include real customer configuration exports, live output, raw configs, `.env`, `out/`, `raw/`, `tmp/`, `dist/`, commercial device images, CML images, IOS images, VM disks, or license files in source control or release assets.
- Do not include hostnames, IP addresses, usernames, SNMP communities, serial numbers, domains, config paths, banner text, keys, tokens, password hashes, or passwords in fixtures.
- GNS3, CML, and actual device output must be sanitized before use as test fixtures.
- PyPI and TestPyPI publishing remain deferred.
- Public repository conversion remains out of scope.

## Known Limitations

- v1.1.0 is not tagged or released yet.
- Cisco IOS coverage is still deterministic command-output parsing, not full network emulation.
- Many official items remain `MANUAL_REQUIRED` by design.
- Juniper, FortiGate, FRR, and other vendor parsers remain future work.
- Automatic judgment does not replace assessor review, customer policy, or compensating-control review.

## Upgrade Notes

No migration is expected for existing offline evidence flows. The CLI commands and output bundle remain compatible with `v1.0.0`.

When preparing a release candidate, update the package version to `1.1.0`, rebuild wheel and source distributions, regenerate checksums, and validate installed-wheel behavior before creating an annotated tag.

## Next Steps

- Prepare a `v1.1.0` readiness pass.
- Update package version only after release approval.
- Create an annotated `v1.1.0` tag only after explicit approval.
- Create a private GitHub Release only after the tag and release assets are verified.
