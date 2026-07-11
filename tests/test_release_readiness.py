from __future__ import annotations

from importlib.resources import files
from pathlib import Path

from typer.testing import CliRunner

from kcii_audit import __version__
from kcii_audit.cli import app
from kcii_audit.engine.rulepack import load_default_rulepack

runner = CliRunner()


def test_release_documents_exist_and_are_linked_from_readme():
    required = [
        Path("RELEASE_NOTES.md"),
        Path("PORTFOLIO.md"),
        Path("RELEASE_NOTES_v1.4.0.md"),
        Path("RELEASE_NOTES_v1.4.1.md"),
        Path("RELEASE_NOTES_v1.3.0.md"),
        Path("RELEASE_NOTES_v1.2.0.md"),
        Path("RELEASE_NOTES_v1.1.0.md"),
        Path("RELEASE_NOTES_v1.0.0.md"),
        Path("RELEASE_NOTES_v1.0.0rc2.md"),
        Path("CHANGELOG.md"),
        Path("docs/RELEASE_CHECKLIST.md"),
        Path("docs/PUBLIC_READINESS.md"),
        Path("docs/PROJECT_COMPLETION.md"),
        Path("docs/MAINTENANCE_POLICY.md"),
        Path("docs/PROFILE_COVERAGE.md"),
        Path("docs/END_TO_END_SUPPORT_MATRIX.md"),
        Path("docs/JUNOS_DISPLAY_INHERITANCE_DESIGN.md"),
        Path("docs/V1_4_0_READINESS.md"),
        Path("docs/V1_4_1_READINESS.md"),
        Path("docs/V1_3_0_READINESS.md"),
        Path("docs/V1_2_0_READINESS.md"),
        Path("docs/V1_1_0_READINESS.md"),
        Path("docs/NETWORK_OUTPUT_SANITIZATION.md"),
        Path("docs/V1_0_0_READINESS.md"),
        Path("docs/V1_0_0RC2_READINESS.md"),
        Path("examples/portfolio-preview/README.md"),
    ]
    readme = Path("README.md").read_text(encoding="utf-8")

    for path in required:
        assert path.exists(), path
        assert str(path).replace("\\", "/") in readme


def test_readme_states_release_boundary_and_offline_model():
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "KISA 공식 도구가 아니며" in readme
    assert "직접 원격 접속하지 않습니다" in readme
    assert "Windows 작업 PC" in readme
    assert "MANUAL_REQUIRED" in readme
    assert "security_advisory.md" in readme
    assert "security_advisory.xlsx" in readme
    assert "Docker Compose, Containerlab, GNS3, EVE-NG" in readme
    assert "포트폴리오 요약" in readme
    assert "공개 및 라이선스" in readme
    assert "PORTFOLIO.md" in readme
    assert "docs/PUBLIC_READINESS.md" in readme
    assert "examples/portfolio-preview/README.md" in readme
    assert "v1.4.1 Release" in readme
    assert "모든 권리는 저작자에게" in readme
    assert "재사용, 재배포 또는 파생 저작물" in readme


def test_profile_coverage_document_mentions_every_profile_and_counts():
    coverage = Path("docs/PROFILE_COVERAGE.md").read_text(encoding="utf-8")

    for expected in [
        "Windows Server",
        "Linux Server",
        "Unix Server",
        "DBMS",
        "Network",
        "Security Appliance",
        "`W-01` to `W-64`",
        "`L-01` to `L-08`",
        "`U-01` to `U-67`",
        "`D-01` to `D-26`",
        "`N-01` to `N-38`",
        "`S-01` to `S-23`",
        "| Windows Server | 64 | 8 | 7 | 49 |",
        "| Security Appliance | 23 | 0 | 23 | 0 |",
    ]:
        assert expected in coverage


def test_gitignore_excludes_release_generated_and_sensitive_paths():
    ignored = set(Path(".gitignore").read_text(encoding="utf-8").splitlines())

    for expected in ["out/", "raw/", "tmp/", ".env", ".env.*", "!.env.example"]:
        assert expected in ignored


def test_cli_help_smoke_for_release_commands():
    commands = [
        ["--help"],
        ["classify-file", "--help"],
        ["questionnaire", "--help"],
    ]

    for command in commands:
        result = runner.invoke(app, command)
        assert result.exit_code == 0, result.output
        assert "오프라인" in result.output


def test_release_version_is_final_candidate():
    assert __version__ == "1.4.1"


def test_release_documents_state_current_releases_and_v1_4_0_completion():
    readme = Path("README.md").read_text(encoding="utf-8")
    release_index = Path("RELEASE_NOTES.md").read_text(encoding="utf-8")
    release_notes_v1_4_0 = Path("RELEASE_NOTES_v1.4.0.md").read_text(encoding="utf-8")
    release_notes_v1_4_1 = Path("RELEASE_NOTES_v1.4.1.md").read_text(encoding="utf-8")
    release_notes_v1_3_0 = Path("RELEASE_NOTES_v1.3.0.md").read_text(encoding="utf-8")
    release_notes_v1_2_0 = Path("RELEASE_NOTES_v1.2.0.md").read_text(encoding="utf-8")
    release_notes = Path("RELEASE_NOTES_v1.1.0.md").read_text(encoding="utf-8")
    readiness_v1_4_0 = Path("docs/V1_4_0_READINESS.md").read_text(encoding="utf-8")
    readiness_v1_4_1 = Path("docs/V1_4_1_READINESS.md").read_text(encoding="utf-8")
    readiness_v1_3_0 = Path("docs/V1_3_0_READINESS.md").read_text(encoding="utf-8")
    readiness_v1_2_0 = Path("docs/V1_2_0_READINESS.md").read_text(encoding="utf-8")
    coverage = Path("docs/PROFILE_COVERAGE.md").read_text(encoding="utf-8")
    completion = Path("docs/PROJECT_COMPLETION.md").read_text(encoding="utf-8")
    maintenance = Path("docs/MAINTENANCE_POLICY.md").read_text(encoding="utf-8")
    portfolio = Path("PORTFOLIO.md").read_text(encoding="utf-8")
    public_readiness = Path("docs/PUBLIC_READINESS.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")

    for text in [release_index, release_notes, readiness_v1_2_0, coverage, changelog]:
        assert "v1.1.0" in text
        assert "31f624e" in text

    for text in [release_index, release_notes_v1_2_0, readiness_v1_2_0, coverage, changelog]:
        assert "v1.2.0" in text
        assert "9296245" in text

    assert "최신 릴리스" in readme
    assert "최신 릴리스: `v1.4.1`" in readme
    assert "is the final private GitHub Release" in release_notes
    assert "최신 `v1.4.1` Release 기준 전체 테스트는 `189 passed`" in readme
    assert "dev/v1.4.2" in readme
    assert "dev/v1.5.0" in readme
    assert "`v1.2.0` is fixed at commit `9296245`" in release_index
    assert "`v1.3.0` is fixed at commit `30490b4`" in release_index
    assert "`kcii-audit-suite v1.3.0` is the final private GitHub Release" in release_notes_v1_3_0
    assert "`v1.3.0` is tagged, pushed, and published as a final private GitHub Release" in readiness_v1_3_0
    assert "Package version metadata: `1.3.0`" in readiness_v1_3_0
    assert "Latest Junos realistic normalization commit: `7077334`" in readiness_v1_3_0
    assert "display_set_realistic_sanitized.txt" in release_notes_v1_3_0
    assert "GOOD 14" in release_notes_v1_3_0
    assert "MANUAL_REQUIRED 24" in release_notes_v1_3_0
    assert "complete `groups`, `apply-groups`, and inheritance expansion" in readiness_v1_3_0
    assert "private GitHub Release" in release_notes_v1_2_0
    assert "`v1.2.0` tag: not created" not in readiness_v1_2_0
    assert "Juniper Junos parser MVP" in coverage
    assert "v1.4.0 Release Scope" in coverage
    assert "현재 공개 포트폴리오의 최신 정식 릴리스는 `v1.4.1`" in coverage
    assert "display inheritance" in coverage
    assert "RELEASE_NOTES_v1.4.0.md" in readme
    assert "docs/V1_4_0_READINESS.md" in readme
    assert "docs/PROJECT_COMPLETION.md" in readme
    assert "docs/MAINTENANCE_POLICY.md" in readme
    assert "`v1.4.0` is fixed at commit `178369b`" in release_index
    assert "`kcii-audit-suite v1.4.0` is the final private GitHub Release" in release_notes_v1_4_0
    assert "`v1.4.0` tag fixed at `178369b`" in release_notes_v1_4_0
    assert "Latest Junos inheritance parser skeleton commit: `5cb5d7d`" in readiness_v1_4_0
    assert "Release metadata commit: `178369b`" in readiness_v1_4_0
    assert "Package version metadata: `1.4.0`" in readiness_v1_4_0
    assert "`v1.4.0` tag remains fixed at `178369b`" in readiness_v1_4_0
    assert "GitHub Release for `v1.4.0`: final private release" in readiness_v1_4_0
    assert "GOOD 4" in release_notes_v1_4_0
    assert "MANUAL_REQUIRED 34" in release_notes_v1_4_0
    assert "full profile smoke: passed" in release_notes_v1_4_0
    assert "installed-wheel smoke from a clean non-repository working directory: OK" in release_notes_v1_4_0
    assert "kcii_audit_suite-1.4.0-py3-none-any.whl" in readiness_v1_4_0
    assert "clean installed-wheel smoke: passed" in readiness_v1_4_0
    assert "conflicting inherited values keep all items `MANUAL_REQUIRED`" in readiness_v1_4_0
    assert "Package version metadata: `1.4.1`" in readiness_v1_4_1
    assert "kcii_audit_suite-1.4.1-py3-none-any.whl" in readiness_v1_4_1
    assert "한글 질의서 export/import" in readiness_v1_4_1
    assert "v1.4.0" in release_notes_v1_4_1
    assert "MANUAL_REQUIRED" in release_notes_v1_4_1
    assert "baseline product completion" in completion
    assert "최신 릴리스: `v1.4.1`" in completion
    assert "전체 테스트: `189 passed`" in completion
    assert "`dev/v1.4.2`: 문서 수정과 좁은 범위의 버그 수정" in completion
    assert "`dev/v1.5.0`: 하위 호환 신규 기능" in completion
    assert "Published release tags and assets are immutable" in maintenance
    assert "PyPI/TestPyPI 배포와 저장소 라이선스 변경은 별도 승인" in maintenance
    assert "오프라인 보안 진단 자동화 도구" in portfolio
    assert "MANUAL_REQUIRED" in portfolio
    assert "포트폴리오 검토 목적" in portfolio
    assert "무단 복제, 수정, 재배포" in portfolio
    assert "visibility: PUBLIC" in public_readiness
    assert "All rights reserved / Proprietary" in public_readiness
    assert "Public visibility is for review, not open-source reuse" in public_readiness
    assert "No permission is granted for reuse, redistribution, or derivative works" in public_readiness
    assert "not an official KISA tool" in public_readiness
    assert "최신 릴리스: `v1.4.1` (`1a298ff`)" in public_readiness
    assert "전체 테스트: `189 passed`" in public_readiness
    assert "show configuration | display set" in release_notes_v1_2_0
    assert "GOOD 14" in release_notes_v1_2_0
    assert "MANUAL_REQUIRED 24" in release_notes_v1_2_0


def test_portfolio_preview_contains_expected_synthetic_outputs():
    preview_root = Path("examples/portfolio-preview")
    generated = preview_root / "generated"
    expected = {
        "evidence.jsonl",
        "results.json",
        "detail.xlsx",
        "summary.xlsx",
        "report.md",
        "security_advisory.md",
        "security_advisory.xlsx",
    }

    assert (preview_root / "README.md").exists()
    assert (preview_root / "INPUT_AND_SANITIZATION.md").exists()
    assert {path.name for path in generated.iterdir() if path.is_file()} == expected

    preview = (preview_root / "README.md").read_text(encoding="utf-8")
    boundary = (preview_root / "INPUT_AND_SANITIZATION.md").read_text(encoding="utf-8")
    assert "합성 Windows Server 증적" in preview
    assert "tests\\fixtures\\windows_server\\vulnerable.json" in preview
    assert "취약 | 7" in preview
    assert "수동확인 | 57" in preview
    assert "실제 고객" in boundary
    assert "raw_evidence_hash" in boundary

    for path in [preview_root / "README.md", preview_root / "INPUT_AND_SANITIZATION.md"]:
        text = path.read_text(encoding="utf-8")
        assert "\ufffd" not in text
        assert "???" not in text


def test_packaged_runtime_resources_are_available_from_non_repo_cwd(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    windows_rulepack = load_default_rulepack("kcii-2025-12", "windows")
    dbms_rulepack = load_default_rulepack("kcii-2025-12", "dbms")

    assert windows_rulepack is not None
    assert len(windows_rulepack.items) == 64
    assert dbms_rulepack is not None
    assert len(dbms_rulepack.items) == 26

    questionnaire = files("kcii_audit.resources").joinpath(
        "questionnaires",
        "templates",
        "security_appliance_questionnaire.xlsx",
    )
    assert questionnaire.is_file()


def test_release_documents_do_not_include_sensitive_fixture_placeholders():
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            Path("README.md"),
            Path("PORTFOLIO.md"),
            Path("RELEASE_NOTES.md"),
            Path("RELEASE_NOTES_v1.4.0.md"),
            Path("RELEASE_NOTES_v1.4.1.md"),
            Path("RELEASE_NOTES_v1.3.0.md"),
            Path("RELEASE_NOTES_v1.2.0.md"),
            Path("RELEASE_NOTES_v1.1.0.md"),
            Path("RELEASE_NOTES_v1.0.0.md"),
            Path("RELEASE_NOTES_v1.0.0rc2.md"),
            Path("CHANGELOG.md"),
            Path("docs/RELEASE_CHECKLIST.md"),
            Path("docs/PUBLIC_READINESS.md"),
            Path("docs/PROJECT_COMPLETION.md"),
            Path("docs/MAINTENANCE_POLICY.md"),
            Path("docs/PROFILE_COVERAGE.md"),
            Path("docs/JUNOS_DISPLAY_INHERITANCE_DESIGN.md"),
            Path("docs/V1_4_0_READINESS.md"),
            Path("docs/V1_4_1_READINESS.md"),
            Path("docs/V1_3_0_READINESS.md"),
            Path("docs/V1_2_0_READINESS.md"),
            Path("docs/V1_1_0_READINESS.md"),
            Path("docs/V1_0_0_READINESS.md"),
            Path("docs/V1_0_0RC2_READINESS.md"),
        ]
    )

    for forbidden in [
        "APPLIANCE_ADMIN",
        "fw-prod-01",
        "Allow-Customer-Core",
        "CustomerObject",
        "FGT0000000000",
        "not-a-real-token",
    ]:
        assert forbidden not in combined


def test_runtime_resources_do_not_contain_damaged_korean_markers():
    paths = [
        Path("rulepacks/kcii-2025-12/unix.yaml"),
        Path("rulepacks/kcii-2025-12/unix_items_manifest.yaml"),
        Path("rulepacks/kcii-2025-12/security_appliance.yaml"),
        Path("rulepacks/kcii-2025-12/security_appliance_items_manifest.yaml"),
        Path("questionnaires/security_appliance_schema.yaml"),
        Path("src/kcii_audit/resources/rulepacks/kcii-2025-12/unix.yaml"),
        Path("src/kcii_audit/resources/rulepacks/kcii-2025-12/unix_items_manifest.yaml"),
        Path("src/kcii_audit/resources/rulepacks/kcii-2025-12/security_appliance.yaml"),
        Path("src/kcii_audit/resources/rulepacks/kcii-2025-12/security_appliance_items_manifest.yaml"),
        Path("src/kcii_audit/resources/questionnaires/security_appliance_schema.yaml"),
    ]

    for path in paths:
        assert "???" not in path.read_text(encoding="utf-8"), path
