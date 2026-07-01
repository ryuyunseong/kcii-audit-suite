from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from kcii_audit.schemas.result import AssessmentStatus

RuleOperator = Literal["equals", "not_equals", "gte", "gt", "lte", "lt", "exists"]


class RuleCondition(BaseModel):
    """Single-field deterministic rule condition."""

    model_config = ConfigDict(extra="forbid")

    field: str = Field(min_length=1)
    operator: RuleOperator
    value: Any = None

    @field_validator("value")
    @classmethod
    def value_required_for_comparison(cls, value: Any, info) -> Any:
        operator = info.data.get("operator")
        if operator != "exists" and value is None:
            raise ValueError("value is required unless operator is exists")
        return value


class DecisionRule(BaseModel):
    """Rulepack status decision."""

    model_config = ConfigDict(extra="forbid")

    status: AssessmentStatus
    when: RuleCondition
    reason: str = Field(min_length=1)


class RulepackItem(BaseModel):
    """One audit item in a rulepack."""

    model_config = ConfigDict(extra="forbid")

    domain: str | None = None
    category: str = Field(min_length=1)
    item_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    severity: Literal["low", "medium", "high", "critical"]
    target_platforms: list[str] = Field(min_length=1)
    supported_dbms: list[str] | None = None
    commands_or_queries_by_dbms: dict[str, str] | None = None
    supported_unix: list[str] | None = None
    commands_by_unix: dict[str, str] | None = None
    supported_appliance_types: list[str] | None = None
    config_hints_by_vendor: dict[str, str] | None = None
    questionnaire_fields: list[str] | None = None
    evidence_source: list[str] | None = None
    automation_level: Literal["auto", "partial", "manual", "unsupported"] | None = None
    decision_mode: str | None = None
    collector: str = Field(min_length=1)
    evidence_fields: list[str] = Field(min_length=1)
    decision_rules: list[DecisionRule] = Field(min_length=1)
    manual_required_when: str | None = None
    remediation: str = Field(min_length=1)
    report_text: str = Field(min_length=1)
    remediation_summary: str | None = None
    advisory_template: str | None = None


class Rulepack(BaseModel):
    """Validated YAML rulepack."""

    model_config = ConfigDict(extra="forbid")

    guide_version: str = Field(min_length=1)
    domain: str = Field(min_length=1)
    items: list[RulepackItem] = Field(min_length=1)

    @field_validator("items")
    @classmethod
    def item_ids_must_be_unique(cls, items: list[RulepackItem]) -> list[RulepackItem]:
        seen: set[str] = set()
        duplicates: set[str] = set()
        for item in items:
            if item.item_id in seen:
                duplicates.add(item.item_id)
            seen.add(item.item_id)
        if duplicates:
            joined = ", ".join(sorted(duplicates))
            raise ValueError(f"duplicate item_id in rulepack: {joined}")
        return items
