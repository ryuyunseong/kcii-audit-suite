from __future__ import annotations

import re
from typing import Any

SENSITIVE_KEYWORDS = (
    "authorization",
    "certificate",
    "cookie",
    "credential",
    "key",
    "password",
    "secret",
    "serial",
    "token",
)

EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
URL_RE = re.compile(r"\bhttps?://[^\s\"']+", re.IGNORECASE)
WINDOWS_PATH_RE = re.compile(r"\b[A-Za-z]:\\(?:[^\\/:*?\"<>|\r\n]+\\?)+")
UNIX_PATH_RE = re.compile(r"(?<!\w)/(?:[A-Za-z0-9._-]+/)*[A-Za-z0-9._-]+")
PHONE_RE = re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\d{2,4}[-.\s]?){2,3}\d{4}\b")


def redact_record(record: dict[str, Any]) -> dict[str, Any]:
    """Return a redacted copy of a JSON-serializable record."""
    return _redact_value(record)


def _redact_value(value: Any, key: str | None = None) -> Any:
    if isinstance(value, dict):
        redacted: dict[str, Any] = {}
        for child_key, child_value in value.items():
            if _is_sensitive_key(child_key):
                redacted[child_key] = "[REDACTED_SECRET]"
            else:
                redacted[child_key] = _redact_value(child_value, child_key)
        return redacted

    if isinstance(value, list):
        return [_redact_value(item, key) for item in value]

    if isinstance(value, str):
        if key and _is_sensitive_key(key):
            return "[REDACTED_SECRET]"
        return _redact_text(value)

    return value


def _is_sensitive_key(key: str) -> bool:
    normalized = key.lower().replace("-", "_")
    return any(keyword in normalized for keyword in SENSITIVE_KEYWORDS)


def _redact_text(value: str) -> str:
    redacted = EMAIL_RE.sub("[EMAIL_1]", value)
    redacted = URL_RE.sub("[URL_1]", redacted)
    redacted = IPV4_RE.sub("[IPV4_1]", redacted)
    redacted = WINDOWS_PATH_RE.sub("[PATH_1]", redacted)
    redacted = UNIX_PATH_RE.sub("[PATH_1]", redacted)
    redacted = PHONE_RE.sub("[PHONE_1]", redacted)
    return redacted
