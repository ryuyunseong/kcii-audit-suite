# kcii-audit-suite v1.0.0

`kcii-audit-suite v1.0.0` is the first final-candidate release for the offline K-CII vulnerability assessment helper. It is not an official KISA tool, not a production remote collector, and not a replacement for assessor judgment.

This release is prepared from the `v1.0.0rc2` baseline. The `v1.0.0rc1` tag remains fixed at `e93d18b`, and the `v1.0.0rc2` tag remains fixed at `59d3d38`.

## Summary

The v1.0.0 release branch stops feature work and focuses on release stabilization:

- preserves Windows Server, Unix Server, DBMS, Network, and Security Appliance full item registration
- preserves Linux Server MVP coverage
- preserves the seven-file output bundle
- documents known limitations and manual-review boundaries
- keeps operational use offline and read-only

## Included Profile Scope

- Windows Server: `W-01` to `W-64`, with selected deterministic and partial judgment
- Linux Server: `L-01` to `L-08` MVP
- Unix Server: `U-01` to `U-67`, fixture-based AIX, Solaris, HP-UX, and Linux-compatible parser support
- DBMS: `D-01` to `D-26`, PostgreSQL, MySQL, and MariaDB offline parser support
- Network: `N-01` to `N-38`, Cisco IOS simulator/parser MVP
- Security Appliance: `S-01` to `S-23`, questionnaire-centered evidence flow

## Changes Since v1.0.0rc2

- Package version is set to `1.0.0`.
- Final release notes and readiness checklist are added.
- Release checklist commands are updated for v1.0.0 wheel, source distribution, checksum, tag, and private GitHub Release preparation.
- No new functional scope is added after rc2.

## Output Files

Default classification creates:

- `evidence.jsonl`
- `results.json`
- `detail.xlsx`
- `summary.xlsx`
- `report.md`
- `security_advisory.md`
- `security_advisory.xlsx`

`--no-advisory` creates only the first five output files.

## Security Notes

- Do not include real customer evidence, live output, raw DBMS output, appliance config exports, `.env`, `out/`, `raw/`, `tmp/`, or `dist/` in source control.
- Do not include account names, database names, connection strings, passwords, password hashes, tokens, keys, certificate bodies, internal URLs, hostnames, serial numbers, policy names, object names, IP addresses, or license files in samples or release assets.
- Docker, DBMS Docker Compose, Containerlab, GNS3, EVE-NG, and simulator flows are development and verification aids only.
- Operational use remains offline: the owner or assessor runs approved read-only commands or SQL on the target and moves sanitized results to the Windows work PC.

## Known Limitations

- Many registered items intentionally remain `MANUAL_REQUIRED`.
- Automatic judgment is conservative and does not replace customer policy or compensating-control review.
- Oracle, MSSQL, Tibero, Altibase, and Cubrid DBMS parsers are not implemented.
- Security Appliance vendor-specific config parsers remain future work beyond the questionnaire-centered flow.
- Network automation remains Cisco IOS MVP.
- PyPI and TestPyPI publishing are deferred.

## Release Gate

Before creating a `v1.0.0` tag or private GitHub Release:

- run `python -m pytest`
- run smoke commands in `docs/V1_0_0_READINESS.md`
- verify generated outputs do not contain synthetic sensitive fixture values
- build wheel and source distribution
- generate `dist/SHA256SUMS.txt`
- install the wheel in a clean environment and run CLI smoke checks

## Next Steps

- Create `v1.0.0` annotated tag only after explicit approval.
- Create a private GitHub Release only after tag approval.
- Continue future feature work on a separate branch such as `dev/v1.0.1`, `dev/v1.1.0`, or a scoped feature branch.
