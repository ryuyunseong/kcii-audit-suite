# v1.3.0 Readiness Draft

This document is the draft readiness checklist for the `dev/v1.3.0` branch. It is not a release record. Do not create a `v1.3.0` tag or GitHub Release until explicit approval is given.

`v1.3.0` is not tagged or released. Package version metadata is prepared as `1.3.0` for release smoke, build, checksum, and installed-wheel validation.

## Branch And Tag State

- Development branch: `dev/v1.3.0`
- Latest Junos realistic normalization commit: `7077334`
- Package version metadata: `1.3.0`
- Baseline final release: `v1.2.0`
- `v1.2.0` tag remains fixed at `9296245`
- `v1.1.0` tag remains fixed at `31f624e`
- `v1.0.0` tag remains fixed at `31983bd`
- `v1.0.0rc2` tag remains fixed at `59d3d38`
- `v1.0.0rc1` tag remains fixed at `e93d18b`
- `v1.3.0` tag: not created
- PyPI/TestPyPI publishing: deferred
- Public repository conversion: out of scope

## Junos v1.3.0 Boundary

Supported input remains:

- sanitized `show configuration | display set`
- equivalent display-set text containing active `set ...` statements
- prompt-prefixed display-set output where valid `set ...` lines can be extracted

Supported vendor values:

- `junos`
- `juniper_junos`

Unsupported or deferred input:

- brace-style Junos configuration
- XML configuration
- JSON configuration
- complete `groups`, `apply-groups`, and inheritance expansion
- direct device access, NETCONF, SSH collection, or live collection

Unsupported Junos formats must not be treated as safe. They should produce `unsupported_format`, `needs_display_set`, or `MANUAL_REQUIRED` evidence rather than deterministic good results.

## Test Commands

Run from the repository root with the project virtual environment active.

```powershell
.\.venv\Scripts\python -m pytest tests\test_network_junos.py tests\test_network_vendor_regression.py tests\test_network_cisco_ios_realistic.py
.\.venv\Scripts\python -m pytest tests\test_release_readiness.py
.\.venv\Scripts\python -m pytest
git diff --check
```

Expected result:

- targeted Network tests pass
- release readiness tests pass
- full test suite passes
- `git diff --check` reports no whitespace errors; Windows LF to CRLF warnings may appear

## Junos Realistic Smoke Commands

```powershell
Remove-Item -Recurse -Force out\v1.3.0-junos-realistic -ErrorAction SilentlyContinue

.\.venv\Scripts\kcii-audit classify-file `
  --profile network `
  --vendor junos `
  --input tests\fixtures\network\junos\realistic\display_set_realistic_sanitized.txt `
  --output out\v1.3.0-junos-realistic
```

The default smoke output must contain:

- `evidence.jsonl`
- `results.json`
- `detail.xlsx`
- `summary.xlsx`
- `report.md`
- `security_advisory.md`
- `security_advisory.xlsx`

Expected Junos realistic fixture results:

- `N-01` to `N-38` all appear in `results.json`
- status distribution remains `GOOD 14`, `MANUAL_REQUIRED 24`
- `inactive` and `deactivate` lines are not treated as active good evidence
- `apply-groups` is preserved as inheritance-required evidence and keeps dependent judgment conservative
- sanitized placeholders do not appear in normal text or Excel outputs

## Sensitive Information Search

After smoke runs, search generated outputs for synthetic placeholders and high-confidence secret patterns.

```powershell
$placeholderPattern = '\[HOST_1\]|\[IP_1\]|\[USER_1\]|\[COMMUNITY_1\]|\[SERIAL_1\]|\[DOMAIN_1\]|\[PATH_1\]|\[BANNER_1\]|\[SECRET_1\]|\[GROUP_1\]|\[FILTER_1\]|\[PREFIX_LIST_1\]'
$matches = Select-String -Path (Get-ChildItem out\v1.3.0-junos-realistic -Recurse -File | Select-Object -ExpandProperty FullName) -Pattern $placeholderPattern -ErrorAction SilentlyContinue
if ($matches) { $matches | Select-Object Path,LineNumber,Line; exit 1 }

git diff --cached | rg -n -- "-----BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----|github_pat_[A-Za-z0-9_]+|ghp_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16}"
```

Expected result: no matches in generated outputs or staged diffs.

## Build And Checksums

Run this before creating any tag or GitHub Release.

```powershell
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
.\.venv\Scripts\python -m build
$artifacts = @('dist\kcii_audit_suite-1.3.0-py3-none-any.whl', 'dist\kcii_audit_suite-1.3.0.tar.gz')
$lines = foreach ($artifact in $artifacts) {
  $hash = Get-FileHash $artifact -Algorithm SHA256
  "$($hash.Hash)  $(Split-Path $artifact -Leaf)"
}
$lines | Set-Content dist\SHA256SUMS.txt -Encoding utf8
```

Release assets should be limited to:

- `kcii_audit_suite-1.3.0-py3-none-any.whl`
- `kcii_audit_suite-1.3.0.tar.gz`
- `SHA256SUMS.txt`

## Private GitHub Release Pre-Checks

Before any private GitHub Release is created:

- confirm `git status --short --branch` is clean
- confirm the package version is `1.3.0`
- confirm the annotated `v1.3.0` tag points to the intended commit
- confirm `v1.2.0`, `v1.1.0`, `v1.0.0`, `v1.0.0rc1`, and `v1.0.0rc2` have not moved
- confirm wheel, source distribution, and checksum assets are rebuilt from the intended commit
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

- `v1.2.0`
- `v1.1.0`
- `v1.0.0`
- `v1.0.0rc1`
- `v1.0.0rc2`

After `v1.3.0` is created and shared, do not move it either. Create a new tag for any later correction.
