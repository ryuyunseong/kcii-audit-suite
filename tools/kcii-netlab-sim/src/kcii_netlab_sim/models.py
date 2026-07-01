from __future__ import annotations

from dataclasses import dataclass

SUPPORTED_VENDORS = {"cisco_ios"}
SUPPORTED_SCENARIOS = {"good", "vulnerable", "mixed"}


@dataclass(frozen=True)
class CommandResponse:
    command: str
    output: str
