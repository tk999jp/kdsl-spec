# KDSL Packet FLOW Registry v0.1 Draft Candidate

status: v2-draft adopted
canonical: v2-draft
registry: kdsl-packet-flow
version: 0.1-draft
executable_effect: none

## 1. Purpose

This candidate defines semantic flow opcodes for a future KDSL-Packet.

```text
FLOW opcode:=ordered work-state transition label
FLOW opcode != command
FLOW opcode != authority
FLOW opcode != success evidence
```

Exact commands, paths, APIs, branches, tags, and file names remain explicit payload strings.

## 2. Current boundary

```text
registry: kdsl-packet-flow@0.1-draft
status: design-candidate
adopted: no
stable/public-ready: no
Packet executable effect: none
unknown FLOW opcode推測禁止
one-character opcode未定義
```

## 3. Step record

Candidate step shape:

```yaml
- op: FLOW-READ
  detail: "inspect exact source files"
  input: []
  output: []
```

Required:

```text
op
detail
```

Optional:

```text
input
output
condition
gate_refs
stop_on
```

Restrictions:

```text
empty detail禁止
command/path/API変換禁止
opcodeのみでoperation details省略禁止
unknown field/default推測禁止
```

## 4. Candidate opcodes

### FLOW-READ

Purpose:

```text
source/reference/stateを読む
```

Rules:

```text
read target exact
未読を読取済扱禁止
read authority必要時AUTHORITY整合
```

### FLOW-ANALYZE

Purpose:

```text
observed evidenceから原因/差分/影響/選択肢を整理
```

Rules:

```text
observed/inferred分離
原因未確→断定禁止
analysis結果 != approval
```

### FLOW-GATE

Purpose:

```text
Safety Gate/Authority/STOP/normalization前提を評価
```

Rules:

```text
applicable gate欠落禁止
hold/blocked→FLOW-CHANGE進行禁止
state:satisfied != unrelated authority
```

### FLOW-DECIDE

Purpose:

```text
承認済み方針または非破壊的判断分岐を選択
```

Rules:

```text
D禁止対象→U明示承認必須
未承認方針を既定扱禁止
decision evidence保持
```

### FLOW-CHANGE

Purpose:

```text
exact TGT内でstate/file/code/config/docsを変更
```

Rules:

```text
TASK-CHANGE/TASK-PUBLIC/TASK-DATA等の対応class必須
SG-SCOPE/SG-EVIDENCE/SG-AUTHORITY/SG-STOP最低限必須
edit authority exact
TGT外変更禁止
unexpected diff→stop
```

Non-substitutes:

```text
FLOW-CHANGE存在 != edit permission
edit permission != stage/commit/push permission
```

### FLOW-VERIFY

Purpose:

```text
required checksを実行または未実行として分類
```

Rules:

```text
実行結果はR1/R1C evidenceへ記録
未実行をpass扱禁止
build/diff/lint/test/CI pass != RT:v
runtime claim→SG-RUNTIME必要
```

### FLOW-REPORT

Purpose:

```text
R1またはR1C contractで結果/証跡/risk/nextを報告
```

Rules:

```text
OUT result schema整合
NEXT:=proposal_only
COMMIT.proposed != commit authority
未確認/未実行を成功扱禁止
```

### FLOW-STOP

Purpose:

```text
stop condition発火を記録し、関連change flowを停止
```

Rules:

```text
reason/evidence必須
停止後の実行済扱禁止
解除条件推測禁止
```

### FLOW-ASK

Purpose:

```text
必要なU判断/承認/不足入力を要求
```

Rules:

```text
質問対象/選択肢/影響明示
ASK発行 != approval
回答未取得→関連gate hold
```

## 5. Candidate sequencing

Typical non-change flow:

```text
FLOW-READ→FLOW-ANALYZE→FLOW-GATE→FLOW-REPORT
```

Typical change flow:

```text
FLOW-READ→FLOW-ANALYZE→FLOW-GATE→FLOW-DECIDE?→FLOW-CHANGE→FLOW-VERIFY→FLOW-REPORT
```

Stop/ask branches:

```text
any step→FLOW-STOP
FLOW-GATE|FLOW-DECIDE→FLOW-ASK
FLOW-ASK→hold until response/evidence
```

Rules:

```text
FLOW-CHANGE before FLOW-GATE禁止
FLOW-REPORT before required VERIFY completion/分類禁止
FLOW-STOP後のFLOW-CHANGE禁止
FLOW-ASK未解決でdependent FLOW-CHANGE禁止
```

## 6. Opcode compatibility

```text
new opcode追加→compatible candidate
existing opcode permission meaning追加→禁止
existing opcode safety weakening→breaking/prohibited
one-character alias追加→separate version/lint required
```

## 7. Promotion gate

```text
Packet schema ownership review
TASK-FLOW matrix lint
order/branch/terminal-state tests
exact payload preservation tests
Safety Gate/Authority non-substitution tests
U明示承認
```

## 8. Non-goals

```text
shell command language
programming language control flow
implicit retry loop
background execution
approval automation
runtime success inference
PKT:v1有効化
```
