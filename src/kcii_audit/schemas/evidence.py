from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from kcii_audit import __version__


class EvidenceRecord(BaseModel):
    """Normalized evidence summary safe for deterministic evaluation."""

    model_config = ConfigDict(extra="forbid")

    asset_id: str = Field(min_length=1)
    platform: str = Field(min_length=1)
    os_name: str | None = None
    os_version: str | None = None
    guide_version: str = Field(default="kcii-2025-12", min_length=1)
    item_id: str = Field(min_length=1)
    item_title: str = Field(min_length=1)
    collected_at: datetime
    evidence: dict[str, Any]
    raw_evidence_hash: str | None = None
    collector_version: str = __version__
