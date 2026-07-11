# 입력과 비식별화 기준

## 입력 출처

- 입력 파일: `tests/fixtures/windows_server/vulnerable.json`
- 데이터 성격: 테스트 전용 synthetic fixture
- 대상 프로파일: Windows Server
- 자산 식별자: `portfolio-windows-synthetic`

입력 값은 취약 판정과 수동확인 흐름을 재현하기 위해 만든 boolean, integer와 enum 요약입니다. 실제 서버에서 수집한 원문이 아닙니다.

## 공개하지 않는 정보

다음 값은 입력과 생성 산출물에 포함하지 않습니다.

- 실제 고객명, 담당자명과 조직명
- 실제 IP, hostname, domain과 SID
- 실제 계정명, DB명, 접속 문자열과 정책명
- 비밀번호, 해시, token, key와 인증서 본문
- SNMP community, 장비 serial과 license
- 운영 환경의 파일 경로와 설정 원문

## 산출물 경계

- 원본 증적 전문 대신 정규화된 요약과 `raw_evidence_hash`를 사용합니다.
- 보고서 자산 표시는 합성 식별자 또는 `[ASSET_001]`로 제한합니다.
- 근거가 충분하지 않은 항목은 `GOOD`으로 추정하지 않고 `MANUAL_REQUIRED`로 유지합니다.
- 이 예시는 도구의 출력 구조를 보여주기 위한 포트폴리오 자료이며 실제 보안 진단 결과가 아닙니다.
