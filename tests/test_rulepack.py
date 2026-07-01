from __future__ import annotations

from pathlib import Path

import pytest

from kcii_audit.engine.rulepack import RulepackError, evaluate_with_rulepack, load_rulepack
from kcii_audit.parsers.windows_server import records_from_windows_paste
from kcii_audit.schemas.result import AssessmentStatus

RULEPACK_PATH = Path("rulepacks/kcii-2025-12/windows.yaml")
LINUX_RULEPACK_PATH = Path("rulepacks/kcii-2025-12/linux.yaml")


def test_windows_rulepack_loads():
    rulepack = load_rulepack(RULEPACK_PATH)

    assert rulepack.guide_version == "kcii-2025-12"
    assert rulepack.domain == "windows"
    assert [item.item_id for item in rulepack.items] == [f"W-{index:02d}" for index in range(1, 65)]


def test_linux_rulepack_loads():
    rulepack = load_rulepack(LINUX_RULEPACK_PATH)

    assert rulepack.guide_version == "kcii-2025-12"
    assert rulepack.domain == "linux"
    assert [item.item_id for item in rulepack.items] == [f"L-0{i}" for i in range(1, 9)]


def test_windows_rulepack_evaluates_good_fixture():
    rulepack = load_rulepack(RULEPACK_PATH)
    text = Path("tests/fixtures/windows/paste/good-key-value.txt").read_text(encoding="utf-8")
    records = records_from_windows_paste(text, asset_id="win-001")

    results = [evaluate_with_rulepack(record, rulepack) for record in records]

    result_by_item = {
        record.item_id: result
        for record, result in zip(records, results, strict=True)
        if result is not None
    }
    assert result_by_item["W-02"][0] == AssessmentStatus.GOOD
    assert result_by_item["W-09"][0] == AssessmentStatus.GOOD
    assert result_by_item["W-64"][0] == AssessmentStatus.GOOD
    assert result_by_item["W-03"][0] == AssessmentStatus.MANUAL_REQUIRED


def test_invalid_rulepack_returns_clear_error(tmp_path):
    broken = tmp_path / "windows.yaml"
    broken.write_text("guide_version: kcii-2025-12\nitems: []\n", encoding="utf-8")

    with pytest.raises(RulepackError, match="invalid rulepack schema"):
        load_rulepack(broken)
