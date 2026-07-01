from __future__ import annotations

from kcii_audit.parsers.dbms_common import records_from_dbms_paste
from kcii_audit.schemas.evidence import EvidenceRecord


def records_from_mariadb_paste(
    text: str,
    *,
    asset_id: str = "dbms-mariadb-paste",
    guide_version: str = "kcii-2025-12",
) -> list[EvidenceRecord]:
    return records_from_dbms_paste(text, dbms="mariadb", asset_id=asset_id, guide_version=guide_version)
