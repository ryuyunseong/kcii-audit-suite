# Release Notes

## v1.4.1 Final Release

`v1.4.1`은 commit `1a298ff`에 고정된 최신 공개 정식 GitHub Release입니다. 한글 리소스 손상 복구, 한글 보안장비 질의서 호환성, 전 프로파일 end-to-end 산출물 계약을 검증한 patch release입니다.

상세 변경은 `RELEASE_NOTES_v1.4.1.md`, 검증 기록은 `docs/V1_4_1_READINESS.md`, 현재 지원 범위는 `docs/END_TO_END_SUPPORT_MATRIX.md`에서 확인할 수 있습니다.

### Validation

- 전체 테스트: `189 passed`
- 모든 지원 프로파일 기본 7개 산출물 smoke 통과
- 한글 질의서 export/import와 기존 영어 헤더 import 호환성 검증
- wheel, sdist, checksum 및 clean wheel 설치 검증
- `v1.4.1`과 이전 공개 태그 및 Release asset 불변

## v1.4.0 Final Release

`v1.4.0` is fixed at commit `178369b` and was published as a final private GitHub Release. It established the first baseline product completion point before the repository became public and `v1.4.1` superseded it as the latest patch release.

The detailed v1.4.0 notes are maintained in `RELEASE_NOTES_v1.4.0.md`, the release-readiness checklist is maintained in `docs/V1_4_0_READINESS.md`, and the baseline completion boundary is maintained in `docs/PROJECT_COMPLETION.md`.

### Scope

- Preserve the published `v1.3.0`, `v1.2.0`, `v1.1.0`, `v1.0.0`, `v1.0.0rc2`, and `v1.0.0rc1` tags.
- Add a conservative Junos `display inheritance` parser skeleton.
- Document sanitized fixture requirements for display-set plus display-inheritance evidence pairs.
- Prepare package version metadata as `1.4.0`.
- Separate automatically usable inherited evidence from cases that must remain `MANUAL_REQUIRED`.
- Mark `v1.4.0` as the private baseline product completion release.
- Keep direct device collection, raw live output, device images, license files, public repository conversion, and PyPI/TestPyPI publishing out of scope.

## v1.3.0 Final Release

`v1.3.0` is fixed at commit `30490b4`, pushed to the private GitHub repository, and published as the latest final GitHub Release. It is not a pre-release.

The detailed v1.3.0 notes are maintained in `RELEASE_NOTES_v1.3.0.md`, and the release-readiness checklist is maintained in `docs/V1_3_0_READINESS.md`.

## v1.2.0 Final Release

`v1.2.0` is fixed at commit `9296245`, pushed to the private GitHub repository, and published as a final GitHub Release. It is not a pre-release.

The detailed v1.2.0 notes are maintained in `RELEASE_NOTES_v1.2.0.md`, and the release-readiness checklist is maintained in `docs/V1_2_0_READINESS.md`.

### Scope

- Baseline final release `v1.1.0` remains fixed at `31f624e`.
- The selected feature was Juniper Junos parser MVP.
- Package version metadata is `1.2.0`.
- Parser work must use sanitized offline `show configuration | display set` fixtures only.
- Cisco IOS `N-01` to `N-38` behavior from `v1.1.0` must remain stable.
- Public repository conversion and PyPI/TestPyPI publishing remain out of scope.

### Validation Gate

Release validation completed before creating the `v1.2.0` tag and private GitHub Release:

- full `python -m pytest`
- targeted Network parser tests for Cisco IOS and the new Junos parser
- profile smoke for any newly added Junos fixture
- sensitive placeholder search over generated text and Excel outputs
- wheel/sdist build and checksum generation after package version update
- installed-wheel smoke from a clean environment

### Known Limits

- Juniper Junos parser MVP is implemented for display-set configuration output.
- Junos smoke currently emits all `N-01` to `N-38` items with `GOOD 14` and `MANUAL_REQUIRED 24` for the sanitized good fixture.
- Brace-style, XML, JSON, and inheritance-expanded Junos configuration parsing are out of scope for the MVP.
- FRRouting, Security Appliance enhancements, raw vault, and Unix fixture expansion are separate future scopes unless separately approved.

## v1.3.0 Development History

`dev/v1.3.0` started after the fixed private `v1.2.0` release.

### Scope

- Preserve the published `v1.2.0`, `v1.1.0`, `v1.0.0`, `v1.0.0rc2`, and `v1.0.0rc1` tags.
- Package version metadata is prepared as `1.3.0`.
- Strengthen Junos display-set fixture sanitization guidance.
- Add sanitized realistic Junos display-set fixture coverage for prompt lines, blank lines, spacing variants, inactive statements, and `apply-groups` evidence.
- Keep `apply-groups` and inheritance-dependent evidence in `MANUAL_REQUIRED` or partial-evidence review until a separate inheritance expansion task is approved.
- Fail closed for unsupported Junos XML/JSON input.
- Add Cisco IOS/Junos common Network regression coverage.
- Keep real device, GNS3, CML, or approved lab outputs out of source control unless sanitized.
- Keep PyPI/TestPyPI publishing and public repository conversion out of scope.

### Validation Gate

The current v1.3.0 draft validation after the Junos realistic normalization change is:

- targeted Network tests: `11 passed`
- release readiness tests: `9 passed`
- full `python -m pytest`: `171 passed`
- Junos realistic smoke: 38 results and seven output files
- Junos realistic smoke distribution: `GOOD 14`, `MANUAL_REQUIRED 24`
- wheel/sdist build and checksum generation for package version `1.3.0`
- clean installed-wheel smoke from outside the repository
- secret and forbidden-path scans: no hits

## v1.1.0 Final Release

`v1.1.0` is fixed at commit `31f624e`, pushed to the private GitHub repository, and published as a final GitHub Release. It is not a pre-release.

### Scope

- Baseline final release `v1.0.0` remains fixed at `31983bd`.
- Cisco IOS Network automatic judgment coverage expands from 9 items to 27 items.
- Network `N-01` to `N-38` full result emission is preserved.
- Realistic sanitized Cisco IOS command output compatibility is improved.
- `kcii-netlab-sim` remains a command-response simulator, not a packet or routing emulator.

### Validation Gate

Release validation completed before creating the `v1.1.0` tag and private GitHub Release:

- full `python -m pytest`: `162 passed`
- Network and realistic fixture smoke commands from `docs/V1_1_0_READINESS.md`
- sensitive placeholder search over generated text and Excel outputs
- wheel/sdist build and checksum generation after package version update
- installed-wheel smoke from a clean environment

### Known Limits

- `MANUAL_REQUIRED` remains expected for policy-dependent Network items.
- Real customer configs, live output, device images, and license files remain out of scope.
- PyPI and TestPyPI publishing remain deferred.

## v1.0.0 Final Candidate

This final-candidate branch is prepared from `v1.0.0rc2` and stops feature work. The goal is release stabilization only: documentation, smoke checks, package build, checksum generation, and private GitHub Release preparation.

### Scope

- No new functional scope after `v1.0.0rc2`.
- Package version is `1.0.0`.
- `v1.0.0rc1` remains fixed at `e93d18b`.
- `v1.0.0rc2` remains fixed at `59d3d38`.

### Validation Gate

Before creating a `v1.0.0` tag or private GitHub Release, run:

- full `python -m pytest`
- smoke commands from `docs/V1_0_0_READINESS.md`
- sensitive-value search over generated outputs
- wheel/sdist build and checksum generation
- installed-wheel smoke from a clean environment

### Known Limits

- `MANUAL_REQUIRED` remains expected for many registered items.
- PyPI and TestPyPI publishing remain deferred.
- Public repository conversion remains out of scope.

## v1.0.0-rc2 Candidate

This private release-candidate draft keeps the offline assessment-helper boundary from rc1 and adds the scoped rc2 hardening work completed on `dev/v1.0.0rc2`.

### Scope

- Windows Server `W-01` to `W-64` remains fully registered, with expanded deterministic and partial judgment for selected read-only evidence summaries.
- DBMS `D-01` to `D-26` remains fully registered, with PostgreSQL, MySQL, and MariaDB sanitized JSON/key-value offline parser coverage.
- Linux, Unix, Network, and Security Appliance profiles retain the rc1 scope.
- Default classification still creates the seven-file output bundle.

### Validation Gate

Before creating a `v1.0.0rc2` tag or GitHub pre-release, run:

- full `python -m pytest`
- rc2 smoke commands from `docs/V1_0_0RC2_READINESS.md`
- sensitive-value search over generated outputs
- wheel/sdist build and checksum generation

### Known Limits

- `MANUAL_REQUIRED` remains expected for many registered items.
- DBMS support remains PostgreSQL, MySQL, and MariaDB only.
- PyPI and TestPyPI publishing remain deferred.
- `v1.0.0rc1` is fixed at `e93d18b` and must not be moved.

## v1.0.0-rc1 Candidate

This release candidate freezes the current scope as an offline assessment helper. It is not an official KISA tool, not a production remote collector, and not a fully automated diagnostic product.

### Scope

- Windows Server `W-01` to `W-64` registered with partial automatic judgment.
- Linux Server `L-01` to `L-08` MVP checks.
- Unix Server `U-01` to `U-67` registered with AIX, Solaris, HP-UX, and Linux fixture-based parser support.
- DBMS `D-01` to `D-26` registered with PostgreSQL, MySQL, and MariaDB offline parser support and Docker live SQL verification.
- Network `N-01` to `N-38` registered with Cisco IOS simulator/parser MVP.
- Security Appliance `S-01` to `S-23` registered with questionnaire Excel export/import and sanitized summary parser support.
- Seven-file output bundle generation:
  - `evidence.jsonl`
  - `results.json`
  - `detail.xlsx`
  - `summary.xlsx`
  - `report.md`
  - `security_advisory.md`
  - `security_advisory.xlsx`

### Validation Gate

Release candidate validation must include:

- Clean virtual environment install.
- `kcii-audit --help`, `classify-file --help`, and `questionnaire --help` smoke checks.
- Profile smoke checks for Windows, Linux, Unix, DBMS, Network, and Security Appliance.
- `--no-advisory` smoke check.
- Full `python -m pytest`.
- Sensitive-content search over generated outputs.

### Known Limits

- Many official items intentionally return `MANUAL_REQUIRED`.
- Vendor-specific security appliance config parsers are MVP wrappers around sanitized summaries.
- Windows, Network, DBMS, and Unix automatic judgment coverage is intentionally conservative.
- The private GitHub pre-release is fixed at commit `e93d18b` with annotated tag `v1.0.0rc1`.
- Follow-up work continued on `dev/v1.0.0rc2`; do not move the `v1.0.0rc1` tag.
- PyPI publishing is intentionally deferred.

### Security Notes

Do not include real customer evidence, raw configs, `.env`, generated `out/`, raw vault files, passwords, hashes, tokens, keys, certificate bodies, internal URLs, hostnames, account names, serial numbers, policy names, object names, or IP addresses in source control.
