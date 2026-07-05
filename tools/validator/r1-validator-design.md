# R1 Validator Design v1.1-sync

目的: `KDSL_RESULT` / R1報告を機械検査し、未実行扱い・RT:v誤認・権限混同・証跡欠落を検出する。

status: design-draft-main-v1.1-sync
implementation: not_started
source_spec: spec/r1/r1-result-spec.md
source_lint: spec/lint/kdsl-lint-checklist.md

## Input

```text
KDSL_RESULT blockを含むMarkdown/text
optional: expected PHASE
optional: expected target files
optional: expected authority
optional: expected RT basis
```

## Required block check

ERROR:

```text
KDSL_RESULTがない
STATUSがない
PHASEがない
Sがない
FILESがない
WHYがない
CMDがない
VERIFYがない
RTがない
RISKがない
NEXTがない
COMMITがない
```

WARN:

```text
EVIDENCEがない（runtime/観測/未確認が関係する場合）
AUTHORITYがない（commit/push/releaseが関係する場合）
```

## STATUS check

Allowed:

```text
success
partial
blocked
noop
failed
needs_user
```

ERROR:

```text
unknown STATUS
successなのにRISK/UNVERIFIEDが重大で未説明
blockedなのに停止理由がない
```

## RT check

Allowed:

```text
p
u
v
na
fail
blk
```

ERROR:

```text
RT:v なのに basis がない
RT:v basis が build/diff/lint/test passのみ
RT:v basis がvalidator passのみ
RT:v basis が推測のみ
Runtime未確認なのにRT:v
build pass == RT:v 扱い
diff pass == RT:v 扱い
lint pass == RT:v 扱い
unit test pass == RT:v 扱い
validator pass == RT:v 扱い
```

WARN:

```text
RT:na だがdocs/guidance only理由がない
RT:u|p なのにRISKにruntime_unverified相当がない
```

## CMD / VERIFY check

ERROR:

```text
CMDに推奨cmd/次候補cmdが混入
VERIFYに未実行検証がpassとして記録
VERIFY passのみでCMDが空
```

WARN:

```text
CMDが空だがSTATUS=success
VERIFYが空だがSTATUS=success
```

制約:

```text
validatorは実際にcmd実行済みかを証明できない
R1本文内の自己申告整合性のみ検査する
```

## FILES check

optional expected target files がある場合:

ERROR:

```text
FILES.changedにtarget外ファイルが含まれる
out_of_scopeありなのにRISK未記録
```

WARN:

```text
FILESが自然文のみで検査困難
changed/out_of_scope分離なし
```

## NEXT / COMMIT check

ERROR:

```text
NEXTが実行許可として書かれている
NEXTに承認待なしで次作業実行を要求している
COMMIT.proposedをcommit実行済み扱い
COMMIT.actualがあるのにhash/message不明
COMMITが自動commit許可として書かれている
```

WARN:

```text
COMMIT actual/proposed/permission_basis分離なし
NEXTが曖昧
```

## EVIDENCE check

推奨block:

```text
EVIDENCE:
  OBSERVED:
  INFERRED:
  NOT_OBSERVED:
  UNVERIFIED:
```

ERROR:

```text
NOT_OBSERVED項目をWHY/Sで確認済み扱い
UNVERIFIED項目をRT:v根拠扱い
INFERRED項目をOBSERVED扱い
```

WARN:

```text
観測/推論/未観測/未確認が自然文内で混在
EVIDENCEがないがRISKに未確認あり
```

## AUTHORITY check

推奨block:

```text
AUTHORITY:
  read:
  edit:
  stage:
  commit:
  push:
  release:
```

Allowed values:

```text
allow
forbid
target_only
allow_once
propose_only
not_requested
not_applicable
```

ERROR:

```text
AUTHORITY.commit=propose_only なのにCOMMIT.actualあり
AUTHORITY.commit=forbid なのにCOMMIT.actualあり
AUTHORITY.push=forbid なのにpush/update_ref実行記録あり
AUTHORITY.release=forbid なのにrelease/tag/assets操作記録あり
```

WARN:

```text
commit/push/releaseが関係するがAUTHORITYなし
permission_basisなし
```

## Output

```text
VALIDATION_RESULT:
STATUS: pass|warn|fail
ERRORS:
WARNINGS:
INFO:
BLOCKING:
SUGGESTED_FIX:
```

## Non-goals

```text
実行済みcmdの真偽証明
Runtime確認の代行
U承認の代行
要件判断
D禁止解除
```
