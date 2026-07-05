# Public Portfolio Readiness

This document tracks what must be true before this repository is made public for portfolio use.

## Current Decision

The project can be prepared as a public portfolio repository, but public conversion itself is a separate action. Do not change repository visibility until the checklist below is reviewed.

Changing repository visibility to public must be an explicit, final action after this checklist passes.

## Blocking Checks Before Public Visibility

- Choose and add a repository license or intentionally keep all rights reserved.
- Replace or clarify `pyproject.toml` license metadata if the selected public license changes.
- Re-check that fixtures are synthetic and sanitized.
- Confirm no real customer evidence, live output, commercial device images, license files, `.env`, raw outputs, or generated reports are tracked.
- Confirm README states the tool is not an official KISA tool.
- Confirm release assets are not replaced during public conversion.

## Non-Blocking But Recommended

- Add a short Korean portfolio summary link near the top of README.
- Keep detailed release history in docs instead of the first screen.
- Add screenshots only if they are generated from synthetic fixtures.
- Keep PyPI/TestPyPI publishing deferred unless separately approved.
- Enable GitHub secret scanning and Dependabot alerts when repository settings allow it.

## Public Content Boundary

Allowed:

- source code
- synthetic fixtures
- sanitized sample outputs generated from synthetic fixtures
- README, portfolio summary, and release documentation
- rulepack metadata and concise source notes

Not allowed:

- real customer files
- raw operational evidence
- passwords, password hashes, tokens, keys, or certificates
- hostnames, account names, IP addresses, serial numbers, object names, policy names, or license files from real environments
- proprietary device images or VM disks

## Portfolio Positioning

The public repository should present the project as:

- an offline infrastructure security assessment helper
- a rulepack and parser-based automation project
- a conservative security reporting workflow
- a packaging, testing, and release-engineering example

Avoid presenting it as:

- an official KISA tool
- a fully automated vulnerability scanner
- a production remote collector
- a tool that stores raw customer evidence

## Final Public Conversion Gate

Before making the repository public, run:

```powershell
git status --short --branch
python -m pytest
git diff --check
git ls-files | Select-String -Pattern '^(out/|raw/|tmp/|dist/|\\.env)'
```

Then review the public GitHub page after visibility changes:

- README renders correctly.
- License state is intentional.
- Release tags still point to the expected commits.
- No generated or private-only files are visible.
