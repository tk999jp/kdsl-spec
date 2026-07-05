# R1 Required Blocks Checker Usage

status: implementation-usage-draft
implementation: first_slice_started
script: tools/validator/r1_required_blocks.py

## Scope

```text
check target: KDSL_RESULT required field presence only
input: Markdown/text file or stdin
output: VALIDATION_RESULT
exit code: 0 pass / 2 fail
```

## Required fields

```text
KDSL_RESULT
STATUS
PHASE
S
FILES
WHY
CMD
VERIFY
RT
RISK
NEXT
COMMIT
```

## Example commands

```text
python tools/validator/r1_required_blocks.py tools/validator/samples/sample_r1_ok.md
python tools/validator/r1_required_blocks.py tools/validator/samples/sample_r1_missing_block.md
```

## Non-scope

```text
RT:v basis validation
NEXT/COMMIT authority validation
template expansion
runtime verification
approval judgment
release/public workflow
```

## Safety note

```text
validator pass != RT:v
validator pass != U approval
validator pass != implementation validity
```
