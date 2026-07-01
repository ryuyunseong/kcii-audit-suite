from __future__ import annotations

from pathlib import Path

import yaml


ENV_EXAMPLE = Path("lab/realistic/dbms/.env.example")
COMPOSE_FILE = Path("lab/realistic/dbms/docker-compose.yml")
LAB_README = Path("lab/realistic/dbms/README.md")
README = Path("README.md")
REALISTIC_LAB = Path("docs/REALISTIC_LAB.md")


def test_dbms_env_example_uses_lab_only_placeholders():
    text = ENV_EXAMPLE.read_text(encoding="utf-8")

    assert "replace-with-temporary-postgres-lab-password" in text
    assert "replace-with-temporary-mysql-lab-password" in text
    assert "replace-with-temporary-mariadb-lab-password" in text
    assert "customerdb" not in text
    assert "192.0.2.10" not in text
    assert "postgresql://" not in text
    assert "mysql://" not in text


def test_dbms_compose_declares_stable_live_container_names_and_env_keys():
    payload = yaml.safe_load(COMPOSE_FILE.read_text(encoding="utf-8"))
    services = payload["services"]

    assert services["postgres"]["container_name"] == "kcii-postgresql"
    assert services["mysql"]["container_name"] == "kcii-mysql"
    assert services["mariadb"]["container_name"] == "kcii-mariadb"
    assert "POSTGRES_PASSWORD" in services["postgres"]["environment"]
    assert "MYSQL_ROOT_PASSWORD" in services["mysql"]["environment"]
    assert "MARIADB_ROOT_PASSWORD" in services["mariadb"]["environment"]


def test_dbms_live_docs_include_offline_and_cleanup_flow():
    combined = "\n".join(
        [
            LAB_README.read_text(encoding="utf-8"),
            README.read_text(encoding="utf-8"),
            REALISTIC_LAB.read_text(encoding="utf-8"),
        ]
    )

    assert "Docker Compose" in combined
    assert ".env.example" in combined
    assert "docker-compose.yml --env-file lab\\realistic\\dbms\\.env up -d" in combined
    assert "dbms-postgresql-live.txt" in combined
    assert "dbms-mysql-live.txt" in combined
    assert "dbms-mariadb-live.txt" in combined
    assert "classify-file --profile dbms --dbms postgresql" in combined
    assert "classify-file --profile dbms --dbms mysql" in combined
    assert "classify-file --profile dbms --dbms mariadb" in combined
    assert "down -v" in combined
    assert "운영 고객사 DBMS 자동 수집용이 아닙니다" in combined
