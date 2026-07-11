# kcii-audit-suite 포트폴리오 요약

## 한 줄 소개

`kcii-audit-suite`는 주요정보통신기반시설 기술적 취약점 분석/평가 업무를 가정해 만든 오프라인 인프라 보안 점검 자동화 도구입니다.

대상 서버나 장비에 직접 원격 접속하지 않고, 담당자가 read-only 명령 결과나 질의서 답변을 전달하면 Windows 작업 PC에서 rulepack 기반으로 `GOOD`, `VULNERABLE`, `MANUAL_REQUIRED`를 분류하고 Excel/Markdown 산출물을 생성합니다.

## 공개 및 라이선스 정책

본 저장소는 포트폴리오 검토 목적으로 공개된 프로젝트입니다.

별도 명시가 없는 한 모든 권리는 저작자에게 있으며, 명시적인 서면 허가 없이 무단 복제, 수정, 재배포, 파생 저작물 작성을 허용하지 않습니다.

본 도구는 KISA 공식 도구가 아니며, 주요정보통신기반시설 취약점 분석/평가 업무의 수동 보안 판단을 대체하지 않습니다.

## 해결하려는 문제

보안 진단 현장에서는 모든 서버, DBMS, 네트워크 장비, 보안장비에 진단자가 직접 접속하기 어렵습니다. 또한 자동판정이 어려운 항목까지 무리하게 단정하면 오탐과 과탐이 발생할 수 있습니다.

이 프로젝트는 다음 원칙으로 문제를 풀었습니다.

- 운영 환경에서는 원격 자동 수집 대신 오프라인 evidence 분석을 사용합니다.
- 판단 근거가 충분한 항목만 자동판정합니다.
- 정책, 인터뷰, 운영 예외 확인이 필요한 항목은 `MANUAL_REQUIRED`로 남깁니다.
- 원본 증적, 계정명, IP, 토큰, 비밀번호, 라이선스 등 민감정보를 산출물에 저장하지 않습니다.
- 동일한 입력에서 일관된 JSON, Excel, Markdown 보고서를 생성합니다.

## 주요 기능

- Windows, Linux, Unix, DBMS, Network, Security Appliance profile 지원
- `kcii-2025-12` rulepack 기준 항목 등록과 오프라인 판정
- Cisco IOS 및 Juniper Junos network parser 지원
- PostgreSQL, MySQL, MariaDB DBMS evidence parser 지원
- 보안장비 질의서 Excel export/import 지원
- 기본 7개 산출물 생성
  - `evidence.jsonl`
  - `results.json`
  - `detail.xlsx`
  - `summary.xlsx`
  - `report.md`
  - `security_advisory.md`
  - `security_advisory.xlsx`

## 기술적 구현 포인트

- Python CLI: `typer` 기반 명령행 도구
- Rulepack: YAML 기반 profile별 점검 항목/판정 규칙 분리
- Parser: 운영체제, DBMS, 네트워크 장비별 evidence normalization
- Report: `openpyxl`과 Markdown 기반 상세/요약/권고문 산출
- Packaging: wheel/sdist 빌드, checksum 생성, clean venv 설치 검증
- Release: GitHub Release 기준으로 버전별 검증 기록 유지
- Test: fixture 기반 parser/rulepack/report 회귀 테스트

## 검증 상태

`v1.4.0` 기준 검증 결과:

- 전체 테스트: `176 passed`
- 기본 profile smoke 통과
- Network Cisco IOS/Junos smoke 통과
- Junos display-inheritance 보수적 처리 검증
- wheel/sdist build 및 checksum 검증
- clean wheel install smoke 통과
- 민감정보/금지 경로 검사 통과

## 보안 설계 원칙

- read-only evidence만 분석합니다.
- 고객사 원본 증적을 repository나 release asset에 포함하지 않습니다.
- fixture는 synthetic/sanitized sample만 사용합니다.
- 비밀번호 해시, 토큰, 키, 인증서 본문, 실제 IP, hostname, 계정명, 라이선스 파일을 저장하지 않습니다.
- 불확실한 항목은 실패 처리하지 않고 `MANUAL_REQUIRED`로 산출합니다.

## 현재 한계

이 프로젝트는 완전 자동 진단 도구가 아닙니다. 실무형 오프라인 보조 도구입니다.

- 운영정책, 담당자 인터뷰, 대체통제 확인이 필요한 항목은 수동확인이 필요합니다.
- Junos inheritance는 충돌/불완전 evidence에서 보수적으로 처리합니다.
- 보안장비는 질의서와 sanitized summary 중심입니다.
- 공개 저장소에는 실제 고객 자료를 포함하지 않으며, 라이선스와 책임 범위 정책을 유지합니다.

## 지원 직무와 연결되는 역량

- 인프라/보안 진단 업무 이해
- 운영 환경 제약을 고려한 자동화 설계
- rule 기반 판정 엔진과 parser 구조화
- 민감정보 보호와 보수적 보안 판단
- 테스트, 패키징, 릴리스 검증 자동화
- 문서화와 유지보수 정책 수립

## 제출용 요약 문구

`kcii-audit-suite`는 주요정보통신기반시설 취약점 점검 업무를 모델로 만든 오프라인 보안 진단 자동화 도구입니다. Windows/Linux/Unix/DBMS/Network/Security Appliance evidence를 rulepack 기반으로 분류하고, Excel/Markdown 보고서와 보안 권고문을 생성합니다. 자동판정 근거가 부족한 항목은 `MANUAL_REQUIRED`로 남기는 보수적 판정 구조를 적용했으며, 민감정보를 저장하지 않는 synthetic fixture 기반 테스트와 release 검증 체계를 갖췄습니다.
