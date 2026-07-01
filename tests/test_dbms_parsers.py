from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

import pytest
from typer.testing import CliRunner

from kcii_audit.cli import app
from kcii_audit.engine.evaluator import evaluate_evidence
from kcii_audit.parsers.dbms_mariadb import records_from_mariadb_paste
from kcii_audit.parsers.dbms_mysql import records_from_mysql_paste
from kcii_audit.parsers.dbms_postgresql import records_from_postgresql_paste
from kcii_audit.schemas.evidence import EvidenceRecord
from kcii_audit.schemas.result import AssessmentStatus

runner = CliRunner()

ParserFunc = Callable[[str], list[EvidenceRecord]]


PARSERS: dict[str, ParserFunc] = {
    "postgresql": records_from_postgresql_paste,
    "mysql": records_from_mysql_paste,
    "mariadb": records_from_mariadb_paste,
}


def _fixture(dbms: str, name: str) -> str:
    return Path("tests/fixtures/dbms", dbms, name).read_text(encoding="utf-8")


def _status_by_item(dbms: str, fixture_name: str) -> dict[str, AssessmentStatus]:
    records = PARSERS[dbms](_fixture(dbms, fixture_name))
    results = evaluate_evidence(records)
    return {result.item_id: result.status for result in results}


@pytest.mark.parametrize("dbms", ["postgresql", "mysql", "mariadb"])
def test_dbms_good_fixture_registers_full_manifest_and_no_vulnerable_auto_items(dbms: str):
    records = PARSERS[dbms](_fixture(dbms, "good.txt"))
    results = evaluate_evidence(records)

    assert [record.item_id for record in records] == [f"D-{index:02d}" for index in range(1, 27)]
    assert all(record.platform == "dbms" for record in records)
    assert all(record.os_name == dbms for record in records)
    assert AssessmentStatus.VULNERABLE not in {result.status for result in results}

    statuses = {result.item_id: result.status for result in results}
    assert statuses["D-01"] == AssessmentStatus.GOOD
    assert statuses["D-02"] == AssessmentStatus.GOOD
    assert statuses["D-26"] == AssessmentStatus.GOOD
    assert statuses["D-25"] == AssessmentStatus.MANUAL_REQUIRED


@pytest.mark.parametrize("dbms", ["postgresql", "mysql", "mariadb"])
def test_dbms_vulnerable_fixture_is_classified(dbms: str):
    statuses = _status_by_item(dbms, "vulnerable.txt")

    for item_id in ["D-01", "D-02", "D-03", "D-04", "D-08", "D-09", "D-10", "D-18", "D-21", "D-26"]:
        assert statuses[item_id] == AssessmentStatus.VULNERABLE
    assert statuses["D-22"] == AssessmentStatus.MANUAL_REQUIRED
    assert statuses["D-25"] == AssessmentStatus.MANUAL_REQUIRED


@pytest.mark.parametrize("dbms", ["postgresql", "mysql", "mariadb"])
def test_dbms_manual_required_fixture_keeps_all_items_manual(dbms: str):
    statuses = _status_by_item(dbms, "manual_required.txt")

    assert set(statuses) == {f"D-{index:02d}" for index in range(1, 27)}
    assert set(statuses.values()) == {AssessmentStatus.MANUAL_REQUIRED}


@pytest.mark.parametrize("dbms", ["postgresql", "mysql", "mariadb"])
def test_dbms_classify_file_creates_full_output_bundle(tmp_path, dbms: str):
    output_dir = tmp_path / f"dbms-{dbms}"
    result = runner.invoke(
        app,
        [
            "classify-file",
            "--profile",
            "dbms",
            "--dbms",
            dbms,
            "--input",
            f"tests/fixtures/dbms/{dbms}/vulnerable.txt",
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
    assert len(payload["results"]) == 26
    assert any(row["status"] == "VULNERABLE" for row in payload["results"])


@pytest.mark.parametrize("dbms", ["postgresql", "mysql", "mariadb"])
def test_dbms_classify_paste_creates_full_output_bundle(tmp_path, dbms: str):
    output_dir = tmp_path / f"dbms-{dbms}"
    result = runner.invoke(
        app,
        [
            "classify-paste",
            "--profile",
            "dbms",
            "--dbms",
            dbms,
            "--output",
            str(output_dir),
        ],
        input=_fixture(dbms, "manual_required.txt"),
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
    assert "D-01" in advisory_text
    assert "D-26" in advisory_text


def test_dbms_no_advisory_keeps_existing_five_output_files(tmp_path):
    output_dir = tmp_path / "dbms-postgresql-no-advisory"
    result = runner.invoke(
        app,
        [
            "classify-file",
            "--profile",
            "dbms",
            "--dbms",
            "postgresql",
            "--input",
            "tests/fixtures/dbms/postgresql/good.txt",
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


def test_dbms_outputs_do_not_store_sensitive_fixture_values(tmp_path):
    output_dir = tmp_path / "dbms-postgresql"
    result = runner.invoke(
        app,
        [
            "classify-file",
            "--profile",
            "dbms",
            "--dbms",
            "postgresql",
            "--input",
            "tests/fixtures/dbms/postgresql/vulnerable.txt",
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
        "[DB_ACCOUNT_ADMIN]",
        "[DB_ACCOUNT_APP]",
        "customerdb",
        "secretdb",
        "192.0.2.10",
        "postgresql://",
        "$2a$not-a-real-hash-placeholder",
    ]:
        assert sensitive_value not in combined


def test_dbms_profile_requires_supported_dbms(tmp_path):
    output_dir = tmp_path / "dbms-unsupported"
    result = runner.invoke(
        app,
        [
            "classify-file",
            "--profile",
            "dbms",
            "--input",
            "tests/fixtures/dbms/postgresql/good.txt",
            "--output",
            str(output_dir),
        ],
    )

    assert result.exit_code == 2
    assert "Only --dbms postgresql" in result.output
