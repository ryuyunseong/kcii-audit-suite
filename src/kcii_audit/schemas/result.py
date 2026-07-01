from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class AssessmentStatus(StrEnum):
    GOOD = "GOOD"
    VULNERABLE = "VULNERABLE"
    MANUAL_REQUIRED = "MANUAL_REQUIRED"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    ERROR = "ERROR"


class EvaluationResult(BaseModel):
    """Deterministic evaluation result used by reports and exports."""

    model_config = ConfigDict(extra="forbid")

    asset_id: str = Field(min_length=1)
    platform: str = Field(min_length=1)
    guide_version: str = Field(min_length=1)
    item_id: str = Field(min_length=1)
    item_title: str = Field(min_length=1)
    status: AssessmentStatus
    status_label: str = ""
    reason: str
    evidence_summary: str
    raw_evidence_hash: str | None = None
    ai_used: bool = False
    masked: bool = False

    @model_validator(mode="after")
    def fill_status_label(self) -> EvaluationResult:
        if not self.status_label:
            self.status_label = {
                AssessmentStatus.GOOD: "양호",
                AssessmentStatus.VULNERABLE: "취약",
                AssessmentStatus.MANUAL_REQUIRED: "수동확인",
                AssessmentStatus.NOT_APPLICABLE: "해당없음",
                AssessmentStatus.ERROR: "오류",
            }[self.status]
        return self
