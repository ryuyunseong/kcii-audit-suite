from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from kcii_netlab_sim.models import SUPPORTED_SCENARIOS, SUPPORTED_VENDORS
from kcii_netlab_sim.shell import default_commands, interactive_shell, run_commands


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="KCII network command-response simulator")
    parser.add_argument("--vendor", choices=sorted(SUPPORTED_VENDORS), required=True)
    parser.add_argument("--scenario", choices=sorted(SUPPORTED_SCENARIOS), default="good")
    parser.add_argument("--commands", type=Path, help="Text file containing one command per line.")
    parser.add_argument("--command", action="append", dest="inline_commands", help="Command to run. May be repeated.")
    parser.add_argument("--output", type=Path, help="Output file. Defaults to stdout.")
    parser.add_argument("--interactive", action="store_true", help="Start an interactive command prompt.")
    args = parser.parse_args(argv)

    if args.interactive:
        interactive_shell(args.vendor, args.scenario)
        return

    commands = _load_commands(args.vendor, args.commands, args.inline_commands)
    output = run_commands(args.vendor, args.scenario, commands)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")


def _load_commands(vendor: str, commands_file: Path | None, inline_commands: list[str] | None) -> list[str]:
    if inline_commands:
        return inline_commands
    if commands_file:
        return commands_file.read_text(encoding="utf-8").splitlines()
    return default_commands(vendor)
