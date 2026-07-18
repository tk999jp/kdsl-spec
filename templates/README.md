# Templates

KDSLの漢字圧縮を維持した再利用部品。TemplateはCore正本でも実行許可でもない。

## 構成

```text
templates/
  base/kdsl_base_dev.md
  tasks/task_corrective_impl.md
  tasks/task_investigation_only.md
  tasks/task_docs_state_closeout.md
  result/r1_result_spec.md
```

## 原則

```text
本文:=漢字圧縮
英語構造KEY既定禁止
Template未読→内容推測禁止
instance固有値:=利用時に明示
安全条件自動追加禁止
AUTHORITY registry／Packet依存禁止
```

## 利用

```text
base + task + result
=> 1つのKDSL_PROMPTへ展開
```

参照名だけをAI coding toolへ渡さない。必要なtemplate本文を読ませ、instance側で目的／正本／対象／成功条件／検証を指定する。

## task方針

```text
修正実装:=調査→実装→試験→検証を同一Phaseで完走
調査のみ:=編集せず事実／推定／未確認を分離
Docs closeout:=明示依頼時だけ、対象docs／stateへ結果反映
```

禁止:

```text
内部component別Phase化
closeout自動生成
未依頼hardening
安全理由scope拡張
旧v2英語KEY／Safety Gate Registry／Authority Railの再導入
```
