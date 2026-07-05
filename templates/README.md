# Templates

KDSL / R1 の再利用可能なprompt template置き場。

このディレクトリは、Core仕様ではなく実運用向けの部品管理を目的とする。

status: draft-main-v1.1-sync

## 想定構成

```text
templates/
  base/
    kdsl_base_dev.md
  tasks/
    task_docs_state_closeout.md
    task_corrective_impl.md
    task_investigation_only.md
  result/
    r1_result_spec.md
```

## 位置づけ

```text
Template:=共通契約/定型手順/報告形式を再利用するための部品
Template != Core正本
Template != 実行許可
Template参照 != 読了
```

## 運用規則

```text
template_unreadable→停止
unknown template/alias/preset推測禁止
template参照のみで読了扱禁止
D禁止/RT:v/NEXT/COMMIT等の保護語弱化禁止
template展開不能→作業禁止またはU確認
template衝突→safety/禁止/停止条件優先
```

## AI coding toolへ渡す場合

必須:

```text
使用template名を明記
template本文を読ませる
template未読時の停止条件を明記
instance側でPhase/HEAD/target/evidence/authorityを明記
```

禁止:

```text
use: template名 だけで実行指示扱い
未読templateを過去文脈から推測
templateのcommit/push権限をinstanceへ自動継承
KDSL-DPをtemplate経由で実装指示扱いにしない
```

## 推奨template分類

```text
base: 共通安全契約
accountability: actor/authority責務
result: R1/KDSL_RESULT
stable_task: 実運用済みtask template
experimental_task: 検証中task template
```

注意:

```text
テンプレートはKDSL本文を短くするためのものだが、未読時に意味が消えるため、AI coding toolへ渡す場合は読込必須条件を明記する。
```
