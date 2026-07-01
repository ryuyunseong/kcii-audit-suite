# DBMS lab

DBMS lab is a local development and verification environment for parser and rulepack checks. It is not an operational DBMS auto-collection feature.

## Operational Flow

1. A DBA or assessor runs approved read-only SQL on the target DBMS.
2. The DBA saves the output as text.
3. The output file is moved to the Windows work PC.
4. The Windows work PC runs offline classification.

```powershell
kcii-audit classify-file --profile dbms --dbms postgresql --input postgresql-result.txt --output out\dbms-postgresql
kcii-audit classify-file --profile dbms --dbms mysql --input mysql-result.txt --output out\dbms-mysql
kcii-audit classify-file --profile dbms --dbms mariadb --input mariadb-result.txt --output out\dbms-mariadb
```

The paste path uses the same parser.

```powershell
Get-Content .\postgresql-result.txt | kcii-audit classify-paste --profile dbms --dbms postgresql --output out\dbms-postgresql
```

The default run creates `evidence.jsonl`, `results.json`, `detail.xlsx`, `summary.xlsx`, `report.md`, `security_advisory.md`, and `security_advisory.xlsx`. Use `--no-advisory` to skip the two advisory files.

## Docker Lab Flow

Copy the example environment file and replace the values with temporary lab-only passwords.

```powershell
Copy-Item lab\realistic\dbms\.env.example lab\realistic\dbms\.env
notepad lab\realistic\dbms\.env
```

Start the local DBMS lab.

```powershell
docker compose -f lab\realistic\dbms\docker-compose.yml --env-file lab\realistic\dbms\.env up -d
```

Load the `.env` values into the current PowerShell session for the client commands below.

```powershell
Get-Content lab\realistic\dbms\.env |
  Where-Object { $_ -and $_ -notmatch '^\s*#' } |
  ForEach-Object {
    $parts = $_ -split '=', 2
    Set-Item -Path "Env:$($parts[0])" -Value $parts[1]
  }
```

Run PostgreSQL read-only SQL and classify the output.

```powershell
Get-Content scripts\targets\dbms\postgresql\collect.sql |
  docker exec -e PGPASSWORD="$env:KCII_LAB_POSTGRES_PASSWORD" -i kcii-postgresql psql -U $env:KCII_LAB_POSTGRES_USER -d $env:KCII_LAB_POSTGRES_DB |
  Set-Content lab\realistic\transfer\inbox\dbms-postgresql-live.txt -Encoding utf8

.\.venv\Scripts\kcii-audit classify-file `
  --profile dbms `
  --dbms postgresql `
  --input lab\realistic\transfer\inbox\dbms-postgresql-live.txt `
  --output out\dbms-postgresql-live
```

Run MySQL read-only SQL and classify the output.

```powershell
Get-Content scripts\targets\dbms\mysql\collect.sql |
  docker exec -e MYSQL_PWD="$env:KCII_LAB_MYSQL_ROOT_PASSWORD" -i kcii-mysql mysql -h 127.0.0.1 -u root --batch --raw --skip-column-names |
  Set-Content lab\realistic\transfer\inbox\dbms-mysql-live.txt -Encoding utf8

.\.venv\Scripts\kcii-audit classify-file `
  --profile dbms `
  --dbms mysql `
  --input lab\realistic\transfer\inbox\dbms-mysql-live.txt `
  --output out\dbms-mysql-live
```

Run MariaDB read-only SQL and classify the output.

```powershell
Get-Content scripts\targets\dbms\mariadb\collect.sql |
  docker exec -e MYSQL_PWD="$env:KCII_LAB_MARIADB_ROOT_PASSWORD" -i kcii-mariadb mariadb -h 127.0.0.1 -u root --batch --raw --skip-column-names |
  Set-Content lab\realistic\transfer\inbox\dbms-mariadb-live.txt -Encoding utf8

.\.venv\Scripts\kcii-audit classify-file `
  --profile dbms `
  --dbms mariadb `
  --input lab\realistic\transfer\inbox\dbms-mariadb-live.txt `
  --output out\dbms-mariadb-live
```

Stop and remove the local lab volumes after verification.

```powershell
docker compose -f lab\realistic\dbms\docker-compose.yml --env-file lab\realistic\dbms\.env down -v
```

Do not store customer credentials, real connection strings, internal DB names, production account names, password hashes, or raw privilege details in this directory.
