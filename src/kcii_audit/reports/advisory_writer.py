from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from openpyxl import Workbook

from kcii_audit.schemas.result import AssessmentStatus, EvaluationResult


@dataclass(frozen=True)
class SecurityAdvisory:
    advisory_id: str
    item_id: str
    title: str
    impact: str
    masked_asset: str
    status_label: str
    reason: str
    expected_impact: str
    recommendation: str
    priority: str
    due_date: str
    retest_method: str
    owner: str
    reference: str
    raw_evidence_hash: str
    masked: bool


ADVISORY_HEADERS = [
    "권고문ID",
    "관련항목ID",
    "제목",
    "영향도",
    "대상자산",
    "판정결과",
    "취약사유",
    "영향",
    "권고조치",
    "우선순위",
    "조치기한",
    "재점검방법",
    "담당부서",
    "참고기준",
    "원본증적해시",
    "마스킹적용여부",
]


def generate_security_advisories(
    results: list[EvaluationResult],
    *,
    include_good: bool = False,
) -> list[SecurityAdvisory]:
    asset_map = _masked_asset_map(results)
    advisories: list[SecurityAdvisory] = []
    advisory_index = 1
    for result in results:
        if result.status == AssessmentStatus.GOOD and not include_good:
            continue
        if result.status in {AssessmentStatus.NOT_APPLICABLE, AssessmentStatus.ERROR}:
            continue

        advisories.append(_build_advisory(result, asset_map[result.asset_id], advisory_index))
        advisory_index += 1
    return advisories


def write_security_advisory_markdown(
    path: Path,
    results: list[EvaluationResult],
    *,
    include_good: bool = False,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    advisories = generate_security_advisories(results, include_good=include_good)
    lines = ["# 보안 권고문", ""]
    if not advisories:
        lines.extend(["권고 대상 항목이 없습니다.", ""])
        path.write_text("\n".join(lines), encoding="utf-8")
        return

    counts = Counter(advisory.status_label for advisory in advisories)
    lines.extend(["## 요약", "", "| 판정 | 권고문 수 |", "| --- | ---: |"])
    for status, count in counts.items():
        lines.append(f"| {status} | {count} |")
    lines.append("")

    for advisory in advisories:
        lines.extend(
            [
                f"## 보안 권고문 {advisory.advisory_id}",
                "",
                f"- 관련 항목: {advisory.item_id}",
                f"- 제목: {advisory.title}",
                f"- 영향도: {advisory.impact}",
                f"- 대상: {advisory.masked_asset}",
                f"- 판정: {advisory.status_label}",
                f"- 취약 사유: {advisory.reason}",
                f"- 예상 영향: {advisory.expected_impact}",
                f"- 권고 조치: {advisory.recommendation}",
                f"- 우선순위: {advisory.priority}",
                f"- 조치 기한: {advisory.due_date}",
                f"- 재점검 방법: {advisory.retest_method}",
                f"- 담당 부서: {advisory.owner}",
                f"- 참고 기준: {advisory.reference}",
                f"- 원본 증적 해시: {advisory.raw_evidence_hash}",
                f"- 마스킹 적용 여부: {'Y' if advisory.masked else 'N'}",
                "",
            ]
        )

    path.write_text("\n".join(lines), encoding="utf-8")


def write_security_advisory_workbook(
    path: Path,
    results: list[EvaluationResult],
    *,
    include_good: bool = False,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    advisories = generate_security_advisories(results, include_good=include_good)
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "보안권고문"
    sheet.append(ADVISORY_HEADERS)
    for advisory in advisories:
        sheet.append(advisory_to_row(advisory))
    workbook.save(path)


def advisory_to_row(advisory: SecurityAdvisory) -> list[str]:
    return [
        advisory.advisory_id,
        advisory.item_id,
        advisory.title,
        advisory.impact,
        advisory.masked_asset,
        advisory.status_label,
        advisory.reason,
        advisory.expected_impact,
        advisory.recommendation,
        advisory.priority,
        advisory.due_date,
        advisory.retest_method,
        advisory.owner,
        advisory.reference,
        advisory.raw_evidence_hash,
        "Y" if advisory.masked else "N",
    ]


def _build_advisory(result: EvaluationResult, masked_asset: str, index: int) -> SecurityAdvisory:
    if result.status == AssessmentStatus.VULNERABLE:
        impact = "상"
        priority = "즉시"
        title = f"{result.item_title} 미흡"
        expected_impact = "기준 미충족 설정이 유지될 경우 권한 오남용, 비인가 접근, 감사 추적 약화로 이어질 수 있습니다."
        recommendation = "관련 설정을 K-CII rulepack 및 조직 보안 기준에 맞게 조정하고 변경 후 재점검하십시오."
        due_date = "단기 조치 권고"
    elif result.status == AssessmentStatus.MANUAL_REQUIRED:
        impact = "중"
        priority = "단기"
        title = f"{result.item_title} 추가 확인 필요"
        expected_impact = "자동 판정에 필요한 증적이 부족하여 실제 취약 여부를 확정할 수 없습니다."
        recommendation = "담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오."
        due_date = "추가 확인 후 결정"
    else:
        impact = "하"
        priority = "중기"
        title = f"{result.item_title} 유지관리 권고"
        expected_impact = "현재 판정은 양호이나 운영 변경 시 기준 미충족 상태로 전환될 수 있습니다."
        recommendation = "현재 설정을 유지하고 정기 점검 시 동일 기준으로 재확인하십시오."
        due_date = "정기 점검"

    return SecurityAdvisory(
        advisory_id=f"ADV-{index:03d}",
        item_id=result.item_id,
        title=title,
        impact=impact,
        masked_asset=masked_asset,
        status_label=result.status_label,
        reason=result.reason,
        expected_impact=expected_impact,
        recommendation=recommendation,
        priority=priority,
        due_date=due_date,
        retest_method=f"{result.item_id} evidence를 다시 수집해 rulepack 판정을 재실행합니다.",
        owner="미지정",
        reference=f"{result.guide_version} rulepack",
        raw_evidence_hash=result.raw_evidence_hash or "",
        masked=True,
    )


def _masked_asset_map(results: list[EvaluationResult]) -> dict[str, str]:
    ordered_assets: list[str] = []
    for result in results:
        if result.asset_id not in ordered_assets:
            ordered_assets.append(result.asset_id)
    return {asset_id: f"[ASSET_{index:03d}]" for index, asset_id in enumerate(ordered_assets, start=1)}
