from __future__ import annotations

import hashlib
import json
import re
from datetime import UTC, datetime
from typing import Any

from kcii_audit.parsers.dbms_items import DBMS_ITEM_IDS, DBMS_ITEM_TITLES
from kcii_audit.schemas.evidence import EvidenceRecord

SUPPORTED_DBMS = {"postgresql", "mysql", "mariadb"}

SAFE_FIELDS_BY_ITEM = {
    "D-01": {"collection_status", "risky_default_account_present"},
    "D-02": {"collection_status", "sample_or_unused_account_count"},
    "D-03": {"collection_status", "password_policy_configured"},
    "D-04": {"collection_status", "excessive_admin_privileges_present"},
    "D-08": {"collection_status", "secure_password_algorithm_configured"},
    "D-09": {"collection_status", "login_failure_lockout_configured"},
    "D-10": {"collection_status", "remote_access_restricted"},
    "D-18": {"collection_status", "public_role_privilege_risk_present"},
    "D-21": {"collection_status", "grant_option_risk_count"},
    "D-22": {"collection_status", "resource_limits_enabled"},
    "D-25": {"collection_status", "version_patch_status_known"},
    "D-26": {"collection_status", "audit_logging_enabled"},
}

FACT_TO_ITEM = {
    "risky_default_account_present": "D-01",
    "sample_or_unused_account_count": "D-02",
    "password_policy_configured": "D-03",
    "excessive_admin_privileges_present": "D-04",
    "secure_password_algorithm_configured": "D-08",
    "login_failure_lockout_configured": "D-09",
    "remote_access_restricted": "D-10",
    "public_role_privilege_risk_present": "D-18",
    "grant_option_risk_count": "D-21",
    "resource_limits_enabled": "D-22",
    "version_patch_status_known": "D-25",
    "audit_logging_enabled": "D-26",
}

MANUAL_EVIDENCE = {
    "collection_status": "not_automated_by_dbms_mvp",
    "manual_required": True,
    "reason": "official DBMS item is registered, but the DBMS MVP parser does not automate this item yet",
}


def records_from_dbms_paste(
    text: str,
    *,
    dbms: str,
    asset_id: str,
    guide_version: str = "kcii-2025-12",
) -> list[EvidenceRecord]:
    normalized_dbms = dbms.strip().lower()
    if normalized_dbms not in SUPPORTED_DBMS:
        raise ValueError(f"unsupported dbms: {dbms}")

    collected_at = datetime.now(UTC)
    raw_hash = "sha256:" + hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()
    facts = _parse_facts(text)

    records: list[EvidenceRecord] = []
    for item_id in DBMS_ITEM_IDS:
        records.append(
            EvidenceRecord(
                asset_id=asset_id,
                platform="dbms",
                os_name=normalized_dbms,
                guide_version=guide_version,
                item_id=item_id,
                item_title=DBMS_ITEM_TITLES[item_id],
                collected_at=collected_at,
                evidence=_evidence_for_item(item_id, facts),
                raw_evidence_hash=raw_hash,
            )
        )
    return records


def _parse_facts(text: str) -> dict[str, Any]:
    payload = _load_json_object(text)
    if payload is not None:
        evidence = payload.get("evidence", payload)
        if isinstance(evidence, dict):
            return dict(evidence)
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


def _evidence_for_item(item_id: str, facts: dict[str, Any]) -> dict[str, Any]:
    keys = SAFE_FIELDS_BY_ITEM.get(item_id)
    if keys is None:
        return dict(MANUAL_EVIDENCE)

    evidence: dict[str, Any] = {"collection_status": "collected"}
    for fact_key, fact_item_id in FACT_TO_ITEM.items():
        if fact_item_id != item_id:
            continue
        if fact_key in facts:
            evidence[fact_key] = _normalize_fact(fact_key, facts[fact_key])
    if len(evidence) == 1:
        return dict(MANUAL_EVIDENCE)
    return evidence


def _normalize_scalar(value: str) -> Any:
    lowered = value.lower()
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if lowered in {"true", "yes", "1", "on", "enabled"}:
        return True
    if lowered in {"false", "no", "0", "off", "disabled"}:
        return False
    return value


def _normalize_fact(key: str, value: Any) -> Any:
    if key in {
        "risky_default_account_present",
        "password_policy_configured",
        "excessive_admin_privileges_present",
        "secure_password_algorithm_configured",
        "login_failure_lockout_configured",
        "remote_access_restricted",
        "public_role_privilege_risk_present",
        "resource_limits_enabled",
        "version_patch_status_known",
        "audit_logging_enabled",
    }:
        if isinstance(value, bool):
            return value
        if isinstance(value, int) and value in {0, 1}:
            return bool(value)
        if isinstance(value, str):
            return _normalize_scalar(value)
        return None
    if key in {"sample_or_unused_account_count", "grant_option_risk_count"}:
        if isinstance(value, bool):
            return int(value)
        try:
            return int(value)
        except (TypeError, ValueError):
            return None
    return value
