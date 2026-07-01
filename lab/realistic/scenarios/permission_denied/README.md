# permission_denied

목적: 권한 부족이나 명령 실행 제한을 프로그램 실패가 아니라 evidence 상태로 기록하는지 검증합니다.

예상 결과:

- collector 또는 sample input에 `permission_denied` 계열 상태 포함
- evaluator는 필요한 경우 `수동확인`으로 분류
- CLI는 전체 실행을 중단하지 않음
