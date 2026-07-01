from __future__ import annotations

import hashlib
import json
import re
from datetime import UTC, datetime
from typing import Any

from kcii_audit.parsers.windows_items import WINDOWS_ITEM_IDS, WINDOWS_ITEM_TITLES
from kcii_audit.schemas.evidence import EvidenceRecord

SAFE_FIELDS_BY_ITEM = {
    "W-01": {"collection_status", "administrator_account_renamed"},
    "W-02": {"collection_status", "guest_account_enabled"},
    "W-04": {"collection_status", "account_lockout_threshold", "account_lockout_threshold_ok"},
    "W-08": {
        "collection_status",
        "account_lockout_duration_minutes",
        "lockout_observation_window_minutes",
        "account_lockout_duration_ok",
    },
    "W-09": {
        "collection_status",
        "minimum_password_length",
        "maximum_password_age_days",
        "minimum_password_age_days",
        "password_history_size",
    },
    "W-10": {"collection_status", "last_username_hidden"},
    "W-13": {"collection_status", "blank_password_remote_logon_blocked"},
    "W-34": {"collection_status", "telnet_service_disabled"},
    "W-64": {"collection_status", "firewall_enabled"},
}

MANUAL_EVIDENCE = {
    "collection_status": "not_automated_by_windows_mvp",
    "manual_required": True,
    "reason": "official Windows Server item is registered, but the Windows MVP parser does not automate this item yet",
}


def records_from_windows_paste(
    text: str,
    *,
    asset_id: str = "windows-paste",
    guide_version: str = "kcii-2025-12",
) -> list[EvidenceRecord]:
    """Convert copied Windows Server results into normalized evidence records."""
    collected_at = datetime.now(UTC)
    raw_hash = "sha256:" + hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()
    facts = _parse_structured_json(text) or _parse_text_evidence(text)

    records: list[EvidenceRecord] = []
    for item_id in WINDOWS_ITEM_IDS:
        records.append(
            EvidenceRecord(
                asset_id=asset_id,
                platform="windows",
                os_name="Windows",
                guide_version=guide_version,
                item_id=item_id,
                item_title=WINDOWS_ITEM_TITLES[item_id],
                collected_at=collected_at,
                evidence=_evidence_for_item(item_id, facts.get(item_id)),
                raw_evidence_hash=raw_hash,
            )
        )
    return records


def _parse_structured_json(text: str) -> dict[str, dict[str, Any]] | None:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return None

    if not isinstance(payload, dict):
        return None

    items = payload.get("items")
    if not isinstance(items, list):
        return None

    parsed: dict[str, dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        evidence = item.get("evidence")
        if not isinstance(evidence, dict):
            continue
        item_id = _normalize_structured_item_id(str(item.get("item_id", "")), evidence)
        if item_id not in WINDOWS_ITEM_TITLES:
            continue
        parsed[item_id] = {**parsed.get(item_id, {}), **evidence}
    return parsed


def _normalize_structured_item_id(item_id: str, evidence: dict[str, Any]) -> str:
    # Compatibility with the first Windows MVP collector, whose IDs predated
    # the official full Windows Server item manifest.
    if "guest_account_enabled" in evidence:
        return "W-02"
    if "firewall_enabled" in evidence:
        return "W-64"
    if "minimum_password_length" in evidence:
        return "W-09"
    return item_id


def _parse_text_evidence(text: str) -> dict[str, dict[str, Any]]:
    parsed: dict[str, dict[str, Any]] = {}
    lower_text = text.lower()

    _add_bool(parsed, "W-01", "administrator_account_renamed", lower_text, ["administrator_account_renamed"])

    guest_enabled = _extract_first_bool_key_value(
        lower_text,
        ["guest_account_enabled", "guest_enabled", "guest_account_active", "guest_active"],
    )
    if guest_enabled is None:
        guest_enabled = _extract_guest_account_status(text)
    if guest_enabled is not None:
        parsed["W-02"] = {
            "collection_status": "collected",
            "guest_account_enabled": guest_enabled,
        }

    lockout_threshold = _extract_first_int_key_value(
        lower_text,
        ["account_lockout_threshold", "lockout_threshold"],
    )
    if lockout_threshold is None:
        lockout_threshold = _extract_net_accounts_int(text, ["Lockout threshold", "잠금 임계값"])
    if lockout_threshold is not None:
        parsed["W-04"] = {
            "collection_status": "collected",
            "account_lockout_threshold": lockout_threshold,
            "account_lockout_threshold_ok": 0 < lockout_threshold <= 5,
        }

    lockout_duration = _extract_first_int_key_value(
        lower_text,
        ["account_lockout_duration_minutes", "lockout_duration_minutes"],
    )
    if lockout_duration is None:
        lockout_duration = _extract_net_accounts_int(text, ["Lockout duration", "잠금 기간"])
    observation_window = _extract_first_int_key_value(
        lower_text,
        ["lockout_observation_window_minutes", "lockout_observation_window"],
    )
    if observation_window is None:
        observation_window = _extract_net_accounts_int(text, ["Lockout observation window", "잠금 관찰 창"])
    if lockout_duration is not None or observation_window is not None:
        duration_ok = (
            lockout_duration is not None
            and observation_window is not None
            and lockout_duration >= 60
            and observation_window >= 60
        )
        parsed["W-08"] = {
            "collection_status": "collected",
            "account_lockout_duration_minutes": lockout_duration,
            "lockout_observation_window_minutes": observation_window,
            "account_lockout_duration_ok": duration_ok,
        }

    min_length = _extract_first_int_key_value(
        lower_text,
        ["minimum_password_length", "min_password_length", "password_min_length"],
    )
    if min_length is None:
        min_length = _extract_minimum_password_length(text)
    if min_length is not None:
        parsed["W-09"] = {
            "collection_status": "collected",
            "minimum_password_length": min_length,
        }

    _add_bool(parsed, "W-10", "last_username_hidden", lower_text, ["last_username_hidden", "dontdisplaylastusername"])
    _add_bool(
        parsed,
        "W-13",
        "blank_password_remote_logon_blocked",
        lower_text,
        ["blank_password_remote_logon_blocked", "limitblankpassworduse"],
    )
    _add_bool(parsed, "W-34", "telnet_service_disabled", lower_text, ["telnet_service_disabled"])

    firewall_enabled = _extract_first_bool_key_value(
        lower_text,
        ["firewall_enabled", "windows_firewall_enabled"],
    )
    if firewall_enabled is None:
        firewall_enabled = _extract_firewall_status(text)
    if firewall_enabled is not None:
        parsed["W-64"] = {
            "collection_status": "collected",
            "firewall_enabled": firewall_enabled,
        }

    return parsed


def _evidence_for_item(item_id: str, evidence: dict[str, Any] | None) -> dict[str, Any]:
    if evidence is None:
        return dict(MANUAL_EVIDENCE)
    if item_id not in SAFE_FIELDS_BY_ITEM:
        return {
            key: value
            for key, value in evidence.items()
            if key in {"collection_status", "manual_required", "reason"}
        } or dict(MANUAL_EVIDENCE)

    allowed = SAFE_FIELDS_BY_ITEM[item_id]
    safe: dict[str, Any] = {}
    for key, value in evidence.items():
        if key not in allowed:
            continue
        safe[key] = _normalize_field_value(key, value)
    if "collection_status" not in safe:
        safe["collection_status"] = "collected"
    return safe


def _add_bool(
    parsed: dict[str, dict[str, Any]],
    item_id: str,
    evidence_key: str,
    text: str,
    source_keys: list[str],
) -> None:
    value = _extract_first_bool_key_value(text, source_keys)
    if value is not None:
        parsed[item_id] = {
            "collection_status": "collected",
            evidence_key: value,
        }


def _extract_first_bool_key_value(text: str, keys: list[str]) -> bool | None:
    for key in keys:
        value = _extract_bool_key_value(text, key)
        if value is not None:
            return value
    return None


def _extract_first_int_key_value(text: str, keys: list[str]) -> int | None:
    for key in keys:
        value = _extract_int_key_value(text, key)
        if value is not None:
            return value
    return None


def _extract_bool_key_value(text: str, key: str) -> bool | None:
    match = re.search(rf"^\s*{re.escape(key)}\s*[:=]\s*(true|false|yes|no|1|0|enabled|disabled)\s*$", text, re.MULTILINE)
    if not match:
        return None
    return _token_means_enabled(match.group(1))


def _extract_int_key_value(text: str, key: str) -> int | None:
    match = re.search(rf"^\s*{re.escape(key)}\s*[:=]\s*(\d+)\s*$", text, re.MULTILINE)
    return int(match.group(1)) if match else None


def _extract_net_accounts_int(text: str, labels: list[str]) -> int | None:
    for label in labels:
        match = re.search(rf"{re.escape(label)}\s*[:=]?\s*(\d+)", text, re.IGNORECASE)
        if match:
            return int(match.group(1))
    return None


def _extract_guest_account_status(text: str) -> bool | None:
    for line in text.splitlines():
        normalized = " ".join(line.strip().split()).lower()
        if not normalized:
            continue
        if normalized.startswith("account active"):
            return _line_means_enabled(normalized)
        if "guest" in normalized and "enabled" in normalized:
            return _line_means_enabled(normalized)
        if "guest" in normalized and "disabled" in normalized:
            return False
        if "계정" in line and ("활성" in line or "사용" in line):
            if "아니" in line or "사용 안" in line or "false" in normalized:
                return False
            if "예" in line or "사용" in line or "true" in normalized:
                return True
    return None


def _extract_firewall_status(text: str) -> bool | None:
    bool_values: list[bool] = []
    previous_name_line = False
    for line in text.splitlines():
        normalized = " ".join(line.strip().split()).lower()
        if not normalized:
            previous_name_line = False
            continue
        if re.match(r"^name\s*:\s*(domain|private|public)\b", normalized):
            previous_name_line = True
            continue
        if normalized.startswith(("domain", "private", "public")):
            enabled = _extract_enabled_token(normalized)
            if enabled is not None:
                bool_values.append(enabled)
            previous_name_line = False
        elif previous_name_line and normalized.startswith("enabled"):
            enabled = _extract_enabled_token(normalized)
            if enabled is not None:
                bool_values.append(enabled)
            previous_name_line = False
        elif "firewall" in normalized and ("enabled" in normalized or "disabled" in normalized):
            bool_values.append(_line_means_enabled(normalized))
            previous_name_line = False
    return all(bool_values) if bool_values else None


def _extract_minimum_password_length(text: str) -> int | None:
    patterns = [
        r"Minimum password length\s+(\d+)",
        r"Minimum password length\s*[:=]\s*(\d+)",
        r"최소\s*암호\s*길이\s*[:=]?\s*(\d+)",
        r"최소\s*비밀번호\s*길이\s*[:=]?\s*(\d+)",
        r"암호\s*최소\s*길이\s*[:=]?\s*(\d+)",
        r"비밀번호\s*최소\s*길이\s*[:=]?\s*(\d+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1))
    return None


def _line_means_enabled(line: str) -> bool:
    if any(token in line for token in ("false", "no", "disabled", "off", "아니", "사용 안")):
        return False
    return any(token in line for token in ("true", "yes", "enabled", "on", "예", "사용"))


def _extract_enabled_token(line: str) -> bool | None:
    tokens = set(re.split(r"[^a-z0-9가-힣]+", line.lower()))
    for token in ("false", "no", "disabled", "off"):
        if token in tokens:
            return False
    for token in ("true", "yes", "enabled", "on"):
        if token in tokens:
            return True
    if "아니" in line or "사용 안" in line:
        return False
    if "예" in line or "사용" in line:
        return True
    return None


def _token_means_enabled(token: str) -> bool:
    return token.lower() in {"true", "yes", "1", "enabled", "on", "예", "사용"}


def _normalize_field_value(field: str, value: Any) -> Any:
    if field in {
        "administrator_account_renamed",
        "guest_account_enabled",
        "account_lockout_threshold_ok",
        "account_lockout_duration_ok",
        "last_username_hidden",
        "blank_password_remote_logon_blocked",
        "telnet_service_disabled",
        "firewall_enabled",
    }:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return _token_means_enabled(value)
        return None
    if field in {
        "account_lockout_threshold",
        "account_lockout_duration_minutes",
        "lockout_observation_window_minutes",
        "minimum_password_length",
        "maximum_password_age_days",
        "minimum_password_age_days",
        "password_history_size",
    }:
        if isinstance(value, bool):
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None
    if field == "collection_status":
        return str(value)
    return value
