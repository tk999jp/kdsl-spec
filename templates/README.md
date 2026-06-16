# Templates

KDSL / R1 の再利用可能なprompt template置き場。

このディレクトリは、Core仕様ではなく実運用向けの部品管理を目的とする。

想定構成:

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

運用規則:

```text
template_unreadable→停止
unknown template/alias/preset推測禁止
template参照のみで読了扱禁止
D禁止/RT:v/NEXT/COMMIT等の保護語弱化禁止
```

注意:

```text
テンプレートはKDSL本文を短くするためのものだが、未読時に意味が消えるため、AI coding toolへ渡す場合は読込必須条件を明記する。
```
