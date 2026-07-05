# R1 RT Basis Checker Verification

status: verified-local-copy
phase: validator-mvp-r1-rt-basis
script: tools/validator/r1_rt_basis.py
samples:
  - tools/validator/samples/sample_rt_v_valid.md
  - tools/validator/samples/sample_rt_v_invalid_basis.md
  - tools/validator/samples/sample_rt_v_no_basis.md

## Scope

```text
verified: RT field basis wording check
verified: accepted runtime basis returns pass
verified: invalid basis returns fail
verified: missing basis returns fail
not_verified: actual runtime execution
not_verified: log authenticity judgment
not_verified: approval judgment
not_verified: NEXT/COMMIT authority validation
```

## Result: sample_rt_v_valid.md

Observed:

```text
VALIDATION_RESULT:
STATUS: pass
ERRORS:
  - none
WARNINGS:
  - none
INFO:
  - accepted runtime basis: 実機確認済, local runtime verified
```

Exit code:

```text
0
```

## Result: sample_rt_v_invalid_basis.md

Observed:

```text
VALIDATION_RESULT:
STATUS: fail
ERRORS:
  - RT:v has no accepted runtime basis
  - RT:v appears based only on invalid evidence: build pass
WARNINGS:
  - none
INFO:
  - none
```

Exit code:

```text
2
```

## Result: sample_rt_v_no_basis.md

Observed:

```text
VALIDATION_RESULT:
STATUS: fail
ERRORS:
  - RT:v has no accepted runtime basis
WARNINGS:
  - none
INFO:
  - none
```

Exit code:

```text
2
```

## Safety note

```text
validator pass != RT:v
validator pass != U approval
validator pass != implementation validity
This verification only confirms RT basis wording behavior.
```
