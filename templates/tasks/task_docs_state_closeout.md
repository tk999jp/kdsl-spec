# Task Template: Docs/State Closeout v0.1-draft

目的: 実装済みPhaseを、確認済み根拠に基づき state/docs のみでcloseoutするためのtask template。

status: template-draft
requires:

```text
templates/base/kdsl_base_dev.md
templates/result/r1_result_spec.md
```

## Intent

```text
action: docs_state_closeout
code_change: forbid
purpose: Phase状態をstate/docsへ正確に反映し、closeoutまたはpending整理する
```

## Required instance fields

```text
PHASE:
STATUS_TO_RECORD:
REPO:
BRANCH:
HEAD_REQUIRED:
RUNTIME_BASIS:
TARGET_STATE_DOCS:
MUST_RECORD:
NOT_OBSERVED:
UNVERIFIED:
COMMIT_MESSAGE:
AUTHORITY:
```

## Default target slice

instance側で明示する。MidFD系の標準候補:

```text
.codex/state/current_focus.md
.codex/state/open_questions.md
.codex/state/phase_backlog.md
.codex/state/decision_log.md
Docs/07_change_log_for_ai.md
```

## Scope

```text
allow:
  - TARGET_STATE_DOCSの編集
  - TARGET_STATE_DOCSの個別stage

deny:
  - code変更
  - target外docs変更
  - public repo操作
  - release/tag/assets操作
  - rollback/revert
  - data schema変更
  - public API変更
```

## AUTHORITY default

```text
read: allow
edit: target_only
stage: target_only
commit: propose_only
push: forbid
release: forbid
```

commitを実行してよい場合はinstance側で明示する。

```text
commit: allow_once
```

## Stop conditions

```text
HEAD_REQUIRED不一致→停止
branch不一致→停止
target外変更必要→停止
code変更必要→停止
RUNTIME_BASIS不確実→RT:v記録禁止/停止
未観測事項を確認済み扱いしないとcloseout不能→停止
rollback/revert/reimplementation必要→停止
U承認が必要な方針変更含→停止/承認待
```

## Required records

MUST_RECORDには次を含める。

```text
何をcloseoutするか
根拠は何か
何が観測されたか
何が未観測か
何が未確認か
RT:vなら根拠は対象環境runtime確認またはU実機観測であること
```

## Verification

標準検証:

```text
git status -sb
git diff --check
git diff --stat
git diff --name-status
rg <phase/evidence keywords> .codex Docs
```

禁止:

```text
未実行verifyをpass扱禁止
build/diff/lint/test passをRT:v扱禁止
```

## R1 requirements

```text
KDSL_RESULT必須
FILESには変更したstate/docsのみ記録
CMDには実行cmdのみ記録
VERIFYには実行verifyのみ記録
RTにはruntime statusとbasisを明記
EVIDENCEでOBSERVED/NOT_OBSERVED/UNVERIFIEDを分離
AUTHORITYでcommit/push/releaseを分離
NEXTは提案のみ
COMMITはactual/proposedを分離
```
