from __future__ import annotations

import json

from typer.testing import CliRunner

from kcii_audit.cli import app

runner = CliRunner()


def test_scan_creates_scaffold_outputs(tmp_path):
    result = runner.invoke(
        app,
        ["scan", "--target", "local", "--profile", "linux", "--output", str(tmp_path)],
    )

    assert result.exit_code == 0, result.output
    assert (tmp_path / "evidence.jsonl").exists()
    assert (tmp_path / "results.json").exists()
    assert (tmp_path / "detail.xlsx").exists()
    assert (tmp_path / "summary.xlsx").exists()
    assert (tmp_path / "report.md").exists()
    assert (tmp_path / "security_advisory.md").exists()
    assert (tmp_path / "security_advisory.xlsx").exists()

    results = json.loads((tmp_path / "results.json").read_text(encoding="utf-8"))
    assert results["results"][0]["status"] == "MANUAL_REQUIRED"
    assert results["results"][0]["item_id"] == "STUB-LINUX-001"


def test_evaluate_reads_evidence_jsonl(tmp_path):
    scan_dir = tmp_path / "scan"
    runner.invoke(app, ["scan", "--output", str(scan_dir)])

    output = tmp_path / "results.json"
    result = runner.invoke(
        app,
        ["evaluate", "--evidence", str(scan_dir / "evidence.jsonl"), "--output", str(output)],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["results"][0]["status"] == "MANUAL_REQUIRED"


def test_report_reads_results_json(tmp_path):
    scan_dir = tmp_path / "scan"
    runner.invoke(app, ["scan", "--output", str(scan_dir)])

    report_path = tmp_path / "report.md"
    result = runner.invoke(
        app,
        ["report", "--results", str(scan_dir / "results.json"), "--output", str(report_path)],
    )

    assert result.exit_code == 0, result.output
    assert "K-CII 점검 결과 보고서" in report_path.read_text(encoding="utf-8")
