from __future__ import annotations

from abc import ABC, abstractmethod

from kcii_audit.schemas.evidence import EvidenceRecord


class BaseCollector(ABC):
    """Read-only collector interface."""

    @abstractmethod
    def collect(self, asset_id: str) -> list[EvidenceRecord]:
        """Collect normalized evidence without changing the target system."""
