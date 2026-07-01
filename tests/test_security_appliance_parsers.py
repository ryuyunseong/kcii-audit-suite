from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from kcii_audit.cli import app
from kcii_audit.engine.evaluator import evaluate_evidence
from kcii_audit.parsers.security_appliance_common import records_from_security_appliance_paste
from kcii_audit.parsers.security_appliance_cisco_asa import records_from_cisco_asa_paste
from kcii_audit.parsers.security_appliance_f5 import records_from_f5_paste
from kcii_audit.parsers.security_appliance_fortigate import records_from_fortigate_paste
from kcii_audit.parsers.security_appliance_paloalto import records_from_paloalto_paste
from kcii_audit.schemas.result import AssessmentStatus

runner = CliRunner()


def _fixture(name: str) -> str:
    return Path("tests/fixtures/security_appliance", name).read_text(encoding="utf-8")


def _status_by_item(fixture_name: str) -> dict[str, AssessmentStatus]:
    records = records_from_security_appliance_paste(
        _fixture(fixture_name),
        appliance_type="firewall",
        asset_id="security-appliance-fixture",
    )
    results = evaluate_evidence(records)
    return {result.item_id: result.status for result in results}


def test_security_appliance_good_fixture_registers_full_manifest_and_no_vulnerable_items():
    records = records_from_security_appliance_paste(
        _fixture("good.txt"),
        appliance_type="firewall",
        asset_id="security-appliance-good",
    )
    results = evaluate_evidence(records)

    assert [record.item_id for record in records] == [f"S-{index:02d}" for index in range(1, 24)]
    assert all(record.platform == "security_appliance" for record in records)
    assert all(record.os_name == "firewall" for record in records)
    assert AssessmentStatus.VULNERABLE not in {result.status for result in results}

    statuses = {result.item_id: result.status for result in results}
    assert statuses["S-01"] == AssessmentStatus.GOOD
    assert statuses["S-23"] == AssessmentStatus.GOOD


def test_security_appliance_vulnerable_fixture_is_classified():
    statuses = _status_by_item("vulnerable.txt")

    assert set(statuses) == {f"S-{index:02d}" for index in range(1, 24)}
    assert set(statuses.values()) == {AssessmentStatus.VULNERABLE}


def test_security_appliance_manual_required_fixture_keeps_all_items_manual():
    statuses = _status_by_item("manual_required.txt")

    assert set(statuses) == {f"S-{index:02d}" for index in range(1, 24)}
    assert set(statuses.values()) == {AssessmentStatus.MANUAL_REQUIRED}


def test_security_appliance_vendor_wrappers_use_common_parser():
    fixture = _fixture("good.txt")

    assert records_from_fortigate_paste(fixture)[0].os_name == "fortigate"
    assert records_from_paloalto_paste(fixture)[0].os_name == "paloalto"
    assert records_from_cisco_asa_paste(fixture)[0].os_name == "cisco-asa"
    assert records_from_f5_paste(fixture)[0].os_name == "f5"


def test_security_appliance_classify_file_creates_full_output_bundle(tmp_path):
    output_dir = tmp_path / "security-appliance"
    result = runner.invoke(
        app,
        [
            "classify-file",
            "--profile",
            "security-appliance",
            "--appliance-type",
            "firewall",
            "--input",
            "tests/fixtures/security_appliance/vulnerable.txt",
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
    assert len(payload["results"]) == 23
    assert all(row["status"] == "VULNERABLE" for row in payload["results"])


def test_security_appliance_classify_paste_creates_full_output_bundle(tmp_path):
    output_dir = tmp_path / "security-appliance-paste"
    result = runner.invoke(
        app,
        [
            "classify-paste",
            "--profile",
            "security-appliance",
            "--appliance-type",
            "firewall",
            "--output",
            str(output_dir),
        ],
        input=_fixture("manual_required.txt"),
    )

    assert result.exit_code == 0, result.output
    assert (output_dir / "evidence.jsonl").exists()
    assert (output_dir / "results.json").exists()
    assert (output_dir / "detail.xlsx").exists()
    assert (output_dir / "summary.xlsx").exists()
    assert (output_dir / "report.md").exists()
    assert (output_dir / "security_advisory.md").exists()
    assert (output_dir / "security_advisory.xlsx").exists()

    advisory_text = (output_dir / "security_advisory.md").read_text(encoding="utf-8")
    assert "S-01" in advisory_text
    assert "S-23" in advisory_text


def test_security_appliance_no_advisory_keeps_existing_five_output_files(tmp_path):
    output_dir = tmp_path / "security-appliance-no-advisory"
    result = runner.invoke(
        app,
        [
            "classify-file",
            "--profile",
            "security-appliance",
            "--appliance-type",
            "firewall",
            "--input",
            "tests/fixtures/security_appliance/good.txt",
            "--output",
            str(output_dir),
            "--no-advisory",
        ],
    )

    assert result.exit_code == 0, result.output
    assert (output_dir / "evidence.jsonl").exists()
    assert (output_dir / "results.json").exists()
    assert (output_dir / "detail.xlsx").exists()
    assert (output_dir / "summary.xlsx").exists()
    assert (output_dir / "report.md").exists()
    assert not (output_dir / "security_advisory.md").exists()
    assert not (output_dir / "security_advisory.xlsx").exists()


def test_security_appliance_outputs_do_not_store_sensitive_fixture_values(tmp_path):
    output_dir = tmp_path / "security-appliance"
    result = runner.invoke(
        app,
        [
            "classify-file",
            "--profile",
            "security-appliance",
            "--appliance-type",
            "firewall",
            "--input",
            "tests/fixtures/security_appliance/vulnerable.txt",
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
    for sensitive_value in [
        "[APPLIANCE_ADMIN]",
        "198.51.100.80",
        "fw-prod-01.example.invalid",
        "example.invalid",
        "Allow-Customer-Core",
        "CustomerObject",
        "[REDACTED_DEVICE_IDENTIFIER]",
        "[REDACTED_SECRET_MATERIAL]",
        "[REDACTED_CERTIFICATE_MATERIAL]",
    ]:
        assert sensitive_value not in combined


def test_security_appliance_profile_requires_supported_type(tmp_path):
    output_dir = tmp_path / "security-appliance-unsupported"
    result = runner.invoke(
        app,
        [
            "classify-file",
            "--profile",
            "security-appliance",
            "--appliance-type",
            "unsupported",
            "--input",
            "tests/fixtures/security_appliance/good.txt",
            "--output",
            str(output_dir),
        ],
    )

    assert result.exit_code == 2
    assert "unsupported security appliance type" in result.output
