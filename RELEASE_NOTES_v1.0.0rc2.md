# kcii-audit-suite v1.0.0rc2

`kcii-audit-suite v1.0.0rc2` is a private release-candidate draft for offline evidence classification and reporting. It is not an official KISA tool, does not perform production remote collection, and does not replace assessor judgment.

The `v1.0.0rc1` tag remains fixed at `e93d18b`. rc2 work is based on `dev/v1.0.0rc2`.

## Summary

This candidate keeps the `kcii-2025-12` rulepack baseline and narrows rc2 scope to verified Windows Server and DBMS improvements:

- Windows Server automatic and partial judgment expansion.
- DBMS PostgreSQL, MySQL, and MariaDB offline parser input handling hardening.
- Stable seven-file output bundle across supported profiles.
- Conservative `MANUAL_REQUIRED` handling for unsupported or ambiguous evidence.

## Changes Since v1.0.0rc1

- Windows Server classification now handles additional read-only summary evidence for password policy, administrative shares, selected risky services, audit policy, and Event Log settings.
- DBMS classification now accepts sanitized JSON and key/value evidence for PostgreSQL, MySQL, and MariaDB.
- DBMS permission-denied and unsupported output paths are treated as `MANUAL_REQUIRED` instead of runtime failures.
- DBMS fixture coverage now includes JSON good/vulnerable samples and common permission-denied/unsupported samples.
- Release readiness tests now expect package version `1.0.0rc2`.

## Windows Server Changes

- Added deterministic or partial checks for selected W-series items where sanitized evidence is sufficient.
- Uses `secedit /export` and `auditpol /get` only as read-only evidence sources.
- Does not store raw `secedit` or `auditpol` output in normal reports, workbooks, or advisory files.
- Keeps W-01 to W-64 output coverage intact.

## DBMS Changes

- Supports PostgreSQL, MySQL, and MariaDB offline evidence classification through `--profile dbms --dbms <type>`.
- Accepts sanitized JSON and key/value summary outputs.
- Stores only booleans, integers, enums, counts, manual-check state, and `raw_evidence_hash`.
- Ignores account lists, database lists, connection strings, password hashes, and raw log text.
- Treats permission-denied and unsupported outputs as manual-review evidence.

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

## Validation

The rc2 release gate should include:

- `python -m pytest`
- profile `classify-file` smoke checks
- at least one `classify-paste` smoke check per applicable profile family
- seven-file output bundle checks
- `--no-advisory` smoke check
- sensitive-value search over generated outputs
- package build and checksum generation

The current local rc2 preparation validated `159 passed` before release-note work started.

## Security Notes

- Do not commit real customer evidence, live output, raw DBMS output, appliance config exports, `.env`, `out/`, `raw/`, `tmp/`, or `dist/`.
- Do not include account names, database names, connection strings, passwords, password hashes, tokens, keys, certificate bodies, internal URLs, hostnames, serial numbers, policy names, object names, or IP addresses in samples or release assets.
- Docker, DBMS Docker Compose, Containerlab, GNS3, EVE-NG, and simulator flows are development and verification aids only.
- Operational use remains offline: the owner or assessor runs approved read-only commands or SQL on the target and moves sanitized results to the Windows work PC.

## Known Limitations

- Many registered items intentionally remain `MANUAL_REQUIRED`.
- Oracle, MSSQL, Tibero, Altibase, and Cubrid DBMS parsers are not implemented.
- Security Appliance vendor-specific config parsers remain future work beyond the questionnaire-centered flow.
- Network automation remains Cisco IOS MVP.
- PyPI and TestPyPI publishing are deferred.

## Upgrade Notes

- Existing rc1 users should treat rc2 as a private pre-release candidate, not a final release.
- The `v1.0.0rc1` tag must not be moved.
- Create `v1.0.0rc2` only after the final smoke, package build, checksum, and release asset checks pass.

## Next Steps

- Run the rc2 smoke checklist in `docs/V1_0_0RC2_READINESS.md`.
- Build wheel and sdist for version `1.0.0rc2`.
- Generate `dist/SHA256SUMS.txt`.
- After explicit approval, create the annotated `v1.0.0rc2` tag and private GitHub pre-release.
