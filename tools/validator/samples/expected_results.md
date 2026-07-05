# R1 Required Blocks Sample Expected Results

status: sample-expectation-draft
script: tools/validator/r1_required_blocks.py

## sample_r1_ok.md

Command:

```text
python tools/validator/r1_required_blocks.py tools/validator/samples/sample_r1_ok.md
```

Expected:

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

Expected exit code:

```text
0
```

## sample_r1_missing_block.md

Command:

```text
python tools/validator/r1_required_blocks.py tools/validator/samples/sample_r1_missing_block.md
```

Expected:

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

Expected exit code:

```text
2
```
