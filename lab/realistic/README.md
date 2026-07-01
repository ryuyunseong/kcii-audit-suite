# realistic lab

이 디렉터리는 운영 고객사 자동 수집용이 아니라 개발/검증용 랩입니다.

운영 고객사 흐름은 대상 시스템에서 read-only 점검 결과를 만든 뒤 Windows 작업 PC로 가져와 `kcii-audit classify-file` 또는 `classify-paste`로 오프라인 분석하는 방식입니다.

랩 목표:

- parser가 실제형 입력을 안정적으로 정규화하는지 검증
- rulepack이 `양호`, `취약`, `수동확인`을 재현하는지 검증
- Excel/Markdown 산출물이 민감정보 없이 생성되는지 검증
- Docker, VM, Containerlab, GNS3/EVE-NG를 운영 수집이 아닌 개발/테스트 용도로 분리

자세한 설명은 `docs/REALISTIC_LAB.md`를 참고합니다.
