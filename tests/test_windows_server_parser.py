from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from kcii_audit.cli import app
from kcii_audit.engine.evaluator import evaluate_evidence
from kcii_audit.parsers.windows_server import records_from_windows_paste
from kcii_audit.schemas.result import AssessmentStatus

FIXTURE_DIR = Path("tests/fixtures/windows_server")
runner = CliRunner()


def _statuses_for_fixture(name: str) -> dict[str, AssessmentStatus]:
    text = (FIXTURE_DIR / name).read_text(encoding="utf-8")
    records = records_from_windows_paste(text, asset_id="win-rc2")
    results = evaluate_evidence(records)
    assert [record.item_id for record in records] == [f"W-{index:02d}" for index in range(1, 65)]
    return {result.item_id: result.status for result in results}


def _evidence_for_fixture(name: str) -> dict[str, dict]:
    text = (FIXTURE_DIR / name).read_text(encoding="utf-8")
    records = records_from_windows_paste(text, asset_id="win-rc2")
    return {record.item_id: record.evidence for record in records}


def test_windows_rc2_good_fixture_expands_good_automatic_results():
    statuses = _statuses_for_fixture("good.json")

    for item_id in ["W-09", "W-17", "W-18", "W-21", "W-29", "W-40", "W-42"]:
        assert statuses[item_id] == AssessmentStatus.GOOD


def test_windows_rc2_vulnerable_fixture_expands_vulnerable_results():
    statuses = _statuses_for_fixture("vulnerable.json")

    for item_id in ["W-09", "W-17", "W-18", "W-21", "W-29", "W-40", "W-42"]:
        assert statuses[item_id] == AssessmentStatus.VULNERABLE


def test_windows_rc2_permission_denied_is_manual_required():
    statuses = _statuses_for_fixture("permission_denied.json")

    assert statuses["W-17"] == AssessmentStatus.MANUAL_REQUIRED
    assert statuses["W-40"] == AssessmentStatus.MANUAL_REQUIRED


def test_windows_rc2_unsupported_text_keeps_all_items_manual_required():
    statuses = _statuses_for_fixture("unsupported_output.txt")

    assert set(statuses.values()) == {AssessmentStatus.MANUAL_REQUIRED}


def test_windows_rc2_secedit_text_updates_password_policy_summary():
    good_statuses = _statuses_for_fixture("secedit_good.txt")
    vulnerable_statuses = _statuses_for_fixture("secedit_vulnerable.txt")
    evidence = _evidence_for_fixture("secedit_good.txt")

    assert good_statuses["W-09"] == AssessmentStatus.GOOD
    assert vulnerable_statuses["W-09"] == AssessmentStatus.VULNERABLE
    assert evidence["W-09"]["password_policy_ok"] is True
    assert evidence["W-09"]["password_complexity_enabled"] is True
    assert evidence["W-09"]["password_history_size"] == 12


def test_windows_rc2_auditpol_text_updates_audit_policy_summary():
    good_statuses = _statuses_for_fixture("auditpol_good.txt")
    vulnerable_statuses = _statuses_for_fixture("auditpol_vulnerable.txt")

    assert good_statuses["W-40"] == AssessmentStatus.GOOD
    assert vulnerable_statuses["W-40"] == AssessmentStatus.VULNERABLE


def test_windows_rc2_cli_generates_seven_outputs_and_advisory(tmp_path):
    output_dir = tmp_path / "windows-rc2"
    result = runner.invoke(
        app,
        [
            "classify-file",
            "--profile",
            "windows",
            "--input",
            str(FIXTURE_DIR / "vulnerable.json"),
            "--output",
            str(output_dir),
        ],
    )

    assert result.exit_code == 0, result.output
    for expected in [
        "evidence.jsonl",
        "results.json",
        "detail.xlsx",
        "summary.xlsx",
        "report.md",
        "security_advisory.md",
        "security_advisory.xlsx",
    ]:
        assert (output_dir / expected).exists(), expected

    results = json.loads((output_dir / "results.json").read_text(encoding="utf-8"))
    status_by_item = {item["item_id"]: item["status"] for item in results["results"]}
    assert status_by_item["W-17"] == "VULNERABLE"
    assert status_by_item["W-42"] == "VULNERABLE"
    assert "W-17" in (output_dir / "security_advisory.md").read_text(encoding="utf-8")


def test_windows_rc2_outputs_do_not_store_sensitive_fixture_values(tmp_path):
    output_dir = tmp_path / "windows-mixed"
    result = runner.invoke(
        app,
        [
            "classify-file",
            "--profile",
            "windows",
            "--input",
            str(FIXTURE_DIR / "mixed.json"),
            "--output",
            str(output_dir),
        ],
    )

    assert result.exit_code == 0, result.output
    combined = "\n".join(
        [
            (output_dir / "evidence.jsonl").read_text(encoding="utf-8"),
            (output_dir / "results.json").read_text(encoding="utf-8"),
            (output_dir / "report.md").read_text(encoding="utf-8"),
            (output_dir / "security_advisory.md").read_text(encoding="utf-8"),
        ]
    )
    for forbidden in [
        "win-prod-01",
        "example.invalid",
        "S-1-5-21",
        "C:\\Windows\\System32\\winevt\\Logs\\Security.evtx",
        "ADMIN$",
        "C$",
    ]:
        assert forbidden not in combined
