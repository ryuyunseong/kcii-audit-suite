# v1.0.0rc2 Readiness

This document is the rc2 release-candidate gate for `dev/v1.0.0rc2`. It records what must pass before an annotated `v1.0.0rc2` tag or private GitHub pre-release is created.

Do not move `v1.0.0rc1`. Do not publish to PyPI or TestPyPI during rc2 preparation.

## Scope

- Windows Server: expanded deterministic and partial judgment for selected read-only evidence summaries.
- DBMS: PostgreSQL, MySQL, and MariaDB offline parser MVP hardening for sanitized JSON and key/value inputs.
- Linux Server: existing MVP retained.
- Unix Server: existing registered manifest and fixture-based parser retained.
- Network: existing Cisco IOS MVP retained.
- Security Appliance: existing questionnaire and sanitized summary flow retained.
- Output contract: default seven-file bundle retained.

## Smoke Commands

Run from the repository root with the project virtual environment active.

```powershell
Remove-Item -Recurse -Force out\rc2-smoke -ErrorAction SilentlyContinue

.\.venv\Scripts\kcii-audit classify-file --profile windows --input tests\fixtures\windows_server\good.json --output out\rc2-smoke\windows-good
.\.venv\Scripts\kcii-audit classify-file --profile windows --input tests\fixtures\windows_server\vulnerable.json --output out\rc2-smoke\windows-vulnerable

.\.venv\Scripts\kcii-audit classify-file --profile linux --input tests\fixtures\linux_server\good.json --output out\rc2-smoke\linux-good
.\.venv\Scripts\kcii-audit classify-file --profile linux --input tests\fixtures\linux_server\vulnerable.json --output out\rc2-smoke\linux-vulnerable

.\.venv\Scripts\kcii-audit classify-file --profile unix --unix aix --input tests\fixtures\unix_server\aix\good.json --output out\rc2-smoke\unix-aix-good
.\.venv\Scripts\kcii-audit classify-file --profile unix --unix solaris --input tests\fixtures\unix_server\solaris\vulnerable.json --output out\rc2-smoke\unix-solaris-vulnerable

.\.venv\Scripts\kcii-audit classify-file --profile dbms --dbms postgresql --input tests\fixtures\dbms\postgresql\good.json --output out\rc2-smoke\dbms-postgresql-good
.\.venv\Scripts\kcii-audit classify-file --profile dbms --dbms mysql --input tests\fixtures\dbms\mysql\vulnerable.json --output out\rc2-smoke\dbms-mysql-vulnerable
.\.venv\Scripts\kcii-audit classify-file --profile dbms --dbms mariadb --input tests\fixtures\dbms\mariadb\vulnerable.json --output out\rc2-smoke\dbms-mariadb-vulnerable

.\.venv\Scripts\kcii-audit classify-file --profile network --vendor cisco_ios --input tests\fixtures\network\cisco_ios\vulnerable.txt --output out\rc2-smoke\network-cisco-vulnerable

.\.venv\Scripts\kcii-audit classify-file --profile security-appliance --appliance-type firewall --input tests\fixtures\security_appliance\vulnerable.txt --output out\rc2-smoke\security-appliance-vulnerable

Get-Content tests\fixtures\dbms\permission_denied.json | .\.venv\Scripts\kcii-audit classify-paste --profile dbms --dbms postgresql --output out\rc2-smoke\dbms-permission-denied-paste
Get-Content tests\fixtures\network\cisco_ios\mixed.txt | .\.venv\Scripts\kcii-audit classify-paste --profile network --vendor cisco_ios --output out\rc2-smoke\network-paste

.\.venv\Scripts\kcii-audit classify-file --profile linux --input tests\fixtures\linux_server\good.json --output out\rc2-smoke\linux-no-advisory --no-advisory
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
$matches = Select-String -Path (Get-ChildItem out\rc2-smoke -Recurse -File | Select-Object -ExpandProperty FullName) -Pattern $pattern -ErrorAction SilentlyContinue
if ($matches) { $matches | Select-Object Path,LineNumber,Line; exit 1 }
```

Expected result: no matches in generated outputs.

## Build And Checksums

```powershell
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
.\.venv\Scripts\python -m build
Get-FileHash dist\kcii_audit_suite-1.0.0rc2-py3-none-any.whl -Algorithm SHA256
Get-FileHash dist\kcii_audit_suite-1.0.0rc2.tar.gz -Algorithm SHA256
Get-FileHash dist\* -Algorithm SHA256 |
  Format-Table Algorithm,Hash,Path -AutoSize |
  Out-File dist\SHA256SUMS.txt -Encoding utf8
```

Release assets should be limited to:

- `kcii_audit_suite-1.0.0rc2-py3-none-any.whl`
- `kcii_audit_suite-1.0.0rc2.tar.gz`
- `SHA256SUMS.txt`

## Tag And Release Boundary

Create the annotated `v1.0.0rc2` tag and private GitHub pre-release only after explicit user approval.

Do not:

- move `v1.0.0rc1`
- push directly to `main`
- publish to PyPI or TestPyPI
- make the repository public
- attach real customer evidence, live output, raw configs, licenses, or secrets
