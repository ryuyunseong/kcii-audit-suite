from __future__ import annotations

from pathlib import Path

import yaml

from kcii_audit.engine.rulepack import load_rulepack

MANIFEST_PATH = Path("rulepacks/kcii-2025-12/unix_items_manifest.yaml")
RULEPACK_PATH = Path("rulepacks/kcii-2025-12/unix.yaml")


def _load_manifest() -> dict:
    return yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_unix_manifest_contains_official_item_table_entries():
    manifest = _load_manifest()
    item_ids = [item["item_id"] for item in manifest["items"]]

    assert manifest["guide_version"] == "kcii-2025-12"
    assert manifest["domain"] == "unix"
    assert item_ids == [f"U-{index:02d}" for index in range(1, 68)]
    assert manifest["items"][0]["title"] == "root 계정 원격 접속 제한"
    assert manifest["items"][-1]["title"] == "로그 디렉터리 소유자 및 권한 설정"
    assert "Official Unix item code" in manifest["source"]["source_note"]


def test_unix_rulepack_loads_and_matches_manifest_items():
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


def test_unix_manifest_automation_levels_and_supported_unix_are_explicit():
    manifest = _load_manifest()
    allowed = {"auto", "partial", "manual"}
    partial_items = {item["item_id"] for item in manifest["items"] if item["automation_level"] == "partial"}

    assert {item["automation_level"] for item in manifest["items"]} <= allowed
    assert {"U-01", "U-02", "U-03", "U-04", "U-05", "U-16", "U-18", "U-52", "U-65", "U-66"} <= partial_items
    assert all(item["supported_unix"] == ["aix", "solaris", "hpux", "linux"] for item in manifest["items"])
