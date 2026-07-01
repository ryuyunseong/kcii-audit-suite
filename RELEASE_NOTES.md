# Release Notes

## v1.0.0-rc2 Candidate

This private release-candidate draft keeps the offline assessment-helper boundary from rc1 and adds the scoped rc2 hardening work completed on `dev/v1.0.0rc2`.

### Scope

- Windows Server `W-01` to `W-64` remains fully registered, with expanded deterministic and partial judgment for selected read-only evidence summaries.
- DBMS `D-01` to `D-26` remains fully registered, with PostgreSQL, MySQL, and MariaDB sanitized JSON/key-value offline parser coverage.
- Linux, Unix, Network, and Security Appliance profiles retain the rc1 scope.
- Default classification still creates the seven-file output bundle.

### Validation Gate

Before creating a `v1.0.0rc2` tag or GitHub pre-release, run:

- full `python -m pytest`
- rc2 smoke commands from `docs/V1_0_0RC2_READINESS.md`
- sensitive-value search over generated outputs
- wheel/sdist build and checksum generation

### Known Limits

- `MANUAL_REQUIRED` remains expected for many registered items.
- DBMS support remains PostgreSQL, MySQL, and MariaDB only.
- PyPI and TestPyPI publishing remain deferred.
- `v1.0.0rc1` is fixed at `e93d18b` and must not be moved.

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
