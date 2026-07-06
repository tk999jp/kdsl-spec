# R1 Authority Guard Verification

status: verified-local-copy
phase: validator-r1-authority-guard
script: tools/validator/r1_authority_guard.py
samples:
  - tools/validator/samples/sample_authority_ok.md
  - tools/validator/samples/sample_authority_warn.md
  - tools/validator/samples/sample_authority_fail.md

## Scope

```text
verified: NEXT proposal-only shape returns pass
verified: COMMIT actual/proposed/none shape returns pass
verified: ambiguous NEXT/COMMIT shape returns warn
verified: missing COMMIT returns fail
not_verified: natural language complete semantic parsing
not_verified: approval judgment
not_verified: Git operation judgment
```

## Expected local commands

```text
python tools/validator/r1_authority_guard.py tools/validator/samples/sample_authority_ok.md => exit 0
python tools/validator/r1_authority_guard.py tools/validator/samples/sample_authority_warn.md => exit 1
python tools/validator/r1_authority_guard.py tools/validator/samples/sample_authority_fail.md => exit 2
python tools/validator/kdsl_validate.py --target r1 tools/validator/samples/sample_authority_ok.md => exit 0
```

## Safety note

```text
authority guard pass != U approval
authority guard pass != next-task approval
authority guard pass != commit approval
authority guard pass != RT:v
```
