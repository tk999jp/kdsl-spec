# R1 Validator MVP Implementation Notes

status: implementation-notes-draft
implementation: not_started
scope: r1-required-block-check-first

## 1. Purpose

This note defines the smallest safe implementation step for the R1 validator.

The first implementation slice should only check whether a text contains the required `KDSL_RESULT` skeleton fields. It must not claim runtime verification, user approval, or implementation validity.

## 2. First slice

```text
Phase: validator-mvp-r1-required-blocks
scope:
  - read one Markdown/text file
  - check required KDSL_RESULT fields
  - print VALIDATION_RESULT
  - return nonzero exit when required fields are missing
non_scope:
  - RT:v basis validation
  - NEXT/COMMIT authority validation
  - template expansion
  - GitHub Actions
  - release/public workflow
```

## 3. Required fields

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

## 4. Output contract

```text
VALIDATION_RESULT:
STATUS: pass|fail
ERRORS:
WARNINGS:
INFO:
```

## 5. Safety constraints

```text
validator未実行→pass扱禁止
validator pass != RT:v
validator pass != U承認
validator pass != 実装妥当性保証
validator failure時→該当箇所を修正またはU確認
```

## 6. Follow-up slices

```text
Slice 2: RT:v invalid basis keyword check
Slice 3: NEXT/COMMIT basic authority confusion check
Slice 4: template lint minimum check
```

## 7. Stop conditions

```text
validator passを承認扱いする文面が入る→停止
RT:v代替に見える→停止
D禁止解除に見える→停止
release/public前提になる→停止
```
