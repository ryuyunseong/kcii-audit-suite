# 실제 고객사 유사 테스트 랩

이 문서는 `kcii-audit-suite`의 개발/검증용 랩 구조를 설명합니다.

이 랩은 운영 고객사 자동 수집용이 아닙니다. 운영 기본 흐름은 대상 시스템, DBMS, 네트워크 장비, 보안 장비에서 담당자가 read-only 점검 스크립트 또는 명령을 실행하고, 결과 파일이나 붙여넣기 텍스트를 Windows 작업 PC로 가져와 `kcii-audit classify-file` 또는 `classify-paste`로 오프라인 분석하는 방식입니다.

Docker, VM, Containerlab, GNS3/EVE-NG는 parser, rulepack, Excel/Markdown 산출을 실제 고객사와 유사한 결과 이동 흐름으로 검증하기 위한 개발/테스트 환경입니다.

## 운영 흐름

```text
대상 시스템 또는 장비
  -> read-only 점검 스크립트, SQL, show command, config export 실행
  -> 결과 파일 또는 복사 가능한 텍스트 생성
  -> Windows 작업 PC로 이동
  -> kcii-audit classify-file 또는 classify-paste
  -> evidence.jsonl, results.json, detail.xlsx, summary.xlsx, report.md, security_advisory.md, security_advisory.xlsx 생성
```

운영 환경에서는 Windows 작업 PC가 고객사 전체 서버, DBMS, 장비에 직접 접속해 설정을 가져오는 원격 자동 수집을 기본값으로 제공하지 않습니다.

## 랩 구조

```text
lab/realistic/
├── README.md
├── transfer/
│   ├── inbox/
│   └── out/
├── scenarios/
│   ├── good/
│   ├── vulnerable/
│   ├── mixed/
│   ├── permission_denied/
│   └── unsupported_output/
├── windows_server/
├── linux_server/
├── unix_server/
├── dbms/
├── network/
└── security_appliance/
```

## 결과 이동 절차

1. 대상 시스템에서 점검 스크립트 또는 명령을 read-only로 실행합니다.
2. 생성된 결과 파일을 `lab/realistic/transfer/inbox/`에 복사합니다.
3. Windows 작업 PC에서 다음 명령으로 분석합니다.

```powershell
kcii-audit classify-file --profile windows --input lab\realistic\transfer\inbox\windows-result.json --output lab\realistic\transfer\out\windows
```

Linux 결과는 다음처럼 분석합니다.

```powershell
kcii-audit classify-file --profile linux --input lab\realistic\transfer\inbox\linux-result.json --output lab\realistic\transfer\out\linux
```

4. 산출물은 `lab/realistic/transfer/out/` 아래에 생성합니다.
5. 결과물과 보안 권고문에 고객명, IP, 계정명, 도메인, 시리얼, 토큰, 키, 인증서 본문 등 민감정보가 남지 않았는지 확인합니다.

기본 권고문 생성 기준:

- 취약 항목: 조치 권고
- 수동확인 항목: 추가 확인 권고
- 양호 항목: 기본 제외

양호 항목도 유지관리 권고로 남기려면 `--include-good-advisory`를 사용합니다. 별도 권고문 파일 생성을 끄려면 `--no-advisory`를 사용합니다.

## 시나리오

| 시나리오 | 목적 |
| --- | --- |
| `good` | 양호 판정 재현 |
| `vulnerable` | 취약 판정 재현 |
| `mixed` | 양호/취약/수동확인이 섞인 실제형 입력 검증 |
| `permission_denied` | 권한 부족을 실패가 아닌 evidence로 기록하는지 검증 |
| `unsupported_output` | 미지원 출력 형식을 수동확인으로 넘기는지 검증 |

## 대상별 랩

### Windows Server

Windows Server는 Docker가 아니라 VM 기반 테스트가 현실적입니다. Hyper-V, VMware, VirtualBox, Azure VM 등 승인된 VM에서 `scripts/targets/windows_server/collect.ps1`을 실행하고 결과 JSON을 `transfer/inbox/`로 복사합니다.

Windows Server rulepack은 KISA PDF Windows 서버 항목 표의 `W-01`~`W-64`를 모두 등록합니다. 현재 `collect.ps1`과 parser는 일부 항목만 자동 판정하고, 나머지는 삭제하지 않고 수동확인으로 남깁니다. 기존 MVP에서 사용하던 Guest, 방화벽, 최소 암호 길이 증적은 공식 항목 기준으로 각각 `W-02`, `W-64`, `W-09`에 매핑됩니다.

### Linux Server

Linux Server는 Docker 컨테이너와 VM 테스트를 모두 사용합니다. Docker는 parser fixture를 빠르게 만들 때 유용하고, systemd/PAM/auditd처럼 컨테이너에서 제한되는 항목은 VM에서 확인합니다.

대상 Linux Server에서 실행하는 기본 스크립트:

```sh
sh ./scripts/targets/linux_server/collect.sh --pretty > linux-result.json
```

MVP 검증 항목:

- root SSH 접속 제한
- UID 0 계정 수 요약
- 패스워드 최소 길이 확인 가능 여부
- 패스워드 만료 정책 확인 가능 여부
- `/etc/passwd` 권한
- `/etc/shadow` 권한
- SSH PasswordAuthentication 설정
- 로그 설정 확인 가능 여부

주의사항:

- `/etc/shadow` 본문은 수집하지 않고 권한 정보만 수집합니다.
- 계정명 전체 목록은 결과물에 저장하지 않습니다.
- PAM, authselect, systemd, auditd 항목은 컨테이너만으로 완전 재현이 어렵기 때문에 VM 검증도 병행합니다.

### Unix Server

Unix Server는 AIX, Solaris, HP-UX, Linux 호환 Unix 결과를 fixture 중심으로 검증합니다. 운영 환경에서는 Windows 작업 PC가 Unix 서버에 원격 접속해 자동 수집하지 않습니다. 대상 서버에서 승인된 read-only POSIX sh 스크립트를 실행하고 결과 파일을 Windows 작업 PC로 가져와 오프라인 판정합니다.

대상 Unix 서버 실행 예시는 다음과 같습니다.

```sh
sh ./scripts/targets/unix_server/collect.sh > unix-result.json
```

Windows 작업 PC 판정 예시는 다음과 같습니다.

```powershell
kcii-audit classify-file --profile unix --unix aix --input lab\realistic\transfer\inbox\unix-result.json --output lab\realistic\transfer\out\unix-aix
kcii-audit classify-file --profile unix --unix solaris --input lab\realistic\transfer\inbox\unix-result.json --output lab\realistic\transfer\out\unix-solaris
kcii-audit classify-file --profile unix --unix hpux --input lab\realistic\transfer\inbox\unix-result.json --output lab\realistic\transfer\out\unix-hpux
kcii-audit classify-file --profile unix --unix linux --input lab\realistic\transfer\inbox\unix-result.json --output lab\realistic\transfer\out\unix-linux
```

AIX/HP-UX/Solaris는 실제 장비 접근이 어렵고 명령 출력 차이가 크기 때문에 현재 MVP는 전체 `U-01`~`U-67` 등록과 OS별 fixture parser 검증을 우선합니다. 자동판정이 어려운 항목은 삭제하지 않고 `MANUAL_REQUIRED`로 산출합니다. collector는 POSIX sh 호환성을 우선하며 Bash 전용 문법을 피합니다.

### DBMS

DBMS는 PostgreSQL, MySQL, MariaDB Docker Compose 랩으로 개발 검증합니다. 운영 환경에서는 DBA 또는 진단자가 read-only SQL을 직접 실행하고 결과를 Windows 작업 PC로 가져오는 흐름이 기본입니다.

운영 판정 예시는 다음과 같습니다.

```powershell
kcii-audit classify-file --profile dbms --dbms postgresql --input lab\realistic\transfer\inbox\postgresql-result.txt --output lab\realistic\transfer\out\dbms-postgresql
kcii-audit classify-file --profile dbms --dbms mysql --input lab\realistic\transfer\inbox\mysql-result.txt --output lab\realistic\transfer\out\dbms-mysql
kcii-audit classify-file --profile dbms --dbms mariadb --input lab\realistic\transfer\inbox\mariadb-result.txt --output lab\realistic\transfer\out\dbms-mariadb
```

DBMS SQL은 `scripts/targets/dbms/postgresql/collect.sql`, `scripts/targets/dbms/mysql/collect.sql`, `scripts/targets/dbms/mariadb/collect.sql`에 있습니다. SQL은 read-only 요약값만 출력해야 하며 계정명 전체 목록, DB명 전체 목록, 비밀번호 해시, 접속 문자열, 권한 상세 원문은 저장하지 않습니다.

Docker Compose 랩은 parser/rulepack 검증용입니다. 운영 고객사 DBMS에 자동 접속하거나 원격 수집하는 흐름으로 사용하지 않습니다.

Docker 랩 검증 절차는 다음 흐름으로 실행합니다.

```powershell
Copy-Item lab\realistic\dbms\.env.example lab\realistic\dbms\.env
notepad lab\realistic\dbms\.env
docker compose -f lab\realistic\dbms\docker-compose.yml --env-file lab\realistic\dbms\.env up -d
```

PostgreSQL/MySQL/MariaDB SQL 출력은 각각 `lab\realistic\transfer\inbox\dbms-postgresql-live.txt`, `lab\realistic\transfer\inbox\dbms-mysql-live.txt`, `lab\realistic\transfer\inbox\dbms-mariadb-live.txt`에 저장한 뒤 `classify-file --profile dbms --dbms <type>`로 분석합니다. 세부 명령은 `lab/realistic/dbms/README.md`를 기준으로 합니다.

검증 후에는 다음 명령으로 로컬 랩 볼륨을 제거합니다.

```powershell
docker compose -f lab\realistic\dbms\docker-compose.yml --env-file lab\realistic\dbms\.env down -v
```

DBMS offline parser note for `dev/v1.0.0rc2`: PostgreSQL, MySQL, and MariaDB inputs may be sanitized JSON or key/value summaries. Permission-denied or unsupported DBMS output is classified as `MANUAL_REQUIRED` and should still produce the standard output bundle. Do not place account lists, database lists, connection strings, password hashes, or raw log text in operational samples or fixtures.

### Network

#### kcii-netlab-sim command-response simulator

`tools/kcii-netlab-sim`은 실제 네트워크 에뮬레이터가 아니라 parser/rulepack/report 테스트용 command-response simulator입니다. Cisco IOS `good`, `vulnerable`, `mixed` 시나리오의 비식별 `show` 명령 출력을 만들고, 그 결과를 `kcii-audit classify-file --profile network --vendor cisco_ios`로 분석합니다.

```powershell
$env:PYTHONPATH="tools\kcii-netlab-sim\src"
python -m kcii_netlab_sim --vendor cisco_ios --scenario mixed --commands scripts\targets\network\cisco_ios\show_commands.txt --output lab\realistic\transfer\inbox\cisco_ios_mixed.txt
kcii-audit classify-file --profile network --vendor cisco_ios --input lab\realistic\transfer\inbox\cisco_ios_mixed.txt --output lab\realistic\transfer\out\network-cisco
```

역할 구분:

| 도구 | 역할 |
| --- | --- |
| `kcii-netlab-sim` | 벤더별 명령-응답 출력 재현, parser/rulepack/report 테스트 |
| Containerlab + FRR | 가벼운 실제 라우팅/토폴로지 랩 |
| GNS3 / EVE-NG / Cisco CML | 벤더 이미지 기반 장비 동작 검증 |
| `kcii-audit-suite` | 오프라인 증적 정규화, rulepack 판정, Excel/Markdown/권고문 산출 |

네트워크 rulepack은 KISA PDF 네트워크 장비 항목 표의 `N-01`~`N-38`을 모두 등록합니다. Cisco IOS parser가 명령어 출력만으로 자동 판정하지 못하는 항목은 삭제하지 않고 수동확인으로 남겨 후속 증적 수집 범위를 명확히 합니다.

네트워크 랩은 Containerlab + FRRouting을 기본 경량 테스트로 둡니다. GNS3/EVE-NG는 Cisco, Juniper, FortiGate 등 벤더 이미지 기반 검증이 필요한 경우 선택적으로 사용합니다. 상용 장비 이미지, 라이선스 파일, 운영 설정 원문은 저장소에 포함하지 않습니다.

#### Junos display-set fixture handling

Junos fixture work starts with offline `show configuration | display set` output only. The parser does not connect to Junos devices and does not collect live data.

Before any real lab, GNS3, CML, or device-derived Junos output is committed, it must be converted into a sanitized fixture:

- hostname -> `[HOST_1]`
- IP address or prefix -> `[IP_1]`
- username -> `[USER_1]`
- SNMP community -> `[COMMUNITY_1]`
- serial number -> `[SERIAL_1]`
- domain -> `[DOMAIN_1]`
- file path or config backup path -> `[PATH_1]`
- banner text -> `[BANNER_1]`
- key, token, hash, password, or credential value -> `[SECRET_1]`

Keep brace-style, XML, JSON, group, `apply-groups`, and inheritance-expanded configuration out of deterministic judgment unless a separate parser task is approved. In the current scope those inputs must remain `MANUAL_REQUIRED` or `needs_display_set`.

Do not store customer configuration exports, raw live output, Junos images, CML images, VM disks, or license files in the repository.

### Security Appliance

Security appliance MVP flow:

```powershell
kcii-audit questionnaire export --profile security-appliance --output out\security_appliance_questionnaire.xlsx
kcii-audit questionnaire import --profile security-appliance --input out\security_appliance_questionnaire.xlsx --output out\security-appliance-questionnaire
kcii-audit classify-file --profile security-appliance --appliance-type firewall --input lab\realistic\transfer\inbox\security-appliance-summary.txt --output out\security-appliance
```

Operational use stays offline. Device owners provide sanitized config export summaries, screen evidence summaries, and questionnaire answers; the Windows work PC does not remotely connect to firewalls, IPS/IDS, WAF, VPN, Anti-DDoS, FortiGate, PAN-OS, Cisco ASA, or F5 devices. The lab validates questionnaire import, synthetic config summaries, parser behavior, rulepack completeness, and output generation rather than real appliance emulation.

Do not place customer names, IP addresses, admin account names, hostnames, domains, policy names, object names, serial numbers, license keys, tokens, or certificate bodies in lab samples. Missing questionnaire answers remain `MANUAL_REQUIRED`; missing or contradictory evidence is kept as a warning in sanitized evidence only.

보안 장비는 실제 에뮬레이션이 어렵거나 라이선스 제약이 큰 항목이 많습니다. config export sample, 정책/로그/계정 설정 export, Excel questionnaire를 조합해 parser와 rulepack을 검증합니다.

## 민감정보 원칙

- 실제 고객명, IP, 계정명, 도메인, 내부 URL, 시리얼, 토큰, 키, 인증서 본문을 sample에 넣지 않습니다.
- sample config와 fixture는 비식별 값만 사용합니다.
- raw 입력은 기본 저장하지 않고, 결과물에는 normalized evidence와 hash만 남깁니다.
- 원격 자동 수집 기능은 lab 전용 또는 승인된 환경 전용 옵션으로만 별도 검토합니다.
