# v1.4.0 Readiness Draft

This document records the readiness checklist for the `dev/v1.4.0` branch. It is a draft only. No `v1.4.0` tag or GitHub Release has been created.

## Branch And Tag State

- Development branch: `dev/v1.4.0`
- Latest Junos inheritance parser skeleton commit: `5cb5d7d`
- Package version metadata: `1.4.0`
- Baseline final release: `v1.3.0`
- `v1.3.0` tag remains fixed at `30490b4`
- `v1.2.0` tag remains fixed at `9296245`
- `v1.1.0` tag remains fixed at `31f624e`
- `v1.0.0` tag remains fixed at `31983bd`
- `v1.0.0rc2` tag remains fixed at `59d3d38`
- `v1.0.0rc1` tag remains fixed at `e93d18b`
- `v1.4.0` tag: not created
- GitHub Release for `v1.4.0`: not created
- PyPI/TestPyPI publishing: deferred
- Public repository conversion: out of scope

## Junos v1.4.0 Boundary

Supported draft input:

- sanitized `show configuration | display set`
- sanitized `show configuration | display inheritance`
- combined display-set plus display-inheritance text
- synthetic display-inheritance fixture lines using `effective-statement`, `conflict-statement`, `inheritance-source`, and `apply-groups-except`

Supported vendor values remain:

- `junos`
- `juniper_junos`

Conservative behavior:

- display-set with `apply-groups` but no inheritance context keeps `inheritance_required=True` and remains review-heavy
- clear inherited evidence can become partial evidence only for selected fields
- conflicting inherited values keep all items `MANUAL_REQUIRED`
- incomplete source context keeps all items `MANUAL_REQUIRED`
- inactive or deactivated inherited statements must not become active good evidence
- source group names and raw configuration lines must not be stored in normal output evidence

Unsupported or deferred input:

- brace-style Junos configuration
- XML configuration
- JSON configuration
- full Junos inheritance semantics
- NETCONF, SSH collection, direct device access, or live collection

## Test Commands

Run from the repository root with the project virtual environment active.

```powershell
.\.venv\Scripts\python -m pytest tests\test_network_junos.py tests\test_network_vendor_regression.py tests\test_release_readiness.py
.\.venv\Scripts\python -m pytest
git diff --check
git tag -l "v1.4.0"
```

Expected result:

- targeted Junos and Network vendor tests pass
- release readiness tests pass
- full test suite passes
- `git diff --check` reports no whitespace errors; Windows LF to CRLF warnings may appear
- `git tag -l "v1.4.0"` returns no tag before explicit release approval

Current release-preparation validation result:

- release readiness tests: `9 passed`
- full `python -m pytest`: `176 passed`
- full profile smoke: passed
- Junos inheritance smoke distribution: `GOOD 4`, `MANUAL_REQUIRED 34`
- build: `kcii_audit_suite-1.4.0-py3-none-any.whl` and `kcii_audit_suite-1.4.0.tar.gz`
- checksum: `dist/SHA256SUMS.txt`
- clean installed-wheel smoke: passed
- high-confidence secret pattern scan: no hits
- forbidden path scan: no hits
- `v1.4.0` tag: not created

## Junos Inheritance Smoke Command

```powershell
Remove-Item -Recurse -Force out\v1.4.0-junos-inheritance -ErrorAction SilentlyContinue

.\.venv\Scripts\kcii-audit classify-file `
  --profile network `
  --vendor junos `
  --input tests\fixtures\network\junos\inheritance\display_inheritance_effective_good.txt `
  --output out\v1.4.0-junos-inheritance
```

The default smoke output must contain:

- `evidence.jsonl`
- `results.json`
- `detail.xlsx`
- `summary.xlsx`
- `report.md`
- `security_advisory.md`
- `security_advisory.xlsx`

Expected inheritance smoke result for the synthetic clear fixture:

- `N-01` to `N-38` all appear in `results.json`
- status distribution remains `GOOD 4`, `MANUAL_REQUIRED 34`
- `inheritance_available=True`
- `inheritance_source_count=1`
- source group names and fixture placeholders do not appear in normal output text

## Sensitive Information Search

After smoke runs, search generated outputs for synthetic placeholders and high-confidence secret patterns.

```powershell
$placeholderPattern = '\[HOST_1\]|\[IP_1\]|\[USER_1\]|\[COMMUNITY_1\]|\[SERIAL_1\]|\[DOMAIN_1\]|\[PATH_1\]|\[BANNER_1\]|\[SECRET_1\]|\[GROUP_1\]|\[GROUP_2\]|\[FILTER_1\]|\[FILTER_2\]|\[PREFIX_LIST_1\]|\[PREFIX_LIST_2\]'
$matches = Select-String -Path (Get-ChildItem out\v1.4.0-junos-inheritance -Recurse -File | Select-Object -ExpandProperty FullName) -Pattern $placeholderPattern -ErrorAction SilentlyContinue
if ($matches) { $matches | Select-Object Path,LineNumber,Line; exit 1 }

git diff --cached | rg -n -- "-----BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----|github_pat_[A-Za-z0-9_]+|ghp_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16}"
```

Expected result: no matches in generated outputs or staged diffs.

## Release Smoke And Build

Run this before creating any tag or GitHub Release.

```powershell
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
.\.venv\Scripts\python -m build
$artifacts = @('dist\kcii_audit_suite-1.4.0-py3-none-any.whl', 'dist\kcii_audit_suite-1.4.0.tar.gz')
$lines = foreach ($artifact in $artifacts) {
  $hash = Get-FileHash $artifact -Algorithm SHA256
  "$($hash.Hash)  $(Split-Path $artifact -Leaf)"
}
$lines | Set-Content dist\SHA256SUMS.txt -Encoding utf8
```

Release assets should be limited to:

- `kcii_audit_suite-1.4.0-py3-none-any.whl`
- `kcii_audit_suite-1.4.0.tar.gz`
- `SHA256SUMS.txt`

## Private GitHub Release Pre-Checks

Before any `v1.4.0` private GitHub Release is created:

- confirm `git status --short --branch` is clean
- confirm package version metadata is `1.4.0`
- confirm full profile smoke and Junos inheritance smoke pass
- confirm wheel, source distribution, and checksum assets are rebuilt from the intended commit
- confirm `v1.3.0`, `v1.2.0`, `v1.1.0`, `v1.0.0`, `v1.0.0rc2`, and `v1.0.0rc1` have not moved
- confirm downloaded release assets match `SHA256SUMS.txt`
- confirm PyPI/TestPyPI publishing remains deferred unless separately approved

## Prohibited Files And Assets

Do not commit or attach:

- `out/`
- `raw/`
- `tmp/`
- `dist/`
- `.env` or local secret files
- real customer evidence
- live device output before sanitization
- commercial device configs
- Junos, IOS, CML, VM, or appliance images
- license files
- tokens, keys, password hashes, certificates, or credential material

## Tag Movement Rule

Published release tags are immutable for this project. Do not move:

- `v1.3.0`
- `v1.2.0`
- `v1.1.0`
- `v1.0.0`
- `v1.0.0rc1`
- `v1.0.0rc2`

After `v1.4.0` is created and shared, do not move it either. Create a new tag for any later correction.
