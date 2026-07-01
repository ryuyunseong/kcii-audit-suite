from __future__ import annotations

import hashlib
import re
from datetime import UTC, datetime
from typing import Any

from kcii_audit.schemas.evidence import EvidenceRecord

NETWORK_ITEMS: list[tuple[str, str]] = [
    ("N-01", "비밀번호 설정"),
    ("N-02", "비밀번호 복잡성 설정"),
    ("N-03", "암호화된 비밀번호 가용"),
    ("N-04", "계정 잠금 임계값 설정"),
    ("N-05", "사용자, 명령어별 권한 수준 설정"),
    ("N-06", "VTY 접근(ACL) 설정"),
    ("N-07", "세션 종료 시간 설정"),
    ("N-08", "VTY 접속 시 안전한 프로토콜 사용"),
    ("N-09", "불필요한 보조 입출력 포트 사용 금지"),
    ("N-10", "로그온 시 경고 메시지 설정"),
    ("N-11", "원격 로그서버 사용"),
    ("N-12", "주기적 보안 패치 및 벤더 권고사항 적용"),
    ("N-13", "로깅 버퍼 크기 설정"),
    ("N-14", "정책에 따른 로깅 설정"),
    ("N-15", "NTP 및 시각 동기화 설정"),
    ("N-16", "Timestamp 로그 설정"),
    ("N-17", "SNMP 서비스 확인"),
    ("N-18", "SNMP Community String 복잡성 설정"),
    ("N-19", "SNMP ACL 설정"),
    ("N-20", "SNMP Community 권한 설정"),
    ("N-21", "TFTP 서비스 차단"),
    ("N-22", "Spoofing 방지 필터링 적용"),
    ("N-23", "DDoS 공격 방어 설정 또는 DDoS 장비 사용"),
    ("N-24", "사용하지 않는 인터페이스 비활성화"),
    ("N-25", "TCP Keepalive 서비스 설정"),
    ("N-26", "Finger 서비스 차단"),
    ("N-27", "웹 서비스 차단"),
    ("N-28", "TCP/UDP small 서비스 차단"),
    ("N-29", "Bootp 서비스 차단"),
    ("N-30", "CDP 서비스 차단"),
    ("N-31", "Directed-broadcast 차단"),
    ("N-32", "Source 라우팅 차단"),
    ("N-33", "Proxy ARP 차단"),
    ("N-34", "ICMP unreachable, Redirect 차단"),
    ("N-35", "identd 서비스 차단"),
    ("N-36", "Domain Lookup 차단"),
    ("N-37", "pad 차단"),
    ("N-38", "mask-reply 차단"),
]

AUTO_ITEMS = {
    "N-01",
    "N-03",
    "N-06",
    "N-07",
    "N-08",
    "N-10",
    "N-11",
    "N-15",
    "N-16",
    "N-18",
    "N-19",
    "N-20",
    "N-21",
    "N-25",
    "N-26",
    "N-27",
    "N-28",
    "N-29",
    "N-30",
    "N-31",
    "N-32",
    "N-33",
    "N-34",
    "N-35",
    "N-36",
    "N-37",
    "N-38",
}

SIMPLE_BOOLEAN_ITEM_FIELDS = {
    "N-16": "timestamp_log_configured",
    "N-19": "snmp_acl_configured",
    "N-20": "snmp_read_only",
    "N-21": "tftp_service_blocked",
    "N-25": "tcp_keepalives_configured",
    "N-26": "finger_service_blocked",
    "N-27": "web_service_blocked",
    "N-28": "small_services_blocked",
    "N-29": "bootp_service_blocked",
    "N-30": "cdp_service_blocked",
    "N-31": "directed_broadcast_blocked",
    "N-32": "source_route_blocked",
    "N-33": "proxy_arp_blocked",
    "N-34": "icmp_control_messages_blocked",
    "N-35": "identd_service_blocked",
    "N-36": "domain_lookup_blocked",
    "N-37": "pad_service_blocked",
    "N-38": "mask_reply_blocked",
}


def records_from_cisco_ios_paste(
    text: str,
    *,
    asset_id: str = "network-paste",
    guide_version: str = "kcii-2025-12",
) -> list[EvidenceRecord]:
    """Convert copied Cisco IOS command output into normalized network evidence."""
    collected_at = datetime.now(UTC)
    raw_hash = "sha256:" + hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()
    facts = _extract_facts(text)
    os_version = _extract_ios_version(text)

    records: list[EvidenceRecord] = []
    for item_id, title in NETWORK_ITEMS:
        records.append(
            EvidenceRecord(
                asset_id=asset_id,
                platform="network",
                os_name="Cisco IOS",
                os_version=os_version,
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
    lower = text.lower()
    recognized = any(marker in lower for marker in ("show running-config", "cisco ios", "line vty", "enable "))
    if not recognized:
        return {
            "recognized": False,
            "collection_status": "unsupported_output",
            "manual_reason": "supported Cisco IOS command output was not found",
        }

    enable_secret_configured = _line_exists(text, r"enable\s+secret\b")
    enable_password_configured = _line_exists(text, r"enable\s+password\b")
    password_configured = bool(
        enable_secret_configured
        or enable_password_configured
        or _line_exists(text, r"\bpassword\s+(0\s+)?\S+")
        or _line_exists(text, r"username\s+\S+.*\bsecret\b")
    )
    plaintext_password_present = bool(
        enable_password_configured
        or _line_exists(text, r"\bpassword\s+0\s+\S+")
        or _line_exists(text, r"username\s+\S+.*\bpassword\s+0\b")
    )
    encrypted_passwords_only = enable_secret_configured and not plaintext_password_present

    telnet_allowed = _line_exists(text, r"transport\s+input\s+.*\btelnet\b") or _line_exists(
        text,
        r"transport\s+input\s+all\b",
    )
    ssh_enabled = "ssh enabled" in lower or _line_exists(text, r"ip\s+ssh\s+version\b") or _line_exists(
        text,
        r"transport\s+input\s+.*\bssh\b",
    )
    safe_vty_protocol = ssh_enabled and not telnet_allowed

    exec_timeout_configured = any(
        not re.search(r"\b0\s+0\b", line)
        for line in _matching_lines(text, r"exec-timeout\s+\d+\s+\d+")
    )
    snmp_lines = _matching_lines(text, r"snmp-server\s+community\b")
    weak_snmp_community_present = any(_is_weak_snmp_line(line) for line in snmp_lines)

    return {
        "recognized": True,
        "collection_status": "collected",
        "password_configured": password_configured,
        "enable_secret_configured": enable_secret_configured,
        "plaintext_password_present": plaintext_password_present,
        "encrypted_passwords_only": encrypted_passwords_only,
        "management_acl_applied": _line_exists(text, r"\baccess-class\s+\S+\s+in\b"),
        "exec_timeout_configured": exec_timeout_configured,
        "ssh_enabled": ssh_enabled,
        "telnet_allowed": telnet_allowed,
        "safe_vty_protocol": safe_vty_protocol,
        "banner_configured": _line_exists(text, r"banner\s+(motd|login)\b"),
        "logging_host_configured": _line_exists(text, r"logging\s+host\b") or "logging to [" in lower,
        "ntp_configured": _line_exists(text, r"ntp\s+server\b") or "clock is synchronized" in lower,
        "timestamp_log_configured": _explicit_enabled_state(
            text,
            enabled_pattern=r"service\s+timestamps\s+log\b",
            disabled_pattern=r"no\s+service\s+timestamps\s+log\b",
        ),
        "snmp_community_complex": not weak_snmp_community_present,
        "snmp_service_present": bool(snmp_lines or "snmp agent enabled" in lower),
        "snmp_acl_configured": _snmp_acl_configured(snmp_lines),
        "snmp_read_only": _snmp_read_only(snmp_lines),
        "tftp_service_blocked": not _line_exists(text, r"tftp-server\b"),
        "tcp_keepalives_configured": _line_exists(text, r"service\s+tcp-keepalives-in\b")
        and _line_exists(text, r"service\s+tcp-keepalives-out\b"),
        "finger_service_blocked": _explicit_blocked_state(
            text,
            enabled_pattern=r"service\s+finger\b",
            disabled_pattern=r"no\s+service\s+finger\b",
        ),
        "web_service_blocked": _all_blocked_state(
            text,
            [
                (r"ip\s+http\s+server\b", r"no\s+ip\s+http\s+server\b"),
                (r"ip\s+http\s+secure-server\b", r"no\s+ip\s+http\s+secure-server\b"),
            ],
        ),
        "small_services_blocked": _all_blocked_state(
            text,
            [
                (r"service\s+tcp-small-servers\b", r"no\s+service\s+tcp-small-servers\b"),
                (r"service\s+udp-small-servers\b", r"no\s+service\s+udp-small-servers\b"),
            ],
        ),
        "bootp_service_blocked": _explicit_blocked_state(
            text,
            enabled_pattern=r"ip\s+bootp\s+server\b",
            disabled_pattern=r"no\s+ip\s+bootp\s+server\b",
        ),
        "cdp_service_blocked": _explicit_blocked_state(
            text,
            enabled_pattern=r"cdp\s+run\b",
            disabled_pattern=r"no\s+cdp\s+run\b",
        ),
        "directed_broadcast_blocked": _explicit_blocked_state(
            text,
            enabled_pattern=r"ip\s+directed-broadcast\b",
            disabled_pattern=r"no\s+ip\s+directed-broadcast\b",
        ),
        "source_route_blocked": _explicit_blocked_state(
            text,
            enabled_pattern=r"ip\s+source-route\b",
            disabled_pattern=r"no\s+ip\s+source-route\b",
        ),
        "proxy_arp_blocked": _explicit_blocked_state(
            text,
            enabled_pattern=r"ip\s+proxy-arp\b",
            disabled_pattern=r"no\s+ip\s+proxy-arp\b",
        ),
        "icmp_control_messages_blocked": _all_blocked_state(
            text,
            [
                (r"ip\s+redirects\b", r"no\s+ip\s+redirects\b"),
                (r"ip\s+unreachables\b", r"no\s+ip\s+unreachables\b"),
            ],
        ),
        "identd_service_blocked": _explicit_blocked_state(
            text,
            enabled_pattern=r"ip\s+identd\b",
            disabled_pattern=r"no\s+ip\s+identd\b",
        ),
        "domain_lookup_blocked": _explicit_blocked_state(
            text,
            enabled_pattern=r"ip\s+domain-lookup\b",
            disabled_pattern=r"no\s+ip\s+domain-lookup\b",
        ),
        "pad_service_blocked": _explicit_blocked_state(
            text,
            enabled_pattern=r"service\s+pad\b",
            disabled_pattern=r"no\s+service\s+pad\b",
        ),
        "mask_reply_blocked": _explicit_blocked_state(
            text,
            enabled_pattern=r"ip\s+mask-reply\b",
            disabled_pattern=r"no\s+ip\s+mask-reply\b",
        ),
    }


def _evidence_for_item(item_id: str, facts: dict[str, Any]) -> dict[str, Any]:
    if facts.get("recognized") is False:
        return {
            "collection_status": facts["collection_status"],
            "manual_required": True,
            "reason": facts["manual_reason"],
        }

    if item_id == "N-01":
        return {
            "collection_status": facts["collection_status"],
            "password_configured": facts["password_configured"],
        }
    if item_id == "N-03":
        return {
            "collection_status": facts["collection_status"],
            "enable_secret_configured": facts["enable_secret_configured"],
            "plaintext_password_present": facts["plaintext_password_present"],
            "encrypted_passwords_only": facts["encrypted_passwords_only"],
        }
    if item_id == "N-06":
        return {
            "collection_status": facts["collection_status"],
            "management_acl_applied": facts["management_acl_applied"],
        }
    if item_id == "N-07":
        return {
            "collection_status": facts["collection_status"],
            "exec_timeout_configured": facts["exec_timeout_configured"],
        }
    if item_id == "N-08":
        return {
            "collection_status": facts["collection_status"],
            "ssh_enabled": facts["ssh_enabled"],
            "telnet_allowed": facts["telnet_allowed"],
            "safe_vty_protocol": facts["safe_vty_protocol"],
        }
    if item_id == "N-10":
        return {
            "collection_status": facts["collection_status"],
            "banner_configured": facts["banner_configured"],
        }
    if item_id == "N-11":
        return {
            "collection_status": facts["collection_status"],
            "logging_host_configured": facts["logging_host_configured"],
        }
    if item_id == "N-15":
        return {
            "collection_status": facts["collection_status"],
            "ntp_configured": facts["ntp_configured"],
        }
    if item_id == "N-18":
        return {
            "collection_status": facts["collection_status"],
            "snmp_service_present": facts["snmp_service_present"],
            "snmp_community_complex": facts["snmp_community_complex"],
        }
    if item_id in SIMPLE_BOOLEAN_ITEM_FIELDS:
        field = SIMPLE_BOOLEAN_ITEM_FIELDS[item_id]
        return {
            "collection_status": facts["collection_status"],
            field: facts[field],
        }
    return {
        "collection_status": "not_automated_by_cisco_ios_mvp",
        "manual_required": True,
        "reason": "official network item is registered, but the Cisco IOS MVP parser does not automate this item yet",
    }


def _extract_ios_version(text: str) -> str | None:
    config_match = re.search(r"(?im)^\s*version\s+([0-9][^\s]*)", text)
    if config_match:
        return config_match.group(1)
    if "cisco ios" in text.lower():
        return "unknown"
    return None


def _line_exists(text: str, pattern: str) -> bool:
    return bool(re.search(rf"(?im)^\s*{pattern}", text))


def _explicit_enabled_state(text: str, *, enabled_pattern: str, disabled_pattern: str) -> bool | None:
    if _line_exists(text, enabled_pattern):
        return True
    if _line_exists(text, disabled_pattern):
        return False
    return None


def _explicit_blocked_state(text: str, *, enabled_pattern: str, disabled_pattern: str) -> bool | None:
    if _line_exists(text, enabled_pattern):
        return False
    if _line_exists(text, disabled_pattern):
        return True
    return None


def _all_blocked_state(text: str, patterns: list[tuple[str, str]]) -> bool | None:
    states = [
        _explicit_blocked_state(text, enabled_pattern=enabled_pattern, disabled_pattern=disabled_pattern)
        for enabled_pattern, disabled_pattern in patterns
    ]
    if any(state is False for state in states):
        return False
    if all(state is True for state in states):
        return True
    return None


def _matching_lines(text: str, pattern: str) -> list[str]:
    regex = re.compile(rf"(?im)^\s*{pattern}.*$")
    return [match.group(0).strip() for match in regex.finditer(text)]


def _is_weak_snmp_line(line: str) -> bool:
    lowered = line.lower()
    if "[community_weak]" in lowered:
        return True
    return bool(re.search(r"\b(public|private)\b", lowered))


def _snmp_acl_configured(snmp_lines: list[str]) -> bool | None:
    if not snmp_lines:
        return None
    return all(_snmp_line_has_acl(line) for line in snmp_lines)


def _snmp_read_only(snmp_lines: list[str]) -> bool | None:
    if not snmp_lines:
        return None
    return all(not _snmp_line_allows_write(line) for line in snmp_lines)


def _snmp_line_has_acl(line: str) -> bool:
    match = re.search(r"(?i)\bsnmp-server\s+community\s+\S+\s+(?:view\s+\S+\s+)?(?:ro|rw)\b(?P<tail>.*)$", line)
    return bool(match and match.group("tail").strip())


def _snmp_line_allows_write(line: str) -> bool:
    return bool(re.search(r"(?i)\bsnmp-server\s+community\s+\S+\s+(?:view\s+\S+\s+)?rw\b", line))
