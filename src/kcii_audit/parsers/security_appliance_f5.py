from __future__ import annotations

from kcii_audit.parsers.security_appliance_common import records_from_security_appliance_paste
from kcii_audit.schemas.evidence import EvidenceRecord


def records_from_f5_paste(
    text: str,
    *,
    asset_id: str = "security-appliance-f5-paste",
    guide_version: str = "kcii-2025-12",
) -> list[EvidenceRecord]:
    return records_from_security_appliance_paste(
        text,
        appliance_type="f5",
        asset_id=asset_id,
        guide_version=guide_version,
    )
