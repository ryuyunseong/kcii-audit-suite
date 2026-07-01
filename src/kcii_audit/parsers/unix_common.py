from __future__ import annotations

import hashlib
import json
import re
from datetime import UTC, datetime
from typing import Any

from kcii_audit.parsers.unix_items import UNIX_ITEM_IDS, UNIX_ITEM_TITLES
from kcii_audit.schemas.evidence import EvidenceRecord

SUPPORTED_UNIX = {"aix", "solaris", "hpux", "linux"}

UNIX_FACT_TO_ITEM = {
    "root_remote_login_restricted": "U-01",
    "password_policy_configured": "U-02",
    "account_lockout_configured": "U-03",
    "password_file_protected": "U-04",
    "uid0_extra_count": "U-05",
    "su_restricted": "U-06",
    "session_timeout_configured": "U-12",
    "password_hash_algorithm_secure": "U-13",
    "root_path_secure": "U-14",
    "passwd_permission_ok": "U-16",
    "shadow_permission_ok": "U-18",
    "umask_secure": "U-30",
    "finger_service_disabled": "U-34",
    "r_services_disabled": "U-36",
    "cron_permission_ok": "U-37",
    "nfs_service_disabled": "U-39",
    "nfs_access_control_configured": "U-40",
    "rpc_service_disabled": "U-42",
    "tftp_talk_disabled": "U-44",
    "telnet_service_disabled": "U-52",
    "ftp_encrypted_or_disabled": "U-54",
    "snmp_service_disabled": "U-58",
    "login_banner_configured": "U-62",
    "sudo_access_controlled": "U-63",
    "version_patch_status_known": "U-64",
    "ntp_configured": "U-65",
    "system_logging_configured": "U-66",
    "log_directory_permission_ok": "U-67",
}

COUNT_FACTS = {"uid0_extra_count"}

MANUAL_EVIDENCE = {
    "collection_status": "not_automated_by_unix_mvp",
    "manual_required": True,
    "reason": "official Unix item is registered, but the Unix MVP parser does not automate this item yet",
}


def records_from_unix_paste(
    text: str,
    *,
    unix_flavor: str,
    asset_id: str,
    guide_version: str = "kcii-2025-12",
) -> list[EvidenceRecord]:
    normalized_flavor = unix_flavor.strip().lower()
    if normalized_flavor not in SUPPORTED_UNIX:
        raise ValueError(f"unsupported unix flavor: {unix_flavor}")

    collected_at = datetime.now(UTC)
    raw_hash = "sha256:" + hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()
    facts, payload_guide_version = _parse_facts(text, guide_version)

    records: list[EvidenceRecord] = []
    for item_id in UNIX_ITEM_IDS:
        records.append(
            EvidenceRecord(
                asset_id=asset_id,
                platform="unix",
                os_name=normalized_flavor,
                guide_version=payload_guide_version,
                item_id=item_id,
                item_title=UNIX_ITEM_TITLES[item_id],
                collected_at=collected_at,
                evidence=_evidence_for_item(item_id, facts),
                raw_evidence_hash=raw_hash,
            )
        )
    return records


def _parse_facts(text: str, guide_version: str) -> tuple[dict[str, Any], str]:
    payload = _load_json_object(text)
    if payload is not None:
        evidence = payload.get("evidence", payload)
        payload_guide_version = str(payload.get("guide_version", guide_version))
        if isinstance(evidence, dict):
            return dict(evidence), payload_guide_version
        return {}, payload_guide_version
    return _parse_key_value_text(text), guide_version


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
    evidence: dict[str, Any] = {"collection_status": "collected"}
    for fact_key, fact_item_id in UNIX_FACT_TO_ITEM.items():
        if fact_item_id != item_id or fact_key not in facts:
            continue
        normalized = _normalize_fact(fact_key, facts[fact_key])
        if normalized is not None:
            evidence[fact_key] = normalized
    if len(evidence) == 1:
        return dict(MANUAL_EVIDENCE)
    return evidence


def _normalize_scalar(value: str) -> Any:
    lowered = value.lower()
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if lowered in {"true", "yes", "1", "on", "enabled", "secure", "restricted"}:
        return True
    if lowered in {"false", "no", "0", "off", "disabled", "insecure", "unrestricted"}:
        return False
    return value


def _normalize_fact(key: str, value: Any) -> Any:
    if key in COUNT_FACTS:
        if isinstance(value, bool):
            return int(value)
        try:
            return int(value)
        except (TypeError, ValueError):
            return None
    if isinstance(value, bool):
        return value
    if isinstance(value, int) and value in {0, 1}:
        return bool(value)
    if isinstance(value, str):
        scalar = _normalize_scalar(value)
        return scalar if isinstance(scalar, bool) else None
    return None
