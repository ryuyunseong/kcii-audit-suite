# Linux Server lab

Linux Server 테스트는 Docker 컨테이너와 VM을 모두 사용합니다.

Docker가 적합한 항목:

- 파일 존재 여부
- SSH 설정 파일 fixture
- 패스워드 정책 파일 fixture
- parser와 report 산출 검증

VM이 필요한 항목:

- systemd 서비스 상태
- PAM 동작
- auditd 설정
- 실제 권한 부족/명령 제한 상황

대상 Linux Server에서 실행:

```sh
sh ./scripts/targets/linux_server/collect.sh --pretty > linux-result.json
```

Windows 작업 PC에서 분석:

```powershell
kcii-audit classify-file --profile linux --input lab\realistic\transfer\inbox\linux-result.json --output lab\realistic\transfer\out\linux
```

현재 MVP 항목:

- root SSH 접속 제한
- UID 0 계정 수 요약
- 패스워드 최소 길이
- 패스워드 만료 정책
- `/etc/passwd` 권한
- `/etc/shadow` 권한
- SSH PasswordAuthentication 설정
- 로그 설정 확인 가능 여부

주의:

- 스크립트는 read-only 동작만 수행합니다.
- `/etc/shadow` 본문을 읽거나 저장하지 않습니다.
- 계정명 전체 목록, hostname, domain, 내부 IP는 결과물에 직접 저장하지 않습니다.
