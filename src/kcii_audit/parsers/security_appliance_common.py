from __future__ import annotations

import hashlib
import json
import re
from datetime import UTC, datetime
from typing import Any

from kcii_audit.parsers.security_appliance_items import (
    SECURITY_APPLIANCE_FACT_BY_ITEM,
    SECURITY_APPLIANCE_ITEM_IDS,
    SECURITY_APPLIANCE_ITEM_TITLES,
    SUPPORTED_APPLIANCE_TYPES,
)
from kcii_audit.schemas.evidence import EvidenceRecord

SUPPORTED_APPLIANCE_TYPE_SET = set(SUPPORTED_APPLIANCE_TYPES)

MANUAL_EVIDENCE = {
    "collection_status": "interview_required",
    "manual_required": True,
    "reason": "security appliance item requires questionnaire, interview, or sanitized config evidence",
}


def records_from_security_appliance_paste(
    text: str,
    *,
    appliance_type: str,
    asset_id: str,
    guide_version: str = "kcii-2025-12",
) -> list[EvidenceRecord]:
    normalized_type = normalize_appliance_type(appliance_type)
    raw_hash = "sha256:" + hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()
    facts = _parse_facts(text)
    return records_from_security_appliance_facts(
        facts,
        appliance_type=normalized_type,
        asset_id=asset_id,
        guide_version=guide_version,
        raw_evidence_hash=raw_hash,
        evidence_source="config_or_questionnaire_summary",
    )


def records_from_security_appliance_facts(
    facts: dict[str, Any],
    *,
    appliance_type: str,
    asset_id: str,
    guide_version: str = "kcii-2025-12",
    raw_evidence_hash: str | None = None,
    evidence_source: str = "questionnaire",
    warnings_by_item: dict[str, list[str]] | None = None,
) -> list[EvidenceRecord]:
    normalized_type = normalize_appliance_type(appliance_type)
    collected_at = datetime.now(UTC)
    warnings = warnings_by_item or {}

    records: list[EvidenceRecord] = []
    for item_id in SECURITY_APPLIANCE_ITEM_IDS:
        records.append(
            EvidenceRecord(
                asset_id=asset_id,
                platform="security_appliance",
                os_name=normalized_type,
                guide_version=guide_version,
                item_id=item_id,
                item_title=SECURITY_APPLIANCE_ITEM_TITLES[item_id],
                collected_at=collected_at,
                evidence=_evidence_for_item(
                    item_id,
                    facts,
                    appliance_type=normalized_type,
                    evidence_source=evidence_source,
                    warnings=warnings.get(item_id, []),
                ),
                raw_evidence_hash=raw_evidence_hash,
            )
        )
    return records


def normalize_appliance_type(appliance_type: str) -> str:
    normalized = appliance_type.strip().lower().replace("_", "-")
    aliases = {
        "anti-ddos": "anti-ddos",
        "antiddos": "anti-ddos",
        "cisco-asa": "cisco-asa",
        "ciscoasa": "cisco-asa",
        "palo-alto": "paloalto",
        "paloalto": "paloalto",
        "pan-os": "paloalto",
        "panos": "paloalto",
        "big-ip": "f5",
        "bigip": "f5",
        "f5-big-ip": "f5",
    }
    normalized = aliases.get(normalized, normalized)
    if normalized not in SUPPORTED_APPLIANCE_TYPE_SET:
        raise ValueError(f"unsupported security appliance type: {appliance_type}")
    return normalized


def _parse_facts(text: str) -> dict[str, Any]:
    payload = _load_json_object(text)
    if payload is not None:
        evidence = payload.get("evidence", payload)
        if isinstance(evidence, dict):
            return {str(key).lower(): value for key, value in evidence.items()}
    return _parse_key_value_text(text)


def _load_json_object(text: str) -> dict[str, Any] | None:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def _parse_key_value_text(text: str) -> dict[str, Any]:
    facts: dict[str, Any] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip().strip("|").strip()
        if not line or line.startswith(("--", "#")):
            continue
        match = re.match(r"^([A-Za-z][A-Za-z0-9_]+)\s*(?:=|:)\s*(.*?)\s*$", line)
        if not match:
            continue
        key = match.group(1).lower()
        value = match.group(2).strip().strip("'\"")
        facts[key] = _normalize_scalar(value)
    return facts


def _evidence_for_item(
    item_id: str,
    facts: dict[str, Any],
    *,
    appliance_type: str,
    evidence_source: str,
    warnings: list[str],
) -> dict[str, Any]:
    fact_key = SECURITY_APPLIANCE_FACT_BY_ITEM[item_id]
    if fact_key not in facts:
        evidence = dict(MANUAL_EVIDENCE)
        evidence["appliance_type"] = appliance_type
        evidence["evidence_source"] = evidence_source
        if warnings:
            evidence["warnings"] = sorted(set(warnings))
        return evidence

    normalized_value = _normalize_bool(facts[fact_key])
    if normalized_value is None:
        evidence = dict(MANUAL_EVIDENCE)
        evidence["appliance_type"] = appliance_type
        evidence["evidence_source"] = evidence_source
        evidence["reason"] = "security appliance evidence value could not be normalized safely"
        if warnings:
            evidence["warnings"] = sorted(set(warnings))
        return evidence

    evidence = {
        "collection_status": "collected",
        "appliance_type": appliance_type,
        "evidence_source": evidence_source,
        fact_key: normalized_value,
    }
    if warnings:
        evidence["warnings"] = sorted(set(warnings))
    return evidence


def _normalize_scalar(value: str) -> Any:
    lowered = value.lower()
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if lowered in {"true", "yes", "y", "1", "on", "enabled", "configured", "restricted", "reviewed"}:
        return True
    if lowered in {"false", "no", "n", "0", "off", "disabled", "not_configured", "unrestricted", "unreviewed"}:
        return False
    return value


def _normalize_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, int) and value in {0, 1}:
        return bool(value)
    if isinstance(value, str):
        normalized = _normalize_scalar(value.strip())
        return normalized if isinstance(normalized, bool) else None
    return None
