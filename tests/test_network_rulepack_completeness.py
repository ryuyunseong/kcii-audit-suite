from __future__ import annotations

from pathlib import Path

import yaml

from kcii_audit.engine.rulepack import load_rulepack

MANIFEST_PATH = Path("rulepacks/kcii-2025-12/network_items_manifest.yaml")
RULEPACK_PATH = Path("rulepacks/kcii-2025-12/network.yaml")


def _load_manifest() -> dict:
    return yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_network_manifest_contains_official_item_table_entries():
    manifest = _load_manifest()
    item_ids = [item["item_id"] for item in manifest["items"]]

    assert manifest["guide_version"] == "kcii-2025-12"
    assert manifest["domain"] == "network"
    assert item_ids == [f"N-{index:02d}" for index in range(1, 39)]
    assert manifest["items"][0]["title"] == "비밀번호 설정"
    assert manifest["items"][-1]["title"] == "mask-reply 차단"
    assert "Official network item code" in manifest["source"]["source_note"]


def test_network_rulepack_loads_and_matches_manifest_items():
    manifest = _load_manifest()
    rulepack = load_rulepack(RULEPACK_PATH)

    manifest_ids = [item["item_id"] for item in manifest["items"]]
    rulepack_ids = [item.item_id for item in rulepack.items]

    assert rulepack.guide_version == manifest["guide_version"]
    assert rulepack.domain == manifest["domain"]
    assert rulepack_ids == manifest_ids
    assert all(item.remediation for item in rulepack.items)
    assert all(item.report_text for item in rulepack.items)


def test_network_manifest_automation_levels_are_explicit():
    manifest = _load_manifest()
    allowed = {"auto", "partial", "manual", "unsupported_vendor"}
    auto_items = {item["item_id"] for item in manifest["items"] if item["automation_level"] == "auto"}

    assert {item["automation_level"] for item in manifest["items"]} <= allowed
    assert {"N-01", "N-03", "N-06", "N-07", "N-08", "N-10", "N-11", "N-15", "N-18"} <= auto_items
