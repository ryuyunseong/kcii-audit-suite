from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook

from kcii_audit.parsers.security_appliance_items import (
    SECURITY_APPLIANCE_FACT_BY_ITEM,
    SECURITY_APPLIANCE_ITEMS,
)

QUESTIONNAIRE_SHEETS = [
    "00_작성안내",
    "01_자산목록",
    "02_계정관리",
    "03_접근관리",
    "04_정책관리",
    "05_로그관리",
    "06_업데이트관리",
    "07_백업및복구",
    "08_관제연동",
    "09_인터뷰결과",
    "10_자동판정",
]

QUESTION_HEADERS = [
    "item_id",
    "question",
    "answer_type",
    "required_evidence",
    "options",
    "mapping_rule",
    "answer",
    "evidence_status",
    "notes",
]

ITEM_SHEET_BY_CATEGORY = {
    "계정 관리": "02_계정관리",
    "접근 관리": "03_접근관리",
    "패치 관리": "06_업데이트관리",
    "로그 관리": "05_로그관리",
    "기능 관리": "04_정책관리",
}

OVERRIDE_ITEM_SHEET = {
    "S-12": "07_백업및복구",
    "S-13": "08_관제연동",
    "S-19": "08_관제연동",
    "S-20": "08_관제연동",
    "S-21": "08_관제연동",
    "S-22": "08_관제연동",
}


def write_security_appliance_questionnaire(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    workbook = Workbook()
    workbook.active.title = QUESTIONNAIRE_SHEETS[0]
    for sheet_name in QUESTIONNAIRE_SHEETS[1:]:
        workbook.create_sheet(sheet_name)

    _write_guide_sheet(workbook["00_작성안내"])
    _write_asset_sheet(workbook["01_자산목록"])
    _write_question_sheets(workbook)
    _write_interview_sheet(workbook["09_인터뷰결과"])
    _write_auto_decision_sheet(workbook["10_자동판정"])
    workbook.save(path)


def _write_guide_sheet(sheet) -> None:
    sheet.append(["항목", "내용"])
    sheet.append(["목적", "보안장비 설정 export, 화면 증적, 담당자 인터뷰를 오프라인 판정 evidence로 정리합니다."])
    sheet.append(["운영 원칙", "장비에 원격 자동 접속하지 않고 담당자가 제공한 결과만 Windows 작업 PC에서 판정합니다."])
    sheet.append(["민감정보", "고객명, IP, 계정명, 정책명, 시리얼, 토큰, 인증서 본문을 입력하지 않습니다."])
    sheet.append(["답변", "answer에는 예 또는 아니오를 입력하고, 판단이 어려우면 비워 둡니다."])
    sheet.append(["증적", "evidence_status에는 provided, missing, contradictory 중 하나를 입력할 수 있습니다."])


def _write_asset_sheet(sheet) -> None:
    sheet.append(["field", "value"])
    sheet.append(["asset_alias", ""])
    sheet.append(["appliance_type", ""])
    sheet.append(["evidence_date", ""])
    sheet.append(["reviewer_role", ""])


def _write_question_sheets(workbook: Workbook) -> None:
    for sheet_name in QUESTIONNAIRE_SHEETS[2:9]:
        workbook[sheet_name].append(QUESTION_HEADERS)

    for item in SECURITY_APPLIANCE_ITEMS:
        sheet_name = OVERRIDE_ITEM_SHEET.get(item["item_id"], ITEM_SHEET_BY_CATEGORY[item["category"]])
        workbook[sheet_name].append(_question_row(item))


def _question_row(item: dict[str, str]) -> list[str]:
    return [
        item["item_id"],
        f"{item['title']} 항목이 기관 정책과 운영 기준에 따라 설정 또는 수행되어 있습니까?",
        "boolean",
        _required_evidence(item["category"]),
        "예|아니오|미확인",
        SECURITY_APPLIANCE_FACT_BY_ITEM[item["item_id"]],
        "",
        "",
        "",
    ]


def _required_evidence(category: str) -> str:
    if category == "계정 관리":
        return "계정 정책 설정 화면 또는 담당자 확인 요약"
    if category == "접근 관리":
        return "관리 접근 통제 설정 화면 또는 담당자 확인 요약"
    if category == "패치 관리":
        return "벤더 권고 검토 및 패치 적용 절차 확인 요약"
    if category == "로그 관리":
        return "로그 설정, 보관, 동기화 설정 화면 또는 운영 절차 확인 요약"
    return "정책, 탐지/차단, 서비스 노출, 관제 연동 운영 확인 요약"


def _write_interview_sheet(sheet) -> None:
    sheet.append(["item_id", "interview_topic", "answer_summary", "evidence_status", "validation_warning"])
    for item in SECURITY_APPLIANCE_ITEMS:
        sheet.append([item["item_id"], item["title"], "", "", ""])


def _write_auto_decision_sheet(sheet) -> None:
    sheet.append(["item_id", "mapping_rule", "decision_hint"])
    for item in SECURITY_APPLIANCE_ITEMS:
        sheet.append([item["item_id"], SECURITY_APPLIANCE_FACT_BY_ITEM[item["item_id"]], "예=GOOD, 아니오=VULNERABLE, 공란=MANUAL_REQUIRED"])
