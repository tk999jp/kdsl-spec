# Task Template: Corrective Implementation v0.1-draft

目的: 既存Phase内の不具合・未改善点に対して、原因候補を絞った限定補正を行うためのtask template。

status: template-draft
requires:

```text
templates/base/kdsl_base_dev.md
templates/result/r1_result_spec.md
```

## Intent

```text
action: corrective_impl
purpose: 既存要件/既存policy内で、観測済み問題に対して最小Slice補正を行う
```

## Required instance fields

```text
PHASE:
OBSERVED_PROBLEM:
EXPECTED_BEHAVIOR:
REPO:
BRANCH:
HEAD_REQUIRED:
TARGET_SLICE:
NON_TARGET:
KNOWN_GOOD:
KNOWN_BAD:
STOP_CONDITIONS:
VERIFY_REQUIRED:
AUTHORITY:
```

## Scope

```text
allow:
  - TARGET_SLICE内の限定編集
  - 既存policy内の補正
  - 指定verifyの実行

deny:
  - 広域修正
  - 方針変更
  - 要件変更
  - UI契約変更 unless U明示承認
  - data schema変更
  - public API変更
  - rollback/revert unless U明示承認
  - public repo操作
  - release/tag/assets操作
```

## AUTHORITY default

```text
read: allow
edit: target_only
stage: target_only
commit: propose_only
push: forbid
release: forbid
destructive_ops: forbid
```

commit実行を許可する場合はinstance側で明示する。

```text
commit: allow_once
```

## Diagnostic rules

```text
原因未確→広域修正禁止
Runtime NG→現policy内限定補正優先
U観測 > AI推測
既に改善済みの挙動を破壊禁止
変更前に主犯候補/影響範囲/対象Sliceを確認
```

## Stop conditions

```text
HEAD_REQUIRED不一致→停止
target外変更必要→停止
方針変更/要件変更が必要→停止/承認待
rollback/revert/reimplementation必要→停止/承認待
原因不明で広域修正が必要→停止
VERIFY_REQUIRED実行不能→RISKへ記録, success扱注意
public/release/tag/assets操作が必要→停止
```

## Verification

instance側で明示する。

標準候補:

```text
git status -sb
git diff --check
git diff --stat
git diff --name-status
build/test/lint/runtime smoke as applicable
```

制約:

```text
未実行verifyをpass扱禁止
build/test/lint pass != RT:v
Runtime未確認→RT:u|p
```

## R1 requirements

```text
KDSL_RESULT必須
FILESは変更ファイルのみ
WHYは観測/推論を分離
CMD/VERIFYは実行済みのみ
RTは対象環境runtime確認の有無を明記
EVIDENCEでOBSERVED/INFERRED/UNVERIFIEDを分離
AUTHORITYでcommit/push/release権限を分離
NEXTは提案のみ
COMMITはactual/proposedを分離
```
