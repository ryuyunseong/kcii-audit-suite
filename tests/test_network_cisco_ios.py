from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from kcii_audit.cli import app
from kcii_audit.engine.evaluator import evaluate_evidence
from kcii_audit.parsers.network_cisco_ios import records_from_cisco_ios_paste
from kcii_audit.schemas.result import AssessmentStatus

runner = CliRunner()


def _fixture(name: str) -> str:
    return Path("tests/fixtures/network/cisco_ios", name).read_text(encoding="utf-8")


def _status_by_item(fixture_name: str) -> dict[str, AssessmentStatus]:
    records = records_from_cisco_ios_paste(_fixture(fixture_name), asset_id="network-001")
    results = evaluate_evidence(records)
    return {result.item_id: result.status for result in results}


def test_cisco_ios_good_fixture_registers_full_manifest_and_no_vulnerable_auto_items():
    records = records_from_cisco_ios_paste(_fixture("good.txt"), asset_id="network-001")
    results = evaluate_evidence(records)

    assert [record.item_id for record in records] == [f"N-{index:02d}" for index in range(1, 39)]
    assert all(result.platform == "network" for result in results)
    assert AssessmentStatus.VULNERABLE not in {result.status for result in results}
    assert _status_by_item("good.txt")["N-02"] == AssessmentStatus.MANUAL_REQUIRED


def test_cisco_ios_vulnerable_fixture_is_classified():
    statuses = _status_by_item("vulnerable.txt")

    assert statuses["N-03"] == AssessmentStatus.VULNERABLE
    assert statuses["N-06"] == AssessmentStatus.VULNERABLE
    assert statuses["N-07"] == AssessmentStatus.VULNERABLE
    assert statuses["N-08"] == AssessmentStatus.VULNERABLE
    assert statuses["N-11"] == AssessmentStatus.VULNERABLE
    assert statuses["N-18"] == AssessmentStatus.VULNERABLE
    assert statuses["N-19"] == AssessmentStatus.VULNERABLE
    assert statuses["N-20"] == AssessmentStatus.VULNERABLE
    assert statuses["N-21"] == AssessmentStatus.VULNERABLE
    assert statuses["N-27"] == AssessmentStatus.VULNERABLE
    assert statuses["N-29"] == AssessmentStatus.VULNERABLE
    assert statuses["N-30"] == AssessmentStatus.VULNERABLE
    assert statuses["N-31"] == AssessmentStatus.VULNERABLE
    assert statuses["N-32"] == AssessmentStatus.VULNERABLE
    assert statuses["N-33"] == AssessmentStatus.VULNERABLE
    assert statuses["N-34"] == AssessmentStatus.VULNERABLE
    assert statuses["N-36"] == AssessmentStatus.VULNERABLE
    assert statuses["N-15"] == AssessmentStatus.MANUAL_REQUIRED


def test_cisco_ios_mixed_fixture_keeps_distinct_statuses():
    statuses = _status_by_item("mixed.txt")

    assert statuses["N-03"] == AssessmentStatus.GOOD
    assert statuses["N-06"] == AssessmentStatus.VULNERABLE
    assert statuses["N-08"] == AssessmentStatus.VULNERABLE
    assert statuses["N-11"] == AssessmentStatus.GOOD
    assert statuses["N-16"] == AssessmentStatus.GOOD
    assert statuses["N-19"] == AssessmentStatus.VULNERABLE
    assert statuses["N-20"] == AssessmentStatus.GOOD
    assert statuses["N-27"] == AssessmentStatus.MANUAL_REQUIRED
    assert statuses["N-30"] == AssessmentStatus.MANUAL_REQUIRED
    assert statuses["N-15"] == AssessmentStatus.MANUAL_REQUIRED
    assert statuses["N-18"] == AssessmentStatus.GOOD


def test_network_classify_file_creates_full_output_bundle(tmp_path):
    output_dir = tmp_path / "network-cisco"
    result = runner.invoke(
        app,
        [
            "classify-file",
            "--profile",
            "network",
            "--vendor",
            "cisco_ios",
            "--input",
            "tests/fixtures/network/cisco_ios/vulnerable.txt",
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

    payload = json.loads((output_dir / "results.json").read_text(encoding="utf-8"))
    assert len(payload["results"]) == 38


def test_network_outputs_do_not_store_cisco_sensitive_placeholders(tmp_path):
    output_dir = tmp_path / "network-cisco"
    result = runner.invoke(
        app,
        [
            "classify-file",
            "--profile",
            "network",
            "--vendor",
            "cisco_ios",
            "--input",
            "tests/fixtures/network/cisco_ios/vulnerable.txt",
            "--output",
            str(output_dir),
        ],
    )

    assert result.exit_code == 0, result.output
    combined = (
        (output_dir / "evidence.jsonl").read_text(encoding="utf-8")
        + (output_dir / "results.json").read_text(encoding="utf-8")
        + (output_dir / "report.md").read_text(encoding="utf-8")
        + (output_dir / "security_advisory.md").read_text(encoding="utf-8")
    )
    assert "[COMMUNITY_WEAK]" not in combined
    assert "[USER_ADMIN]" not in combined
    assert "[SERIAL_1]" not in combined
    assert "KCII-IOS-SIM" not in combined


def test_network_profile_requires_supported_vendor(tmp_path):
    output_dir = tmp_path / "network-cisco"
    result = runner.invoke(
        app,
        [
            "classify-file",
            "--profile",
            "network",
            "--input",
            "tests/fixtures/network/cisco_ios/good.txt",
            "--output",
            str(output_dir),
        ],
    )

    assert result.exit_code == 2
    assert "--vendor cisco_ios와 junos만 지원합니다" in result.output
