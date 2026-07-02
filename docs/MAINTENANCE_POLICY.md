# Maintenance Policy

This policy applies after the private `v1.4.0` baseline product completion release.

## Version Branching

- Patch versions such as `v1.4.1` are for documentation corrections, test fixes, and narrow bug fixes that do not add product scope.
- Minor versions such as `v1.5.0` are for backward-compatible feature additions.
- Major versions are reserved for incompatible output, CLI, rulepack, or operating-model changes.

Keep patch and feature work separate. Do not combine parser expansion, raw evidence retention, public-release preparation, and unrelated documentation cleanup in one change.

## Release Immutability

Published release tags and assets are immutable for this project.

Do not move or replace:

- `v1.4.0`
- `v1.3.0`
- `v1.2.0`
- `v1.1.0`
- `v1.0.0`
- `v1.0.0rc2`
- `v1.0.0rc1`

If a published release needs correction, create a new tag and release.

## Prohibited Repository Content

Do not commit or attach:

- `out/`, `raw/`, `tmp/`, or `dist/`
- `.env` or local secret files
- real customer evidence
- live output before sanitization
- commercial device configuration exports
- device images, VM disks, CML images, IOS images, Junos images, or appliance images
- license files
- credentials, tokens, keys, password hashes, certificates, or private URLs

Only synthetic fixtures and sanitized documentation examples are allowed.

## Required Release Validation

Before any future release tag is created, run and record:

- targeted tests for the changed area
- full `python -m pytest`
- profile smoke for affected profiles
- seven-output file verification for default classification
- `--no-advisory` output verification when relevant
- sensitive placeholder and high-confidence secret scans
- `python -m build`
- wheel and source distribution checksum generation
- clean installed-wheel smoke from outside the repository
- `git diff --check`
- tag immutability checks for existing releases

Release assets should remain limited to the wheel, source distribution, and checksum file unless a separate approval explicitly changes the release packaging policy.

## Public Readiness Review

Public repository conversion requires a separate review. At minimum, check:

- license selection and third-party notices
- responsibility and non-official-KISA disclaimers
- sample and fixture sanitization
- rulepack source-note language
- absence of customer evidence and proprietary device material
- support boundary for `MANUAL_REQUIRED`
- PyPI/TestPyPI publishing decision

Do not convert the repository to public or publish to PyPI/TestPyPI without explicit approval.
