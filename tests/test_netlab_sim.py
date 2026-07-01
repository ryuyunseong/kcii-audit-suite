from __future__ import annotations

import sys
from pathlib import Path

TOOLS_SRC = Path("tools/kcii-netlab-sim/src").resolve()
if str(TOOLS_SRC) not in sys.path:
    sys.path.insert(0, str(TOOLS_SRC))

from kcii_netlab_sim.shell import default_commands, run_commands  # noqa: E402


def test_cisco_ios_simulator_generates_default_command_responses():
    output = run_commands("cisco_ios", "vulnerable", default_commands("cisco_ios"))

    assert "KCII-IOS# show running-config" in output
    assert "KCII-IOS# show ip ssh" in output
    assert "enable password [REDACTED_DEFAULT_PASSWORD]" in output
    assert "snmp-server community [COMMUNITY_WEAK] RO" in output


def test_cisco_ios_simulator_handles_unsupported_command_as_output():
    output = run_commands("cisco_ios", "good", ["show not-a-real-command"])

    assert "% Unsupported command: show not-a-real-command" in output
