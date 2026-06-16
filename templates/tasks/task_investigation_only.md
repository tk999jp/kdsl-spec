# Task Template: Investigation Only v0.1-draft

目的: 実装・編集を行わず、共有材料/リポジトリ/ログ/差分を調査して、次の安全な判断材料をR1で返すためのtask template。

status: template-draft
requires:

```text
templates/base/kdsl_base_dev.md
templates/result/r1_result_spec.md
```

## Intent

```text
action: investigation_only
edit: forbid
commit: forbid
push: forbid
purpose: 原因候補/影響範囲/次の安全な一手を整理する
```

## Required instance fields

```text
PHASE:
QUESTION:
REPO_OR_MATERIAL:
TARGET_SCOPE:
NON_TARGET:
KNOWN_OBSERVATIONS:
STOP_CONDITIONS:
```

## Scope

```text
allow:
  - read
  - search
  - inspect
  - summarize
  - propose

deny:
  - file edit
  - code change
  - git add
  - git commit
  - git push
  - public repo操作
  - release/tag/assets操作
  - rollback/revert
  - destructive operation
```

## AUTHORITY default

```text
read: allow
edit: forbid
stage: forbid
commit: forbid
push: forbid
release: forbid
destructive_ops: forbid
```

## Investigation rules

```text
共有材先読必須
共有材判可→AI丸投禁止
検索失敗→不存在断定禁止
原因未確→広域修正禁止
観測/推論/未確認を分離
U観測 > AI推測
```

## Stop conditions

```text
調査範囲外の実装変更が必要→停止
D禁止含む方針変更が必要→承認待
破壊操作が必要→停止
runtime確認が必要だが未実行→RT:u|p
証拠不十分で断定不能→needs_userまたはblocked
```

## Output expectations

```text
観測
原因候補
主犯候補
影響範囲
改善済/未改善
次の安全な一手
未確認点
```

## R1 requirements

```text
KDSL_RESULT必須
STATUSはsuccess/partial/blocked/needs_user/noopから選択
FILESはchanged:noneを明記
CMDは実行cmdのみ
VERIFYは実行した確認のみ
RTは通常naまたはu/p
NEXTは提案のみ
COMMITはnone/proposedのみ, 実行禁止
```
