# CP-Lift Boundary Example

status: v2-draft example
canonical: no
scope: KDSL-CP to KDSL-Packet boundary

## 1. KDSL-CP is enough

```text
KDSL-CP漢:
役: 小説編集者/批評者
目: novel材→多角review+改善提案
材: novel_text
出: 総評/魅力/弱点/改善案
守: 材外設定追加禁止, 不→断定禁止
確: 本文根拠あり, 抽象論のみ禁止
```

Judgment:

```text
KDSL-CP可
理由:
  実装なし
  repo操作なし
  runtime確認なし
  release/tag操作なし
  R1検収不要
```

## 2. CP-Lift required

```text
KDSL-CP:
Role: 開発支援
Goal: QuickAccessDialogのTab順を修正
Input: repo path / target file / observed UI bug
Output: 修正内容と検証結果
Guard: 未確認→断定禁止, 広域修正禁止
```

Judgment:

```text
KDSL-CP単体禁止
理由:
  実装/改修を含む
  repo/path/fileを含む
  検証/実機確認が必要
  AI coding toolへ渡す可能性あり

必要:
  KDSL-Packet または Full KDSLへ昇格
```

## 3. Lifted packet sketch

```text
KDSL_PROMPT:
PKT:v1
BASE:<registered-base-id>
TASK:<registered-task-id>
SRC:{repo:<repo>,branch:<branch>,clean:req}
READ:[state/docs]
TGT:<target>
OBS:[observed_issue]
GOAL:[specific_fix_goal]
NON:[global_rewrite,rollback,public,release]
STOP:[dirty,branch_mismatch,D含,cause_unknown_wide]
FLOW:PF>RS>IN>HY>MP>BD>R1C
VERIFY:B,G; RT:u
OUT:R1C
```

Notes:

```text
unknown BASE/TASK/FLOW推測禁止
未読参照→読了扱禁止
build/test pass != RT:v
```
