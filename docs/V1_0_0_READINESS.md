# v1.0.0 Readiness

This document is the final release-candidate gate for `release/v1.0.0`. It records the checks required before an annotated `v1.0.0` tag or private GitHub Release is created.

Do not move `v1.0.0rc1` or `v1.0.0rc2`. Do not publish to PyPI or TestPyPI during v1.0.0 preparation.

## Scope

- No feature additions after `v1.0.0rc2`.
- Documentation, release validation, packaging, and checksum preparation only.
- Existing profile coverage and known limitations remain as documented in `docs/PROFILE_COVERAGE.md`.

## Smoke Commands

Run from the repository root with the project virtual environment active.

```powershell
Remove-Item -Recurse -Force out\v1-smoke -ErrorAction SilentlyContinue

.\.venv\Scripts\kcii-audit classify-file --profile windows --input tests\fixtures\windows_server\good.json --output out\v1-smoke\windows-good
.\.venv\Scripts\kcii-audit classify-file --profile windows --input tests\fixtures\windows_server\vulnerable.json --output out\v1-smoke\windows-vulnerable

.\.venv\Scripts\kcii-audit classify-file --profile linux --input tests\fixtures\linux_server\good.json --output out\v1-smoke\linux-good
.\.venv\Scripts\kcii-audit classify-file --profile linux --input tests\fixtures\linux_server\vulnerable.json --output out\v1-smoke\linux-vulnerable

.\.venv\Scripts\kcii-audit classify-file --profile unix --unix aix --input tests\fixtures\unix_server\aix\good.json --output out\v1-smoke\unix-aix-good
.\.venv\Scripts\kcii-audit classify-file --profile unix --unix solaris --input tests\fixtures\unix_server\solaris\vulnerable.json --output out\v1-smoke\unix-solaris-vulnerable

.\.venv\Scripts\kcii-audit classify-file --profile dbms --dbms postgresql --input tests\fixtures\dbms\postgresql\good.json --output out\v1-smoke\dbms-postgresql-good
.\.venv\Scripts\kcii-audit classify-file --profile dbms --dbms mysql --input tests\fixtures\dbms\mysql\vulnerable.json --output out\v1-smoke\dbms-mysql-vulnerable
.\.venv\Scripts\kcii-audit classify-file --profile dbms --dbms mariadb --input tests\fixtures\dbms\mariadb\vulnerable.json --output out\v1-smoke\dbms-mariadb-vulnerable

.\.venv\Scripts\kcii-audit classify-file --profile network --vendor cisco_ios --input tests\fixtures\network\cisco_ios\vulnerable.txt --output out\v1-smoke\network-cisco-vulnerable

.\.venv\Scripts\kcii-audit classify-file --profile security-appliance --appliance-type firewall --input tests\fixtures\security_appliance\vulnerable.txt --output out\v1-smoke\security-appliance-vulnerable

Get-Content tests\fixtures\dbms\permission_denied.json | .\.venv\Scripts\kcii-audit classify-paste --profile dbms --dbms postgresql --output out\v1-smoke\dbms-permission-denied-paste
Get-Content tests\fixtures\network\cisco_ios\mixed.txt | .\.venv\Scripts\kcii-audit classify-paste --profile network --vendor cisco_ios --output out\v1-smoke\network-paste

.\.venv\Scripts\kcii-audit classify-file --profile linux --input tests\fixtures\linux_server\good.json --output out\v1-smoke\linux-no-advisory --no-advisory
.\.venv\Scripts\kcii-audit questionnaire export --profile security-appliance --output out\v1-smoke\security_appliance_questionnaire.xlsx
.\.venv\Scripts\kcii-audit questionnaire import --profile security-appliance --input out\v1-smoke\security_appliance_questionnaire.xlsx --output out\v1-smoke\security-appliance-questionnaire
```

## Output Expectations

Every default smoke output must contain:

- `evidence.jsonl`
- `results.json`
- `detail.xlsx`
- `summary.xlsx`
- `report.md`
- `security_advisory.md`
- `security_advisory.xlsx`

The `linux-no-advisory` output must contain only the first five files and must not contain `security_advisory.md` or `security_advisory.xlsx`.

## Sensitive Search

After smoke runs, search generated outputs for synthetic sensitive placeholders:

```powershell
$pattern = '\[DB_ACCOUNT_ADMIN\]|\[DB_ACCOUNT_APP\]|customerdb|secretdb|192\.0\.2\.10|postgresql://|mysql://|mariadb://|\$2a\$not-a-real-hash-placeholder|win-prod-01|example\.invalid|S-1-5-21|ADMIN\$|C\$'
$matches = Select-String -Path (Get-ChildItem out\v1-smoke -Recurse -File | Select-Object -ExpandProperty FullName) -Pattern $pattern -ErrorAction SilentlyContinue
if ($matches) { $matches | Select-Object Path,LineNumber,Line; exit 1 }
```

Expected result: no matches in generated outputs.

## Build And Checksums

```powershell
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
.\.venv\Scripts\python -m build
$artifacts = @('dist\kcii_audit_suite-1.0.0-py3-none-any.whl', 'dist\kcii_audit_suite-1.0.0.tar.gz')
$lines = foreach ($artifact in $artifacts) {
  $hash = Get-FileHash $artifact -Algorithm SHA256
  "$($hash.Hash)  $(Split-Path $artifact -Leaf)"
}
$lines | Set-Content dist\SHA256SUMS.txt -Encoding utf8
```

Release assets should be limited to:

- `kcii_audit_suite-1.0.0-py3-none-any.whl`
- `kcii_audit_suite-1.0.0.tar.gz`
- `SHA256SUMS.txt`

## Tag And Release Boundary

Create the annotated `v1.0.0` tag and private GitHub Release only after explicit user approval.

Do not:

- move `v1.0.0rc1`
- move `v1.0.0rc2`
- push directly to `main`
- publish to PyPI or TestPyPI
- make the repository public
- attach real customer evidence, live output, raw configs, licenses, or secrets
