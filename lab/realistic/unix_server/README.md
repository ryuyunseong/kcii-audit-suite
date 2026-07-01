# Unix Server lab

Unix Server lab is a fixture-first verification area for AIX, Solaris, HP-UX, and Linux-compatible Unix outputs. It is not an operational remote collection feature.

## Operational Flow

1. An approved assessor runs the POSIX sh collector on the target Unix server.
2. The collector uses read-only commands and writes sanitized JSON.
3. The result file is moved to the Windows work PC.
4. The Windows work PC runs offline classification.

```sh
sh ./scripts/targets/unix_server/collect.sh > unix-result.json
```

```powershell
kcii-audit classify-file --profile unix --unix aix --input unix-result.json --output out\unix-aix
kcii-audit classify-file --profile unix --unix solaris --input unix-result.json --output out\unix-solaris
kcii-audit classify-file --profile unix --unix hpux --input unix-result.json --output out\unix-hpux
kcii-audit classify-file --profile unix --unix linux --input unix-result.json --output out\unix-linux
```

Paste mode uses the same parser.

```powershell
Get-Content .\unix-result.json | kcii-audit classify-paste --profile unix --unix aix --output out\unix-aix
```

## Verification Limits

AIX, Solaris, and HP-UX command behavior differs by vendor version and is hard to reproduce fully in a local container lab. The first Unix MVP therefore starts with:

- Full `U-01` through `U-67` manifest and rulepack registration.
- AIX/Solaris/HP-UX/Linux fixtures.
- Conservative `MANUAL_REQUIRED` results for OS-specific checks that need local policy or vendor output review.
- Partial automatic decisions only for sanitized boolean/count evidence.

The collector is written for POSIX `sh` compatibility and avoids Bash-only syntax. Do not add commands that modify system configuration. Do not collect `/etc/shadow` contents, password hashes, private keys, certificate bodies, full account lists, hostnames, domains, internal IPs, or raw privilege details.
