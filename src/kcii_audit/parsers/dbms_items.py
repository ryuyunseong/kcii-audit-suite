from __future__ import annotations

DBMS_ITEMS: list[dict[str, str]] = [
    {"item_id": "D-01", "title": "기본 계정의 비밀번호, 정책 등을 변경하여 사용", "category": "계정 관리", "severity": "high"},
    {"item_id": "D-02", "title": "데이터베이스의 불필요 계정을 제거하거나, 잠금설정 후 사용", "category": "계정 관리", "severity": "high"},
    {"item_id": "D-03", "title": "비밀번호의 사용기간 및 복잡도를 기관의 정책에 맞도록 설정", "category": "계정 관리", "severity": "high"},
    {"item_id": "D-04", "title": "데이터베이스 관리자 권한을 꼭 필요한 계정 및 그룹에 대해서만 허용", "category": "계정 관리", "severity": "high"},
    {"item_id": "D-05", "title": "비밀번호 재사용에 대한 제약 설정", "category": "계정 관리", "severity": "medium"},
    {"item_id": "D-06", "title": "DB 사용자 계정을 개별적으로 부여하여 사용", "category": "계정 관리", "severity": "medium"},
    {"item_id": "D-07", "title": "root 권한으로 서비스 구동 제한", "category": "계정 관리", "severity": "medium"},
    {"item_id": "D-08", "title": "안전한 암호화 알고리즘 사용", "category": "계정 관리", "severity": "high"},
    {"item_id": "D-09", "title": "일정 횟수의 로그인 실패 시 이에 대한 잠금정책 설정", "category": "계정 관리", "severity": "medium"},
    {"item_id": "D-10", "title": "원격에서 DB 서버로의 접속 제한", "category": "접근 관리", "severity": "high"},
    {"item_id": "D-11", "title": "DBA 이외의 인가되지 않은 사용자가 시스템 테이블에 접근할 수 없도록 설정", "category": "접근 관리", "severity": "high"},
    {"item_id": "D-12", "title": "안전한 리스너 비밀번호 설정 및 사용", "category": "접근 관리", "severity": "high"},
    {"item_id": "D-13", "title": "불필요한 ODBC/OLE-DB 데이터 소스와 드라이브를 제거하여 사용", "category": "접근 관리", "severity": "medium"},
    {"item_id": "D-14", "title": "데이터베이스의 주요 설정파일, 비밀번호 파일 등과 같은 주요 파일들의 접근 권한이 적절하게 설정", "category": "접근 관리", "severity": "medium"},
    {"item_id": "D-15", "title": "관리자 이외의 사용자가 오라클 리스너의 접속을 통해 리스너 로그 및 trace 파일에 대한 변경 제한", "category": "접근 관리", "severity": "low"},
    {"item_id": "D-16", "title": "Windows 인증 모드 사용", "category": "접근 관리", "severity": "low"},
    {"item_id": "D-17", "title": "Audit Table은 데이터베이스 관리자 계정에 접근하도록 제한", "category": "옵션 관리", "severity": "low"},
    {"item_id": "D-18", "title": "응용프로그램 또는 DBA 계정의 Role이 Public으로 설정되지 않도록 조정", "category": "옵션 관리", "severity": "high"},
    {"item_id": "D-19", "title": "OS_ROLES, REMOTE_OS_AUTHENTICATION, REMOTE_OS_ROLES를 FALSE로 설정", "category": "옵션 관리", "severity": "high"},
    {"item_id": "D-20", "title": "인가되지 않은 Object owner의 제한", "category": "옵션 관리", "severity": "low"},
    {"item_id": "D-21", "title": "인가되지 않은 GRANT OPTION 사용 제한", "category": "옵션 관리", "severity": "medium"},
    {"item_id": "D-22", "title": "데이터베이스의 자원 제한 기능을 TRUE로 설정", "category": "옵션 관리", "severity": "low"},
    {"item_id": "D-23", "title": "xp_cmdshell 사용 제한", "category": "옵션 관리", "severity": "high"},
    {"item_id": "D-24", "title": "Registry Procedure 권한 제한", "category": "옵션 관리", "severity": "high"},
    {"item_id": "D-25", "title": "주기적 보안 패치 및 벤더 권고 사항 적용", "category": "패치 관리", "severity": "high"},
    {"item_id": "D-26", "title": "데이터베이스의 접근, 변경, 삭제 등의 감사 기록이 기관의 감사 기록 정책에 적합하도록 설정", "category": "패치 관리", "severity": "high"},
]

DBMS_ITEM_IDS = [item["item_id"] for item in DBMS_ITEMS]
DBMS_ITEM_TITLES = {item["item_id"]: item["title"] for item in DBMS_ITEMS}
DBMS_ITEM_BY_ID = {item["item_id"]: item for item in DBMS_ITEMS}

DBMS_AUTOMATED_ITEM_IDS = {
    "D-01",
    "D-02",
    "D-03",
    "D-04",
    "D-08",
    "D-09",
    "D-10",
    "D-18",
    "D-21",
    "D-22",
    "D-25",
    "D-26",
}
