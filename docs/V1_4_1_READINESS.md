# v1.4.1 릴리스 준비 기록

## 목적

`v1.4.1`은 한글 리소스 손상 복구, 한글 질의서 호환성, 전 프로파일 end-to-end 산출물 계약을 고정하는 patch release입니다.

## 버전·태그 경계

- Package version metadata: `1.4.1`
- 기준 브랜치: `codex/v1.4.1-korean-localization`
- 새 태그: `v1.4.1`
- 기존 `v1.4.0` tag remains fixed at `178369b`
- `v1.4.0` Release asset은 교체하지 않습니다.
- GitHub 저장소는 PUBLIC을 유지합니다.
- PyPI/TestPyPI에는 배포하지 않습니다.

## 필수 검증

```powershell
python -m pytest tests\test_release_readiness.py
python -m pytest tests\test_end_to_end_support_matrix.py
python -m pytest
python -m build
git diff --check
```

현재 검증 결과:

- 전체 테스트: `189 passed`
- release-readiness 및 end-to-end acceptance: `22 passed`

## End-to-End 대상

- Windows fixture → 64개 결과, 7개 산출물
- Linux fixture → 8개 결과, 7개 산출물
- Unix AIX fixture → 67개 결과, 7개 산출물
- PostgreSQL/MySQL/MariaDB fixture → 각각 26개 결과, 7개 산출물
- Cisco IOS/Junos fixture → 각각 38개 결과, 7개 산출물
- Security Appliance fixture → 23개 결과, 7개 산출물
- 한글 질의서 export/import와 legacy 영어 헤더 import
- `--no-advisory` → 5개 산출물

## 한글·리소스 검증

- Runtime YAML, Markdown, JSON과 Excel에서 손상된 한글 표식 0건
- root rulepack과 package resource SHA-256 일치
- root questionnaire YAML/Excel과 package resource 일치
- CLI 기본·classify-file·questionnaire 도움말 한글 표시

## 민감정보·금지 경로 검증

- high-confidence secret pattern 0건
- 실제 고객 증적과 장비 설정 0건
- `out/`, `raw/`, `tmp/`, `dist/`, `.env`, `.venv/`, `.pytest_cache/` 커밋 제외
- Release asset은 wheel, sdist, checksum 3개로 제한

## Build·설치 검증

- wheel: `dist/kcii_audit_suite-1.4.1-py3-none-any.whl`
- sdist: `dist/kcii_audit_suite-1.4.1.tar.gz`
- checksum: `dist/SHA256SUMS.txt`
- 저장소 밖 clean venv에 wheel 설치
- 설치된 wheel만으로 Windows, DBMS, Network와 questionnaire export smoke 수행

## 릴리스 조건

1. 전체 테스트와 end-to-end acceptance test가 통과해야 합니다.
2. PR을 main에 병합한 커밋을 annotated tag `v1.4.1`로 고정합니다.
3. GitHub Release는 final release로 생성하며 prerelease로 표시하지 않습니다.
4. Release asset을 다시 다운로드해 wheel·sdist checksum을 대조합니다.
