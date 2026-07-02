# kcii-netlab-sim

`kcii-netlab-sim`은 네트워크 장비 에뮬레이터가 아니라 parser와 rulepack 테스트를 위한 command-response simulator입니다.

운영 장비에 접속하지 않고, 벤더별 `show` 명령 출력 형태를 재현해 `kcii-audit-suite`의 network profile을 검증하는 용도입니다. 실제 라우팅 동작, 패킷 포워딩, 라이선스 이미지 실행은 Containerlab/FRR, GNS3, EVE-NG, Cisco CML 같은 별도 랩에서 검증합니다.

## 실행 예시

```powershell
$env:PYTHONPATH="tools\kcii-netlab-sim\src"
python -m kcii_netlab_sim --vendor cisco_ios --scenario vulnerable --commands scripts\targets\network\cisco_ios\show_commands.txt --output out\cisco_ios_vulnerable.txt
```

지원 시나리오:

- `good`
- `vulnerable`
- `mixed`

지원 벤더:

- `cisco_ios`

## 민감정보 원칙

- 실제 고객사 config, 장비 이미지, 라이선스 파일을 저장하지 않습니다.
- hostname, IP, username, SNMP community, serial은 비식별 placeholder만 사용합니다.
- simulator 출력은 parser 테스트 입력입니다. audit 결과물에는 전체 config 원문을 저장하지 않아야 합니다.

GNS3, CML, 또는 승인된 랩 출력과 대조할 때도 원문을 저장하지 말고 `docs/NETWORK_OUTPUT_SANITIZATION.md` 기준으로 비식별화한 fixture만 사용합니다.
