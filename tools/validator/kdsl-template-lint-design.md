# KDSL Template Lint Design v1.1-sync

目的: KDSL_PROMPTのtemplate参照・instance項目・権限・停止条件の欠落/衝突を機械検査する。

status: design-draft-main-v1.1-sync
implementation: not_started
source_templates:

```text
templates/base/kdsl_base_dev.md
templates/result/r1_result_spec.md
templates/tasks/*.md
```

## Input

```text
KDSL_PROMPT text
optional: template index
optional: expected available templates
optional: repo/branch/head context
```

## Template reference check

ERROR:

```text
use: template名 があるが該当templateが存在しない
template_unreadable→停止 の条件がない
unknown template/alias/preset推測禁止 がない
template参照のみで読了扱禁止 がない
```

WARN:

```text
use: なしだが共通安全契約が不足
base/task/resultのいずれかが欠けている
```

## Required instance fields check

base template使用時の必須項目:

```text
Phase
目的
repo/path/branch/HEAD条件
対象Slice
非対象
変更対象
AUTHORITY
禁止
停止条件
検証
R1/KDSL_RESULT要求
```

docs_state_closeout template使用時の必須項目:

```text
PHASE
STATUS_TO_RECORD
REPO
BRANCH
HEAD_REQUIRED
RUNTIME_BASIS
TARGET_STATE_DOCS
MUST_RECORD
NOT_OBSERVED
UNVERIFIED
COMMIT_MESSAGE
AUTHORITY
```

corrective_impl template使用時の必須項目:

```text
PHASE
OBSERVED_PROBLEM
EXPECTED_BEHAVIOR
REPO
BRANCH
HEAD_REQUIRED
TARGET_SLICE
NON_TARGET
KNOWN_GOOD
KNOWN_BAD
STOP_CONDITIONS
VERIFY_REQUIRED
AUTHORITY
```

investigation_only template使用時の必須項目:

```text
PHASE
QUESTION
REPO_OR_MATERIAL
TARGET_SCOPE
NON_TARGET
KNOWN_OBSERVATIONS
STOP_CONDITIONS
```

ERROR:

```text
必須instance field欠落
HEAD_REQUIRED欠落 in repo task
TARGET_SLICE/TARGET_STATE_DOCS欠落 in edit task
AUTHORITY欠落 in edit/stage/commit task
RUNTIME_BASIS欠落なのにRT:v要求
```

## Authority conflict check

ERROR:

```text
AUTHORITY.commit=propose_only なのに作業手順にgit commitあり
AUTHORITY.commit=forbid なのにCOMMIT_MESSAGEが実行前提
AUTHORITY.push=forbid なのにpush/update_ref手順あり
AUTHORITY.release=forbid なのにrelease/tag/assets操作あり
edit=forbid なのに変更対象あり
stage=forbid なのにstage手順あり
public_repo=forbid なのにpublic repo操作あり
```

WARN:

```text
commit権限が曖昧
push/releaseが未記載
public_repo権限が未記載
```

## Safety gate check

ERROR:

```text
D禁止がない
未確認→確認済扱禁止がない
未実行→実行済扱禁止がない
Runtime未確認→確認済扱禁止がない
build/diff/lint/test pass != RT:v がない
NEXT実行許可扱禁止がない
COMMIT自動commit許可扱禁止がない
KDSL-DP直接実行禁止が必要箇所で欠落
P1/P1L正規化必須が必要箇所で欠落
```

WARN:

```text
保護語はあるが対象/動作が曖昧
禁止だけで停止条件がない
停止条件だけで禁止がない
```

## Evidence check

ERROR:

```text
NOT_OBSERVED項目がMUST_RECORDで確認済み扱い
UNVERIFIED項目がRT:v根拠扱い
RUNTIME_BASIS.invalid_basisにあるものをRT:v basisに使用
```

WARN:

```text
OBSERVED/NOT_OBSERVED/UNVERIFIEDの分離なし
RUNTIME_BASISが自然文のみで検査困難
```

## Target slice check

ERROR:

```text
target外変更を許可している
対象Sliceなしで編集許可
非対象が空なのに広域task
```

WARN:

```text
targetが自然文のみ
targetとnon_targetの境界が曖昧
```

## R1 requirement check

ERROR:

```text
KDSL_RESULT skeletonなし
CMD/VERIFY/RT/RISK/NEXT/COMMITのいずれか欠落
未実行cmd記載禁止がない
未実行verify pass扱禁止がない
RT:v条件がない
NEXT/COMMIT権限混同禁止がない
```

WARN:

```text
EVIDENCE/AUTHORITY推奨blockなし
COMMIT actual/proposed分離なし
```

## Output

```text
TEMPLATE_LINT_RESULT:
STATUS: pass|warn|fail
ERRORS:
WARNINGS:
INFO:
MISSING_FIELDS:
AUTHORITY_CONFLICTS:
SAFETY_GATE_GAPS:
SUGGESTED_FIX:
```

## Non-goals

```text
template内容の完全展開実装
自然言語の完全意味解析
実行許可判断
U承認代行
Runtime確認代行
```
