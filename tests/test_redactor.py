from __future__ import annotations

import json

from typer.testing import CliRunner

from kcii_audit.ai.redactor import redact_record
from kcii_audit.cli import app

runner = CliRunner()


def test_redact_record_masks_common_sensitive_values():
    masked = redact_record(
        {
            "host": "db01.example.invalid",
            "ip": "192.0.2.25",
            "path": "/etc/ssh/sshd_config",
            "admin_email": "admin@example.com",
            "password": "plain-text-password",
        }
    )

    assert masked["ip"] == "[IPV4_1]"
    assert masked["path"] == "[PATH_1]"
    assert masked["admin_email"] == "[EMAIL_1]"
    assert masked["password"] == "[REDACTED_SECRET]"


def test_redact_command_writes_masked_jsonl(tmp_path):
    input_path = tmp_path / "evidence.jsonl"
    output_path = tmp_path / "masked.jsonl"
    input_path.write_text(
        json.dumps({"evidence": {"ip": "198.51.100.10", "token": "secret-token"}}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        ["redact", "--input", str(input_path), "--output", str(output_path)],
    )

    assert result.exit_code == 0, result.output
    masked = json.loads(output_path.read_text(encoding="utf-8"))
    assert masked["evidence"]["ip"] == "[IPV4_1]"
    assert masked["evidence"]["token"] == "[REDACTED_SECRET]"
