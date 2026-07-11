# KDSL Validator CI Baseline Review

status: implementation-candidate
review_date: 2026-07-11
branch: agent/kdsl-validator-ci
target: main

## 1. Purpose

Run the repository sample expectation suite automatically before and after integration changes.

```text
command: python tools/validator/run_samples.py
expected: total 23 / failed 0
```

## 2. Workflow

```text
path: .github/workflows/validator.yml
runner: ubuntu-latest
python: 3.11
permissions: contents: read
timeout: 5 minutes
```

Triggers:

```text
pull_request -> main
push -> main
workflow_dispatch
```

Action majors:

```text
actions/checkout@v7
actions/setup-python@v6
```

## 3. Scope

```text
R1 required-block samples
RT:v basis samples
NEXT/COMMIT authority samples
template-reference samples
template-expansion-evidence samples
CompactPrompt standard/kanji-v1 samples
CompactPrompt required-block/restricted-alias/CP-Lift samples
combined wrapper target samples
```

## 4. Safety boundary

```text
CI pass != RT:v
CI pass != U承認
CI pass != semantic equivalence
CI pass != safety proof
CI pass != implementation validity
CI pass != stable/public-ready judgment
CI pass != tag/release/Release Assets permission
```

The workflow has read-only repository contents permission and does not commit, push, create releases, modify tags, or upload Release Assets.

## 5. Merge gate

```text
PR workflow run exists
workflow conclusion: success
sample summary: total 23 / failed 0
PR mergeable
U continuation authorization exists
```

## 6. Explicit non-actions

```text
Core specification changeなし
R1C/SG/Packet registry changeなし
stable化なし
tag操作なし
release操作なし
Release Assets操作なし
```
