# Security appliance lab

This lab validates the security appliance questionnaire and sanitized config-summary parser only. It is not a remote collector and does not emulate production firewalls, IPS/IDS, WAF, VPN, Anti-DDoS, FortiGate, PAN-OS, Cisco ASA, or F5 devices.

Primary workflow:

```powershell
kcii-audit questionnaire export --profile security-appliance --output out\security_appliance_questionnaire.xlsx
kcii-audit questionnaire import --profile security-appliance --input out\security_appliance_questionnaire.xlsx --output out\security-appliance-questionnaire
kcii-audit classify-file --profile security-appliance --appliance-type firewall --input lab\realistic\transfer\inbox\security-appliance-summary.txt --output out\security-appliance
```

Operational evidence should be reduced to boolean, enum, count, or warning summaries before classification. Do not store customer names, IP addresses, admin account names, hostnames, domains, policy names, object names, serial numbers, license keys, tokens, certificate bodies, or full config exports in this repository.

보안 장비는 실제 에뮬레이션과 자동 수집이 어려운 경우가 많습니다.

검증 방식:

- config export sample
- 정책/로그/계정 설정 export sample
- Excel questionnaire sample
- parser + rulepack + report 산출 검증

운영 흐름:

1. 장비 담당자가 승인된 방식으로 config 또는 정책 정보를 export합니다.
2. 자동 확인이 어려운 항목은 질의서에 답변합니다.
3. 결과를 Windows 작업 PC로 가져와 parser와 rulepack으로 판정합니다.

상용 장비 이미지, 라이선스 파일, 운영 설정 원문은 저장소에 포함하지 않습니다.
