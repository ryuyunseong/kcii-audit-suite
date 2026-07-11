# End-to-End 지원 매트릭스

이 문서는 `kcii-audit-suite`가 `kcii-2025-12` 기준에서 제공하는 오프라인 입력, 판정, 산출물과 명시적인 미지원 범위를 정리합니다.

전체 항목 등록은 전체 자동판정을 의미하지 않습니다. 증적이 부족하거나 운영정책·대체통제 확인이 필요한 항목은 `MANUAL_REQUIRED`로 유지합니다.

## 지원 매트릭스

| 프로파일 | 등록 항목 범위 | 지원 대상 | 입력 방식 | 자동판정 범위 | 수동확인 조건 | 테스트 fixture | 생성 산출물 | 미지원 범위 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Windows Server | `W-01`~`W-64` | Windows Server 계열 | `collect.ps1` JSON, key/value, `secedit`, `auditpol`, 파일·붙여넣기 | 자동 8, 부분 7 | 계정·공유·IIS·운영정책, 권한 부족, 증적 누락 | `tests/fixtures/windows/paste/good-collector.json` | 기본 7개 | 모든 Windows 버전·언어 조합의 완전 자동판정 |
| Linux Server | `L-01`~`L-08` | Linux MVP | collector JSON, 파일·붙여넣기 | 8개 부분 판정 | PAM·audit·서비스 관리자 맥락, 권한 부족 | `tests/fixtures/linux_server/good.json` | 기본 7개 | 전체 공식 Linux 항목 집합 |
| Unix Server | `U-01`~`U-67` | AIX, Solaris, HP-UX, Linux 호환 출력 | POSIX sh JSON/key-value, 파일·붙여넣기 | 28개 부분 판정 | OS별 출력 차이, 명령 미지원, 권한 부족, 정책 의존 | `tests/fixtures/unix_server/aix/good.json` | 기본 7개 | 모든 실제 OS 버전 출력의 완전 자동판정 |
| DBMS | `D-01`~`D-26` | PostgreSQL, MySQL, MariaDB | read-only SQL JSON/key-value, 파일·붙여넣기 | 12개 부분 판정 | 권한·역할·감사·원격접속 정책, 출력 미지원 | `tests/fixtures/dbms/*/good.json` | 기본 7개 | Oracle, MSSQL, Tibero, Altibase, Cubrid |
| Network | `N-01`~`N-38` | Cisco IOS, Juniper Junos | show 명령 또는 비식별 설정 텍스트, 파일·붙여넣기 | Cisco IOS 자동 27, Junos 명확한 display-set 증적 | 정책 의존 설정, 미지원 출력, 불완전 inheritance | `tests/fixtures/network/cisco_ios/good.txt`, `tests/fixtures/network/junos/display_set_good.txt` | 기본 7개 | 실제 패킷·라우팅 에뮬레이션, Junos brace/XML/JSON 전체 해석 |
| Security Appliance | `S-01`~`S-23` | Firewall, IPS/IDS, WAF, VPN, Anti-DDoS와 지원 벤더 유형 | 한글/legacy Excel 질의서, 인터뷰, 비식별 설정 요약 | 질의서 `예/아니오` 및 명확한 요약 증적 | 공란·미확인·모순·증적 누락·벤더 원문 미지원 | `tests/fixtures/security_appliance/good.txt` | 기본 7개 | 상용 벤더 설정 전체 해석과 원격 장비 수집 |

## 공통 판정 계약

- `GOOD`: 지원되는 증적이 rulepack의 양호 조건과 일치합니다.
- `VULNERABLE`: 지원되는 증적이 rulepack의 취약 조건과 일치합니다.
- `MANUAL_REQUIRED`: 추가 증적, 인터뷰, 운영정책 또는 대체통제 검토가 필요합니다.

미지원 형식과 권한 부족을 양호로 간주하지 않습니다. parser는 등록 항목을 누락하지 않고 보수적인 판정 결과를 생성합니다.

## 기본 7개 산출물

모든 지원 프로파일은 기본 실행에서 다음 파일을 생성합니다.

1. `evidence.jsonl`
2. `results.json`
3. `detail.xlsx`
4. `summary.xlsx`
5. `report.md`
6. `security_advisory.md`
7. `security_advisory.xlsx`

`--no-advisory`를 사용하면 보안 권고문 2개를 제외한 앞의 5개 파일을 생성합니다.

`detail.xlsx`에는 상세결과, 취약점목록, 수동확인과 보안권고문 시트가 있으며 `summary.xlsx`에는 종합통계, 분야별통계와 권고문통계가 있습니다.

## 네트워크 검증 경계

`kcii-netlab-sim`은 Cisco IOS 명령 출력용 command-response simulator입니다. Packet Tracer, GNS3 또는 CML처럼 실제 패킷 전달과 라우팅을 수행하지 않습니다.

Junos는 별도 simulator가 없습니다. `show configuration | display set`과 제한적인 `display inheritance` 증적을 parser fixture로 검증합니다. 충돌, 누락, `apply-groups-except`, brace-style, XML과 JSON 입력은 `MANUAL_REQUIRED`입니다.

## 보안장비 질의서 계약

질의서 export는 작성안내부터 자동판정까지 11개 한글 시트를 생성합니다. 한글 헤더와 기존 영어 헤더를 모두 import할 수 있습니다.

- `예`: `GOOD`
- `아니오`: `VULNERABLE`
- 공란 또는 `미확인`: `MANUAL_REQUIRED`
- 증적 누락: `evidence_missing` 경고
- 모순 답변: `validation_warning` 경고

자유 입력한 인터뷰 원문과 비고는 결과 산출물에 저장하지 않습니다.

## 민감정보 경계

실제 고객 증적, DB명·계정명 목록, 접속 문자열, 비밀번호·해시, IP, hostname, community, serial, key, token, 인증서 본문, 장비 이미지와 라이선스 파일은 저장소와 일반 산출물에 포함하지 않습니다.
