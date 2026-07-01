# Release Notes

## v1.0.0-rc1 Candidate

This release candidate freezes the current scope as an offline assessment helper. It is not an official KISA tool, not a production remote collector, and not a fully automated diagnostic product.

### Scope

- Windows Server `W-01` to `W-64` registered with partial automatic judgment.
- Linux Server `L-01` to `L-08` MVP checks.
- Unix Server `U-01` to `U-67` registered with AIX, Solaris, HP-UX, and Linux fixture-based parser support.
- DBMS `D-01` to `D-26` registered with PostgreSQL, MySQL, and MariaDB offline parser support and Docker live SQL verification.
- Network `N-01` to `N-38` registered with Cisco IOS simulator/parser MVP.
- Security Appliance `S-01` to `S-23` registered with questionnaire Excel export/import and sanitized summary parser support.
- Seven-file output bundle generation:
  - `evidence.jsonl`
  - `results.json`
  - `detail.xlsx`
  - `summary.xlsx`
  - `report.md`
  - `security_advisory.md`
  - `security_advisory.xlsx`

### Validation Gate

Release candidate validation must include:

- Clean virtual environment install.
- `kcii-audit --help`, `classify-file --help`, and `questionnaire --help` smoke checks.
- Profile smoke checks for Windows, Linux, Unix, DBMS, Network, and Security Appliance.
- `--no-advisory` smoke check.
- Full `python -m pytest`.
- Sensitive-content search over generated outputs.

### Known Limits

- Many official items intentionally return `MANUAL_REQUIRED`.
- Vendor-specific security appliance config parsers are MVP wrappers around sanitized summaries.
- Windows, Network, DBMS, and Unix automatic judgment coverage is intentionally conservative.
- The private GitHub pre-release is fixed at commit `e93d18b` with annotated tag `v1.0.0rc1`.
- Further work should continue on `dev/v1.0.0rc2`; do not move the `v1.0.0rc1` tag.
- PyPI publishing is intentionally deferred.

### Security Notes

Do not include real customer evidence, raw configs, `.env`, generated `out/`, raw vault files, passwords, hashes, tokens, keys, certificate bodies, internal URLs, hostnames, account names, serial numbers, policy names, object names, or IP addresses in source control.
