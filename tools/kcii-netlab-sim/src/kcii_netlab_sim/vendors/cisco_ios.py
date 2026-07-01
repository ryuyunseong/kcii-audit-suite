from __future__ import annotations

DEFAULT_COMMANDS = [
    "show running-config",
    "show startup-config",
    "show version",
    "show ip interface brief",
    "show users",
    "show line",
    "show logging",
    "show ntp status",
    "show snmp",
    "show ip ssh",
    "show access-lists",
]


def get_response(scenario: str, command: str) -> str:
    normalized = " ".join(command.strip().split()).lower()
    responses = _scenario_responses(scenario)
    if normalized in responses:
        return responses[normalized]
    return f"% Unsupported command: {command.strip()}"


def _scenario_responses(scenario: str) -> dict[str, str]:
    if scenario == "good":
        return _responses_for(_GOOD_RUNNING_CONFIG, good=True)
    if scenario == "vulnerable":
        return _responses_for(_VULNERABLE_RUNNING_CONFIG, good=False)
    if scenario == "mixed":
        return _responses_for(_MIXED_RUNNING_CONFIG, good=False, mixed=True)
    raise ValueError(f"unsupported cisco_ios scenario: {scenario}")


def _responses_for(running_config: str, *, good: bool, mixed: bool = False) -> dict[str, str]:
    startup_config = running_config.replace("! running", "! startup")
    if good:
        logging = "Syslog logging: enabled\n    Logging to [LOG_SERVER]\n"
        ntp = "Clock is synchronized, stratum 3, reference is [NTP_SERVER]\n"
        snmp = "SNMP agent enabled\nCommunity strings are configured with restricted ACLs\n"
        ssh = "SSH Enabled - version 2.0\nAuthentication methods: publickey,password\n"
        acl = "Standard IP access list MGMT-ACL\n    10 permit [MGMT_NET] [WILDCARD]\n"
    elif mixed:
        logging = "Syslog logging: enabled\n    Logging to [LOG_SERVER]\n"
        ntp = "Clock is unsynchronized, no reference clock\n"
        snmp = "SNMP agent enabled\nCommunity string requires manual complexity review\n"
        ssh = "SSH Enabled - version 2.0\n"
        acl = "% No access list named MGMT-ACL\n"
    else:
        logging = "Syslog logging: disabled\n"
        ntp = "Clock is unsynchronized, no reference clock\n"
        snmp = "SNMP agent enabled\nWeak community placeholder detected\n"
        ssh = "%SSH has not been enabled\n"
        acl = "% No access list named MGMT-ACL\n"

    return {
        "show running-config": running_config,
        "show startup-config": startup_config,
        "show version": _SHOW_VERSION,
        "show ip interface brief": _SHOW_IP_INTERFACE_BRIEF,
        "show users": _SHOW_USERS,
        "show line": _SHOW_LINE,
        "show logging": logging,
        "show ntp status": ntp,
        "show snmp": snmp,
        "show ip ssh": ssh,
        "show access-lists": acl,
    }


_SHOW_VERSION = """Cisco IOS Software, KCII Simulator
Compiled by kcii-netlab-sim
ROM: Bootstrap program is KCII simulator
Processor board ID [SERIAL_1]
"""

_SHOW_IP_INTERFACE_BRIEF = """Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     unassigned      YES unset  up                    up
GigabitEthernet0/1     unassigned      YES unset  administratively down down
"""

_SHOW_USERS = """Line       User       Host(s)              Idle       Location
*  2 vty 0     [USER_ADMIN] idle                 00:00:00   [MGMT_HOST]
"""

_SHOW_LINE = """Tty Line Typ     Tx/Rx     A Modem  Roty AccO AccI  Uses  Noise Overruns Int
  0    0 CTY              -    -      -    -    -     0      0     0/0       -
  2    2 VTY              -    -      -    -    -     1      0     0/0       -
"""

_GOOD_RUNNING_CONFIG = """! running
version 17.9
service password-encryption
hostname KCII-IOS-SIM
enable secret 9 [HASHED_ENABLE_SECRET]
username [USER_ADMIN] privilege 15 secret 9 [HASHED_USER_SECRET]
banner motd ^C[AUTHORIZED_ACCESS_ONLY]^C
logging host [LOG_SERVER]
ntp server [NTP_SERVER]
ip ssh version 2
ip access-list standard MGMT-ACL
 permit [MGMT_NET] [WILDCARD]
line vty 0 4
 access-class MGMT-ACL in
 exec-timeout 10 0
 login local
 transport input ssh
snmp-server community [COMMUNITY_COMPLEX] RO MGMT-ACL
no ip http server
no ip bootp server
no cdp run
end
"""

_VULNERABLE_RUNNING_CONFIG = """! running
version 17.9
hostname KCII-IOS-SIM
enable password [REDACTED_DEFAULT_PASSWORD]
username [USER_ADMIN] privilege 15 password 0 [REDACTED_USER_PASSWORD]
line vty 0 4
 exec-timeout 0 0
 login
 password 0 [REDACTED_LINE_PASSWORD]
 transport input telnet
snmp-server community [COMMUNITY_WEAK] RO
ip http server
ip bootp server
cdp run
end
"""

_MIXED_RUNNING_CONFIG = """! running
version 17.9
service password-encryption
hostname KCII-IOS-SIM
enable secret 9 [HASHED_ENABLE_SECRET]
username [USER_ADMIN] privilege 15 secret 9 [HASHED_USER_SECRET]
banner login ^C[AUTHORIZED_ACCESS_ONLY]^C
logging host [LOG_SERVER]
ip ssh version 2
line vty 0 4
 exec-timeout 15 0
 login local
 transport input ssh telnet
snmp-server community [COMMUNITY_COMPLEX] RO
end
"""
