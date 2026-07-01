# Changelog

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
