from __future__ import annotations

from functools import lru_cache
from importlib.resources import files
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from kcii_audit.schemas.evidence import EvidenceRecord
from kcii_audit.schemas.result import AssessmentStatus
from kcii_audit.schemas.rulepack import RuleCondition, Rulepack, RulepackItem


class RulepackError(ValueError):
    """Raised when a rulepack cannot be loaded or validated."""


def load_rulepack(path: Path | Traversable) -> Rulepack:
    """Load and validate a YAML rulepack."""
    if not path.exists():
        raise RulepackError(f"rulepack file not found: {path}")

    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise RulepackError(f"invalid YAML in rulepack {path}: {exc}") from exc

    if not isinstance(payload, dict):
        raise RulepackError(f"rulepack must be a YAML object: {path}")

    try:
        return Rulepack.model_validate(payload)
    except ValidationError as exc:
        raise RulepackError(f"invalid rulepack schema in {path}: {exc}") from exc


@lru_cache(maxsize=16)
def load_default_rulepack(guide_version: str, domain: str) -> Rulepack | None:
    """Load a repository rulepack if it exists."""
    for candidate in _default_rulepack_candidates(guide_version, domain):
        if candidate.exists():
            return load_rulepack(candidate)
    return None


def evaluate_with_rulepack(record: EvidenceRecord, rulepack: Rulepack) -> tuple[AssessmentStatus, str] | None:
    """Evaluate a record against the matching rulepack item."""
    item = _find_item(rulepack, record)
    if item is None:
        return None

    for decision_rule in item.decision_rules:
        if _condition_matches(record.evidence, decision_rule.when):
            return decision_rule.status, decision_rule.reason

    missing = [field for field in item.evidence_fields if field not in record.evidence]
    if missing:
        return AssessmentStatus.MANUAL_REQUIRED, f"필수 evidence 필드가 없습니다: {', '.join(missing)}"
    return AssessmentStatus.MANUAL_REQUIRED, "rulepack 조건에 일치하는 판정 규칙이 없습니다."


def _default_rulepack_candidates(guide_version: str, domain: str) -> list[Path | Traversable]:
    repo_root = Path(__file__).resolve().parents[3]
    return [
        Path.cwd() / "rulepacks" / guide_version / f"{domain}.yaml",
        files("kcii_audit.resources").joinpath("rulepacks", guide_version, f"{domain}.yaml"),
        repo_root / "rulepacks" / guide_version / f"{domain}.yaml",
    ]


def _find_item(rulepack: Rulepack, record: EvidenceRecord) -> RulepackItem | None:
    if rulepack.guide_version != record.guide_version:
        return None
    for item in rulepack.items:
        if item.item_id == record.item_id and record.platform in item.target_platforms:
            return item
    return None


def _condition_matches(evidence: dict[str, Any], condition: RuleCondition) -> bool:
    exists = condition.field in evidence and evidence[condition.field] is not None
    if condition.operator == "exists":
        return exists
    if not exists:
        return False

    actual = evidence[condition.field]
    expected = condition.value

    if condition.operator == "equals":
        return actual == expected
    if condition.operator == "not_equals":
        return actual != expected
    if condition.operator in {"gte", "gt", "lte", "lt"}:
        if not isinstance(actual, int | float) or not isinstance(expected, int | float):
            return False
        if condition.operator == "gte":
            return actual >= expected
        if condition.operator == "gt":
            return actual > expected
        if condition.operator == "lte":
            return actual <= expected
        return actual < expected
    return False
