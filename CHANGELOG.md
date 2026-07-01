# Changelog

## [1.0.0-rc2] - 2026-07-02

### Added

- Windows Server rc2 automatic and partial judgment expansion for selected read-only evidence summaries.
- DBMS sanitized JSON fixture coverage for PostgreSQL, MySQL, and MariaDB.
- DBMS permission-denied and unsupported-output fixtures.
- `RELEASE_NOTES_v1.0.0rc2.md` and `docs/V1_0_0RC2_READINESS.md`.

### Changed

- Package version moved to `1.0.0rc2` for rc2 build verification.
- DBMS parser now preserves permission-denied and insufficient-privilege states as `MANUAL_REQUIRED` evidence.
- Release readiness documentation now describes rc2 smoke, checksum, and tag boundaries.

### Security

- DBMS JSON fixture tests verify that account names, database names, connection strings, IP-like placeholders, and password-hash placeholders are not written to normal outputs.
- rc2 release notes keep production remote collection, PyPI publishing, and public release out of scope.

### Known Limitations

- rc2 is still a private pre-release candidate.
- Oracle, MSSQL, Tibero, Altibase, and Cubrid DBMS support remains future work.
- Many registered items remain intentionally manual.

## [1.0.0-rc1] - 2026-07-01

### Added

- Full registered item manifests for Windows Server, Unix Server, DBMS, Network, and Security Appliance profiles.
- Linux Server MVP rulepack and parser flow.
- Offline `classify-file` and `classify-paste` flows for all implemented profiles.
- Security Appliance questionnaire Excel export/import.
- Seven-file output bundle with detail, summary, report, and security advisory artifacts.
- Docker DBMS lab documentation and live verification flow.
- Network Cisco IOS simulator/parser MVP.
- Release readiness documents:
  - `RELEASE_NOTES.md`
  - `docs/RELEASE_CHECKLIST.md`
  - `docs/PROFILE_COVERAGE.md`

### Changed

- CLI help now explicitly describes the tool as offline and non-official.
- README was rewritten for release-candidate use, operating model, smoke commands, and security rules.
- `.gitignore` now excludes `raw/` and `tmp/` in addition to generated outputs and local environment files.
- Package version was moved to `1.0.0rc1` for a release-candidate build.

### Security

- Fixtures and parser tests enforce synthetic evidence and prevent sensitive placeholder leakage into generated reports/advisories.
- Raw evidence text is not stored in normal output artifacts; normalized summaries and `raw_evidence_hash` are used instead.

### Known Limitations

- `MANUAL_REQUIRED` remains expected for many items.
- Security Appliance vendor parsers require later FortiGate, PAN-OS, Cisco ASA, and F5 config-specific expansion.
- The local release candidate is tagged as `v1.0.0rc1`, but remote push, GitHub Release creation, and PyPI publishing are deferred.
