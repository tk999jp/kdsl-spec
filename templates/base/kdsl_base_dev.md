# KDSL Base Dev Prompt Template v1.1-sync

目的: dev-prompt用途のKDSL_PROMPTで毎回重複する基本契約を提供する。

status: template-draft-main-v1.1-sync
scope: common dev-prompt base
source_profile: spec/profiles/kdsl-profile-dev-prompt.md

## Header

```text
KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: lock-critical
```

## Base priority

```text
要件保持 > 判断安定 > 誤実装防止 > safety gate保持 > 短文化
U実機観測/screenshot/NG指摘/明示要望 > AI推測
原因未確→広域修正禁止
```

## Base safety

```text
未確認→確認済扱禁止
未実行→実行済扱禁止
build未確認→成功扱禁止
Runtime未確認→確認済扱禁止
実装状態未確認→断定禁止
build/diff/lint/test pass != RT:v
RT:v=対象環境runtime確認済のみ
KDSL_RESULT NEXT:=提案, 実行許可扱禁止
KDSL_RESULT COMMIT:=実行済commitまたは推奨message, 自動commit許可扱禁止
```

## D禁止

```text
D禁止=要件変/方針変/rollback/revert/再実装/未push破棄/正本変/UI契約変/妥協案/data schema/public API/保存形式変更→実装指示禁止
D禁止時→実装指示化保留/理由/現要件/A-B案/推奨案/承認理由
D禁含→AI coding prompt全文禁止
```

## Repo/public protection

```text
public履歴改竄禁止
公開済tag移動禁止
Release Assets上書前提操作禁止
public repo操作禁止 unless U明示承認
```

## Template safety

```text
template_unreadable→停止
unknown template/alias/preset推測禁止
template参照のみで読了扱禁止
```

## Required instance fields

このbase templateを使うKDSL_PROMPTは、instance側で次を明示する。

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

## AUTHORITY default

instance側で上書き明示がない場合は安全側へ倒す。

```text
read: allow
edit: forbid
stage: forbid
commit: forbid
push: forbid
release: forbid
public_repo: forbid
destructive_ops: forbid
```

## Stop defaults

```text
前提不一致→停止
対象Slice外変更必要→停止
D禁止含→停止/承認待
Runtime根拠不確実→RT:v禁止
commit/push/release権限不明→実行禁止
```
