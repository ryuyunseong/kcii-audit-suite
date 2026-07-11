# K-CII 점검 결과 보고서

## 개요

- 기준 버전: kcii-2025-12
- 산출 상태: 판정 완료
- 원본 민감정보 포함 여부: 포함하지 않음

## 종합 결과

| 판정 | 건수 |
| --- | ---: |
| 수동확인 | 57 |
| 취약 | 7 |


## 상세 결과

| 자산ID | 분야 | 항목ID | 항목명 | 판정 | 판정근거 |
| --- | --- | --- | --- | --- | --- |
| portfolio-windows-synthetic | windows | W-01 | Administrator 계정 이름 변경 등 보안성 강화 | 수동확인 | 필수 evidence 필드가 없습니다: administrator_account_renamed |
| portfolio-windows-synthetic | windows | W-02 | Guest 계정 비활성화 | 수동확인 | 필수 evidence 필드가 없습니다: guest_account_enabled |
| portfolio-windows-synthetic | windows | W-03 | 불필요한 계정 제거 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-04 | 계정 잠금 임계값 설정 | 수동확인 | 필수 evidence 필드가 없습니다: account_lockout_threshold_ok |
| portfolio-windows-synthetic | windows | W-05 | 해독 가능한 암호화를 사용하여 암호 저장 해제 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-06 | 관리자 그룹에 최소한의 사용자 포함 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-07 | Everyone 사용 권한을 익명 사용자에게 적용 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-08 | 계정 잠금 기간 설정 | 수동확인 | 필수 evidence 필드가 없습니다: account_lockout_duration_ok |
| portfolio-windows-synthetic | windows | W-09 | 비밀번호 관리정책 설정 | 취약 | Windows password policy summary does not meet one or more rc2 checks. |
| portfolio-windows-synthetic | windows | W-10 | 마지막 사용자 이름 표시 안 함 | 수동확인 | 필수 evidence 필드가 없습니다: last_username_hidden |
| portfolio-windows-synthetic | windows | W-11 | 로컬 로그온 허용 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-12 | 익명 SID/이름 변환 허용 해제 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-13 | 콘솔 로그온 시 로컬 계정에서 빈 암호 사용 제한 | 수동확인 | 필수 evidence 필드가 없습니다: blank_password_remote_logon_blocked |
| portfolio-windows-synthetic | windows | W-14 | 원격터미널 접속 가능한 사용자 그룹 제한 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-15 | 사용자 개인키 사용 시 암호 입력 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-16 | 공유 권한 및 사용자 그룹 설정 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-17 | 하드디스크 기본 공유 제거 | 취약 | One or more default administrative shares were present in the sanitized share summary. |
| portfolio-windows-synthetic | windows | W-18 | 불필요한 서비스 제거 | 취약 | The rc2 unnecessary-service summary identified an enabled risky service. |
| portfolio-windows-synthetic | windows | W-19 | 불필요한 IIS 서비스 구동 점검 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-20 | NetBIOS 바인딩 서비스 구동 점검 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-21 | 암호화되지 않는 FTP 서비스 비활성화 | 취약 | FTP service appeared enabled and requires encrypted-service review. |
| portfolio-windows-synthetic | windows | W-22 | FTP 디렉토리 접근권한 설정 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-23 | 공유 서비스에 대한 익명 접근 제한 설정 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-24 | FTP 접근 제어 설정 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-25 | DNS Zone Transfer 설정 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-26 | RDS(Remote Data Services)제거 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-27 | 최신 Windows OS Build 버전 적용 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-28 | 터미널 서비스 암호화 수준 설정 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-29 | 불필요한 SNMP 서비스 구동 점검 | 취약 | SNMP service appeared enabled and requires service-necessity review. |
| portfolio-windows-synthetic | windows | W-30 | SNMP Community String 복잡성 설정 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-31 | SNMP Access control 설정 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-32 | DNS 서비스 구동 점검 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-33 | HTTP/FTP/SMTP 배너 차단 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-34 | Telnet 서비스 비활성화 | 수동확인 | 필수 evidence 필드가 없습니다: telnet_service_disabled |
| portfolio-windows-synthetic | windows | W-35 | 불필요한 ODBC/OLE-DB 데이터 소스와 드라이브 제거 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-36 | 원격터미널 접속 타임아웃 설정 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-37 | 예약된 작업에 의심스러운 명령이 등록되어 있는지 점검 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-38 | 주기적 보안 패치 및 벤더 권고사항 적용 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-39 | 백신 프로그램 업데이트 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-40 | 정책에 따른 시스템 로깅 설정 | 취약 | One or more core audit policy categories were missing success or failure auditing in the sanitized summary. |
| portfolio-windows-synthetic | windows | W-41 | NTP 및 시각 동기화 설정 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-42 | 이벤트 로그 관리 설정 | 취약 | Event Log service or minimum log-size summary did not meet the rc2 check. |
| portfolio-windows-synthetic | windows | W-43 | 이벤트 로그 파일 접근 통제 설정 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-44 | 원격으로 액세스할 수 있는 레지스트리 경로 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-45 | 백신 프로그램 설치 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-46 | SAM 파일 접근 통제 설정 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-47 | 화면보호기 설정 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-48 | 로그온하지 않고 시스템 종료 허용 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-49 | 원격 시스템에서 강제로 시스템 종료 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-50 | 보안 감사를 로그할 수 없는 경우 즉시 시스템 종료 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-51 | SAM 계정과 공유의 익명 열거 허용 안 함 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-52 | Autologon 기능 제어 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-53 | 이동식 미디어 포맷 및 꺼내기 허용 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-54 | Dos공격 방어 레지스트리 설정 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-55 | 사용자가 프린터 드라이버를 설치할 수 없게 함 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-56 | SMB 세션 중단 관리 설정 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-57 | 로그온 시 경고 메시지 설정 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-58 | 사용자별 홈 디렉터리 권한 설정 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-59 | LAN Manager 인증 수준 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-60 | 보안 채널 데이터 디지털 암호화 또는 서명 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-61 | 파일 및 디렉토리 보호 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-62 | 시작프로그램 목록 분석 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-63 | 도메인 컨트롤러-사용자의 시간 동기화 | 수동확인 | 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다. |
| portfolio-windows-synthetic | windows | W-64 | 윈도우 방화벽 설정 | 수동확인 | 필수 evidence 필드가 없습니다: firewall_enabled |


## 보안 권고문 요약

| 판정 | 권고문 수 |
| --- | ---: |
| 수동확인 | 57 |
| 취약 | 7 |



## 상세 권고문

### ADV-001 Administrator 계정 이름 변경 등 보안성 강화 추가 확인 필요

- 관련 항목: W-01
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 필수 evidence 필드가 없습니다: administrator_account_renamed
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-01 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-002 Guest 계정 비활성화 추가 확인 필요

- 관련 항목: W-02
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 필수 evidence 필드가 없습니다: guest_account_enabled
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-02 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-003 불필요한 계정 제거 추가 확인 필요

- 관련 항목: W-03
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-03 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-004 계정 잠금 임계값 설정 추가 확인 필요

- 관련 항목: W-04
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 필수 evidence 필드가 없습니다: account_lockout_threshold_ok
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-04 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-005 해독 가능한 암호화를 사용하여 암호 저장 해제 추가 확인 필요

- 관련 항목: W-05
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-05 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-006 관리자 그룹에 최소한의 사용자 포함 추가 확인 필요

- 관련 항목: W-06
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-06 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-007 Everyone 사용 권한을 익명 사용자에게 적용 추가 확인 필요

- 관련 항목: W-07
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-07 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-008 계정 잠금 기간 설정 추가 확인 필요

- 관련 항목: W-08
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 필수 evidence 필드가 없습니다: account_lockout_duration_ok
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-08 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-009 비밀번호 관리정책 설정 미흡

- 관련 항목: W-09
- 영향도: 상
- 대상: [ASSET_001]
- 판정: 취약
- 취약 사유: Windows password policy summary does not meet one or more rc2 checks.
- 권고 조치: 관련 설정을 K-CII rulepack 및 조직 보안 기준에 맞게 조정하고 변경 후 재점검하십시오.
- 재점검 방법: W-09 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-010 마지막 사용자 이름 표시 안 함 추가 확인 필요

- 관련 항목: W-10
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 필수 evidence 필드가 없습니다: last_username_hidden
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-10 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-011 로컬 로그온 허용 추가 확인 필요

- 관련 항목: W-11
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-11 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-012 익명 SID/이름 변환 허용 해제 추가 확인 필요

- 관련 항목: W-12
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-12 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-013 콘솔 로그온 시 로컬 계정에서 빈 암호 사용 제한 추가 확인 필요

- 관련 항목: W-13
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 필수 evidence 필드가 없습니다: blank_password_remote_logon_blocked
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-13 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-014 원격터미널 접속 가능한 사용자 그룹 제한 추가 확인 필요

- 관련 항목: W-14
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-14 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-015 사용자 개인키 사용 시 암호 입력 추가 확인 필요

- 관련 항목: W-15
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-15 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-016 공유 권한 및 사용자 그룹 설정 추가 확인 필요

- 관련 항목: W-16
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-16 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-017 하드디스크 기본 공유 제거 미흡

- 관련 항목: W-17
- 영향도: 상
- 대상: [ASSET_001]
- 판정: 취약
- 취약 사유: One or more default administrative shares were present in the sanitized share summary.
- 권고 조치: 관련 설정을 K-CII rulepack 및 조직 보안 기준에 맞게 조정하고 변경 후 재점검하십시오.
- 재점검 방법: W-17 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-018 불필요한 서비스 제거 미흡

- 관련 항목: W-18
- 영향도: 상
- 대상: [ASSET_001]
- 판정: 취약
- 취약 사유: The rc2 unnecessary-service summary identified an enabled risky service.
- 권고 조치: 관련 설정을 K-CII rulepack 및 조직 보안 기준에 맞게 조정하고 변경 후 재점검하십시오.
- 재점검 방법: W-18 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-019 불필요한 IIS 서비스 구동 점검 추가 확인 필요

- 관련 항목: W-19
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-19 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-020 NetBIOS 바인딩 서비스 구동 점검 추가 확인 필요

- 관련 항목: W-20
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-20 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-021 암호화되지 않는 FTP 서비스 비활성화 미흡

- 관련 항목: W-21
- 영향도: 상
- 대상: [ASSET_001]
- 판정: 취약
- 취약 사유: FTP service appeared enabled and requires encrypted-service review.
- 권고 조치: 관련 설정을 K-CII rulepack 및 조직 보안 기준에 맞게 조정하고 변경 후 재점검하십시오.
- 재점검 방법: W-21 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-022 FTP 디렉토리 접근권한 설정 추가 확인 필요

- 관련 항목: W-22
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-22 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-023 공유 서비스에 대한 익명 접근 제한 설정 추가 확인 필요

- 관련 항목: W-23
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-23 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-024 FTP 접근 제어 설정 추가 확인 필요

- 관련 항목: W-24
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-24 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-025 DNS Zone Transfer 설정 추가 확인 필요

- 관련 항목: W-25
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-25 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-026 RDS(Remote Data Services)제거 추가 확인 필요

- 관련 항목: W-26
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-26 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-027 최신 Windows OS Build 버전 적용 추가 확인 필요

- 관련 항목: W-27
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-27 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-028 터미널 서비스 암호화 수준 설정 추가 확인 필요

- 관련 항목: W-28
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-28 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-029 불필요한 SNMP 서비스 구동 점검 미흡

- 관련 항목: W-29
- 영향도: 상
- 대상: [ASSET_001]
- 판정: 취약
- 취약 사유: SNMP service appeared enabled and requires service-necessity review.
- 권고 조치: 관련 설정을 K-CII rulepack 및 조직 보안 기준에 맞게 조정하고 변경 후 재점검하십시오.
- 재점검 방법: W-29 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-030 SNMP Community String 복잡성 설정 추가 확인 필요

- 관련 항목: W-30
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-30 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-031 SNMP Access control 설정 추가 확인 필요

- 관련 항목: W-31
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-31 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-032 DNS 서비스 구동 점검 추가 확인 필요

- 관련 항목: W-32
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-32 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-033 HTTP/FTP/SMTP 배너 차단 추가 확인 필요

- 관련 항목: W-33
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-33 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-034 Telnet 서비스 비활성화 추가 확인 필요

- 관련 항목: W-34
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 필수 evidence 필드가 없습니다: telnet_service_disabled
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-34 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-035 불필요한 ODBC/OLE-DB 데이터 소스와 드라이브 제거 추가 확인 필요

- 관련 항목: W-35
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-35 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-036 원격터미널 접속 타임아웃 설정 추가 확인 필요

- 관련 항목: W-36
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-36 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-037 예약된 작업에 의심스러운 명령이 등록되어 있는지 점검 추가 확인 필요

- 관련 항목: W-37
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-37 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-038 주기적 보안 패치 및 벤더 권고사항 적용 추가 확인 필요

- 관련 항목: W-38
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-38 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-039 백신 프로그램 업데이트 추가 확인 필요

- 관련 항목: W-39
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-39 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-040 정책에 따른 시스템 로깅 설정 미흡

- 관련 항목: W-40
- 영향도: 상
- 대상: [ASSET_001]
- 판정: 취약
- 취약 사유: One or more core audit policy categories were missing success or failure auditing in the sanitized summary.
- 권고 조치: 관련 설정을 K-CII rulepack 및 조직 보안 기준에 맞게 조정하고 변경 후 재점검하십시오.
- 재점검 방법: W-40 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-041 NTP 및 시각 동기화 설정 추가 확인 필요

- 관련 항목: W-41
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-41 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-042 이벤트 로그 관리 설정 미흡

- 관련 항목: W-42
- 영향도: 상
- 대상: [ASSET_001]
- 판정: 취약
- 취약 사유: Event Log service or minimum log-size summary did not meet the rc2 check.
- 권고 조치: 관련 설정을 K-CII rulepack 및 조직 보안 기준에 맞게 조정하고 변경 후 재점검하십시오.
- 재점검 방법: W-42 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-043 이벤트 로그 파일 접근 통제 설정 추가 확인 필요

- 관련 항목: W-43
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-43 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-044 원격으로 액세스할 수 있는 레지스트리 경로 추가 확인 필요

- 관련 항목: W-44
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-44 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-045 백신 프로그램 설치 추가 확인 필요

- 관련 항목: W-45
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-45 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-046 SAM 파일 접근 통제 설정 추가 확인 필요

- 관련 항목: W-46
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-46 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-047 화면보호기 설정 추가 확인 필요

- 관련 항목: W-47
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-47 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-048 로그온하지 않고 시스템 종료 허용 추가 확인 필요

- 관련 항목: W-48
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-48 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-049 원격 시스템에서 강제로 시스템 종료 추가 확인 필요

- 관련 항목: W-49
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-49 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-050 보안 감사를 로그할 수 없는 경우 즉시 시스템 종료 추가 확인 필요

- 관련 항목: W-50
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-50 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-051 SAM 계정과 공유의 익명 열거 허용 안 함 추가 확인 필요

- 관련 항목: W-51
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-51 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-052 Autologon 기능 제어 추가 확인 필요

- 관련 항목: W-52
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-52 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-053 이동식 미디어 포맷 및 꺼내기 허용 추가 확인 필요

- 관련 항목: W-53
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-53 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-054 Dos공격 방어 레지스트리 설정 추가 확인 필요

- 관련 항목: W-54
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-54 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-055 사용자가 프린터 드라이버를 설치할 수 없게 함 추가 확인 필요

- 관련 항목: W-55
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-55 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-056 SMB 세션 중단 관리 설정 추가 확인 필요

- 관련 항목: W-56
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-56 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-057 로그온 시 경고 메시지 설정 추가 확인 필요

- 관련 항목: W-57
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-57 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-058 사용자별 홈 디렉터리 권한 설정 추가 확인 필요

- 관련 항목: W-58
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-58 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-059 LAN Manager 인증 수준 추가 확인 필요

- 관련 항목: W-59
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-59 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-060 보안 채널 데이터 디지털 암호화 또는 서명 추가 확인 필요

- 관련 항목: W-60
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-60 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-061 파일 및 디렉토리 보호 추가 확인 필요

- 관련 항목: W-61
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-61 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-062 시작프로그램 목록 분석 추가 확인 필요

- 관련 항목: W-62
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-62 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-063 도메인 컨트롤러-사용자의 시간 동기화 추가 확인 필요

- 관련 항목: W-63
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 공식 Windows Server 항목은 등록되어 있으나 Windows MVP parser에서 자동 판정하지 않습니다.
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-63 evidence를 다시 수집해 rulepack 판정을 재실행합니다.

### ADV-064 윈도우 방화벽 설정 추가 확인 필요

- 관련 항목: W-64
- 영향도: 중
- 대상: [ASSET_001]
- 판정: 수동확인
- 취약 사유: 필수 evidence 필드가 없습니다: firewall_enabled
- 권고 조치: 담당자 확인, 추가 증적, 대체 통제 여부를 수집한 뒤 수동 판정을 완료하십시오.
- 재점검 방법: W-64 evidence를 다시 수집해 rulepack 판정을 재실행합니다.



## 조치 권고

취약 및 수동확인 항목은 보안 권고문에 따라 조치 또는 추가 확인을 진행합니다.

## 부록

원본 증적은 보고서에 포함하지 않고 `raw_evidence_hash` 기반으로 참조합니다.