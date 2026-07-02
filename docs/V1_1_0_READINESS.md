# v1.1.0 Readiness Draft

This document is the draft readiness checklist for the `dev/v1.1.0` branch. It is not a release record. Do not create a `v1.1.0` tag or GitHub Release until explicit approval is given.

`v1.1.0` is not tagged or released.

## Branch And Tag State

- Development branch: `dev/v1.1.0`
- Baseline final release: `v1.0.0`
- `v1.0.0` tag remains fixed at `31983bd`
- `v1.0.0rc2` tag remains fixed at `59d3d38`
- `v1.0.0rc1` tag remains fixed at `e93d18b`
- `v1.1.0` tag: not created
- PyPI/TestPyPI publishing: deferred
- Public repository conversion: out of scope

## Test Commands

Run from the repository root with the project virtual environment active.

```powershell
.\.venv\Scripts\python -m pytest tests\test_network_cisco_ios.py tests\test_network_cisco_ios_realistic.py tests\test_network_rulepack_completeness.py tests\test_netlab_sim.py
.\.venv\Scripts\python -m pytest tests\test_release_readiness.py
.\.venv\Scripts\python -m pytest
git diff --check
```

Expected result:

- targeted Network tests pass
- release readiness tests pass
- full test suite passes
- `git diff --check` reports no whitespace errors; Windows LF to CRLF warnings may appear

## Network Smoke Commands

```powershell
Remove-Item -Recurse -Force out\v1.1.0-smoke -ErrorAction SilentlyContinue

.\.venv\Scripts\kcii-audit classify-file `
  --profile network `
  --vendor cisco_ios `
  --input tests\fixtures\network\cisco_ios\vulnerable.txt `
  --output out\v1.1.0-smoke\network-cisco-vulnerable

.\.venv\Scripts\kcii-audit classify-file `
  --profile network `
  --vendor cisco_ios `
  --input tests\fixtures\network\cisco_ios\realistic\sanitized_lab_mixed.txt `
  --output out\v1.1.0-smoke\network-cisco-realistic
```

Each default smoke output must contain:

- `evidence.jsonl`
- `results.json`
- `detail.xlsx`
- `summary.xlsx`
- `report.md`
- `security_advisory.md`
- `security_advisory.xlsx`

Expected Network results:

- `N-01` to `N-38` all appear in `results.json`
- realistic fixture status distribution remains `GOOD 27`, `MANUAL_REQUIRED 11`

## Sensitive Information Search

After smoke runs, search generated outputs for synthetic placeholders and high-confidence secret patterns.

```powershell
$placeholderPattern = '\[HOST_1\]|\[IP_1\]|\[USER_1\]|\[COMMUNITY_1\]|\[SERIAL_1\]|\[DOMAIN_1\]|\[PATH_1\]|\[BANNER_1\]|\[SECRET_1\]'
$matches = Select-String -Path (Get-ChildItem out\v1.1.0-smoke -Recurse -File | Select-Object -ExpandProperty FullName) -Pattern $placeholderPattern -ErrorAction SilentlyContinue
if ($matches) { $matches | Select-Object Path,LineNumber,Line; exit 1 }

git diff --cached | rg -n -- "-----BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----|github_pat_[A-Za-z0-9_]+|ghp_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16}"
```

Expected result: no matches in generated outputs or staged diffs.

## Build And Checksums

Run this only after the package version is updated to `1.1.0` and the release candidate is approved.

```powershell
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
.\.venv\Scripts\python -m build
$artifacts = @('dist\kcii_audit_suite-1.1.0-py3-none-any.whl', 'dist\kcii_audit_suite-1.1.0.tar.gz')
$lines = foreach ($artifact in $artifacts) {
  $hash = Get-FileHash $artifact -Algorithm SHA256
  "$($hash.Hash)  $(Split-Path $artifact -Leaf)"
}
$lines | Set-Content dist\SHA256SUMS.txt -Encoding utf8
```

Release assets should be limited to:

- `kcii_audit_suite-1.1.0-py3-none-any.whl`
- `kcii_audit_suite-1.1.0.tar.gz`
- `SHA256SUMS.txt`

## Private GitHub Release Pre-Checks

Before a private GitHub Release is created:

- confirm `git status --short --branch` is clean
- confirm the annotated `v1.1.0` tag points to the intended commit
- confirm `v1.0.0`, `v1.0.0rc1`, and `v1.0.0rc2` have not moved
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
- IOS, CML, VM, or appliance images
- license files
- tokens, keys, password hashes, certificates, or credential material

## Tag Movement Rule

Published release tags are immutable for this project. Do not move:

- `v1.0.0`
- `v1.0.0rc1`
- `v1.0.0rc2`

After `v1.1.0` is created and shared, do not move it either. Create a new tag for any later correction.
