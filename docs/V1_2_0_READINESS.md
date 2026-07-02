# v1.2.0 Readiness Record

This document records the readiness checklist used for the `dev/v1.2.0` branch before the final private `v1.2.0` GitHub Release was created. Do not move the published `v1.2.0` tag or replace its release assets.

`v1.2.0` is tagged, pushed, and published as a final private GitHub Release fixed at `9296245`.

## Branch And Tag State

- Development branch: `dev/v1.2.0`
- Package version metadata: `1.2.0`
- Baseline final release: `v1.1.0`
- `v1.2.0` tag remains fixed at `9296245`
- `v1.1.0` tag remains fixed at `31f624e`
- `v1.0.0` tag remains fixed at `31983bd`
- `v1.0.0rc2` tag remains fixed at `59d3d38`
- `v1.0.0rc1` tag remains fixed at `e93d18b`
- GitHub Release for `v1.2.0`: final private release
- PyPI/TestPyPI publishing: deferred
- Public repository conversion: out of scope

## Junos MVP Boundary

Supported input:

- sanitized `show configuration | display set`
- equivalent display-set text containing active `set ...` statements

Supported vendor values:

- `junos`
- `juniper_junos`

Unsupported or deferred input:

- brace-style Junos configuration
- XML configuration
- JSON configuration
- complete `groups`, `apply-groups`, and inheritance expansion
- direct device access, NETCONF, SSH collection, or live collection

Unsupported Junos formats must not be treated as safe. Brace-style input should produce `needs_display_set` or `MANUAL_REQUIRED`.

## Test Commands

Run from the repository root with the project virtual environment active.

```powershell
.\.venv\Scripts\python -m pytest tests\test_network_junos.py tests\test_network_cisco_ios.py tests\test_network_cisco_ios_realistic.py tests\test_network_rulepack_completeness.py tests\test_netlab_sim.py
.\.venv\Scripts\python -m pytest tests\test_release_readiness.py
.\.venv\Scripts\python -m pytest
git diff --check
```

Expected result:

- targeted Network tests pass
- release readiness tests pass
- full test suite passes
- `git diff --check` reports no whitespace errors; Windows LF to CRLF warnings may appear

## Junos Smoke Commands

```powershell
Remove-Item -Recurse -Force out\v1.2.0-smoke -ErrorAction SilentlyContinue

.\.venv\Scripts\kcii-audit classify-file `
  --profile network `
  --vendor junos `
  --input tests\fixtures\network\junos\display_set_good.txt `
  --output out\v1.2.0-smoke\network-junos-good

.\.venv\Scripts\kcii-audit classify-file `
  --profile network `
  --vendor juniper_junos `
  --input tests\fixtures\network\junos\display_set_vulnerable.txt `
  --output out\v1.2.0-smoke\network-junos-vulnerable

.\.venv\Scripts\kcii-audit classify-file `
  --profile network `
  --vendor junos `
  --input tests\fixtures\network\junos\brace_config_unsupported.txt `
  --output out\v1.2.0-smoke\network-junos-brace-unsupported
```

Each default smoke output must contain:

- `evidence.jsonl`
- `results.json`
- `detail.xlsx`
- `summary.xlsx`
- `report.md`
- `security_advisory.md`
- `security_advisory.xlsx`

Expected Junos good fixture results:

- `N-01` to `N-38` all appear in `results.json`
- status distribution remains `GOOD 14`, `MANUAL_REQUIRED 24`
- sanitized placeholders do not appear in normal text or Excel outputs

Expected unsupported brace fixture behavior:

- `N-01` to `N-38` all appear in `results.json`
- items remain `MANUAL_REQUIRED`
- evidence indicates `needs_display_set` rather than treating brace-style input as complete evidence

## Sensitive Information Search

After smoke runs, search generated outputs for synthetic placeholders and high-confidence secret patterns.

```powershell
$placeholderPattern = '\[HOST_1\]|\[IP_1\]|\[USER_1\]|\[COMMUNITY_1\]|\[SERIAL_1\]|\[DOMAIN_1\]|\[PATH_1\]|\[BANNER_1\]|\[SECRET_1\]'
$matches = Select-String -Path (Get-ChildItem out\v1.2.0-smoke -Recurse -File | Select-Object -ExpandProperty FullName) -Pattern $placeholderPattern -ErrorAction SilentlyContinue
if ($matches) { $matches | Select-Object Path,LineNumber,Line; exit 1 }

git diff --cached | rg -n -- "-----BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----|github_pat_[A-Za-z0-9_]+|ghp_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16}"
```

Expected result: no matches in generated outputs or staged diffs.

## Root And Packaged Resource Sync

The root rulepack and packaged runtime resource copy must stay synchronized.

```powershell
Compare-Object `
  (Get-Content -Raw rulepacks\kcii-2025-12\network.yaml) `
  (Get-Content -Raw src\kcii_audit\resources\rulepacks\kcii-2025-12\network.yaml)

Compare-Object `
  (Get-Content -Raw rulepacks\kcii-2025-12\network_items_manifest.yaml) `
  (Get-Content -Raw src\kcii_audit\resources\rulepacks\kcii-2025-12\network_items_manifest.yaml)
```

Expected result: no output from either command.

## Build And Checksums

Run this before creating any tag or GitHub Release.

```powershell
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
.\.venv\Scripts\python -m build
$artifacts = @('dist\kcii_audit_suite-1.2.0-py3-none-any.whl', 'dist\kcii_audit_suite-1.2.0.tar.gz')
$lines = foreach ($artifact in $artifacts) {
  $hash = Get-FileHash $artifact -Algorithm SHA256
  "$($hash.Hash)  $(Split-Path $artifact -Leaf)"
}
$lines | Set-Content dist\SHA256SUMS.txt -Encoding utf8
```

Release assets should be limited to:

- `kcii_audit_suite-1.2.0-py3-none-any.whl`
- `kcii_audit_suite-1.2.0.tar.gz`
- `SHA256SUMS.txt`

## Private GitHub Release Pre-Checks

Before any replacement or follow-up private GitHub Release action is considered:

- confirm `git status --short --branch` is clean
- confirm the package version is `1.2.0`
- confirm the annotated `v1.2.0` tag still points to `9296245`
- confirm `v1.1.0`, `v1.0.0`, `v1.0.0rc1`, and `v1.0.0rc2` have not moved
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

- `v1.1.0`
- `v1.0.0`
- `v1.0.0rc1`
- `v1.0.0rc2`

After `v1.2.0` is created and shared, do not move it either. Create a new tag for any later correction.
