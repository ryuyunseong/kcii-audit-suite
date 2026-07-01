from __future__ import annotations

from collections.abc import Iterable

from kcii_netlab_sim.models import SUPPORTED_SCENARIOS, SUPPORTED_VENDORS
from kcii_netlab_sim.vendors import cisco_ios


def default_commands(vendor: str) -> list[str]:
    _validate_vendor(vendor)
    if vendor == "cisco_ios":
        return list(cisco_ios.DEFAULT_COMMANDS)
    raise ValueError(f"unsupported vendor: {vendor}")


def run_commands(vendor: str, scenario: str, commands: Iterable[str]) -> str:
    _validate_vendor(vendor)
    _validate_scenario(scenario)
    rendered: list[str] = []
    for command in commands:
        command = command.strip()
        if not command or command.startswith("#"):
            continue
        rendered.append(f"KCII-IOS# {command}")
        rendered.append(_response(vendor, scenario, command).rstrip())
    return "\n\n".join(rendered).rstrip() + "\n"


def interactive_shell(vendor: str, scenario: str) -> None:
    _validate_vendor(vendor)
    _validate_scenario(scenario)
    prompt = "KCII-IOS# "
    while True:
        try:
            command = input(prompt)
        except EOFError:
            break
        if command.strip().lower() in {"exit", "quit"}:
            break
        print(_response(vendor, scenario, command))


def _response(vendor: str, scenario: str, command: str) -> str:
    if vendor == "cisco_ios":
        return cisco_ios.get_response(scenario, command)
    raise ValueError(f"unsupported vendor: {vendor}")


def _validate_vendor(vendor: str) -> None:
    if vendor not in SUPPORTED_VENDORS:
        supported = ", ".join(sorted(SUPPORTED_VENDORS))
        raise ValueError(f"unsupported vendor: {vendor}; supported vendors: {supported}")


def _validate_scenario(scenario: str) -> None:
    if scenario not in SUPPORTED_SCENARIOS:
        supported = ", ".join(sorted(SUPPORTED_SCENARIOS))
        raise ValueError(f"unsupported scenario: {scenario}; supported scenarios: {supported}")
