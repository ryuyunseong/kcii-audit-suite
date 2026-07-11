# 공개 포트폴리오 점검 기록

이 문서는 `kcii-audit-suite`를 채용 포트폴리오 검토 목적으로 공개하기 전에 적용한 범위와 안전 경계를 기록합니다.

## 공개 상태

- 저장소: `ryuyunseong/kcii-audit-suite`
- visibility: PUBLIC
- 기본 브랜치: `main`
- 최신 릴리스: `v1.4.1` (`1a298ff`)
- 최초 기본 제품 완료 기준: `v1.4.0` (`178369b`)
- 전체 테스트: `189 passed`
- 라이선스: All rights reserved / Proprietary
- PyPI/TestPyPI: 미배포

Public visibility is for review, not open-source reuse.

No permission is granted for reuse, redistribution, or derivative works without explicit written permission.

## 공개 전 확인 항목

- README와 `PORTFOLIO.md`에 프로젝트 목적과 한계를 표시했습니다.
- 이 프로젝트가 not an official KISA tool임을 표시했습니다.
- 원격 자동 수집기가 아니며 수동 보안 판단을 대신하지 않는다고 명시했습니다.
- `v1.4.1`과 이전 태그 및 Release asset을 변경하지 않았습니다.
- 실제 고객 증적과 상용 장비 자료를 포함하지 않았습니다.
- secret pattern과 금지 경로 검사를 수행했습니다.
- wheel/sdist/checksum과 clean wheel 설치를 검증했습니다.
- 합성 fixture로 생성한 7개 결과 미리보기를 별도 예제 디렉터리에 공개했습니다.

## 공개 가능한 자료

- Python source와 parser 구조
- YAML rulepack과 manifest
- synthetic·sanitized fixture
- Excel/Markdown report writer
- 보안장비 한글 질의서 양식
- command-response simulator
- synthetic fixture 기반 결과 미리보기
- 테스트, 패키징과 릴리스 검증 문서

## 공개 금지 자료

- 실제 고객 증적, live output와 설정 export
- 장비 이미지와 라이선스 파일
- 실제 IP, hostname, 계정명, 시리얼과 정책명
- 비밀번호, 해시, 토큰, 키와 인증서 본문
- `.env`, `out/`, `raw/`, `tmp/`, `dist/`

## 책임 범위

- KISA 상세가이드는 rulepack 항목과 판정 기준을 구성하기 위한 기준 자료입니다.
- 이 도구는 공식 진단 도구나 법적 적합성 보증 수단이 아닙니다.
- `MANUAL_REQUIRED` 항목은 담당자 인터뷰, 추가 증적과 대체통제 검토가 필요합니다.
- 조직 정책과 운영 예외를 반영한 최종 판정은 진단자가 수행합니다.

## 공개 후 유지 원칙

- 기존 Release tag와 asset을 이동하거나 교체하지 않습니다.
- 실제 고객 자료를 fixture나 문서 예시로 추가하지 않습니다.
- 공개 저장소의 라이선스를 임의로 오픈소스 라이선스로 변경하지 않습니다.
- 새 기능과 버그 수정은 새 브랜치와 새 버전으로 분리합니다.

## 제출 URL

`https://github.com/ryuyunseong/kcii-audit-suite`
