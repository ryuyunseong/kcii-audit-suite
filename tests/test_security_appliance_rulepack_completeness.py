from __future__ import annotations

from pathlib import Path

import yaml

from kcii_audit.engine.rulepack import load_rulepack

MANIFEST_PATH = Path("rulepacks/kcii-2025-12/security_appliance_items_manifest.yaml")
RULEPACK_PATH = Path("rulepacks/kcii-2025-12/security_appliance.yaml")


def _load_manifest() -> dict:
    return yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_security_appliance_manifest_contains_official_item_table_entries():
    manifest = _load_manifest()
    item_ids = [item["item_id"] for item in manifest["items"]]

    assert manifest["guide_version"] == "kcii-2025-12"
    assert manifest["domain"] == "security_appliance"
    assert item_ids == [f"S-{index:02d}" for index in range(1, 24)]
    assert manifest["items"][0]["title"] == "보안 장비 Default 계정 변경"
    assert manifest["items"][-1]["title"] == "유해 트래픽 탐지/차단 정책 설정"
    assert "Official security appliance item code" in manifest["source"]["source_note"]


def test_security_appliance_rulepack_loads_and_matches_manifest_items():
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


def test_security_appliance_manifest_supported_types_and_sources_are_explicit():
    manifest = _load_manifest()
    allowed = {"auto", "partial", "manual"}
    expected_types = ["firewall", "ips", "ids", "waf", "vpn", "anti-ddos", "fortigate", "paloalto", "cisco-asa", "f5"]

    assert {item["automation_level"] for item in manifest["items"]} <= allowed
    assert all(item["supported_appliance_types"] == expected_types for item in manifest["items"])
    assert all("questionnaire" in item["evidence_source"] for item in manifest["items"])


def test_security_appliance_rulepack_has_questionnaire_mapping_fields():
    rulepack = load_rulepack(RULEPACK_PATH)

    assert all(item.supported_appliance_types for item in rulepack.items)
    assert all(item.config_hints_by_vendor for item in rulepack.items)
    assert all(item.questionnaire_fields for item in rulepack.items)
    assert all(item.automation_level == "partial" for item in rulepack.items)
