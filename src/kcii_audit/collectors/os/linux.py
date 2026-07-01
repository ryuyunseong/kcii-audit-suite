from __future__ import annotations

from datetime import UTC, datetime
from platform import freedesktop_os_release

from kcii_audit.collectors.base import BaseCollector
from kcii_audit.schemas.evidence import EvidenceRecord


class LinuxCollector(BaseCollector):
    """Linux collector scaffold.

    This class intentionally does not execute audit commands yet. It only emits
    a placeholder evidence record so CLI and report plumbing can be tested.
    """

    def collect(self, asset_id: str) -> list[EvidenceRecord]:
        os_name, os_version = self._detect_os_metadata()
        return [
            EvidenceRecord(
                asset_id=asset_id,
                platform="linux",
                os_name=os_name,
                os_version=os_version,
                item_id="STUB-LINUX-001",
                item_title="Linux collector placeholder",
                collected_at=datetime.now(UTC),
                evidence={
                    "collection_status": "not_collected",
                    "reason": "repository scaffold only; read-only collector logic is not implemented yet",
                },
                raw_evidence_hash=None,
            )
        ]

    @staticmethod
    def _detect_os_metadata() -> tuple[str | None, str | None]:
        try:
            release = freedesktop_os_release()
        except OSError:
            return None, None
        return release.get("NAME"), release.get("VERSION_ID")
