from __future__ import annotations

from pathlib import Path

import yaml

from kcii_audit.engine.rulepack import load_rulepack
from kcii_audit.parsers.windows_items import WINDOWS_ITEM_IDS

MANIFEST_PATH = Path("rulepacks/kcii-2025-12/windows_items_manifest.yaml")
RULEPACK_PATH = Path("rulepacks/kcii-2025-12/windows.yaml")


def _load_manifest() -> dict:
    return yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_windows_manifest_contains_official_item_table_entries():
    manifest = _load_manifest()
    item_ids = [item["item_id"] for item in manifest["items"]]

    assert manifest["guide_version"] == "kcii-2025-12"
    assert manifest["domain"] == "windows"
    assert item_ids == [f"W-{index:02d}" for index in range(1, 65)]
    assert item_ids == WINDOWS_ITEM_IDS
    assert manifest["items"][0]["title"] == "Administrator 계정 이름 변경 등 보안성 강화"
    assert manifest["items"][-1]["title"] == "윈도우 방화벽 설정"
    assert "Official Windows Server item code" in manifest["source"]["source_note"]


def test_windows_rulepack_loads_and_matches_manifest_items():
    manifest = _load_manifest()
    rulepack = load_rulepack(RULEPACK_PATH)

    manifest_ids = [item["item_id"] for item in manifest["items"]]
    rulepack_ids = [item.item_id for item in rulepack.items]

    assert rulepack.guide_version == manifest["guide_version"]
    assert rulepack.domain == manifest["domain"]
    assert rulepack_ids == manifest_ids
    assert all(item.remediation for item in rulepack.items)
    assert all(item.report_text for item in rulepack.items)


def test_windows_manifest_automation_levels_are_explicit():
    manifest = _load_manifest()
    allowed = {"auto", "partial", "manual", "unsupported"}
    automation_by_item = {item["item_id"]: item["automation_level"] for item in manifest["items"]}

    assert set(automation_by_item.values()) <= allowed
    assert automation_by_item["W-02"] == "auto"
    assert automation_by_item["W-09"] == "partial"
    assert automation_by_item["W-17"] == "auto"
    assert automation_by_item["W-18"] == "partial"
    assert automation_by_item["W-21"] == "partial"
    assert automation_by_item["W-29"] == "partial"
    assert automation_by_item["W-40"] == "partial"
    assert automation_by_item["W-42"] == "partial"
    assert automation_by_item["W-64"] == "auto"
