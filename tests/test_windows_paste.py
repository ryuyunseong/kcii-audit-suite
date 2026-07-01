from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from kcii_audit.cli import app
from kcii_audit.engine.evaluator import evaluate_evidence
from kcii_audit.parsers.windows_server import records_from_windows_paste
from kcii_audit.schemas.result import AssessmentStatus

runner = CliRunner()


@pytest.mark.parametrize(
    ("fixture", "expected"),
    [
        ("net-accounts-en-vulnerable.txt", [("W-09", "minimum_password_length", 0, AssessmentStatus.VULNERABLE)]),
        ("net-accounts-ko-good.txt", [("W-09", "minimum_password_length", 12, AssessmentStatus.GOOD)]),
        ("net-user-guest-en-good.txt", [("W-02", "guest_account_enabled", False, AssessmentStatus.GOOD)]),
        ("net-user-guest-ko-vulnerable.txt", [("W-02", "guest_account_enabled", True, AssessmentStatus.VULNERABLE)]),
        ("firewall-powershell-good.txt", [("W-64", "firewall_enabled", True, AssessmentStatus.GOOD)]),
        ("firewall-powershell-vulnerable.txt", [("W-64", "firewall_enabled", False, AssessmentStatus.VULNERABLE)]),
        ("firewall-format-list-good.txt", [("W-64", "firewall_enabled", True, AssessmentStatus.GOOD)]),
        (
            "mixed-sensitive-vulnerable.txt",
            [
                ("W-02", "guest_account_enabled", True, AssessmentStatus.VULNERABLE),
                ("W-64", "firewall_enabled", False, AssessmentStatus.VULNERABLE),
                ("W-09", "minimum_password_length", 6, AssessmentStatus.VULNERABLE),
            ],
        ),
    ],
)
def test_windows_realistic_paste_fixtures_are_classified(fixture, expected):
    text = Path("tests/fixtures/windows/paste", fixture).read_text(encoding="utf-8")
    records = records_from_windows_paste(text, asset_id="win-001")
    results = evaluate_evidence(records)

    by_item = {record.item_id: record for record in records}
    by_result = {result.item_id: result for result in results}

    assert [record.item_id for record in records] == [f"W-{index:02d}" for index in range(1, 65)]
    for item_id, evidence_key, evidence_value, status in expected:
        assert by_item[item_id].evidence[evidence_key] == evidence_value
        assert by_result[item_id].status == status


def test_windows_key_value_paste_is_classified():
    text = Path("tests/fixtures/windows/paste/good-key-value.txt").read_text(encoding="utf-8")
    records = records_from_windows_paste(text, asset_id="win-001")

    results = evaluate_evidence(records)

    assert [result.item_id for result in results] == [f"W-{index:02d}" for index in range(1, 65)]
    status_by_item = {result.item_id: result.status for result in results}
    assert status_by_item["W-02"] == AssessmentStatus.GOOD
    assert status_by_item["W-09"] == AssessmentStatus.GOOD
    assert status_by_item["W-64"] == AssessmentStatus.GOOD
    assert status_by_item["W-03"] == AssessmentStatus.MANUAL_REQUIRED


def test_windows_vulnerable_key_value_paste_is_classified():
    text = Path("tests/fixtures/windows/paste/vulnerable-key-value.txt").read_text(encoding="utf-8")
    records = records_from_windows_paste(text, asset_id="win-001")

    results = evaluate_evidence(records)

    status_by_item = {result.item_id: result.status for result in results}
    assert status_by_item["W-02"] == AssessmentStatus.VULNERABLE
    assert status_by_item["W-09"] == AssessmentStatus.VULNERABLE
    assert status_by_item["W-64"] == AssessmentStatus.VULNERABLE


def test_windows_missing_fixture_is_manual_required_for_missing_rulepack_field():
    text = Path("tests/fixtures/windows/paste/manual-collector.json").read_text(encoding="utf-8")
    records = records_from_windows_paste(text, asset_id="win-001")

    results = evaluate_evidence(records)

    status_by_item = {result.item_id: result.status for result in results}
    assert status_by_item["W-03"] == AssessmentStatus.MANUAL_REQUIRED
    assert status_by_item["W-02"] == AssessmentStatus.MANUAL_REQUIRED


def test_windows_json_paste_is_classified_by_cli(tmp_path):
    paste_path = tmp_path / "windows.json"
    output_dir = tmp_path / "out"
    paste_path.write_text(
        Path("tests/fixtures/windows/paste/good-collector.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        ["classify-paste", "--profile", "windows", "--input", str(paste_path), "--output", str(output_dir)],
    )

    assert result.exit_code == 0, result.output
    results = json.loads((output_dir / "results.json").read_text(encoding="utf-8"))
    assert len(results["results"]) == 64
    status_by_item = {item["item_id"]: item["status"] for item in results["results"]}
    assert status_by_item["W-02"] == "GOOD"
    assert status_by_item["W-09"] == "GOOD"
    assert status_by_item["W-64"] == "GOOD"


def test_windows_json_file_is_classified_by_cli_alias(tmp_path):
    paste_path = tmp_path / "windows.json"
    output_dir = tmp_path / "out"
    paste_path.write_text(
        Path("tests/fixtures/windows/paste/good-collector.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        ["classify-file", "--profile", "windows", "--input", str(paste_path), "--output", str(output_dir)],
    )

    assert result.exit_code == 0, result.output
    results = json.loads((output_dir / "results.json").read_text(encoding="utf-8"))
    assert len(results["results"]) == 64
    status_by_item = {item["item_id"]: item["status"] for item in results["results"]}
    assert status_by_item["W-02"] == "GOOD"
    assert status_by_item["W-09"] == "GOOD"
    assert status_by_item["W-64"] == "GOOD"


def test_windows_utf16_file_is_classified_by_cli_alias(tmp_path):
    paste_path = tmp_path / "windows-utf16.json"
    output_dir = tmp_path / "out"
    paste_path.write_text(
        Path("tests/fixtures/windows/paste/good-collector.json").read_text(encoding="utf-8"),
        encoding="utf-16",
    )

    result = runner.invoke(
        app,
        ["classify-file", "--profile", "windows", "--input", str(paste_path), "--output", str(output_dir)],
    )

    assert result.exit_code == 0, result.output
    results = json.loads((output_dir / "results.json").read_text(encoding="utf-8"))
    status_by_item = {item["item_id"]: item["status"] for item in results["results"]}
    assert len(results["results"]) == 64
    assert status_by_item["W-02"] == "GOOD"
    assert status_by_item["W-09"] == "GOOD"
    assert status_by_item["W-64"] == "GOOD"


def test_mixed_sensitive_paste_does_not_store_raw_text_in_outputs(tmp_path):
    paste_path = Path("tests/fixtures/windows/paste/mixed-sensitive-vulnerable.txt")
    output_dir = tmp_path / "out"

    result = runner.invoke(
        app,
        ["classify-paste", "--profile", "windows", "--input", str(paste_path), "--output", str(output_dir)],
    )

    assert result.exit_code == 0, result.output
    combined_output = (
        (output_dir / "evidence.jsonl").read_text(encoding="utf-8")
        + (output_dir / "results.json").read_text(encoding="utf-8")
        + (output_dir / "report.md").read_text(encoding="utf-8")
    )
    assert "SERVER01" not in combined_output
    assert "example.invalid" not in combined_output
    assert "S-1-5-21" not in combined_output
    assert "C:\\Users\\Guest" not in combined_output
