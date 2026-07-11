# 프로파일 지원 범위

이 문서는 `kcii-2025-12` rulepack의 등록 범위, 자동화 수준과 알려진 제한사항을 정리합니다. 이 도구는 KISA 공식 도구가 아니라 오프라인 분석·평가 보조 도구입니다.

## 전체 현황

| Profile | Registered items | Auto | Partial | Manual | 설명 |
| --- | ---: | ---: | ---: | ---: | --- |
| Windows Server | 64 | 8 | 7 | 49 | 전체 항목 등록, 일부 자동·부분 판정 |
| Linux Server | 8 | 0 | 8 | 0 | `L-01`~`L-08` MVP, 전체 공식 범위 아님 |
| Unix Server | 67 | 0 | 28 | 39 | AIX·Solaris·HP-UX·Linux 호환 출력 |
| DBMS | 26 | 0 | 12 | 14 | PostgreSQL·MySQL·MariaDB 오프라인 parser |
| Network | 38 | 27 | 0 | 11 | Cisco IOS·Junos parser와 Cisco IOS simulator |
| Security Appliance | 23 | 0 | 23 | 0 | 질의서·인터뷰 중심 증적 흐름 |

자동화 수준의 의미:

- `auto`: 현재 parser가 지원하는 증적만으로 결정론적 판정이 가능합니다.
- `partial`: 일부 조건은 자동판정하지만 운영 맥락이나 추가 증적 확인이 필요할 수 있습니다.
- `manual`: 항목은 결과에 포함되며 진단자의 수동확인이 필요합니다.
- `unsupported`: 현재 parser 범위 밖이며 지원 예정 범위로 문서화합니다.

## Windows Server

- 범위: `W-01` to `W-64`
- 상태: 전체 항목 등록, 부분 자동판정
- 주요 자동화: 계정 잠금, 일부 비밀번호 정책, 기본 공유, 일부 위험 서비스, 감사·이벤트 로그 요약
- 제한사항: 계정 목록, 공유 권한, IIS, 운영정책과 예외 검토는 수동확인 비중이 높습니다.
- 다음 후보: 감사정책, 서비스, 공유·익명 접근, 이벤트 로그 보존정책 확대

## Linux Server

- 범위: `L-01` to `L-08`
- 상태: MVP 결정론적 점검
- 제한사항: 전체 공식 Linux 항목 집합이 아닙니다. PAM, audit와 서비스 관리자 동작은 컨테이너 결과만으로 실제 서버를 대체할 수 없습니다.
- 다음 후보: 전체 Unix/Linux 기준 정합성 확대와 배포판별 fixture 추가

## Unix Server

- 범위: `U-01` to `U-67`
- 지원 유형: AIX, Solaris, HP-UX, Linux 호환 출력
- 상태: 전체 항목 등록, fixture 기반 보수적 parser
- 제한사항: 실제 출력은 OS 버전과 벤더 설정에 따라 달라집니다. 명령 미지원, 권한 부족, 모호한 출력은 `MANUAL_REQUIRED`입니다.
- 다음 후보: 비식별 실제 출력 정규화, 서비스·로그 정책 증적 확대

## DBMS

- 범위: `D-01` to `D-26`
- 지원 DBMS: PostgreSQL, MySQL, MariaDB
- 상태: JSON 및 key/value 오프라인 parser, Docker Compose 개발 랩 검증
- 제한사항: Oracle, MSSQL, Tibero, Altibase, Cubrid는 구현하지 않았습니다. 비밀번호 정책, 감사, 역할, 원격 제한은 보수적으로 판정합니다.
- 다음 후보: 패스워드 정책, 감사·로그, 원격 접근 제한, 추가 DBMS 엔진

## Network

- 범위: `N-01` to `N-38`
- Cisco IOS: 자동 27, 수동 11
- Junos: `show configuration | display set` 중심 MVP, 보수적 `display inheritance` skeleton
- simulator: `kcii-netlab-sim`은 Cisco IOS command-response simulator이며 패킷·라우팅 에뮬레이터가 아닙니다.
- 제한사항: Junos brace-style, XML, JSON 전체 해석과 완전한 inheritance 확장은 지원하지 않습니다. 모호한 설정은 `MANUAL_REQUIRED`입니다.
- 다음 후보: 실제 장비·GNS3·CML 비식별 출력 확대, AAA와 관리 접근 정책 자동화

## Security Appliance

- 범위: `S-01` to `S-23`
- 대상 유형: Firewall, IPS/IDS, WAF, VPN, Anti-DDoS, FortiGate, Palo Alto PAN-OS, Cisco ASA, F5 BIG-IP
- 상태: 한글 질의서 Excel export/import, 인터뷰 증적, 비식별 설정 요약 parser
- 제한사항: 벤더별 parser는 공통 비식별 요약 parser를 감싸는 초기 구현입니다. 정책 검토, 관제, 백업과 운영 절차는 질의서·인터뷰 확인이 필요합니다.
- 다음 후보: FortiGate, PAN-OS, Cisco ASA, F5 설정 요약 parser 심화

## 결과 해석

- `GOOD` / 양호: 제공된 비식별 증적이 양호 조건을 충족했습니다.
- `VULNERABLE` / 취약: 제공된 비식별 증적이 취약 조건과 일치했습니다.
- `MANUAL_REQUIRED` / 수동확인: 추가 증적, 인터뷰, 대체통제 또는 진단자 판단이 필요합니다. 프로그램 실패가 아닙니다.

지원되는 모든 프로파일은 등록된 전체 항목을 결과에 유지합니다. parser 실패, 명령 미지원과 권한 부족은 항목을 누락하지 않고 `MANUAL_REQUIRED` 근거로 처리합니다.

## 산출물

기본 판정은 다음 7개 파일을 생성합니다.

- `evidence.jsonl`
- `results.json`
- `detail.xlsx`
- `summary.xlsx`
- `report.md`
- `security_advisory.md`
- `security_advisory.xlsx`

취약·수동확인 항목은 기본적으로 보안 권고문에 포함됩니다.

## 공식 가이드 반영 원칙

1. 항목 ID, 항목명, 중요도와 영역을 승인된 로컬 가이드 원문과 대조합니다.
2. 공식 항목명을 임의로 만들지 않습니다.
3. 가이드 원문을 저장소에 장문 복제하지 않습니다.
4. manifest와 rulepack에 공식 항목을 함께 등록합니다.
5. 증적이 충분할 때만 `auto` 또는 `partial`로 지정합니다.
6. 정책 의존적이거나 모호한 항목은 `manual`로 유지합니다.
7. 실제 고객 정보 대신 synthetic·sanitized fixture만 사용합니다.

## 민감정보 처리

- 실제 고객 증적, 설정 원문, `.env`, 비밀번호, 해시, 토큰, 키, 인증서 본문, hostname, 도메인, 계정명, 시리얼과 IP를 저장하지 않습니다.
- boolean, integer, enum, count, masked identifier, warning과 `raw_evidence_hash`만 저장합니다.
- 출력 형식 미지원이나 권한 부족을 양호로 해석하지 않습니다.

## 릴리스 이력

- `v1.0.0rc1`: `e93d18b`
- `v1.0.0rc2`: `59d3d38`
- `v1.0.0`: `31983bd`
- `v1.1.0`: `31f624e`, Cisco IOS 자동판정 확대
- `v1.2.0`: `9296245`, Juniper Junos parser MVP
- `v1.3.0`: `30490b4`, realistic Junos 출력 정규화
- `v1.4.0`: `178369b`, Junos display inheritance 보수적 지원과 baseline product completion
- `v1.4.1`: `1a298ff`, 한글 리소스·질의서 호환성과 전 프로파일 산출물 계약 보강

`v1.4.0 Release Scope`은 최초 기본 제품 완료 기준이며, 현재 공개 포트폴리오의 최신 정식 릴리스는 `v1.4.1`입니다. 공개된 태그와 Release asset은 이동하거나 교체하지 않습니다.
