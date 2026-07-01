# Release Checklist

Use this checklist before publishing or handing off a release candidate.

## Environment

- [ ] Start from a clean workspace.
- [ ] Confirm no real customer evidence is present.
- [ ] Confirm `.env`, generated `out/`, `raw/`, and `tmp/` files are not part of source control.
- [ ] Create a clean virtual environment:

```powershell
python -m venv tmp\venv-release-check
tmp\venv-release-check\Scripts\python -m pip install -e ".[dev]"
```

## CLI Help

```powershell
tmp\venv-release-check\Scripts\kcii-audit --help
tmp\venv-release-check\Scripts\kcii-audit classify-file --help
tmp\venv-release-check\Scripts\kcii-audit questionnaire --help
```

## Automated Tests

```powershell
tmp\venv-release-check\Scripts\python -m pytest
```

Expected result: all tests pass.

## Package Build

```powershell
tmp\venv-release-check\Scripts\python -m build
Get-ChildItem dist
```

Expected result:

- One source distribution under `dist/`
- One wheel under `dist/`

Install the built wheel in a separate clean environment:

```powershell
python -m venv tmp\venv-wheel-check
tmp\venv-wheel-check\Scripts\python -m pip install (Get-ChildItem dist\*.whl | Select-Object -First 1).FullName
tmp\venv-wheel-check\Scripts\kcii-audit --help
tmp\venv-wheel-check\Scripts\kcii-audit classify-file --help
tmp\venv-wheel-check\Scripts\kcii-audit questionnaire --help
```

## Installed Wheel Self-Contained Classification

Run this from a directory outside the repository to confirm runtime resources are packaged in the wheel and not loaded from the source tree:

```powershell
$tmpRoot = Join-Path $env:TEMP "kcii-wheel-self-contained"
Remove-Item -Recurse -Force $tmpRoot -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force $tmpRoot | Out-Null
python -m venv "$tmpRoot\venv"
$wheel = (Get-ChildItem dist\*.whl | Select-Object -First 1).FullName
& "$tmpRoot\venv\Scripts\python" -m pip install $wheel

New-Item -ItemType Directory -Force "$tmpRoot\inputs" | Out-Null
Copy-Item tests\fixtures\windows\paste\good-collector.json "$tmpRoot\inputs\windows-good.json"
Copy-Item tests\fixtures\linux_server\good.json "$tmpRoot\inputs\linux-good.json"
Copy-Item tests\fixtures\unix_server\aix\good.json "$tmpRoot\inputs\unix-aix-good.json"
Copy-Item tests\fixtures\dbms\postgresql\good.txt "$tmpRoot\inputs\dbms-postgresql-good.txt"
Copy-Item tests\fixtures\network\cisco_ios\good.txt "$tmpRoot\inputs\network-cisco-good.txt"
Copy-Item tests\fixtures\security_appliance\good.txt "$tmpRoot\inputs\security-appliance-good.txt"

Push-Location $tmpRoot
.\venv\Scripts\kcii-audit classify-file --profile windows --input .\inputs\windows-good.json --output .\out\windows-good
.\venv\Scripts\kcii-audit classify-file --profile linux --input .\inputs\linux-good.json --output .\out\linux-good
.\venv\Scripts\kcii-audit classify-file --profile unix --unix aix --input .\inputs\unix-aix-good.json --output .\out\unix-aix-good
.\venv\Scripts\kcii-audit classify-file --profile dbms --dbms postgresql --input .\inputs\dbms-postgresql-good.txt --output .\out\dbms-postgresql-good
.\venv\Scripts\kcii-audit classify-file --profile network --vendor cisco_ios --input .\inputs\network-cisco-good.txt --output .\out\network-cisco-good
.\venv\Scripts\kcii-audit classify-file --profile security-appliance --appliance-type firewall --input .\inputs\security-appliance-good.txt --output .\out\security-appliance-good
.\venv\Scripts\kcii-audit classify-file --profile linux --input .\inputs\linux-good.json --output .\out\linux-no-advisory --no-advisory
.\venv\Scripts\kcii-audit questionnaire export --profile security-appliance --output .\out\security_appliance_questionnaire.xlsx
Pop-Location
```

Expected result:

- Each default profile output has the seven-file bundle.
- `linux-no-advisory` has no `security_advisory.md` or `security_advisory.xlsx`.
- Results include profile-specific `GOOD` outcomes where the good fixture contains sufficient evidence.
- `security_appliance_questionnaire.xlsx` is created from the installed wheel.

## Profile Smoke Commands

Windows:

```powershell
tmp\venv-release-check\Scripts\kcii-audit classify-file --profile windows --input tests\fixtures\windows\paste\good-collector.json --output out\release-smoke-windows
```

Linux:

```powershell
tmp\venv-release-check\Scripts\kcii-audit classify-file --profile linux --input tests\fixtures\linux_server\good.json --output out\release-smoke-linux
```

Unix:

```powershell
tmp\venv-release-check\Scripts\kcii-audit classify-file --profile unix --unix aix --input tests\fixtures\unix_server\aix\good.json --output out\release-smoke-unix-aix
```

DBMS:

```powershell
tmp\venv-release-check\Scripts\kcii-audit classify-file --profile dbms --dbms postgresql --input tests\fixtures\dbms\postgresql\good.txt --output out\release-smoke-dbms-postgresql
```

Network:

```powershell
tmp\venv-release-check\Scripts\kcii-audit classify-file --profile network --vendor cisco_ios --input tests\fixtures\network\cisco_ios\good.txt --output out\release-smoke-network-cisco
```

Security Appliance:

```powershell
tmp\venv-release-check\Scripts\kcii-audit questionnaire export --profile security-appliance --output out\release-security-appliance-questionnaire.xlsx
tmp\venv-release-check\Scripts\kcii-audit questionnaire import --profile security-appliance --input out\release-security-appliance-questionnaire.xlsx --output out\release-smoke-security-appliance-questionnaire
tmp\venv-release-check\Scripts\kcii-audit classify-file --profile security-appliance --appliance-type firewall --input tests\fixtures\security_appliance\good.txt --output out\release-smoke-security-appliance
```

No-advisory option:

```powershell
tmp\venv-release-check\Scripts\kcii-audit classify-file --profile linux --input tests\fixtures\linux_server\good.json --output out\release-smoke-no-advisory --no-advisory
```

## Output Check

Each default smoke output should contain:

- `evidence.jsonl`
- `results.json`
- `detail.xlsx`
- `summary.xlsx`
- `report.md`
- `security_advisory.md`
- `security_advisory.xlsx`

The `--no-advisory` output should not contain `security_advisory.md` or `security_advisory.xlsx`.

## Sensitive Content Search

Search generated outputs and release documents before publishing:

```powershell
rg -n "password|token|secret|BEGIN CERTIFICATE|PRIVATE KEY|license_key|serial_number|connection string" out docs README.md RELEASE_NOTES.md CHANGELOG.md
```

Findings must be reviewed manually because some policy words may appear in documentation. Real values must not appear.

## Release Boundary

- [ ] Keep release scope at offline evidence classification and reporting.
- [ ] Do not add new production remote collection behavior during release stabilization.
- [ ] Do not publish tags, releases, or repositories until the user explicitly asks for that step.
