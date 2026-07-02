from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from typer.testing import CliRunner

from kcii_audit.cli import app
from kcii_audit.engine.evaluator import evaluate_evidence
from kcii_audit.parsers.network_cisco_ios import records_from_cisco_ios_paste
from kcii_audit.parsers.network_junos import records_from_junos_paste
from kcii_audit.schemas.result import AssessmentStatus

runner = CliRunner()

NETWORK_ITEM_IDS = [f"N-{index:02d}" for index in range(1, 39)]
SENSITIVE_PLACEHOLDERS = [
    "[HOST_1]",
    "[IP_1]",
    "[IP_2]",
    "[IP_3]",
    "[USER_1]",
    "[COMMUNITY_1]",
    "[SERIAL_1]",
    "[DOMAIN_1]",
    "[PATH_1]",
    "[BANNER_1]",
    "[SECRET_1]",
    "[GROUP_1]",
    "[FILTER_1]",
    "[PREFIX_LIST_1]",
]


def test_network_vendor_regression_matrix_preserves_full_manifest():
    cases = [
        {
            "name": "cisco-ios-realistic",
            "parser": records_from_cisco_ios_paste,
            "fixture": Path("tests/fixtures/network/cisco_ios/realistic/sanitized_lab_mixed.txt"),
            "expected_counts": {
                AssessmentStatus.GOOD: 27,
                AssessmentStatus.MANUAL_REQUIRED: 11,
            },
        },
        {
            "name": "junos-display-set",
            "parser": records_from_junos_paste,
            "fixture": Path("tests/fixtures/network/junos/display_set_good.txt"),
            "expected_counts": {
                AssessmentStatus.GOOD: 14,
                AssessmentStatus.MANUAL_REQUIRED: 24,
            },
        },
        {
            "name": "junos-realistic-display-set",
            "parser": records_from_junos_paste,
            "fixture": Path("tests/fixtures/network/junos/realistic/display_set_realistic_sanitized.txt"),
            "expected_counts": {
                AssessmentStatus.GOOD: 14,
                AssessmentStatus.MANUAL_REQUIRED: 24,
            },
        },
    ]

    for case in cases:
        records = case["parser"](case["fixture"].read_text(encoding="utf-8"), asset_id=case["name"])
        results = evaluate_evidence(records)
        counts = Counter(result.status for result in results)

        assert [record.item_id for record in records] == NETWORK_ITEM_IDS
        assert len(results) == 38
        assert counts[AssessmentStatus.VULNERABLE] == 0
        for status, expected_count in case["expected_counts"].items():
            assert counts[status] == expected_count, case["name"]


def test_network_vendor_regression_classify_file_outputs_are_sanitized(tmp_path):
    cases = [
        {
            "vendor": "cisco_ios",
            "fixture": "tests/fixtures/network/cisco_ios/realistic/sanitized_lab_mixed.txt",
            "output": "network-cisco-ios",
        },
        {
            "vendor": "junos",
            "fixture": "tests/fixtures/network/junos/display_set_good.txt",
            "output": "network-junos",
        },
        {
            "vendor": "juniper_junos",
            "fixture": "tests/fixtures/network/junos/realistic/display_set_realistic_sanitized.txt",
            "output": "network-junos-realistic",
        },
    ]

    for case in cases:
        output_dir = tmp_path / case["output"]
        result = runner.invoke(
            app,
            [
                "classify-file",
                "--profile",
                "network",
                "--vendor",
                case["vendor"],
                "--input",
                case["fixture"],
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
        assert [row["item_id"] for row in payload["results"]] == NETWORK_ITEM_IDS

        combined = "\n".join(
            (output_dir / name).read_text(encoding="utf-8")
            for name in ["evidence.jsonl", "results.json", "report.md", "security_advisory.md"]
        )
        for placeholder in SENSITIVE_PLACEHOLDERS:
            assert placeholder not in combined


def test_junos_unsupported_brace_config_remains_manual_required():
    fixture = Path("tests/fixtures/network/junos/brace_config_unsupported.txt")
    records = records_from_junos_paste(fixture.read_text(encoding="utf-8"), asset_id="network-junos-brace")
    results = evaluate_evidence(records)

    assert [record.item_id for record in records] == NETWORK_ITEM_IDS
    assert {record.evidence["collection_status"] for record in records} == {"needs_display_set"}
    assert {result.status for result in results} == {AssessmentStatus.MANUAL_REQUIRED}
