from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from kcii_audit.cli import app
from kcii_audit.engine.evaluator import evaluate_evidence
from kcii_audit.parsers.linux_server import records_from_linux_paste

runner = CliRunner()


def _fixture(name: str) -> str:
    return Path("tests/fixtures/linux_server", name).read_text(encoding="utf-8")


def test_linux_good_fixture_is_classified():
    records = records_from_linux_paste(_fixture("good.json"), asset_id="linux-001")
    results = evaluate_evidence(records)

    assert [record.item_id for record in records] == [f"L-0{i}" for i in range(1, 9)]
    assert all(result.status_label == "양호" for result in results)


def test_linux_vulnerable_fixture_is_classified():
    records = records_from_linux_paste(_fixture("vulnerable.json"), asset_id="linux-001")
    results = evaluate_evidence(records)
    status_by_item = {result.item_id: result.status_label for result in results}

    assert status_by_item["L-01"] == "취약"
    assert status_by_item["L-02"] == "취약"
    assert status_by_item["L-03"] == "취약"
    assert status_by_item["L-04"] == "취약"
    assert status_by_item["L-05"] == "취약"
    assert status_by_item["L-06"] == "취약"
    assert status_by_item["L-07"] == "취약"
    assert status_by_item["L-08"] == "수동확인"


def test_linux_permission_denied_fixture_is_manual_required():
    records = records_from_linux_paste(_fixture("permission_denied.json"), asset_id="linux-001")
    results = evaluate_evidence(records)

    assert len(results) == 8
    assert all(result.status_label == "수동확인" for result in results)
    assert all("필수 evidence 필드" in result.reason for result in results)


def test_linux_unsupported_output_is_manual_required():
    records = records_from_linux_paste(_fixture("unsupported_output.txt"), asset_id="linux-001")
    results = evaluate_evidence(records)

    assert [record.item_id for record in records] == ["L-UNSUPPORTED-OUTPUT"]
    assert [result.status_label for result in results] == ["수동확인"]


def test_linux_classify_file_creates_outputs(tmp_path):
    output_dir = tmp_path / "linux-good"
    result = runner.invoke(
        app,
        [
            "classify-file",
            "--profile",
            "linux",
            "--input",
            "tests/fixtures/linux_server/good.json",
            "--output",
            str(output_dir),
        ],
    )

    assert result.exit_code == 0, result.output
    assert (output_dir / "evidence.jsonl").exists()
    assert (output_dir / "results.json").exists()
    assert (output_dir / "detail.xlsx").exists()
    assert (output_dir / "summary.xlsx").exists()
    assert (output_dir / "report.md").exists()
    assert (output_dir / "security_advisory.md").exists()
    assert (output_dir / "security_advisory.xlsx").exists()

    report = (output_dir / "report.md").read_text(encoding="utf-8")
    assert "kcii-2025-12" in report


def test_linux_classify_paste_with_input_file_creates_outputs(tmp_path):
    output_dir = tmp_path / "linux-good-paste"
    result = runner.invoke(
        app,
        [
            "classify-paste",
            "--profile",
            "linux",
            "--input",
            "tests/fixtures/linux_server/good.json",
            "--output",
            str(output_dir),
        ],
    )

    assert result.exit_code == 0, result.output
    assert (output_dir / "results.json").exists()


def test_linux_sensitive_fixture_values_are_not_stored_in_outputs(tmp_path):
    output_dir = tmp_path / "linux-vulnerable"
    result = runner.invoke(
        app,
        [
            "classify-file",
            "--profile",
            "linux",
            "--input",
            "tests/fixtures/linux_server/vulnerable.json",
            "--output",
            str(output_dir),
        ],
    )

    assert result.exit_code == 0, result.output
    combined_output = (
        (output_dir / "evidence.jsonl").read_text(encoding="utf-8")
        + (output_dir / "results.json").read_text(encoding="utf-8")
        + (output_dir / "report.md").read_text(encoding="utf-8")
    )
    assert "adminroot" not in combined_output
    assert "linux-vulnerable-01" not in combined_output
    assert "192.0.2.20" not in combined_output


def test_linux_evidence_json_contains_only_normalized_fields(tmp_path):
    output_dir = tmp_path / "linux-good"
    runner.invoke(
        app,
        [
            "classify-file",
            "--profile",
            "linux",
            "--input",
            "tests/fixtures/linux_server/good.json",
            "--output",
            str(output_dir),
        ],
    )

    rows = [
        json.loads(line)
        for line in (output_dir / "evidence.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    serialized = json.dumps(rows, ensure_ascii=False)
    assert "raw_accounts" not in serialized
    assert "linux-prod-01" not in serialized
    assert "example.invalid" not in serialized
