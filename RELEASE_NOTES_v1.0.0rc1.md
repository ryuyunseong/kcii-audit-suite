# kcii-audit-suite v1.0.0rc1

## Summary

`kcii-audit-suite v1.0.0rc1` is a release candidate for an offline vulnerability assessment assistant for Korean critical information infrastructure review workflows.

This tool is not an official KISA tool. It parses read-only assessment outputs collected separately from target systems, classifies findings using local rulepacks, and generates Excel and Markdown security assessment deliverables.

## Included

- Windows Server `W-01` to `W-64` offline evidence classification with partial automatic judgment.
- Linux Server MVP offline evidence classification.
- Unix Server `U-01` to `U-67` fixture-based support for AIX, Solaris, HP-UX, and Linux-compatible outputs.
- DBMS `D-01` to `D-26` support with PostgreSQL, MySQL, and MariaDB offline parsers and Docker live SQL verification.
- Network `N-01` to `N-38` support with Cisco IOS parser and `kcii-netlab-sim` command-response simulator MVP.
- Security Appliance `S-01` to `S-23` questionnaire Excel export/import and sanitized summary parser.
- Rulepack-based evaluator.
- Security advisory generation.
- Excel and Markdown outputs.
- Sensitive-value minimization in generated outputs.
- Realistic lab documentation for parser, rulepack, and report validation.

## Outputs

Default classification generates:

- `evidence.jsonl`
- `results.json`
- `detail.xlsx`
- `summary.xlsx`
- `report.md`
- `security_advisory.md`
- `security_advisory.xlsx`

## Validation

- Test result: `133 passed`
- Build artifacts:
  - `kcii_audit_suite-1.0.0rc1-py3-none-any.whl`
  - `kcii_audit_suite-1.0.0rc1.tar.gz`
- Tag: `v1.0.0rc1`
- Commit: `286a5bd`

## Security Notes

- Raw customer evidence is not committed.
- `out/`, `raw/`, `tmp/`, `dist/`, `.env`, `.venv/`, and `.pytest_cache/` are ignored.
- Generated reports avoid storing full raw evidence.
- Sensitive values such as hostnames, private IPs, account names, domains, SNMP communities, serial numbers, tokens, keys, and certificate bodies must not be included in fixtures or release assets.
- PyPI publishing is intentionally deferred for this release candidate.

## Known Limitations

- This is an offline assessment helper, not a fully automated diagnostic product.
- Many registered items intentionally return `MANUAL_REQUIRED`.
- Security Appliance vendor config parsers are MVP wrappers around sanitized summaries.
- Windows, Network, DBMS, and Unix automatic judgment coverage remains conservative.
- `kcii-netlab-sim` is a command-response simulator, not a full network emulator.
- Real device, GNS3, CML, or Containerlab output comparison still needs further validation.

## Recommended Next Steps

- Publish first to a private GitHub repository as a pre-release.
- Keep wheel and sdist artifacts as GitHub Release assets only.
- Defer PyPI publishing until package naming, licensing, public-scope, and official-tool disclaimer review are complete.
- Continue feature work on a later release candidate or development branch.
