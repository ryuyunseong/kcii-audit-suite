from __future__ import annotations

import hashlib
import re
from datetime import UTC, datetime
from typing import Any

from kcii_audit.parsers.network_cisco_ios import NETWORK_ITEMS, SIMPLE_BOOLEAN_ITEM_FIELDS
from kcii_audit.schemas.evidence import EvidenceRecord

INHERITANCE_POSITIVE_OVERRIDES = {
    "ssh_enabled",
    "banner_configured",
    "logging_host_configured",
    "ntp_configured",
    "timestamp_log_configured",
    "snmp_service_present",
    "snmp_read_only",
}


def records_from_junos_paste(
    text: str,
    *,
    asset_id: str = "network-junos-paste",
    guide_version: str = "kcii-2025-12",
) -> list[EvidenceRecord]:
    """Convert copied Junos display-set output into normalized network evidence."""
    collected_at = datetime.now(UTC)
    raw_hash = "sha256:" + hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()
    facts = _extract_facts(text)

    records: list[EvidenceRecord] = []
    for item_id, title in NETWORK_ITEMS:
        records.append(
            EvidenceRecord(
                asset_id=asset_id,
                platform="network",
                os_name="Juniper Junos",
                os_version=None,
                guide_version=guide_version,
                item_id=item_id,
                item_title=title,
                collected_at=collected_at,
                evidence=_evidence_for_item(item_id, facts),
                raw_evidence_hash=raw_hash,
            )
        )
    return records


def _extract_facts(text: str) -> dict[str, Any]:
    active_lines, inactive_lines = _split_display_set_lines(text)
    inheritance_facts = _extract_display_inheritance_facts(text)
    if not active_lines:
        if inheritance_facts["present"]:
            return _facts_from_display_inheritance(inheritance_facts)
        if _looks_like_brace_config(text):
            return {
                "recognized": False,
                "collection_status": "needs_display_set",
                "manual_reason": "Junos brace-style configuration is not parsed by the v1.2.0 MVP; provide show configuration | display set output",
            }
        if _looks_like_xml_config(text):
            return {
                "recognized": False,
                "collection_status": "unsupported_format",
                "manual_reason": "Junos XML configuration is not parsed by the display-set parser",
            }
        if _looks_like_json_config(text):
            return {
                "recognized": False,
                "collection_status": "unsupported_format",
                "manual_reason": "Junos JSON configuration is not parsed by the display-set parser",
            }
        return {
            "recognized": False,
            "collection_status": "unsupported_output",
            "manual_reason": "Junos display-set configuration lines were not found",
        }

    lower_lines = [line.lower() for line in active_lines]
    recognized = any(
        line.startswith(
            (
                "set system ",
                "set interfaces ",
                "set security ",
                "set protocols ",
                "set snmp ",
                "set firewall ",
                "set forwarding-options ",
            )
        )
        for line in lower_lines
    )
    if not recognized:
        return {
            "recognized": False,
            "collection_status": "unsupported_output",
            "manual_reason": "supported Junos display-set configuration lines were not found",
        }

    encrypted_password_present = _line_exists(active_lines, r"set\s+system\s+(root-authentication|login\s+user\s+\S+\s+authentication)\s+encrypted-password\b")
    plaintext_password_present = _line_exists(active_lines, r"set\s+system\s+(root-authentication|login\s+user\s+\S+\s+authentication)\s+plain-text-password\b")
    password_configured = True if encrypted_password_present or plaintext_password_present else None
    encrypted_passwords_only = None
    if encrypted_password_present or plaintext_password_present:
        encrypted_passwords_only = encrypted_password_present and not plaintext_password_present

    ssh_enabled = _line_exists(active_lines, r"set\s+system\s+services\s+ssh\b")
    telnet_allowed = _line_exists(active_lines, r"set\s+system\s+services\s+telnet\b")
    safe_vty_protocol = None
    if ssh_enabled or telnet_allowed:
        safe_vty_protocol = ssh_enabled and not telnet_allowed

    idle_timeout = _extract_positive_int(active_lines, r"set\s+system\s+login\s+idle-timeout\s+(?P<value>\d+)\b")
    exec_timeout_configured = None if idle_timeout is None else idle_timeout > 0

    snmp_communities = _snmp_community_tokens(active_lines)
    snmp_lines = _matching_lines(active_lines, r"set\s+snmp\s+community\s+\S+\b")
    weak_snmp = any(_is_weak_snmp_line(line) for line in snmp_lines)
    inheritance_required = _has_apply_groups(active_lines)

    facts = {
        "recognized": True,
        "collection_status": "collected",
        "input_format": "junos_display_set",
        "inactive_lines_ignored": bool(inactive_lines),
        "inheritance_required": inheritance_required,
        "password_configured": password_configured,
        "encrypted_passwords_only": encrypted_passwords_only,
        "plaintext_password_present": plaintext_password_present,
        "management_acl_applied": _management_acl_applied(active_lines),
        "exec_timeout_configured": exec_timeout_configured,
        "ssh_enabled": ssh_enabled,
        "telnet_allowed": telnet_allowed,
        "safe_vty_protocol": safe_vty_protocol,
        "banner_configured": _line_exists(active_lines, r"set\s+system\s+login\s+(message|announcement)\b"),
        "logging_host_configured": _line_exists(active_lines, r"set\s+system\s+syslog\s+host\b"),
        "ntp_configured": _line_exists(active_lines, r"set\s+system\s+ntp\s+(server|peer)\b"),
        "timestamp_log_configured": True
        if _line_exists(active_lines, r"set\s+system\s+syslog\s+time-format\b")
        else None,
        "snmp_service_present": bool(snmp_lines),
        "snmp_community_complex": None if not snmp_lines else not weak_snmp,
        "snmp_acl_configured": _snmp_acl_configured(active_lines, snmp_communities),
        "snmp_read_only": _snmp_read_only(active_lines, snmp_communities),
        "tftp_service_blocked": False if _line_exists(active_lines, r"set\s+system\s+services\s+tftp\b") else None,
        "tcp_keepalives_configured": None,
        "finger_service_blocked": False if _line_exists(active_lines, r"set\s+system\s+services\s+finger\b") else None,
        "web_service_blocked": False if _line_exists(active_lines, r"set\s+system\s+services\s+web-management\b") else None,
        "small_services_blocked": None,
        "bootp_service_blocked": False if _line_exists(active_lines, r"set\s+forwarding-options\s+helpers\s+bootp\b") else None,
        "cdp_service_blocked": None,
        "directed_broadcast_blocked": False
        if _line_exists(active_lines, r"set\s+forwarding-options\s+directed-broadcast\b")
        else None,
        "source_route_blocked": True
        if _line_exists(active_lines, r"set\s+system\s+internet-options\s+no-source-route\b")
        else None,
        "proxy_arp_blocked": False if _line_exists(active_lines, r"set\s+interfaces\s+.*\bproxy-arp\b") else None,
        "icmp_control_messages_blocked": True if _line_exists(active_lines, r"set\s+system\s+no-redirects\b") else None,
        "identd_service_blocked": None,
        "domain_lookup_blocked": None,
        "pad_service_blocked": None,
        "mask_reply_blocked": None,
    }
    return _merge_inheritance_facts(facts, inheritance_facts)


def _evidence_for_item(item_id: str, facts: dict[str, Any]) -> dict[str, Any]:
    if facts.get("recognized") is False:
        return {
            "collection_status": facts["collection_status"],
            "manual_required": True,
            "reason": facts["manual_reason"],
        }

    base = {
        "collection_status": facts["collection_status"],
        "input_format": facts["input_format"],
    }
    if facts.get("inactive_lines_ignored"):
        base["inactive_lines_ignored"] = True
    if facts.get("inheritance_required"):
        base["inheritance_required"] = True
    if facts.get("inheritance_available"):
        base["inheritance_available"] = True
    if facts.get("inheritance_conflict"):
        base["inheritance_conflict"] = True
    if facts.get("inheritance_incomplete"):
        base["inheritance_incomplete"] = True
    if "inheritance_source_count" in facts:
        base["inheritance_source_count"] = facts["inheritance_source_count"]
    if facts.get("automation_scope"):
        base["automation_scope"] = facts["automation_scope"]

    if facts.get("inheritance_blocks_automation"):
        return base | {
            "manual_required": True,
            "reason": _manual_reason(facts),
        }

    if item_id == "N-01":
        return base | {"password_configured": facts["password_configured"]}
    if item_id == "N-03":
        return base | {
            "encrypted_passwords_only": facts["encrypted_passwords_only"],
            "plaintext_password_present": facts["plaintext_password_present"],
        }
    if item_id == "N-06":
        return base | {"management_acl_applied": facts["management_acl_applied"]}
    if item_id == "N-07":
        return base | {"exec_timeout_configured": facts["exec_timeout_configured"]}
    if item_id == "N-08":
        return base | {
            "ssh_enabled": facts["ssh_enabled"],
            "telnet_allowed": facts["telnet_allowed"],
            "safe_vty_protocol": facts["safe_vty_protocol"],
        }
    if item_id == "N-10":
        return base | {"banner_configured": facts["banner_configured"]}
    if item_id == "N-11":
        return base | {"logging_host_configured": facts["logging_host_configured"]}
    if item_id == "N-15":
        return base | {"ntp_configured": facts["ntp_configured"]}
    if item_id == "N-18":
        return base | {
            "snmp_service_present": facts["snmp_service_present"],
            "snmp_community_complex": facts["snmp_community_complex"],
        }
    if item_id in SIMPLE_BOOLEAN_ITEM_FIELDS:
        field = SIMPLE_BOOLEAN_ITEM_FIELDS[item_id]
        return base | {field: facts[field]}
    return base | {
        "manual_required": True,
        "reason": _manual_reason(facts),
    }


def _split_display_set_lines(text: str) -> tuple[list[str], list[str]]:
    active: list[str] = []
    inactive: list[str] = []
    for raw_line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        line = raw_line.replace("\x08", "").replace("--More--", "").strip()
        line = _strip_prompt_prefix(line)
        if not line or line.startswith("#") or re.fullmatch(r"[-=]{3,}", line):
            continue
        lowered = line.lower()
        if "show configuration" in lowered and "display set" in lowered:
            continue
        if line.endswith(">") or line.endswith("#"):
            continue
        if lowered.startswith("inactive:"):
            inactive_line = line.split(":", 1)[1].strip()
            if inactive_line:
                inactive.append(inactive_line)
            continue
        if lowered.startswith("deactivate "):
            inactive.append(line)
            continue
        if lowered.startswith("set "):
            active.append(re.sub(r"\s+", " ", line))
    return active, inactive


def _extract_display_inheritance_facts(text: str) -> dict[str, Any]:
    lines, inactive_lines = _split_display_inheritance_lines(text)
    if not lines:
        return {"present": False}

    source_count = 0
    effective_lines: list[str] = []
    conflict_lines: list[str] = []
    incomplete = False

    for line in lines:
        lowered = line.lower()
        if lowered.startswith("inheritance-source"):
            if re.search(r"(?i)\b(missing|unknown)\b", line):
                incomplete = True
                continue
            source_count += 1
            continue
        if lowered.startswith("apply-groups-except"):
            incomplete = True
            continue
        if lowered.startswith("conflict-statement"):
            conflict_lines.append(_strip_inheritance_source(line.removeprefix("conflict-statement").strip()))
            continue
        if lowered.startswith("effective-statement"):
            if re.search(r"(?i)\bsource-group\s+(missing|unknown)\b", line) or " source-group " not in lowered:
                incomplete = True
            effective_lines.append(_strip_inheritance_source(line.removeprefix("effective-statement").strip()))

    conflict = bool(conflict_lines)
    fields = _inherited_effective_fields(effective_lines) if effective_lines and not conflict and not incomplete else {}
    return {
        "present": True,
        "available": bool(effective_lines),
        "source_count": source_count,
        "conflict": conflict,
        "incomplete": incomplete,
        "inactive_lines_ignored": bool(inactive_lines),
        "fields": fields,
    }


def _split_display_inheritance_lines(text: str) -> tuple[list[str], list[str]]:
    active: list[str] = []
    inactive: list[str] = []
    for raw_line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        line = raw_line.replace("\x08", "").replace("--More--", "").strip()
        line = _strip_prompt_prefix(line)
        if not line or line.startswith("#") or re.fullmatch(r"[-=]{3,}", line):
            continue
        lowered = line.lower()
        if "show configuration" in lowered and "display inheritance" in lowered:
            continue
        if line.endswith(">") or line.endswith("#"):
            continue
        if lowered.startswith("inactive:"):
            inactive_line = line.split(":", 1)[1].strip()
            if inactive_line:
                inactive.append(inactive_line)
            continue
        if lowered.startswith("deactivate "):
            inactive.append(line)
            continue
        if lowered.startswith(("inheritance-source", "effective-statement", "conflict-statement", "apply-groups-except")):
            active.append(re.sub(r"\s+", " ", line))
    return active, inactive


def _facts_from_display_inheritance(inheritance_facts: dict[str, Any]) -> dict[str, Any]:
    facts = _empty_junos_facts("junos_display_inheritance")
    facts.update(
        {
            "inheritance_required": True,
            "inheritance_available": inheritance_facts["available"],
            "inheritance_conflict": inheritance_facts["conflict"],
            "inheritance_incomplete": inheritance_facts["incomplete"],
            "inheritance_source_count": inheritance_facts["source_count"],
            "inactive_lines_ignored": inheritance_facts["inactive_lines_ignored"],
            "automation_scope": "manual_review"
            if inheritance_facts["conflict"] or inheritance_facts["incomplete"]
            else "partial",
            "inheritance_blocks_automation": inheritance_facts["conflict"] or inheritance_facts["incomplete"],
        }
    )
    if not facts["inheritance_blocks_automation"]:
        facts.update(inheritance_facts["fields"])
    return facts


def _empty_junos_facts(input_format: str) -> dict[str, Any]:
    return {
        "recognized": True,
        "collection_status": "collected",
        "input_format": input_format,
        "inactive_lines_ignored": False,
        "inheritance_required": False,
        "inheritance_available": False,
        "inheritance_conflict": False,
        "inheritance_incomplete": False,
        "inheritance_source_count": 0,
        "automation_scope": "manual_review",
        "inheritance_blocks_automation": False,
        "password_configured": None,
        "encrypted_passwords_only": None,
        "plaintext_password_present": None,
        "management_acl_applied": None,
        "exec_timeout_configured": None,
        "ssh_enabled": None,
        "telnet_allowed": None,
        "safe_vty_protocol": None,
        "banner_configured": None,
        "logging_host_configured": None,
        "ntp_configured": None,
        "timestamp_log_configured": None,
        "snmp_service_present": None,
        "snmp_community_complex": None,
        "snmp_acl_configured": None,
        "snmp_read_only": None,
        "tftp_service_blocked": None,
        "tcp_keepalives_configured": None,
        "finger_service_blocked": None,
        "web_service_blocked": None,
        "small_services_blocked": None,
        "bootp_service_blocked": None,
        "cdp_service_blocked": None,
        "directed_broadcast_blocked": None,
        "source_route_blocked": None,
        "proxy_arp_blocked": None,
        "icmp_control_messages_blocked": None,
        "identd_service_blocked": None,
        "domain_lookup_blocked": None,
        "pad_service_blocked": None,
        "mask_reply_blocked": None,
    }


def _merge_inheritance_facts(facts: dict[str, Any], inheritance_facts: dict[str, Any]) -> dict[str, Any]:
    if not inheritance_facts["present"]:
        facts["inheritance_available"] = False
        facts["inheritance_conflict"] = False
        facts["inheritance_incomplete"] = False
        facts["inheritance_source_count"] = 0
        facts["automation_scope"] = "display_set"
        facts["inheritance_blocks_automation"] = False
        return facts

    facts["input_format"] = "junos_display_set_with_inheritance"
    facts["inheritance_required"] = True
    facts["inheritance_available"] = inheritance_facts["available"]
    facts["inheritance_conflict"] = inheritance_facts["conflict"]
    facts["inheritance_incomplete"] = inheritance_facts["incomplete"]
    facts["inheritance_source_count"] = inheritance_facts["source_count"]
    facts["inactive_lines_ignored"] = facts.get("inactive_lines_ignored", False) or inheritance_facts["inactive_lines_ignored"]
    facts["automation_scope"] = (
        "manual_review"
        if inheritance_facts["conflict"] or inheritance_facts["incomplete"]
        else "partial"
    )
    facts["inheritance_blocks_automation"] = inheritance_facts["conflict"] or inheritance_facts["incomplete"]
    if facts["inheritance_blocks_automation"]:
        return facts

    for field, value in inheritance_facts["fields"].items():
        if value is None:
            continue
        if facts.get(field) is None or (field in INHERITANCE_POSITIVE_OVERRIDES and facts.get(field) is False and value is True):
            facts[field] = value
    return facts


def _strip_inheritance_source(line: str) -> str:
    return re.sub(r"(?i)\s+source-group\s+\S+\s*$", "", line).strip()


def _inherited_effective_fields(lines: list[str]) -> dict[str, Any]:
    ssh_enabled = _inherited_line_exists(lines, r"system\s+services\s+ssh\b")
    telnet_absent = _inherited_line_exists(lines, r"system\s+services\s+telnet\s+absent\b")
    telnet_allowed = True if _inherited_line_exists(lines, r"system\s+services\s+telnet\b") and not telnet_absent else None
    if telnet_absent:
        telnet_allowed = False
    safe_vty_protocol = None
    if ssh_enabled is not None or telnet_allowed is not None:
        safe_vty_protocol = bool(ssh_enabled) and telnet_allowed is False

    snmp_service_present = True if _inherited_line_exists(lines, r"snmp\s+community\b") else None
    snmp_read_only = None
    if snmp_service_present:
        if _inherited_line_exists(lines, r"snmp\s+community\s+\S+\s+authorization\s+read-write\b"):
            snmp_read_only = False
        elif _inherited_line_exists(lines, r"snmp\s+community\s+\S+\s+authorization\s+read-only\b"):
            snmp_read_only = True

    idle_timeout = _extract_inherited_positive_int(lines, r"system\s+login\s+idle-timeout\s+(?P<value>\d+)\b")
    return {
        "exec_timeout_configured": None if idle_timeout is None else idle_timeout > 0,
        "ssh_enabled": ssh_enabled,
        "telnet_allowed": telnet_allowed,
        "safe_vty_protocol": safe_vty_protocol,
        "banner_configured": True if _inherited_line_exists(lines, r"system\s+login\s+(message|announcement)\b") else None,
        "logging_host_configured": True if _inherited_line_exists(lines, r"system\s+syslog\s+host\b") else None,
        "ntp_configured": True if _inherited_line_exists(lines, r"system\s+ntp\s+(server|peer)\b") else None,
        "timestamp_log_configured": True if _inherited_line_exists(lines, r"system\s+syslog\s+time-format\b") else None,
        "snmp_service_present": snmp_service_present,
        "snmp_read_only": snmp_read_only,
    }


def _inherited_line_exists(lines: list[str], pattern: str) -> bool | None:
    regex = re.compile(rf"(?i)^{pattern}")
    return True if any(regex.search(line) for line in lines) else None


def _extract_inherited_positive_int(lines: list[str], pattern: str) -> int | None:
    regex = re.compile(rf"(?i)^{pattern}")
    for line in lines:
        match = regex.search(line)
        if match:
            return int(match.group("value"))
    return None


def _strip_prompt_prefix(line: str) -> str:
    return re.sub(r"^\S+@\S+[>#]\s+", "", line)


def _looks_like_brace_config(text: str) -> bool:
    return bool(re.search(r"(?m)^\s*(system|interfaces|security|protocols|snmp|firewall)\s*\{", text)) and "}" in text


def _looks_like_xml_config(text: str) -> bool:
    stripped = text.lstrip()
    return stripped.startswith("<") and bool(re.search(r"<(configuration|system|interfaces|security|protocols)\b", stripped, re.IGNORECASE))


def _looks_like_json_config(text: str) -> bool:
    stripped = text.lstrip()
    return stripped.startswith("{") and bool(re.search(r'"(configuration|system|interfaces|security|protocols)"\s*:', stripped, re.IGNORECASE))


def _has_apply_groups(lines: list[str]) -> bool:
    return any(
        re.search(r"(?i)^set\s+(apply-groups\b|.+\sapply-groups\b)", line)
        for line in lines
    )


def _manual_reason(facts: dict[str, Any]) -> str:
    if facts.get("inheritance_conflict"):
        return "Junos inherited configuration contains conflicting statements; assessor review is required"
    if facts.get("inheritance_incomplete"):
        return "Junos inherited configuration is incomplete or source context is missing; assessor review is required"
    if facts.get("inheritance_required"):
        return "Junos apply-groups or inherited configuration is present; full inheritance expansion is not automated and assessor review is required"
    return "official network item is registered, but the Junos display-set MVP parser does not automate this item yet"


def _line_exists(lines: list[str], pattern: str) -> bool:
    regex = re.compile(rf"(?i)^{pattern}")
    return any(regex.search(line) for line in lines)


def _matching_lines(lines: list[str], pattern: str) -> list[str]:
    regex = re.compile(rf"(?i)^{pattern}")
    return [line for line in lines if regex.search(line)]


def _extract_positive_int(lines: list[str], pattern: str) -> int | None:
    regex = re.compile(rf"(?i)^{pattern}")
    for line in lines:
        match = regex.search(line)
        if match:
            return int(match.group("value"))
    return None


def _management_acl_applied(lines: list[str]) -> bool | None:
    filter_names = {
        match.group("name")
        for line in lines
        if (match := re.search(r"(?i)^set\s+firewall\s+family\s+inet\s+filter\s+(?P<name>\S+)\s+term\s+\S+\s+from\s+(source-address|source-prefix-list)\b", line))
    }
    if not filter_names:
        return None
    applied_filters = {
        match.group("name")
        for line in lines
        if (match := re.search(r"(?i)^set\s+interfaces\s+\S+.*\s+family\s+inet\s+filter\s+input\s+(?P<name>\S+)(?:\s|$)", line))
    }
    return bool(filter_names & applied_filters)


def _snmp_community_tokens(lines: list[str]) -> set[str]:
    tokens: set[str] = set()
    for line in lines:
        match = re.search(r"(?i)^set\s+snmp\s+community\s+(?P<token>\S+)(?:\s|$)", line)
        if match:
            tokens.add(match.group("token"))
    return tokens


def _is_weak_snmp_line(line: str) -> bool:
    return bool(re.search(r"(?i)\b(public|private)\b", line))


def _snmp_acl_configured(lines: list[str], communities: set[str]) -> bool | None:
    if not communities:
        return None
    return all(
        any(
            re.search(rf"(?i)^set\s+snmp\s+community\s+{re.escape(community)}\s+(clients|client-list-name)(?:\s|$)", line)
            for line in lines
        )
        for community in communities
    )


def _snmp_read_only(lines: list[str], communities: set[str]) -> bool | None:
    if not communities:
        return None
    has_read_write = any(
        re.search(rf"(?i)^set\s+snmp\s+community\s+{re.escape(community)}\s+authorization\s+read-write(?:\s|$)", line)
        for community in communities
        for line in lines
    )
    if has_read_write:
        return False
    has_read_only_for_all = all(
        any(
            re.search(rf"(?i)^set\s+snmp\s+community\s+{re.escape(community)}\s+authorization\s+read-only(?:\s|$)", line)
            for line in lines
        )
        for community in communities
    )
    return True if has_read_only_for_all else None
