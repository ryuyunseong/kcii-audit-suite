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
        Path("RELEASE_NOTES_v1.2.0.md"),
        Path("RELEASE_NOTES_v1.1.0.md"),
        Path("RELEASE_NOTES_v1.0.0.md"),
        Path("RELEASE_NOTES_v1.0.0rc2.md"),
        Path("CHANGELOG.md"),
        Path("docs/RELEASE_CHECKLIST.md"),
        Path("docs/PROFILE_COVERAGE.md"),
        Path("docs/V1_2_0_READINESS.md"),
        Path("docs/V1_1_0_READINESS.md"),
        Path("docs/NETWORK_OUTPUT_SANITIZATION.md"),
        Path("docs/V1_0_0_READINESS.md"),
        Path("docs/V1_0_0RC2_READINESS.md"),
    ]
    readme = Path("README.md").read_text(encoding="utf-8")

    for path in required:
        assert path.exists(), path
        assert str(path).replace("\\", "/") in readme


def test_readme_states_release_boundary_and_offline_model():
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "not an official KISA tool" in readme
    assert "not a remote automatic collector" in readme
    assert "Windows work PC" in readme
    assert "MANUAL_REQUIRED" in readme
    assert "security_advisory.md" in readme
    assert "security_advisory.xlsx" in readme
    assert "Docker, Containerlab, GNS3, EVE-NG" in readme


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
        assert "offline" in result.output.lower()


def test_release_version_is_final_candidate():
    assert __version__ == "1.2.0"


def test_release_documents_state_v1_2_0_released_and_v1_3_0_development_status():
    readme = Path("README.md").read_text(encoding="utf-8")
    release_index = Path("RELEASE_NOTES.md").read_text(encoding="utf-8")
    release_notes_v1_2_0 = Path("RELEASE_NOTES_v1.2.0.md").read_text(encoding="utf-8")
    release_notes = Path("RELEASE_NOTES_v1.1.0.md").read_text(encoding="utf-8")
    readiness_v1_2_0 = Path("docs/V1_2_0_READINESS.md").read_text(encoding="utf-8")
    coverage = Path("docs/PROFILE_COVERAGE.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")

    for text in [readme, release_index, release_notes, readiness_v1_2_0, coverage, changelog]:
        assert "v1.1.0" in text
        assert "31f624e" in text

    for text in [readme, release_index, release_notes_v1_2_0, readiness_v1_2_0, coverage, changelog]:
        assert "v1.2.0" in text
        assert "9296245" in text

    assert "latest final GitHub Release" in readme
    assert "is the final private GitHub Release" in release_notes
    assert "dev/v1.3.0" in readme
    assert "`v1.2.0` is fixed at commit `9296245`" in release_index
    assert "No `v1.3.0` tag or GitHub Release has been created." in release_index
    assert "private GitHub Release" in release_notes_v1_2_0
    assert "`v1.2.0` tag: not created" not in readiness_v1_2_0
    assert "Juniper Junos parser MVP" in coverage
    assert "v1.3.0 Development Scope" in coverage
    assert "show configuration | display set" in release_notes_v1_2_0
    assert "GOOD 14" in release_notes_v1_2_0
    assert "MANUAL_REQUIRED 24" in release_notes_v1_2_0


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
            Path("RELEASE_NOTES.md"),
            Path("RELEASE_NOTES_v1.2.0.md"),
            Path("RELEASE_NOTES_v1.1.0.md"),
            Path("RELEASE_NOTES_v1.0.0.md"),
            Path("RELEASE_NOTES_v1.0.0rc2.md"),
            Path("CHANGELOG.md"),
            Path("docs/RELEASE_CHECKLIST.md"),
            Path("docs/PROFILE_COVERAGE.md"),
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
