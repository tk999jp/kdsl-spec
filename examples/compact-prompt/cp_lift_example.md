# CP-Lift Boundary Example

status: v2-draft example
canonical: no
scope: KDSL-CP to Full KDSL / future Packet boundary

## 1. KDSL-CP is enough

```text
KDSL-CP漢:
役: 小説編集者/批評者
目: novel input→多角review+改善提案
材: novel_text
出: 総評/魅力/弱点/改善案
守: 入力外設定追加禁止, 不明→断定禁止
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
Check: 実装/検証/報告条件確認
```

Judgment:

```text
KDSL-CP単体禁止
理由:
  実装/改修を含む
  repo/path/fileを含む
  検証/実機確認が必要
  AI coding toolへ渡す

現行lift先:
  Full KDSL profile:dev-prompt
```

## 3. Current executable lift sketch

```text
KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: lock-critical

目標: QuickAccessDialogのTab順修正
入力: repo/path/file/U観測
必須: repo preflight / state読込 / 原因確認 / 最小修正 / build検証 / KDSL_RESULT報告
禁止: 未確認広域修正 / 即rollback / build passをRT:v扱い
```

Notes:

```text
KDSL_PROMPT先頭固定
D禁止時KDSL_PROMPT出力禁止
build/test pass != RT:v
NEXT:=提案, 実行許可扱禁止
COMMIT自動commit許可扱禁止
```

## 4. Future Packet design only

```text
PACKET_DRAFT:
status: non-executable
schema: undefined
fields: BASE/TASK/SRC/READ/TGT/OBS/GOAL/NON/STOP/FLOW/VERIFY/OUT
```

Reason:

```text
Packet schema未定義
BASE/TASK/FLOW/SG registry未定義
R1C schema未定義
```

Restrictions:

```text
PKT:v1使用禁止
PACKET_DRAFTをAI coding toolへ直接投入禁止
unknown BASE/TASK/FLOW/SG/R1C推測禁止
canonical registry完成後に再評価
```
