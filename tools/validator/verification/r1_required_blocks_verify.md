# R1 Required Blocks Checker Verification

status: verified-local-copy
phase: validator-mvp-r1-required-blocks-verify
script: tools/validator/r1_required_blocks.py
samples:
  - tools/validator/samples/sample_r1_ok.md
  - tools/validator/samples/sample_r1_missing_block.md

## Scope

```text
verified: required KDSL_RESULT field presence check
not_verified: RT:v basis validation
not_verified: NEXT/COMMIT authority validation
not_verified: template expansion
not_verified: GitHub Actions
not_verified: release/public workflow
```

## Method

```text
1. Fetch current main script content.
2. Fetch current main sample files.
3. Recreate the fetched script and samples in a local Python runtime.
4. Run the script against both samples.
5. Compare stdout and exit code with expected results.
```

## Result: sample_r1_ok.md

Command:

```text
python r1_required_blocks.py sample_r1_ok.md
```

Observed:

```text
VALIDATION_RESULT:
STATUS: pass
ERRORS:
  - none
WARNINGS:
  - none
INFO:
  - required block check passed
```

Exit code:

```text
0
```

Judgment:

```text
pass
```

## Result: sample_r1_missing_block.md

Command:

```text
python r1_required_blocks.py sample_r1_missing_block.md
```

Observed:

```text
VALIDATION_RESULT:
STATUS: fail
ERRORS:
  - missing required field: CMD
  - missing required field: VERIFY
  - missing required field: RT
  - missing required field: RISK
  - missing required field: NEXT
  - missing required field: COMMIT
WARNINGS:
  - none
INFO:
  - required block check failed
```

Exit code:

```text
2
```

Judgment:

```text
pass
```

## Safety note

```text
validator pass != RT:v
validator pass != U approval
validator pass != implementation validity
This verification only confirms first-slice required-field behavior.
```
