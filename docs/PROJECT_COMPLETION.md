# v1.4.0 기본 제품 개발 완료 기준

`kcii-audit-suite v1.4.0`은 오프라인 취약점 분석·평가 보조 흐름의 baseline product completion 기준입니다.

이는 모든 등록 항목이 완전 자동화됐다는 뜻이 아닙니다. 지원 프로파일의 증적을 오프라인으로 분류하고, 결정론적 증적은 보수적으로 판정하며, 근거가 부족한 항목을 `MANUAL_REQUIRED`로 유지하는 기본 제품 흐름이 완성됐다는 뜻입니다.

## 기준 상태

- 기준 릴리스: `v1.4.0`
- 태그 대상: `178369b`
- 패키지 버전: `1.4.0`
- 배포: 공개 GitHub Release
- 저장소 공개 목적: 채용 포트폴리오 검토
- PyPI/TestPyPI: 미배포

`v1.4.0` 태그와 Release asset은 이동하거나 교체하지 않습니다. 이후 수정은 새 patch 또는 minor 버전으로 분리합니다.

## 완료된 제품 흐름

1. 대상 시스템 담당자가 read-only 명령, SQL, 설정 요약 또는 질의서를 준비합니다.
2. 결과를 Windows 작업 PC로 전달합니다.
3. `classify-file` 또는 `classify-paste`가 프로파일별 parser로 증적을 정규화합니다.
4. `kcii-2025-12` rulepack이 양호·취약·수동확인을 판정합니다.
5. 항목별 체크리스트, 통계, 보고서와 보안 권고문을 생성합니다.

지원 범위:

- Windows Server
- Linux Server MVP
- Unix Server: AIX, Solaris, HP-UX, Linux 호환 출력
- DBMS: PostgreSQL, MySQL, MariaDB
- Network: Cisco IOS, Juniper Junos
- Security Appliance: 질의서·인터뷰·비식별 설정 요약

## 기본 산출물

- `evidence.jsonl`
- `results.json`
- `detail.xlsx`
- `summary.xlsx`
- `report.md`
- `security_advisory.md`
- `security_advisory.xlsx`

## 안전 경계

- 운영 대상에 원격 자동 접속하지 않습니다.
- 실제 고객 증적과 설정 원문을 저장소·Release asset에 포함하지 않습니다.
- 모호하거나 정책 의존적인 항목을 양호로 단정하지 않습니다.
- 미지원 출력, 권한 부족과 inheritance 충돌은 `MANUAL_REQUIRED`로 처리합니다.
- KISA 공식 도구가 아니며 진단자의 최종 판단을 대체하지 않습니다.

## 후속 브랜치

- `dev/v1.4.1`: 문서 수정과 좁은 범위의 버그 수정
- `dev/v1.5.0`: 하위 호환 신규 기능
- `release/public-readiness`: 공개 정책과 포트폴리오 검토 기록

현재 작업 브랜치에서 기능을 추가하더라도 고정된 `v1.4.0` 태그와 asset에는 반영하지 않습니다.
