# kcii-audit-suite

주요정보통신기반시설 기술적 취약점 분석·평가 업무를 위한 **오프라인 인프라 보안 점검 보조 도구**입니다.

대상 서버나 장비에 직접 원격 접속하지 않습니다. 담당자가 대상 환경에서 read-only 명령, SQL, 설정 요약 또는 질의서를 수집해 Windows 작업 PC로 전달하면 `kcii-audit`가 rulepack 기준으로 `GOOD`, `VULNERABLE`, `MANUAL_REQUIRED`를 판정하고 Excel·JSON·Markdown 보고서를 생성합니다.

> 이 프로젝트는 KISA 공식 도구가 아니며, 진단자의 수동 판단과 고객사 정책·대체통제 검토를 대신하지 않습니다.

## 포트폴리오 요약

- 기준 가이드: KISA 「주요정보통신기반시설 기술적 취약점 분석·평가 방법 상세가이드」 2025-12-24 등록본
- rulepack 기준: `kcii-2025-12`
- 최신 릴리스: `v1.4.1`
- 불변 기준 태그: `v1.4.0` (`178369b`)
- 실행 환경: Python 3.12 이상, Windows 작업 PC
- 저장소 공개 목적: 채용 포트폴리오 검토

프로젝트의 문제 정의와 설계 의도는 [PORTFOLIO.md](PORTFOLIO.md), 공개 전 점검 기록은 [docs/PUBLIC_READINESS.md](docs/PUBLIC_READINESS.md)에서 확인할 수 있습니다.

프로파일별 입력·판정·산출물·미지원 범위는 [docs/END_TO_END_SUPPORT_MATRIX.md](docs/END_TO_END_SUPPORT_MATRIX.md)에 정리했습니다.

## 공개 및 라이선스

본 저장소는 포트폴리오 검토 목적으로 공개되었습니다. 별도 명시가 없는 한 모든 권리는 저작자에게 있습니다. 명시적인 서면 허가 없이 재사용, 재배포 또는 파생 저작물 작성을 허용하지 않습니다.

Public 공개는 오픈소스 사용 허가를 의미하지 않습니다. PyPI/TestPyPI에는 배포하지 않았습니다.

## 운영 흐름

```text
대상 시스템 담당자
  └─ read-only 명령/SQL/설정 요약/질의서 수집
           ↓
Windows 작업 PC로 결과 전달
           ↓
kcii-audit classify-file 또는 classify-paste
           ↓
kcii-2025-12 rulepack 판정
           ↓
Excel·JSON·Markdown 보고서와 보안 권고문 생성
```

Docker Compose, Containerlab, GNS3, EVE-NG와 `kcii-netlab-sim`은 개발·검증 랩용입니다. 운영 고객사 자동 수집이나 원격 접속에 사용하지 않습니다.

DBMS Docker Compose 랩은 운영 고객사 DBMS 자동 수집용이 아닙니다.

## 지원 범위

| 프로파일 | 등록 범위 | 현재 지원 수준 |
| --- | --- | --- |
| Windows Server | `W-01`~`W-64` | 전체 항목 등록, 자동 8·부분 7·수동 49 |
| Linux Server | `L-01`~`L-08` | MVP 범위, 전체 공식 항목 집합은 아님 |
| Unix Server | `U-01`~`U-67` | AIX·Solaris·HP-UX·Linux 호환 출력, 보수적 판정 |
| DBMS | `D-01`~`D-26` | PostgreSQL·MySQL·MariaDB 오프라인 parser |
| Network | `N-01`~`N-38` | Cisco IOS·Junos parser, Cisco IOS 명령-응답 simulator |
| Security Appliance | `S-01`~`S-23` | 질의서 Excel·인터뷰·비식별 설정 요약 중심 |

상세 자동화 개수와 제한사항은 [docs/PROFILE_COVERAGE.md](docs/PROFILE_COVERAGE.md)를 참고하십시오.

`MANUAL_REQUIRED`는 오류가 아닙니다. 증적 부족, 권한 제한, 운영정책 확인, 지원하지 않는 출력 형식처럼 자동판정 근거가 충분하지 않을 때 수동확인이 필요하다는 뜻입니다.

## 판정 결과

| 내부 상태 | 보고서 표시 | 의미 |
| --- | --- | --- |
| `GOOD` | 양호 | 제공된 증적이 rulepack의 양호 조건을 충족 |
| `VULNERABLE` | 취약 | 제공된 증적이 rulepack의 취약 조건과 일치 |
| `MANUAL_REQUIRED` | 수동확인 | 추가 증적·인터뷰·대체통제 검토 필요 |
| `NOT_APPLICABLE` | 해당없음 | 대상 환경에 적용되지 않음 |
| `ERROR` | 오류 | 입력 또는 처리 오류 |

## 기본 산출물

기본 판정은 다음 7개 파일을 생성합니다.

- `evidence.jsonl`: 정규화·비식별화된 증적 요약
- `results.json`: 항목별 판정 결과
- `detail.xlsx`: 상세결과, 취약점, 수동확인, 권고문 시트
- `summary.xlsx`: 종합통계, 분야별통계, 권고문통계
- `report.md`: Markdown 결과 보고서
- `security_advisory.md`: 취약·수동확인 보안 권고문
- `security_advisory.xlsx`: 보안 권고문 Excel

`--no-advisory`를 사용하면 권고문 2개를 제외한 5개 파일만 생성합니다.

## 설치

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e ".[dev]"
.\.venv\Scripts\kcii-audit --help
```

## 사용 예시

Windows Server:

```powershell
kcii-audit classify-file `
  --profile windows `
  --input tests\fixtures\windows\paste\good-collector.json `
  --output out\windows
```

Unix Server:

```powershell
kcii-audit classify-file `
  --profile unix `
  --unix aix `
  --input tests\fixtures\unix_server\aix\good.json `
  --output out\unix-aix
```

DBMS:

```powershell
kcii-audit classify-file `
  --profile dbms `
  --dbms postgresql `
  --input tests\fixtures\dbms\postgresql\good.json `
  --output out\dbms-postgresql
```

Network:

```powershell
kcii-audit classify-file `
  --profile network `
  --vendor cisco_ios `
  --input tests\fixtures\network\cisco_ios\good.txt `
  --output out\network-cisco

kcii-audit classify-file `
  --profile network `
  --vendor junos `
  --input tests\fixtures\network\junos\display_set_good.txt `
  --output out\network-junos
```

보안장비 질의서:

```powershell
kcii-audit questionnaire export `
  --profile security-appliance `
  --output out\security_appliance_questionnaire.xlsx

kcii-audit questionnaire import `
  --profile security-appliance `
  --input out\security_appliance_questionnaire.xlsx `
  --output out\security-appliance
```

표준 입력에 결과를 붙여넣는 `classify-paste`도 각 프로파일에서 동일하게 사용할 수 있습니다.

## 네트워크 검증 도구

`tools/kcii-netlab-sim`은 Cisco IOS 명령에 대해 synthetic `good`, `mixed`, `vulnerable` 출력을 반환하는 command-response simulator입니다.

실제 패킷 포워딩이나 라우팅 프로토콜을 구현한 Packet Tracer급 에뮬레이터가 아닙니다. 실제 장비·GNS3·CML 출력은 반드시 비식별화한 fixture만 저장소에 포함합니다.

Junos는 `show configuration | display set`을 우선 지원하며, `display inheritance`는 충돌하거나 불완전한 경우 `MANUAL_REQUIRED`로 유지합니다. Brace-style, XML, JSON 전체 해석은 지원하지 않습니다.

## 보안장비 질의서

보안장비는 설정 export만으로 판단하기 어려운 운영정책 항목이 많아 다음 시트를 포함한 한글 Excel 질의서를 제공합니다.

- 작성안내와 자산목록
- 계정·접근·정책·로그·업데이트·백업·관제연동
- 인터뷰결과
- 자동판정 안내

`예`는 `GOOD`, `아니오`는 `VULNERABLE`, 공란 또는 `미확인`은 `MANUAL_REQUIRED`로 처리합니다. 증적 누락과 답변 모순은 경고로 기록합니다.

## 보안 원칙

- 운영 대상에는 read-only 명령과 SQL만 사용합니다.
- 실제 고객 증적, 설정 원문, live output, 장비 이미지와 라이선스 파일을 저장소에 포함하지 않습니다.
- 비밀번호, 해시, 토큰, 키, 인증서 본문, 실제 IP, hostname, 계정명과 시리얼을 산출물에 저장하지 않습니다.
- fixture는 synthetic·sanitized 데이터만 사용합니다.
- 원본 대신 boolean, integer, enum, count, warning과 `raw_evidence_hash`를 보관합니다.
- 모르는 출력이나 근거가 부족한 항목을 양호로 단정하지 않습니다.

## 검증

```powershell
.\.venv\Scripts\python -m pytest
git diff --check
```

`v1.4.0` 기준 전체 테스트는 `176 passed`였으며, wheel/sdist 빌드, checksum, clean wheel 설치와 프로파일별 smoke를 검증했습니다.

## 문서

- [CHANGELOG.md](CHANGELOG.md)
- [PORTFOLIO.md](PORTFOLIO.md)
- [RELEASE_NOTES.md](RELEASE_NOTES.md)
- [RELEASE_NOTES_v1.4.0.md](RELEASE_NOTES_v1.4.0.md)
- [RELEASE_NOTES_v1.4.1.md](RELEASE_NOTES_v1.4.1.md)
- [RELEASE_NOTES_v1.3.0.md](RELEASE_NOTES_v1.3.0.md)
- [RELEASE_NOTES_v1.2.0.md](RELEASE_NOTES_v1.2.0.md)
- [RELEASE_NOTES_v1.1.0.md](RELEASE_NOTES_v1.1.0.md)
- [RELEASE_NOTES_v1.0.0.md](RELEASE_NOTES_v1.0.0.md)
- [RELEASE_NOTES_v1.0.0rc1.md](RELEASE_NOTES_v1.0.0rc1.md)
- [RELEASE_NOTES_v1.0.0rc2.md](RELEASE_NOTES_v1.0.0rc2.md)
- [docs/RELEASE_CHECKLIST.md](docs/RELEASE_CHECKLIST.md)
- [docs/PUBLIC_READINESS.md](docs/PUBLIC_READINESS.md)
- [docs/PROJECT_COMPLETION.md](docs/PROJECT_COMPLETION.md)
- [docs/MAINTENANCE_POLICY.md](docs/MAINTENANCE_POLICY.md)
- [docs/PROFILE_COVERAGE.md](docs/PROFILE_COVERAGE.md)
- [docs/END_TO_END_SUPPORT_MATRIX.md](docs/END_TO_END_SUPPORT_MATRIX.md)
- [docs/NETWORK_OUTPUT_SANITIZATION.md](docs/NETWORK_OUTPUT_SANITIZATION.md)
- [docs/JUNOS_DISPLAY_INHERITANCE_DESIGN.md](docs/JUNOS_DISPLAY_INHERITANCE_DESIGN.md)
- [docs/V1_4_0_READINESS.md](docs/V1_4_0_READINESS.md)
- [docs/V1_4_1_READINESS.md](docs/V1_4_1_READINESS.md)
- [docs/V1_3_0_READINESS.md](docs/V1_3_0_READINESS.md)
- [docs/V1_2_0_READINESS.md](docs/V1_2_0_READINESS.md)
- [docs/V1_1_0_READINESS.md](docs/V1_1_0_READINESS.md)
- [docs/V1_0_0_READINESS.md](docs/V1_0_0_READINESS.md)
- [docs/V1_0_0RC2_READINESS.md](docs/V1_0_0RC2_READINESS.md)

## 유지보수 기준

- `v1.4.0` 태그와 Release asset은 변경하지 않습니다.
- 문서·작은 버그 수정은 `dev/v1.4.1`에서 관리합니다.
- 하위 호환 기능 추가는 `dev/v1.5.0` 이후에서 관리합니다.
- 공개 저장소에 실제 고객 자료를 추가하지 않습니다.
