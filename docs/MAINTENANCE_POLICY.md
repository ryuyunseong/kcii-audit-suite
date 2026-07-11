# 유지보수 정책

이 정책은 최초 기본 제품 완료 기준인 `v1.4.0`과 현재 공개 정식 릴리스 `v1.4.1` 이후의 변경에 적용합니다.

## 버전 및 브랜치 정책

- 문서 오탈자, 작은 버그와 회귀 수정: `dev/v1.4.2` 또는 후속 patch 브랜치
- 하위 호환 기능 추가: `dev/v1.5.0` 또는 후속 minor 브랜치
- 공개 정책 검토: `release/public-readiness`

Parser 확장, 원본 증적 보존, 공개 정책과 무관한 문서 정리를 하나의 변경으로 섞지 않습니다.

## 태그와 Release

Published release tags and assets are immutable.

- 기존 태그를 이동하거나 재사용하지 않습니다.
- 공개된 wheel, sdist와 checksum asset을 교체하지 않습니다.
- 수정이 필요하면 새 버전, 새 태그와 새 Release를 만듭니다.
- PyPI/TestPyPI 배포와 저장소 라이선스 변경은 별도 승인이 필요합니다.

## 허용되는 데이터

- synthetic·sanitized fixture
- boolean, integer, enum, count와 warning
- masked identifier
- `raw_evidence_hash`
- 고객 식별이 불가능한 문서 예시

## 금지 데이터

- 실제 고객 증적과 장비 설정 원문
- 운영 DBMS live output
- 계정명, hostname, 도메인, IP, 시리얼과 정책명
- 비밀번호, 해시, 토큰, 키와 인증서 본문
- 장비 이미지, CML/IOS 이미지와 라이선스 파일
- `.env`, `out/`, `raw/`, `tmp/`, `dist/`의 생성 산출물

## 변경 전 검증

```powershell
python -m pytest
git diff --check
```

프로파일 또는 report writer를 변경한 경우 추가로 확인합니다.

- 변경 프로파일의 targeted test
- 기본 7개 산출물 생성
- `--no-advisory` 5개 산출물 생성
- root/package-resource rulepack 동기화
- `???` 손상 문자열 검사
- high-confidence secret pattern 검사
- 금지 경로 추적 여부 검사
- 기존 릴리스 태그 불변 확인

## 판정 정책

- 증적이 충분한 경우에만 `GOOD` 또는 `VULNERABLE`을 반환합니다.
- 미지원·모호·권한 부족·정책 의존 증적은 `MANUAL_REQUIRED`로 유지합니다.
- parser 오류를 숨기거나 양호로 대체하지 않습니다.
- 실제 운영정책과 대체통제는 진단자가 최종 검토합니다.

## 배포 산출물

별도 승인이 없다면 Release asset은 wheel, source distribution과 `SHA256SUMS.txt`로 제한합니다.
