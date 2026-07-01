from __future__ import annotations

SUPPORTED_APPLIANCE_TYPES = [
    "firewall",
    "ips",
    "ids",
    "waf",
    "vpn",
    "anti-ddos",
    "fortigate",
    "paloalto",
    "cisco-asa",
    "f5",
]

SECURITY_APPLIANCE_ITEMS: list[dict[str, str]] = [
    {"item_id": "S-01", "title": "보안 장비 Default 계정 변경", "category": "계정 관리", "severity": "high"},
    {"item_id": "S-02", "title": "비밀번호 관리정책 설정", "category": "계정 관리", "severity": "high"},
    {"item_id": "S-03", "title": "보안 장비 계정별 권한 설정", "category": "계정 관리", "severity": "high"},
    {"item_id": "S-04", "title": "보안 장비 계정 관리", "category": "계정 관리", "severity": "high"},
    {"item_id": "S-05", "title": "계정 잠금 임계값 설정", "category": "계정 관리", "severity": "high"},
    {"item_id": "S-06", "title": "보안장비 원격 관리 접근 통제", "category": "접근 관리", "severity": "high"},
    {"item_id": "S-07", "title": "보안장비 보안 접속", "category": "접근 관리", "severity": "high"},
    {"item_id": "S-08", "title": "세션 종료 시간 설정", "category": "접근 관리", "severity": "high"},
    {"item_id": "S-09", "title": "주기적 보안 패치 및 벤더 권고사항 적용", "category": "패치 관리", "severity": "high"},
    {"item_id": "S-10", "title": "보안장비 로그 설정", "category": "로그 관리", "severity": "medium"},
    {"item_id": "S-11", "title": "보안장비 로그 보관", "category": "로그 관리", "severity": "medium"},
    {"item_id": "S-12", "title": "보안장비 정책 백업 설정", "category": "로그 관리", "severity": "medium"},
    {"item_id": "S-13", "title": "원격 로그 서버 사용", "category": "로그 관리", "severity": "medium"},
    {"item_id": "S-14", "title": "NTP 및 시각 동기화 설정", "category": "로그 관리", "severity": "medium"},
    {"item_id": "S-15", "title": "정책 관리", "category": "기능 관리", "severity": "high"},
    {"item_id": "S-16", "title": "NAT 설정", "category": "기능 관리", "severity": "high"},
    {"item_id": "S-17", "title": "DMZ 설정", "category": "기능 관리", "severity": "high"},
    {"item_id": "S-18", "title": "최소한의 서비스만 제공", "category": "기능 관리", "severity": "high"},
    {"item_id": "S-19", "title": "이상징후 탐지 모니터링 수행", "category": "기능 관리", "severity": "high"},
    {"item_id": "S-20", "title": "장비 사용량 검토", "category": "기능 관리", "severity": "high"},
    {"item_id": "S-21", "title": "SNMP 서비스 확인", "category": "기능 관리", "severity": "high"},
    {"item_id": "S-22", "title": "SNMP Community String 복잡성 설정", "category": "기능 관리", "severity": "high"},
    {"item_id": "S-23", "title": "유해 트래픽 탐지/차단 정책 설정", "category": "기능 관리", "severity": "medium"},
]

SECURITY_APPLIANCE_ITEM_IDS = [item["item_id"] for item in SECURITY_APPLIANCE_ITEMS]
SECURITY_APPLIANCE_ITEM_TITLES = {item["item_id"]: item["title"] for item in SECURITY_APPLIANCE_ITEMS}
SECURITY_APPLIANCE_ITEM_BY_ID = {item["item_id"]: item for item in SECURITY_APPLIANCE_ITEMS}

SECURITY_APPLIANCE_FACT_BY_ITEM = {
    "S-01": "default_account_changed",
    "S-02": "password_policy_configured",
    "S-03": "role_based_admin_privileges_configured",
    "S-04": "admin_account_review_performed",
    "S-05": "account_lockout_configured",
    "S-06": "management_access_restricted",
    "S-07": "secure_management_protocols_enforced",
    "S-08": "session_timeout_configured",
    "S-09": "patch_review_performed",
    "S-10": "logging_enabled",
    "S-11": "log_retention_configured",
    "S-12": "policy_backup_configured",
    "S-13": "remote_log_server_enabled",
    "S-14": "time_sync_configured",
    "S-15": "policy_review_performed",
    "S-16": "nat_policy_reviewed",
    "S-17": "dmz_policy_reviewed",
    "S-18": "minimal_services_exposed",
    "S-19": "anomaly_monitoring_performed",
    "S-20": "capacity_usage_reviewed",
    "S-21": "snmp_service_controlled",
    "S-22": "snmp_community_complex",
    "S-23": "harmful_traffic_policy_configured",
}

SECURITY_APPLIANCE_ITEM_BY_FACT = {
    fact: item_id for item_id, fact in SECURITY_APPLIANCE_FACT_BY_ITEM.items()
}
