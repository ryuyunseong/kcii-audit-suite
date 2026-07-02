# v1.4.0 Baseline Product Completion

`kcii-audit-suite v1.4.0` is the baseline product completion point for the private offline assessment-helper workflow.

This does not mean every registered item is fully automated. It means the core product flow is complete enough to use as the maintained baseline: registered evidence is classified offline, all supported profiles emit consistent outputs, deterministic evidence is judged conservatively, and insufficient evidence remains `MANUAL_REQUIRED`.

## Fixed Baseline

- Baseline release: `v1.4.0`
- Tag target: `178369b`
- Distribution: private GitHub Release
- Repository visibility: private
- Rulepack baseline: `kcii-2025-12`
- Public repository conversion: not performed
- PyPI/TestPyPI publishing: not performed

Do not move the `v1.4.0` tag or replace its release assets. Any later correction must use a new patch or minor version.

## Supported Profiles

The baseline supports the following offline profiles:

- Windows Server
- Linux Server
- Unix Server
- DBMS PostgreSQL, MySQL, and MariaDB
- Network Cisco IOS and Juniper Junos
- Security Appliance questionnaire and sanitized summary evidence

Operational evidence is collected outside this tool by the responsible system owner or assessor, then moved to a Windows work PC for `classify-file` or `classify-paste`.

## Output Contract

Default classification creates seven files:

- `evidence.jsonl`
- `results.json`
- `detail.xlsx`
- `summary.xlsx`
- `report.md`
- `security_advisory.md`
- `security_advisory.xlsx`

The `--no-advisory` option creates only the first five files.

## Judgment Boundary

- All registered items for the supported profile should appear in output.
- Deterministic good evidence may produce `GOOD`.
- Deterministic vulnerable evidence may produce `VULNERABLE`.
- Missing, ambiguous, policy-dependent, unsupported, permission-denied, or inheritance-conflicted evidence must remain `MANUAL_REQUIRED`.
- `MANUAL_REQUIRED` is a valid assessment state, not a runtime failure.

This tool is not an official KISA tool and does not replace assessor judgment, customer policy review, or compensating-control review.

## Security Boundary

The baseline must not store or publish:

- real customer evidence
- raw live output
- unsanitized device configuration
- `.env` files or local secrets
- passwords, password hashes, tokens, keys, or certificate bodies
- hostnames, domains, account names, internal URLs, IP addresses, serial numbers, or license material
- commercial device images, VM images, CML images, IOS images, Junos images, or appliance images

Fixtures and examples must remain synthetic and sanitized.

## Maintenance Split

- `dev/v1.4.1`: documentation fixes and narrow bug fixes only
- `dev/v1.5.0`: new compatible features, such as broader Junos inheritance automation or brace-style normalization
- `release/public-readiness`: licensing, responsibility, sample-data, and disclosure review before any public repository conversion

Feature work must not be added to the fixed `v1.4.0` release asset set.
