from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Iterable

from openpyxl import load_workbook
from typer.testing import CliRunner

from kcii_audit.cli import app
from kcii_audit.engine.evaluator import evaluate_evidence
from kcii_audit.parsers.network_junos import records_from_junos_paste
from kcii_audit.schemas.result import AssessmentStatus

runner = CliRunner()

FIXTURE_DIR = Path("tests/fixtures/network/junos")
SENSITIVE_PLACEHOLDERS = [
    "[HOST_1]",
    "[IP_1]",
    "[IP_2]",
    "[IP_3]",
    "[USER_1]",
    "[COMMUNITY_1]",
    "[BANNER_1]",
    "[SECRET_1]",
]


def _fixture(name: str) -> str:
    return (FIXTURE_DIR / name).read_text(encoding="utf-8")


def test_junos_display_set_fixture_emits_full_network_manifest():
    records = records_from_junos_paste(_fixture("display_set_good.txt"), asset_id="network-junos")
    results = evaluate_evidence(records)
    statuses = {result.item_id: result.status for result in results}
    counts = Counter(result.status for result in results)

    assert [record.item_id for record in records] == [f"N-{index:02d}" for index in range(1, 39)]
    assert all(record.os_name == "Juniper Junos" for record in records)
    assert counts[AssessmentStatus.VULNERABLE] == 0
    assert statuses["N-01"] == AssessmentStatus.GOOD
    assert statuses["N-03"] == AssessmentStatus.GOOD
    assert statuses["N-06"] == AssessmentStatus.GOOD
    assert statuses["N-07"] == AssessmentStatus.GOOD
    assert statuses["N-08"] == AssessmentStatus.GOOD
    assert statuses["N-10"] == AssessmentStatus.GOOD
    assert statuses["N-11"] == AssessmentStatus.GOOD
    assert statuses["N-15"] == AssessmentStatus.GOOD
    assert statuses["N-16"] == AssessmentStatus.GOOD
    assert statuses["N-18"] == AssessmentStatus.GOOD
    assert statuses["N-19"] == AssessmentStatus.GOOD
    assert statuses["N-20"] == AssessmentStatus.GOOD
    assert statuses["N-21"] == AssessmentStatus.MANUAL_REQUIRED
    assert statuses["N-27"] == AssessmentStatus.MANUAL_REQUIRED
    assert statuses["N-32"] == AssessmentStatus.GOOD
    assert statuses["N-34"] == AssessmentStatus.GOOD


def test_junos_display_set_vulnerable_indicators_are_classified():
    records = records_from_junos_paste(_fixture("display_set_vulnerable.txt"), asset_id="network-junos")
    statuses = {result.item_id: result.status for result in evaluate_evidence(records)}

    assert statuses["N-03"] == AssessmentStatus.VULNERABLE
    assert statuses["N-07"] == AssessmentStatus.VULNERABLE
    assert statuses["N-08"] == AssessmentStatus.VULNERABLE
    assert statuses["N-18"] == AssessmentStatus.VULNERABLE
    assert statuses["N-19"] == AssessmentStatus.VULNERABLE
    assert statuses["N-20"] == AssessmentStatus.VULNERABLE
    assert statuses["N-21"] == AssessmentStatus.VULNERABLE
    assert statuses["N-26"] == AssessmentStatus.VULNERABLE
    assert statuses["N-27"] == AssessmentStatus.VULNERABLE
    assert statuses["N-31"] == AssessmentStatus.VULNERABLE
    assert statuses["N-33"] == AssessmentStatus.VULNERABLE


def test_junos_brace_style_config_fails_closed_to_manual_required():
    records = records_from_junos_paste(_fixture("brace_config_unsupported.txt"), asset_id="network-junos")
    results = evaluate_evidence(records)

    assert len(results) == 38
    assert {result.status for result in results} == {AssessmentStatus.MANUAL_REQUIRED}
    assert {record.evidence["collection_status"] for record in records} == {"needs_display_set"}
    assert all("display set" in record.evidence["reason"] for record in records)


def test_junos_classify_file_creates_outputs_without_sensitive_values(tmp_path):
    output_dir = tmp_path / "network-junos"
    result = runner.invoke(
        app,
        [
            "classify-file",
            "--profile",
            "network",
            "--vendor",
            "junos",
            "--input",
            str(FIXTURE_DIR / "display_set_good.txt"),
            "--output",
            str(output_dir),
        ],
    )

    assert result.exit_code == 0, result.output
    for name in [
        "evidence.jsonl",
        "results.json",
        "detail.xlsx",
        "summary.xlsx",
        "report.md",
        "security_advisory.md",
        "security_advisory.xlsx",
    ]:
        assert (output_dir / name).exists()

    payload = json.loads((output_dir / "results.json").read_text(encoding="utf-8"))
    assert len(payload["results"]) == 38

    combined = "\n".join(_output_text_values(output_dir))
    for placeholder in SENSITIVE_PLACEHOLDERS:
        assert placeholder not in combined


def _output_text_values(output_dir: Path) -> Iterable[str]:
    for name in ["evidence.jsonl", "results.json", "report.md", "security_advisory.md"]:
        yield (output_dir / name).read_text(encoding="utf-8")

    for name in ["detail.xlsx", "summary.xlsx", "security_advisory.xlsx"]:
        workbook = load_workbook(output_dir / name, data_only=True)
        try:
            for sheet in workbook.worksheets:
                for row in sheet.iter_rows(values_only=True):
                    for value in row:
                        if value is not None:
                            yield str(value)
        finally:
            workbook.close()
