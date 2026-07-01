from __future__ import annotations

from kcii_audit.engine.rulepack import RulepackError, evaluate_with_rulepack, load_default_rulepack
from kcii_audit.schemas.evidence import EvidenceRecord
from kcii_audit.schemas.result import AssessmentStatus, EvaluationResult


def evaluate_evidence(records: list[EvidenceRecord]) -> list[EvaluationResult]:
    """Evaluate normalized evidence with rulepack-first deterministic logic."""
    results: list[EvaluationResult] = []
    for record in records:
        status, reason = _evaluate_record(record)
        results.append(_build_result(record, status, reason))
    return results


def _build_result(record: EvidenceRecord, status: AssessmentStatus, reason: str) -> EvaluationResult:
    return EvaluationResult(
        asset_id=record.asset_id,
        platform=record.platform,
        guide_version=record.guide_version,
        item_id=record.item_id,
        item_title=record.item_title,
        status=status,
        reason=reason,
        evidence_summary=_summarize_evidence(record),
        raw_evidence_hash=record.raw_evidence_hash,
        ai_used=False,
        masked=False,
    )


def _evaluate_record(record: EvidenceRecord) -> tuple[AssessmentStatus, str]:
    try:
        rulepack = load_default_rulepack(record.guide_version, record.platform)
    except RulepackError:
        rulepack = None
    if rulepack is not None:
        rulepack_result = evaluate_with_rulepack(record, rulepack)
        if rulepack_result is not None:
            return rulepack_result

    if record.platform == "windows":
        return _evaluate_windows_record(record)
    if record.platform == "linux":
        return AssessmentStatus.MANUAL_REQUIRED, "지원되는 Linux 결과 형식으로 분류하지 못했습니다."
    return AssessmentStatus.MANUAL_REQUIRED, "rulepack decision logic is not implemented in the scaffold"


def _evaluate_windows_record(record: EvidenceRecord) -> tuple[AssessmentStatus, str]:
    evidence = record.evidence
    if record.item_id == "W-01":
        renamed = evidence.get("administrator_account_renamed")
        if renamed is True:
            return AssessmentStatus.GOOD, "Administrator 기본 계정 이름이 변경된 것으로 확인되었습니다."
        if renamed is False:
            return AssessmentStatus.MANUAL_REQUIRED, "Administrator 기본 계정 이름이 유지되어 비밀번호 보안성 등 추가 확인이 필요합니다."
        return AssessmentStatus.MANUAL_REQUIRED, "Administrator 계정 보안성 강화 여부를 확인할 수 없습니다."

    if record.item_id == "W-02":
        enabled = evidence.get("guest_account_enabled")
        if enabled is False:
            return AssessmentStatus.GOOD, "Guest 계정이 비활성화되어 있습니다."
        if enabled is True:
            return AssessmentStatus.VULNERABLE, "Guest 계정이 활성화되어 있습니다."
        return AssessmentStatus.MANUAL_REQUIRED, "Guest 계정 활성 상태를 확인할 수 없습니다."

    if record.item_id == "W-09":
        min_length = evidence.get("minimum_password_length")
        if isinstance(min_length, int):
            if min_length >= 8:
                return AssessmentStatus.GOOD, "최소 암호 길이가 MVP 기준 8자 이상입니다."
            return AssessmentStatus.VULNERABLE, "최소 암호 길이가 MVP 기준 8자 미만입니다."
        return AssessmentStatus.MANUAL_REQUIRED, "비밀번호 관리정책 증적을 확인할 수 없습니다."

    if record.item_id == "W-64":
        enabled = evidence.get("firewall_enabled")
        if enabled is True:
            return AssessmentStatus.GOOD, "Windows 방화벽이 모든 확인 대상 프로필에서 활성화되어 있습니다."
        if enabled is False:
            return AssessmentStatus.VULNERABLE, "Windows 방화벽이 하나 이상의 확인 대상 프로필에서 비활성화되어 있습니다."
        return AssessmentStatus.MANUAL_REQUIRED, "Windows 방화벽 활성 상태를 확인할 수 없습니다."

    return AssessmentStatus.MANUAL_REQUIRED, "지원되는 Windows 붙여넣기 항목으로 분류하지 못했습니다."


def _summarize_evidence(record: EvidenceRecord) -> str:
    safe_parts = []
    for key in sorted(record.evidence):
        if key == "reason":
            continue
        safe_parts.append(f"{key}={record.evidence[key]}")
    reason = record.evidence.get("reason")
    if reason:
        safe_parts.append(f"reason={reason}")
    return "; ".join(safe_parts) if safe_parts else "no evidence summary available"
