#!/usr/bin/env sh
set -u

# POSIX sh read-only Unix evidence collector.
# This script prints sanitized JSON for offline classification on a Windows work PC.
# It does not read password hashes, private keys, certificate bodies, account lists, hostnames, domains, or IP addresses.

detect_unix_flavor() {
  case "$(uname -s 2>/dev/null)" in
    AIX) printf '%s\n' "aix" ;;
    SunOS) printf '%s\n' "solaris" ;;
    HP-UX) printf '%s\n' "hpux" ;;
    Linux) printf '%s\n' "linux" ;;
    *) printf '%s\n' "unknown" ;;
  esac
}

bool_or_manual() {
  case "$1" in
    true|false) printf '%s' "$1" ;;
    *) printf '"manual_review_required"' ;;
  esac
}

number_or_manual() {
  case "$1" in
    ''|*[!0-9]*) printf '"manual_review_required"' ;;
    *) printf '%s' "$1" ;;
  esac
}

json_string() {
  printf '"%s"' "$1"
}

first_existing_file() {
  for candidate in "$@"; do
    if [ -f "$candidate" ]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done
  return 1
}

grep_file() {
  pattern="$1"
  file="$2"
  if [ -r "$file" ]; then
    grep "$pattern" "$file" >/dev/null 2>&1
    return $?
  fi
  return 2
}

file_not_world_writable() {
  file="$1"
  if [ ! -e "$file" ]; then
    printf '%s\n' "manual"
    return
  fi
  mode_text=$(ls -ld "$file" 2>/dev/null | awk '{print $1}')
  if [ -z "$mode_text" ]; then
    printf '%s\n' "manual"
    return
  fi
  world_write=$(printf '%s\n' "$mode_text" | awk '{print substr($1,9,1)}')
  if [ "$world_write" = "w" ]; then
    printf '%s\n' "false"
  else
    printf '%s\n' "true"
  fi
}

collect_common_passwd_summary() {
  uid0_extra_count="manual_review_required"
  if [ -r /etc/passwd ]; then
    uid0_extra_count=$(awk -F: '($3 == 0 && $1 != "root") {count++} END {print count + 0}' /etc/passwd 2>/dev/null)
  fi
}

collect_common_file_permissions() {
  passwd_permission_ok=$(file_not_world_writable /etc/passwd)
  shadow_permission_ok="manual_review_required"
  if [ -e /etc/shadow ]; then
    shadow_permission_ok=$(file_not_world_writable /etc/shadow)
  elif [ -e /etc/security/passwd ]; then
    shadow_permission_ok=$(file_not_world_writable /etc/security/passwd)
  fi

  password_file_protected="manual_review_required"
  if [ "$shadow_permission_ok" = "true" ]; then
    password_file_protected="true"
  elif [ "$shadow_permission_ok" = "false" ]; then
    password_file_protected="false"
  fi
}

collect_common_network_services() {
  finger_service_disabled="manual_review_required"
  r_services_disabled="manual_review_required"
  telnet_service_disabled="manual_review_required"
  ftp_encrypted_or_disabled="manual_review_required"
  snmp_service_disabled="manual_review_required"
  nfs_service_disabled="manual_review_required"
  rpc_service_disabled="manual_review_required"
  tftp_talk_disabled="manual_review_required"

  inetd_file=$(first_existing_file /etc/inetd.conf /etc/xinetd.conf 2>/dev/null || printf '')
  if [ -n "$inetd_file" ] && [ -r "$inetd_file" ]; then
    if grep_file '^[ 	]*finger[ 	]' "$inetd_file"; then finger_service_disabled="false"; else finger_service_disabled="true"; fi
    if grep_file '^[ 	]*\(shell\|login\|exec\)[ 	]' "$inetd_file"; then r_services_disabled="false"; else r_services_disabled="true"; fi
    if grep_file '^[ 	]*telnet[ 	]' "$inetd_file"; then telnet_service_disabled="false"; else telnet_service_disabled="true"; fi
    if grep_file '^[ 	]*ftp[ 	]' "$inetd_file"; then ftp_encrypted_or_disabled="false"; else ftp_encrypted_or_disabled="true"; fi
    if grep_file '^[ 	]*\(tftp\|talk\|ntalk\)[ 	]' "$inetd_file"; then tftp_talk_disabled="false"; else tftp_talk_disabled="true"; fi
  fi

  if command -v ps >/dev/null 2>&1; then
    ps_out=$(ps -ef 2>/dev/null)
    if printf '%s\n' "$ps_out" | grep '[s]nmpd' >/dev/null 2>&1; then snmp_service_disabled="false"; else snmp_service_disabled="true"; fi
    if printf '%s\n' "$ps_out" | grep '[n]fsd' >/dev/null 2>&1; then nfs_service_disabled="false"; else nfs_service_disabled="true"; fi
    if printf '%s\n' "$ps_out" | grep '[r]pcbind' >/dev/null 2>&1; then rpc_service_disabled="false"; else rpc_service_disabled="true"; fi
  fi
}

collect_common_security_summary() {
  root_remote_login_restricted="manual_review_required"
  sshd_file=$(first_existing_file /etc/ssh/sshd_config /usr/local/etc/ssh/sshd_config 2>/dev/null || printf '')
  if [ -n "$sshd_file" ] && [ -r "$sshd_file" ]; then
    if grep_file '^[ 	]*PermitRootLogin[ 	][ 	]*no' "$sshd_file"; then
      root_remote_login_restricted="true"
    elif grep_file '^[ 	]*PermitRootLogin' "$sshd_file"; then
      root_remote_login_restricted="false"
    fi
  fi

  root_path_secure="manual_review_required"
  case "${PATH:-}" in
    *::*|.:*|*:.:*|*:.)
      root_path_secure="false"
      ;;
    *)
      root_path_secure="true"
      ;;
  esac

  session_timeout_configured="manual_review_required"
  if [ "${TMOUT:-}" != "" ]; then
    session_timeout_configured="true"
  fi

  ntp_configured="manual_review_required"
  if [ -f /etc/ntp.conf ] || [ -f /etc/chrony.conf ]; then
    ntp_configured="true"
  fi

  system_logging_configured="manual_review_required"
  if [ -f /etc/syslog.conf ] || [ -f /etc/rsyslog.conf ] || [ -d /etc/rsyslog.d ]; then
    system_logging_configured="true"
  fi
}

collect_aix_security_user() {
  if [ -r /etc/security/user ]; then
    if grep_file '^[ 	]*minlen[ 	]*=' /etc/security/user; then password_policy_configured="true"; fi
    if grep_file '^[ 	]*loginretries[ 	]*=' /etc/security/user; then account_lockout_configured="true"; fi
    if grep_file '^[ 	]*histexpire[ 	]*=' /etc/security/user; then password_hash_algorithm_secure="true"; fi
  fi
}

collect_solaris_security() {
  if [ -r /etc/default/passwd ]; then
    if grep_file '^PASSLENGTH=' /etc/default/passwd; then password_policy_configured="true"; fi
    if grep_file '^RETRIES=' /etc/default/login; then account_lockout_configured="true"; fi
  fi
  if command -v auditconfig >/dev/null 2>&1; then
    if auditconfig -getcond >/dev/null 2>&1; then system_logging_configured="true"; fi
  fi
}

collect_hpux_security() {
  if [ -r /etc/default/security ]; then
    if grep_file '^MIN_PASSWORD_LENGTH=' /etc/default/security; then password_policy_configured="true"; fi
    if grep_file '^AUTH_MAXTRIES=' /etc/default/security; then account_lockout_configured="true"; fi
  fi
}

collect_linux_security() {
  if [ -r /etc/login.defs ]; then
    if grep_file '^PASS_MAX_DAYS[ 	]' /etc/login.defs; then password_policy_configured="true"; fi
  fi
  if [ -r /etc/security/faillock.conf ] || grep faillock /etc/pam.d/* >/dev/null 2>&1; then
    account_lockout_configured="true"
  fi
  if [ -r /etc/login.defs ] && grep '^ENCRYPT_METHOD[ 	].*SHA' /etc/login.defs >/dev/null 2>&1; then
    password_hash_algorithm_secure="true"
  fi
}

emit_json() {
  printf '{\n'
  printf '  "schema_version": "kcii-unix-paste-v1",\n'
  printf '  "platform": "unix",\n'
  printf '  "target_type": "unix_server",\n'
  printf '  "guide_version": "kcii-2025-12",\n'
  printf '  "unix_flavor": '; json_string "$unix_flavor"; printf ',\n'
  printf '  "evidence": {\n'
  printf '    "root_remote_login_restricted": %s,\n' "$(bool_or_manual "$root_remote_login_restricted")"
  printf '    "password_policy_configured": %s,\n' "$(bool_or_manual "$password_policy_configured")"
  printf '    "account_lockout_configured": %s,\n' "$(bool_or_manual "$account_lockout_configured")"
  printf '    "password_file_protected": %s,\n' "$(bool_or_manual "$password_file_protected")"
  printf '    "uid0_extra_count": %s,\n' "$(number_or_manual "$uid0_extra_count")"
  printf '    "session_timeout_configured": %s,\n' "$(bool_or_manual "$session_timeout_configured")"
  printf '    "password_hash_algorithm_secure": %s,\n' "$(bool_or_manual "$password_hash_algorithm_secure")"
  printf '    "root_path_secure": %s,\n' "$(bool_or_manual "$root_path_secure")"
  printf '    "passwd_permission_ok": %s,\n' "$(bool_or_manual "$passwd_permission_ok")"
  printf '    "shadow_permission_ok": %s,\n' "$(bool_or_manual "$shadow_permission_ok")"
  printf '    "finger_service_disabled": %s,\n' "$(bool_or_manual "$finger_service_disabled")"
  printf '    "r_services_disabled": %s,\n' "$(bool_or_manual "$r_services_disabled")"
  printf '    "telnet_service_disabled": %s,\n' "$(bool_or_manual "$telnet_service_disabled")"
  printf '    "ftp_encrypted_or_disabled": %s,\n' "$(bool_or_manual "$ftp_encrypted_or_disabled")"
  printf '    "snmp_service_disabled": %s,\n' "$(bool_or_manual "$snmp_service_disabled")"
  printf '    "nfs_service_disabled": %s,\n' "$(bool_or_manual "$nfs_service_disabled")"
  printf '    "rpc_service_disabled": %s,\n' "$(bool_or_manual "$rpc_service_disabled")"
  printf '    "tftp_talk_disabled": %s,\n' "$(bool_or_manual "$tftp_talk_disabled")"
  printf '    "ntp_configured": %s,\n' "$(bool_or_manual "$ntp_configured")"
  printf '    "system_logging_configured": %s\n' "$(bool_or_manual "$system_logging_configured")"
  printf '  },\n'
  printf '  "collection_warnings": []\n'
  printf '}\n'
}

main() {
  unix_flavor=$(detect_unix_flavor)
  password_policy_configured="manual_review_required"
  account_lockout_configured="manual_review_required"
  password_hash_algorithm_secure="manual_review_required"

  collect_common_passwd_summary
  collect_common_file_permissions
  collect_common_network_services
  collect_common_security_summary

  case "$unix_flavor" in
    aix) collect_aix_security_user ;;
    solaris) collect_solaris_security ;;
    hpux) collect_hpux_security ;;
    linux) collect_linux_security ;;
  esac

  emit_json
}

main "$@"
