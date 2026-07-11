# kcii-audit-suite v1.4.1

`v1.4.1`은 public 포트폴리오 저장소의 한글 품질과 전 프로파일 end-to-end 계약을 고정하는 patch release입니다.

## 주요 변경

- Unix와 Security Appliance rulepack의 손상된 한글 판정 근거·조치·권고 문구를 복구했습니다.
- CLI 도움말, 오류와 완료 메시지를 한국어 중심으로 정리했습니다.
- README, 프로파일 지원 범위, 완료·유지보수·공개 정책 문서를 현재 public 상태에 맞게 한글화했습니다.
- 보안장비 질의서에 11개 한글 시트와 한글 입력 헤더를 적용했습니다.
- 기존 영어 헤더로 작성한 질의서도 계속 import할 수 있습니다.
- `detail.xlsx`의 분야별통계, 취약점목록, 예외·대체통제와 AI 판정 로그 시트를 실제 결과 계약에 맞게 초기화·연동했습니다.
- `docs/END_TO_END_SUPPORT_MATRIX.md`와 통합 acceptance test를 추가했습니다.

## 지원 범위

- Windows Server: `W-01`~`W-64`
- Linux Server: `L-01`~`L-08` MVP
- Unix Server: `U-01`~`U-67`, AIX·Solaris·HP-UX·Linux 호환 출력
- DBMS: `D-01`~`D-26`, PostgreSQL·MySQL·MariaDB
- Network: `N-01`~`N-38`, Cisco IOS·Juniper Junos
- Security Appliance: `S-01`~`S-23`, 질의서·인터뷰·비식별 설정 요약

전체 항목 등록은 전체 자동판정을 의미하지 않습니다. 증적이 부족하거나 정책·대체통제 확인이 필요한 항목은 `MANUAL_REQUIRED`입니다.

## 산출물

기본 실행은 다음 7개 파일을 생성합니다.

- `evidence.jsonl`
- `results.json`
- `detail.xlsx`
- `summary.xlsx`
- `report.md`
- `security_advisory.md`
- `security_advisory.xlsx`

`--no-advisory`는 권고문 2개를 제외한 5개 파일을 생성합니다.

## 보안

- 실제 고객 증적, live output, 상용 장비 이미지와 라이선스 파일을 포함하지 않습니다.
- 계정명, DB명, 접속 문자열, IP, hostname, community, serial, password, hash, token과 key를 일반 산출물에 저장하지 않습니다.
- 미지원·모호·권한 부족 증적을 양호로 판정하지 않습니다.
- `v1.4.0` 태그와 기존 Release asset은 변경하지 않았습니다.
- PyPI/TestPyPI에는 배포하지 않습니다.

## 검증 결과

- 전체 테스트: `189 passed`
- release-readiness 및 end-to-end acceptance: `22 passed`
- Windows, Linux, Unix, DBMS 3종, Cisco IOS, Junos, Security Appliance 기본 7개 산출물 확인
- 한글·legacy 영어 질의서 import 확인
- Runtime YAML·Markdown·JSON·Excel 손상 문자열 0건
- root/package-resource checksum 일치

## 알려진 제한사항

- Linux는 `L-01`~`L-08` MVP입니다.
- DBMS는 PostgreSQL, MySQL, MariaDB만 지원합니다.
- `kcii-netlab-sim`은 Cisco IOS command-response simulator이며 패킷·라우팅 에뮬레이터가 아닙니다.
- Junos 별도 simulator는 없으며 brace-style, XML, JSON과 불완전 inheritance는 수동확인 대상입니다.
- 보안장비는 질의서·인터뷰 중심이며 상용 벤더 설정 전체를 해석하지 않습니다.

## 배포 파일

- `kcii_audit_suite-1.4.1-py3-none-any.whl`
- `kcii_audit_suite-1.4.1.tar.gz`
- `SHA256SUMS.txt`
