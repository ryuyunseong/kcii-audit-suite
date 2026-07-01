# kcii-audit-suite

`kcii-audit-suite` is an offline helper for Korean critical information infrastructure vulnerability assessment evidence review. It is not an official KISA tool and does not replace assessor judgment, customer policy, or compensating-control review.

The project is fixed to the local `kcii-2025-12` rulepack baseline. The rulepacks register the item IDs, titles, and severities transcribed from the provided KISA guide tables, but the guide text is not copied in bulk.

## Operating Model

This tool is not a remote automatic collector.

Operational flow:

1. The target system, DBMS, network device, or security appliance owner runs approved read-only commands, SQL, scripts, show commands, config export, or questionnaire collection.
2. The result file or pasted text is moved to the Windows work PC.
3. `kcii-audit classify-file` or `kcii-audit classify-paste` parses the offline evidence.
4. The deterministic rulepack creates results, Excel workbooks, a Markdown report, and security advisory files.

Docker, Containerlab, GNS3, EVE-NG, DBMS Docker Compose, and simulator assets are development and verification lab tools only. They are not production collection flows.

DBMS Docker Compose lab은 운영 고객사 DBMS 자동 수집용이 아닙니다.

## Current Coverage

| Profile | Registered scope | Current automation level |
| --- | --- | --- |
| Windows Server | `W-01` to `W-64` | Full item registration, partial automatic judgment |
| Linux Server | `L-01` to `L-08` MVP | MVP deterministic checks |
| Unix Server | `U-01` to `U-67` | AIX, Solaris, HP-UX, Linux fixture-based offline parser |
| DBMS | `D-01` to `D-26` | PostgreSQL, MySQL, MariaDB offline parser and Docker live verification |
| Network | `N-01` to `N-38` | Cisco IOS simulator/parser MVP |
| Security Appliance | `S-01` to `S-23` | Questionnaire Excel export/import and sanitized summary parser |

`MANUAL_REQUIRED` is a valid result. It means the item is registered but the available sanitized evidence is insufficient for deterministic judgment. It is not a program failure.

Detailed per-profile counts and known limitations are in [docs/PROFILE_COVERAGE.md](docs/PROFILE_COVERAGE.md).

For `dev/v1.0.0rc2`, Windows Server classification expands deterministic and partial checks for password policy summaries, default administrative shares, selected risky services, audit policy summaries, and Event Log settings. `secedit /export` and `auditpol /get` are used only as read-only evidence collection inputs; raw export text is not stored in normal outputs.

## Outputs

Default classification creates seven files:

- `evidence.jsonl`: normalized sanitized evidence summaries
- `results.json`: deterministic judgment results
- `detail.xlsx`: detailed result workbook
- `summary.xlsx`: summary workbook
- `report.md`: Markdown assessment report
- `security_advisory.md`: remediation and manual-check advisory summary
- `security_advisory.xlsx`: advisory workbook

Use `--no-advisory` to create only the first five files. Use `--include-good-advisory` only when good items should also be included as maintenance advisories.

Security advisory files include vulnerable and manual-check items by default. They do not store raw evidence text.

## Install

Python 3.12 or later is required.

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e ".[dev]"
```

Clean environment verification:

```powershell
python -m venv tmp\venv-release-check
tmp\venv-release-check\Scripts\python -m pip install -e ".[dev]"
tmp\venv-release-check\Scripts\kcii-audit --help
tmp\venv-release-check\Scripts\python -m pytest
```

`tmp/` is ignored and can be removed after verification.

## CLI Smoke Commands

Windows Server:

```powershell
kcii-audit classify-file --profile windows --input tests\fixtures\windows\paste\good-collector.json --output out\smoke-windows
Get-Content tests\fixtures\windows\paste\manual-key-value.txt | kcii-audit classify-paste --profile windows --output out\smoke-windows-paste
```

Linux Server:

```powershell
kcii-audit classify-file --profile linux --input tests\fixtures\linux_server\good.json --output out\smoke-linux
Get-Content tests\fixtures\linux_server\permission_denied.json | kcii-audit classify-paste --profile linux --output out\smoke-linux-paste
```

Unix Server:

```powershell
kcii-audit classify-file --profile unix --unix aix --input tests\fixtures\unix_server\aix\good.json --output out\smoke-unix-aix
Get-Content tests\fixtures\unix_server\solaris\manual_required.txt | kcii-audit classify-paste --profile unix --unix solaris --output out\smoke-unix-solaris-paste
```

DBMS:

```powershell
kcii-audit classify-file --profile dbms --dbms postgresql --input tests\fixtures\dbms\postgresql\good.txt --output out\smoke-dbms-postgresql
Get-Content tests\fixtures\dbms\mysql\manual_required.txt | kcii-audit classify-paste --profile dbms --dbms mysql --output out\smoke-dbms-mysql-paste
```

Network:

```powershell
kcii-audit classify-file --profile network --vendor cisco_ios --input tests\fixtures\network\cisco_ios\good.txt --output out\smoke-network-cisco
Get-Content tests\fixtures\network\cisco_ios\mixed.txt | kcii-audit classify-paste --profile network --vendor cisco_ios --output out\smoke-network-cisco-paste
```

Security Appliance:

```powershell
kcii-audit questionnaire export --profile security-appliance --output out\security_appliance_questionnaire.xlsx
kcii-audit questionnaire import --profile security-appliance --input out\security_appliance_questionnaire.xlsx --output out\smoke-security-appliance-questionnaire
kcii-audit classify-file --profile security-appliance --appliance-type firewall --input tests\fixtures\security_appliance\good.txt --output out\smoke-security-appliance
Get-Content tests\fixtures\security_appliance\manual_required.txt | kcii-audit classify-paste --profile security-appliance --appliance-type firewall --output out\smoke-security-appliance-paste
```

No-advisory smoke:

```powershell
kcii-audit classify-file --profile linux --input tests\fixtures\linux_server\good.json --output out\smoke-no-advisory --no-advisory
```

## Security Rules

Do not commit real customer evidence, raw config exports, `.env` files, passwords, password hashes, tokens, keys, certificate bodies, hostnames, domains, account names, serial numbers, policy names, object names, internal URLs, or IP addresses.

Repository samples must stay synthetic and sanitized. `out/`, `raw/`, `tmp/`, `.env`, and `.env.*` are ignored. Keep only `.env.example` placeholders when an example is needed.

The parser should store boolean, integer, enum, count, masked identifier, warning, and `raw_evidence_hash` values only. It should not store full raw evidence in reports, advisory files, workbooks, or fixtures.

## Release Documents

- [CHANGELOG.md](CHANGELOG.md)
- [RELEASE_NOTES.md](RELEASE_NOTES.md)
- [RELEASE_NOTES_v1.0.0rc1.md](RELEASE_NOTES_v1.0.0rc1.md)
- [docs/RELEASE_CHECKLIST.md](docs/RELEASE_CHECKLIST.md)
- [docs/PROFILE_COVERAGE.md](docs/PROFILE_COVERAGE.md)

## Current Release Candidate Status

`v1.0.0rc1` is fixed at commit `e93d18b`, pushed to the private GitHub repository, and published as a GitHub pre-release. Do not move the `v1.0.0rc1` tag.

Ongoing development should happen on `dev/v1.0.0rc2`. The rc2 target is to keep full item registration intact, expand deterministic checks where evidence is reliable, and leave unsupported or ambiguous items as `MANUAL_REQUIRED`.
