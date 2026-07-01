from __future__ import annotations

from pathlib import Path

import yaml

from kcii_audit.engine.rulepack import load_rulepack

MANIFEST_PATH = Path("rulepacks/kcii-2025-12/dbms_items_manifest.yaml")
RULEPACK_PATH = Path("rulepacks/kcii-2025-12/dbms.yaml")


def _load_manifest() -> dict:
    return yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_dbms_manifest_contains_official_item_table_entries():
    manifest = _load_manifest()
    item_ids = [item["item_id"] for item in manifest["items"]]

    assert manifest["guide_version"] == "kcii-2025-12"
    assert manifest["domain"] == "dbms"
    assert item_ids == [f"D-{index:02d}" for index in range(1, 27)]
    assert manifest["items"][0]["title"] == "기본 계정의 비밀번호, 정책 등을 변경하여 사용"
    assert manifest["items"][-1]["title"] == "데이터베이스의 접근, 변경, 삭제 등의 감사 기록이 기관의 감사 기록 정책에 적합하도록 설정"
    assert "Official DBMS item code" in manifest["source"]["source_note"]


def test_dbms_rulepack_loads_and_matches_manifest_items():
    manifest = _load_manifest()
    rulepack = load_rulepack(RULEPACK_PATH)

    manifest_ids = [item["item_id"] for item in manifest["items"]]
    rulepack_ids = [item.item_id for item in rulepack.items]

    assert rulepack.guide_version == manifest["guide_version"]
    assert rulepack.domain == manifest["domain"]
    assert rulepack_ids == manifest_ids
    assert all(item.remediation for item in rulepack.items)
    assert all(item.report_text for item in rulepack.items)
    assert all(item.remediation_summary for item in rulepack.items)
    assert all(item.advisory_template for item in rulepack.items)


def test_dbms_manifest_automation_levels_and_supported_dbms_are_explicit():
    manifest = _load_manifest()
    allowed = {"auto", "partial", "manual"}
    partial_items = {item["item_id"] for item in manifest["items"] if item["automation_level"] == "partial"}

    assert {item["automation_level"] for item in manifest["items"]} <= allowed
    assert {"D-01", "D-02", "D-03", "D-04", "D-08", "D-09", "D-10", "D-18", "D-21", "D-22", "D-25", "D-26"} <= partial_items
    assert all(item["supported_dbms"] == ["postgresql", "mysql", "mariadb"] for item in manifest["items"])
