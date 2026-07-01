# Windows Server lab

Windows Server 테스트는 Docker가 아니라 VM 기반으로 수행합니다.

권장 흐름:

1. 승인된 Windows Server VM을 준비합니다.
2. 대상 VM에서 다음 스크립트를 read-only로 실행합니다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\targets\windows_server\collect.ps1 -Pretty > windows-result.json
```

3. `windows-result.json`을 Windows 작업 PC의 `lab\realistic\transfer\inbox\`로 복사합니다.
4. Windows 작업 PC에서 분석합니다.

```powershell
kcii-audit classify-file --profile windows --input lab\realistic\transfer\inbox\windows-result.json --output lab\realistic\transfer\out\windows
```

주의사항:

- `ExecutionPolicy Bypass`는 진단용 일회성 실행 예시입니다.
- 운영 고객사 배포용은 스크립트 서명 또는 해시 검증 절차를 적용합니다.
- 실제 고객 데이터가 포함된 결과 파일을 커밋하지 않습니다.
