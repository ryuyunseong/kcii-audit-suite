from __future__ import annotations

from kcii_audit.parsers.unix_common import records_from_unix_paste as _records_from_unix_paste
from kcii_audit.schemas.evidence import EvidenceRecord


def records_from_unix_paste(
    text: str,
    *,
    unix_flavor: str,
    asset_id: str = "unix-paste",
    guide_version: str = "kcii-2025-12",
) -> list[EvidenceRecord]:
    return _records_from_unix_paste(
        text,
        unix_flavor=unix_flavor,
        asset_id=asset_id,
        guide_version=guide_version,
    )
