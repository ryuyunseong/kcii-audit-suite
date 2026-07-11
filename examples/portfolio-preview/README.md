# 포트폴리오 결과 미리보기

이 디렉터리는 `kcii-audit-suite v1.4.1`이 합성 Windows Server 증적을 판정해 생성한 실제 결과 예시입니다. 실제 고객, 운영 서버 또는 상용 장비의 정보는 사용하지 않았습니다.

## 재현 명령

```powershell
kcii-audit classify-file `
  --profile windows `
  --input tests\fixtures\windows_server\vulnerable.json `
  --asset-id portfolio-windows-synthetic `
  --output examples\portfolio-preview\generated
```

## 판정 요약

| 판정 | 건수 | 해석 |
| --- | ---: | --- |
| 취약 | 7 | 합성 증적이 rulepack의 취약 조건과 일치 |
| 수동확인 | 57 | 추가 증적, 운영정책 또는 대체통제 확인 필요 |
| 전체 | 64 | Windows Server `W-01`~`W-64` 전체 항목 유지 |

`MANUAL_REQUIRED`는 실패가 아닙니다. 근거가 부족한 항목을 양호로 오판하지 않고 진단자 확인으로 연결한 결과입니다.

## 취약 판정 예시

| 항목 | 항목명 | 결과 요약 |
| --- | --- | --- |
| `W-09` | 비밀번호 관리정책 설정 | 합성 비밀번호 정책이 점검 기준을 충족하지 않음 |
| `W-17` | 하드디스크 기본 공유 제거 | 기본 관리 공유가 존재하는 합성 요약 |
| `W-40` | 정책에 따른 시스템 로깅 설정 | 핵심 감사 정책 설정이 부족한 합성 요약 |

## Excel 핵심 내용 미리보기

### `detail.xlsx`

| 시트 | 주요 내용 |
| --- | --- |
| `02_종합통계` | 수동확인 57건, 취약 7건 |
| `04_상세결과` | 64개 항목의 자산, 항목명, 판정과 근거 |
| `05_취약점목록` | 취약 7건과 조치방안 |
| `06_수동확인` | 수동확인 57건과 추가 확인 사유 |
| `09_보안권고문` | 취약·수동확인 항목별 영향, 권고조치와 재점검 방법 |

### `summary.xlsx`

| 시트 | 판정 | 건수 |
| --- | --- | ---: |
| `종합통계` | 수동확인 | 57 |
| `종합통계` | 취약 | 7 |
| `분야별통계` | Windows 수동확인 | 57 |
| `분야별통계` | Windows 취약 | 7 |

## 생성 산출물

1. [evidence.jsonl](generated/evidence.jsonl): 정규화된 증적과 원본 증적 해시
2. [results.json](generated/results.json): 64개 항목의 구조화된 판정 결과
3. [detail.xlsx](generated/detail.xlsx): 상세결과, 취약점, 수동확인과 권고문 시트
4. [summary.xlsx](generated/summary.xlsx): 종합통계, 분야별통계와 권고문통계
5. [report.md](generated/report.md): 사람이 읽을 수 있는 종합 결과 보고서
6. [security_advisory.md](generated/security_advisory.md): 취약·수동확인 보안 권고문
7. [security_advisory.xlsx](generated/security_advisory.xlsx): 권고문 Excel 목록

입력과 공개 안전 경계는 [INPUT_AND_SANITIZATION.md](INPUT_AND_SANITIZATION.md)를 참고하십시오.
