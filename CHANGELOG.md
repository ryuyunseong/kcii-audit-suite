# Changelog

## [1.1.0] - Unreleased

### Added

- Draft `RELEASE_NOTES_v1.1.0.md` for the `dev/v1.1.0` development branch.
- Draft `docs/V1_1_0_READINESS.md` checklist for v1.1.0 validation before tag or release creation.
- Network output sanitization guidance for Cisco IOS, GNS3, CML, approved lab, and actual device output fixtures.
- Sanitized realistic Cisco IOS fixture coverage and release-readiness documentation references.

### Changed

- Cisco IOS Network automatic judgment coverage is documented as 27 items while preserving `N-01` to `N-38` full result emission.
- Release notes now distinguish the fixed `v1.0.0` release from the unreleased `dev/v1.1.0` development branch.
- Package version metadata is prepared as `1.1.0` for release smoke, build, checksum, and installed-wheel validation.

### Security

- v1.1.0 draft documentation keeps real customer configs, live output, IOS/CML images, commercial device images, license files, and PyPI/TestPyPI publishing out of scope.

### Known Limitations

- `v1.1.0` has not been tagged or released.
- Package version metadata is `1.1.0`, but tag creation and private GitHub Release publication still require separate approval.
- Policy-dependent Network items remain `MANUAL_REQUIRED`.

## [1.0.0] - 2026-07-02

### Added

- `RELEASE_NOTES_v1.0.0.md` final-candidate release notes.
- `docs/V1_0_0_READINESS.md` final release readiness checklist.

### Changed

- Package version moved to `1.0.0` on `release/v1.0.0`.
- Release documentation now separates fixed rc2 artifacts from final v1.0.0 stabilization.
- Release checklist commands now include v1.0.0 build artifacts, checksums, tag, and private GitHub Release preparation.

### Security

- v1.0.0 release notes keep production remote collection, PyPI/TestPyPI publishing, public repository conversion, and real customer evidence out of scope.

### Known Limitations

- No feature scope is added after v1.0.0rc2.
- Many registered items remain intentionally manual or partially automated.

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
