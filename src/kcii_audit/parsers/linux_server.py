from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Any

from kcii_audit.schemas.evidence import EvidenceRecord

LINUX_ITEMS = {
    "L-01": "root SSH 접속 제한",
    "L-02": "UID 0 계정 관리",
    "L-03": "패스워드 최소 길이 확인",
    "L-04": "패스워드 만료 정책 확인",
    "L-05": "/etc/passwd 권한 확인",
    "L-06": "/etc/shadow 권한 확인",
    "L-07": "SSH PasswordAuthentication 설정",
    "L-08": "로그 설정 확인",
}

SAFE_FIELDS_BY_ITEM = {
    "L-01": {"collection_status", "ssh_permit_root_login"},
    "L-02": {"collection_status", "uid0_account_count", "uid0_extra_count"},
    "L-03": {"collection_status", "password_min_length"},
    "L-04": {"collection_status", "password_max_days"},
    "L-05": {"collection_status", "passwd_permission_mode", "passwd_permission_ok"},
    "L-06": {"collection_status", "shadow_permission_mode", "shadow_permission_ok"},
    "L-07": {"collection_status", "ssh_password_authentication"},
    "L-08": {"collection_status", "logging_service_detected"},
}


def records_from_linux_paste(
    text: str,
    *,
    asset_id: str = "linux-paste",
    guide_version: str = "kcii-2025-12",
) -> list[EvidenceRecord]:
    """Convert copied Linux Server results into normalized evidence records."""
    collected_at = datetime.now(UTC)
    raw_hash = "sha256:" + hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()
    payload = _load_json_object(text)

    if payload is None:
        return [_unsupported_record(asset_id, guide_version, collected_at, raw_hash)]

    payload_guide_version = _string_or_default(payload.get("guide_version"), guide_version)
    os_name = _optional_string(payload.get("os_name"))
    os_version = _optional_string(payload.get("os_version"))

    parsed = _parse_items(payload) or _parse_flat_evidence(payload)
    if not parsed:
        return [_unsupported_record(asset_id, payload_guide_version, collected_at, raw_hash)]

    records: list[EvidenceRecord] = []
    for item_id, evidence in parsed.items():
        records.append(
            EvidenceRecord(
                asset_id=asset_id,
                platform="linux",
                os_name=os_name,
                os_version=os_version,
                guide_version=payload_guide_version,
                item_id=item_id,
                item_title=LINUX_ITEMS[item_id],
                collected_at=collected_at,
                evidence=_safe_evidence(item_id, evidence),
                raw_evidence_hash=raw_hash,
            )
        )
    return records


def _load_json_object(text: str) -> dict[str, Any] | None:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def _parse_items(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    items = payload.get("items")
    if not isinstance(items, list):
        return {}

    parsed: dict[str, dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        item_id = item.get("item_id")
        evidence = item.get("evidence")
        if item_id in LINUX_ITEMS and isinstance(evidence, dict):
            parsed[item_id] = {"collection_status": "collected", **evidence}
    return parsed


def _parse_flat_evidence(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    evidence = payload.get("evidence")
    if not isinstance(evidence, dict):
        return {}

    parsed: dict[str, dict[str, Any]] = {}
    _add_if_present(parsed, "L-01", evidence, ["ssh_permit_root_login"])
    _add_if_present(parsed, "L-02", evidence, ["uid0_account_count", "uid0_extra_count"])
    _add_if_present(parsed, "L-03", evidence, ["password_min_length"])
    _add_if_present(parsed, "L-04", evidence, ["password_max_days"])
    _add_if_present(parsed, "L-05", evidence, ["passwd_permission_mode", "passwd_permission_ok"])
    _add_if_present(parsed, "L-06", evidence, ["shadow_permission_mode", "shadow_permission_ok"])
    _add_if_present(parsed, "L-07", evidence, ["ssh_password_authentication"])
    _add_if_present(parsed, "L-08", evidence, ["logging_service_detected"])
    return parsed


def _add_if_present(parsed: dict[str, dict[str, Any]], item_id: str, source: dict[str, Any], fields: list[str]) -> None:
    item_evidence = {"collection_status": "collected"}
    found = False
    for field in fields:
        if field in source:
            item_evidence[field] = _normalize_field_value(field, source[field])
            found = True
    if found:
        parsed[item_id] = item_evidence


def _safe_evidence(item_id: str, evidence: dict[str, Any]) -> dict[str, Any]:
    allowed = SAFE_FIELDS_BY_ITEM[item_id]
    safe: dict[str, Any] = {}
    for key, value in evidence.items():
        if key not in allowed:
            continue
        safe[key] = _normalize_field_value(key, value)
    return safe


def _normalize_field_value(field: str, value: Any) -> Any:
    if field in {
        "ssh_permit_root_login",
        "ssh_password_authentication",
        "passwd_permission_mode",
        "shadow_permission_mode",
        "collection_status",
    }:
        return str(value).strip().lower() if value is not None else None
    if field in {"uid0_account_count", "uid0_extra_count", "password_min_length", "password_max_days"}:
        if isinstance(value, bool):
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None
    if field in {"passwd_permission_ok", "shadow_permission_ok", "logging_service_detected"}:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            lowered = value.strip().lower()
            if lowered in {"true", "yes", "1", "enabled"}:
                return True
            if lowered in {"false", "no", "0", "disabled"}:
                return False
        return None
    return value


def _unsupported_record(
    asset_id: str,
    guide_version: str,
    collected_at: datetime,
    raw_hash: str,
) -> EvidenceRecord:
    return EvidenceRecord(
        asset_id=asset_id,
        platform="linux",
        os_name="Linux",
        guide_version=guide_version,
        item_id="L-UNSUPPORTED-OUTPUT",
        item_title="Linux pasted output requires manual review",
        collected_at=collected_at,
        evidence={
            "collection_status": "unsupported_output",
            "reason": "supported Linux evidence keys were not found in copied output",
        },
        raw_evidence_hash=raw_hash,
    )


def _optional_string(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _string_or_default(value: Any, default: str) -> str:
    if value is None:
        return default
    return str(value)
