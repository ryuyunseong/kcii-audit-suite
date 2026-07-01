from __future__ import annotations

from pathlib import Path


def test_realistic_lab_documentation_exists():
    doc = Path("docs/REALISTIC_LAB.md")
    assert doc.exists()

    text = doc.read_text(encoding="utf-8")
    assert "운영 고객사 자동 수집용이 아닙니다" in text
    assert "Windows 작업 PC" in text
    assert "parser, rulepack" in text


def test_realistic_lab_scaffold_paths_exist():
    required_paths = [
        "lab/realistic/transfer/inbox/README.md",
        "lab/realistic/transfer/out/README.md",
        "lab/realistic/scenarios/good/README.md",
        "lab/realistic/scenarios/vulnerable/README.md",
        "lab/realistic/scenarios/mixed/README.md",
        "lab/realistic/scenarios/permission_denied/README.md",
        "lab/realistic/scenarios/unsupported_output/README.md",
        "lab/realistic/windows_server/README.md",
        "lab/realistic/linux_server/README.md",
        "lab/realistic/unix_server/README.md",
        "lab/realistic/dbms/docker-compose.yml",
        "lab/realistic/network/containerlab/frr-topology.yml",
        "lab/realistic/network/gns3/README.md",
        "lab/realistic/security_appliance/README.md",
    ]

    for required_path in required_paths:
        assert Path(required_path).exists(), required_path
