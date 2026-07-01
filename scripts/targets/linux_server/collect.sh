#!/usr/bin/env sh
set -eu

# Linux Server read-only evidence collection MVP.
# Run this on the target Linux server, then copy the JSON output to the
# Windows work PC and classify it offline with kcii-audit.

PRETTY=false
if [ "${1:-}" = "--pretty" ] || [ "${1:-}" = "-p" ]; then
  PRETTY=true
fi

json_string() {
  # Escape enough for short read-only evidence values.
  printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'
}

json_value() {
  value="${1:-}"
  if [ -z "$value" ]; then
    printf 'null'
  else
    printf '"%s"' "$(json_string "$value")"
  fi
}

json_number() {
  value="${1:-}"
  case "$value" in
    ''|*[!0-9]*)
      printf 'null'
      ;;
    *)
      printf '%s' "$value"
      ;;
  esac
}

json_bool() {
  value="${1:-}"
  case "$value" in
    true|false)
      printf '%s' "$value"
      ;;
    *)
      printf 'null'
      ;;
  esac
}

now_utc() {
  if command -v date >/dev/null 2>&1; then
    date -u '+%Y-%m-%dT%H:%M:%SZ'
  else
    printf 'unknown'
  fi
}

detect_os_name() {
  if [ -r /etc/os-release ]; then
    awk -F= '$1=="NAME"{gsub(/^"|"$/, "", $2); print $2; exit}' /etc/os-release
  fi
}

detect_os_version() {
  if [ -r /etc/os-release ]; then
    awk -F= '$1=="VERSION_ID"{gsub(/^"|"$/, "", $2); print $2; exit}' /etc/os-release
  fi
}

read_sshd_value() {
  key="$1"
  file="/etc/ssh/sshd_config"
  if [ -r "$file" ]; then
    awk -v key="$(printf '%s' "$key" | tr '[:upper:]' '[:lower:]')" '
      /^[[:space:]]*#/ { next }
      NF >= 2 {
        current=tolower($1)
        if (current == key) {
          value=tolower($2)
        }
      }
      END {
        if (value != "") {
          print value
        }
      }
    ' "$file"
  fi
}

uid0_count() {
  if [ -r /etc/passwd ]; then
    awk -F: '$3 == 0 { count++ } END { print count + 0 }' /etc/passwd
  fi
}

password_min_length() {
  if [ -r /etc/security/pwquality.conf ]; then
    awk -F= '
      /^[[:space:]]*#/ { next }
      /^[[:space:]]*minlen[[:space:]]*=/ {
        gsub(/[[:space:]]/, "", $2)
        print $2
        found=1
      }
      END { if (found) exit 0 }
    ' /etc/security/pwquality.conf | tail -n 1
  elif [ -r /etc/login.defs ]; then
    awk '$1 == "PASS_MIN_LEN" { print $2; found=1 } END { if (found) exit 0 }' /etc/login.defs | tail -n 1
  fi
}

password_max_days() {
  if [ -r /etc/login.defs ]; then
    awk '$1 == "PASS_MAX_DAYS" { print $2; found=1 } END { if (found) exit 0 }' /etc/login.defs | tail -n 1
  fi
}

file_mode() {
  file="$1"
  if [ -e "$file" ]; then
    if stat -c '%a' "$file" >/dev/null 2>&1; then
      stat -c '%a' "$file"
    elif stat -f '%Lp' "$file" >/dev/null 2>&1; then
      stat -f '%Lp' "$file"
    fi
  fi
}

mode_ok() {
  mode="${1:-}"
  max="${2:-}"
  case "$mode:$max" in
    *[!0-7]*:*)
      printf 'null'
      ;;
    :*)
      printf 'null'
      ;;
    *)
      if [ "$mode" -le "$max" ]; then
        printf 'true'
      else
        printf 'false'
      fi
      ;;
  esac
}

logging_detected() {
  if command -v rsyslogd >/dev/null 2>&1 || command -v syslogd >/dev/null 2>&1 || [ -d /etc/systemd/journald.conf.d ] || [ -f /etc/systemd/journald.conf ]; then
    printf 'true'
  else
    printf 'false'
  fi
}

ssh_root="$(read_sshd_value PermitRootLogin || true)"
ssh_password="$(read_sshd_value PasswordAuthentication || true)"
uid0_total="$(uid0_count || true)"
uid0_extra=""
if [ -n "$uid0_total" ]; then
  uid0_extra=$((uid0_total - 1))
  if [ "$uid0_extra" -lt 0 ]; then
    uid0_extra=0
  fi
fi
min_length="$(password_min_length || true)"
max_days="$(password_max_days || true)"
passwd_mode="$(file_mode /etc/passwd || true)"
shadow_mode="$(file_mode /etc/shadow || true)"
passwd_ok="$(mode_ok "$passwd_mode" 644)"
shadow_ok="$(mode_ok "$shadow_mode" 640)"
logs_detected="$(logging_detected)"
os_name="$(detect_os_name || true)"
os_version="$(detect_os_version || true)"
collected_at="$(now_utc)"

if [ "$PRETTY" = true ]; then
  cat <<EOF
{
  "schema_version": "kcii-linux-paste-v1",
  "platform": "linux",
  "target_type": "linux_server",
  "guide_version": "kcii-2025-12",
  "collector_version": "0.1.0",
  "collected_at": "$(json_string "$collected_at")",
  "os_name": $(json_value "$os_name"),
  "os_version": $(json_value "$os_version"),
  "evidence": {
    "ssh_permit_root_login": $(json_value "$ssh_root"),
    "ssh_password_authentication": $(json_value "$ssh_password"),
    "uid0_account_count": $(json_number "$uid0_total"),
    "uid0_extra_count": $(json_number "$uid0_extra"),
    "password_min_length": $(json_number "$min_length"),
    "password_max_days": $(json_number "$max_days"),
    "passwd_permission_mode": $(json_value "$passwd_mode"),
    "passwd_permission_ok": $(json_bool "$passwd_ok"),
    "shadow_permission_mode": $(json_value "$shadow_mode"),
    "shadow_permission_ok": $(json_bool "$shadow_ok"),
    "logging_service_detected": $(json_bool "$logs_detected")
  },
  "collection_warnings": []
}
EOF
else
  printf '{"schema_version":"kcii-linux-paste-v1","platform":"linux","target_type":"linux_server","guide_version":"kcii-2025-12","collector_version":"0.1.0","collected_at":"%s","os_name":%s,"os_version":%s,"evidence":{"ssh_permit_root_login":%s,"ssh_password_authentication":%s,"uid0_account_count":%s,"uid0_extra_count":%s,"password_min_length":%s,"password_max_days":%s,"passwd_permission_mode":%s,"passwd_permission_ok":%s,"shadow_permission_mode":%s,"shadow_permission_ok":%s,"logging_service_detected":%s},"collection_warnings":[]}\n' \
    "$(json_string "$collected_at")" \
    "$(json_value "$os_name")" \
    "$(json_value "$os_version")" \
    "$(json_value "$ssh_root")" \
    "$(json_value "$ssh_password")" \
    "$(json_number "$uid0_total")" \
    "$(json_number "$uid0_extra")" \
    "$(json_number "$min_length")" \
    "$(json_number "$max_days")" \
    "$(json_value "$passwd_mode")" \
    "$(json_bool "$passwd_ok")" \
    "$(json_value "$shadow_mode")" \
    "$(json_bool "$shadow_ok")" \
    "$(json_bool "$logs_detected")"
fi
