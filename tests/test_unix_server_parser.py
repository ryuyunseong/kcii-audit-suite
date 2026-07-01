from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from kcii_audit.cli import app
from kcii_audit.engine.evaluator import evaluate_evidence
from kcii_audit.parsers.unix_server import records_from_unix_paste
from kcii_audit.schemas.result import AssessmentStatus

runner = CliRunner()

UNIX_FLAVORS = ["aix", "solaris", "hpux", "linux"]


def _fixture(unix_flavor: str, name: str) -> str:
    return Path("tests/fixtures/unix_server", unix_flavor, name).read_text(encoding="utf-8")


def _status_by_item(unix_flavor: str, fixture_name: str) -> dict[str, AssessmentStatus]:
    records = records_from_unix_paste(_fixture(unix_flavor, fixture_name), unix_flavor=unix_flavor)
    results = evaluate_evidence(records)
    return {result.item_id: result.status for result in results}


@pytest.mark.parametrize("unix_flavor", UNIX_FLAVORS)
def test_unix_good_fixture_registers_full_manifest_and_no_vulnerable_auto_items(unix_flavor: str):
    records = records_from_unix_paste(_fixture(unix_flavor, "good.json"), unix_flavor=unix_flavor)
    results = evaluate_evidence(records)

    assert [record.item_id for record in records] == [f"U-{index:02d}" for index in range(1, 68)]
    assert all(record.platform == "unix" for record in records)
    assert all(record.os_name == unix_flavor for record in records)
    assert AssessmentStatus.VULNERABLE not in {result.status for result in results}

    statuses = {result.item_id: result.status for result in results}
    assert statuses["U-01"] == AssessmentStatus.GOOD
    assert statuses["U-05"] == AssessmentStatus.GOOD
    assert statuses["U-66"] == AssessmentStatus.GOOD
    assert statuses["U-64"] == AssessmentStatus.MANUAL_REQUIRED
    assert statuses["U-07"] == AssessmentStatus.MANUAL_REQUIRED


@pytest.mark.parametrize("unix_flavor", UNIX_FLAVORS)
def test_unix_vulnerable_fixture_is_classified(unix_flavor: str):
    statuses = _status_by_item(unix_flavor, "vulnerable.json")

    for item_id in ["U-01", "U-02", "U-03", "U-04", "U-05", "U-13", "U-16", "U-18", "U-52", "U-65", "U-66"]:
        assert statuses[item_id] == AssessmentStatus.VULNERABLE
    assert statuses["U-64"] == AssessmentStatus.MANUAL_REQUIRED


@pytest.mark.parametrize("unix_flavor", UNIX_FLAVORS)
def test_unix_manual_required_fixture_keeps_all_items_manual(unix_flavor: str):
    statuses = _status_by_item(unix_flavor, "manual_required.txt")

    assert set(statuses) == {f"U-{index:02d}" for index in range(1, 68)}
    assert set(statuses.values()) == {AssessmentStatus.MANUAL_REQUIRED}


@pytest.mark.parametrize("unix_flavor", UNIX_FLAVORS)
def test_unix_classify_file_creates_full_output_bundle(tmp_path, unix_flavor: str):
    output_dir = tmp_path / f"unix-{unix_flavor}"
    result = runner.invoke(
        app,
        [
            "classify-file",
            "--profile",
            "unix",
            "--unix",
            unix_flavor,
            "--input",
            f"tests/fixtures/unix_server/{unix_flavor}/vulnerable.json",
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
    assert len(payload["results"]) == 67
    assert any(row["status"] == "VULNERABLE" for row in payload["results"])


@pytest.mark.parametrize("unix_flavor", UNIX_FLAVORS)
def test_unix_classify_paste_creates_full_output_bundle(tmp_path, unix_flavor: str):
    output_dir = tmp_path / f"unix-{unix_flavor}-paste"
    result = runner.invoke(
        app,
        [
            "classify-paste",
            "--profile",
            "unix",
            "--unix",
            unix_flavor,
            "--output",
            str(output_dir),
        ],
        input=_fixture(unix_flavor, "manual_required.txt"),
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
    assert "U-01" in advisory_text
    assert "U-67" in advisory_text


def test_unix_no_advisory_keeps_existing_five_output_files(tmp_path):
    output_dir = tmp_path / "unix-aix-no-advisory"
    result = runner.invoke(
        app,
        [
            "classify-file",
            "--profile",
            "unix",
            "--unix",
            "aix",
            "--input",
            "tests/fixtures/unix_server/aix/good.json",
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


def test_unix_outputs_do_not_store_sensitive_fixture_values(tmp_path):
    output_dir = tmp_path / "unix-aix"
    result = runner.invoke(
        app,
        [
            "classify-file",
            "--profile",
            "unix",
            "--unix",
            "aix",
            "--input",
            "tests/fixtures/unix_server/aix/vulnerable.json",
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
        "customer_admin",
        "unix-prod-01.example.invalid",
        "example.invalid",
        "192.0.2.40",
        "/home/customer_admin/.ssh/id_rsa",
        "$6$not-a-real-unix-hash",
    ]:
        assert sensitive_value not in combined


def test_unix_profile_requires_supported_flavor(tmp_path):
    output_dir = tmp_path / "unix-unsupported"
    result = runner.invoke(
        app,
        [
            "classify-file",
            "--profile",
            "unix",
            "--input",
            "tests/fixtures/unix_server/aix/good.json",
            "--output",
            str(output_dir),
        ],
    )

    assert result.exit_code == 2
    assert "Only --unix aix" in result.output
