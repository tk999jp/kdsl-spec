# KDSL-CP / KDSL-Packet Bridge v0.1-draft

status: v2-draft
scope: CompactPrompt to Packet boundary / lift and summary rules

## 1. Purpose

This bridge defines when a lightweight KDSL-CP prompt must be lifted to KDSL-Packet or Full KDSL, and how a KDSL-Packet can be summarized back to KDSL-CP for human/project-file use.

```text
KDSL-CP:=一般LLM / Project files / 単体prompt向け軽量prompt
KDSL-Packet:=GPT↔Codex / AI coding tool向け作業契約packet
```

KDSL-CP must not become a shortcut for unsafe implementation instructions.

## 2. CP-Lift

CP-Lift converts or escalates KDSL-CP to KDSL-Packet or Full KDSL.

Lift triggers:

```text
実装/改修/削除を含む
repo/path/branch/commit操作を含む
file/path/API/commandの変更を含む
rollback/revertを含む
未push破棄を含む
RT:v/実機確認を含む
public履歴/tag/Release Assetsを含む
data migrationを含む
正本変更を含む
AI coding toolへ渡す場合
```

If any trigger is present:

```text
KDSL-CP単体実装指示禁止
KDSL-Packet または Full KDSLへ昇格
必要safety gateを明示
```

## 3. Mapping: CP to Packet

```text
KDSL-CP Role    → TASK補助 / actor note
KDSL-CP Goal    → GOAL
KDSL-CP Input   → READ / SRC / OBS
KDSL-CP Output  → OUT
KDSL-CP Rules   → FLOW / VERIFY / TASK rules
KDSL-CP Guard   → BASE / SG / STOP
KDSL-CP Style   → human render / response style
KDSL-CP Check   → VERIFY / lint / R1C requirements
```

## 4. Minimum Packet fields after lift

A lifted Packet should contain at least:

```text
KDSL_PROMPT:
PKT:v1
BASE:
TASK:
SRC:
READ:
TGT:
OBS:
GOAL:
NON:
STOP:
FLOW:
VERIFY:
OUT:
```

Unknown BASE/TASK/FLOW/SG schema must not be guessed.

```text
unknown ID→停止
未読参照→読了扱禁止
```

## 5. Packet-Summary

Packet-Summary converts KDSL-Packet to KDSL-CP for human-facing or Project file summaries.

Mapping:

```text
BASE/TASK/SG/FLOW:
  Guard/Rulesへ要約

SRC/READ/OBS/GOAL/NON:
  Input/Goal/Guardへ要約

OUT/R1C:
  Output/Checkへ要約
```

Packet-Summary is not the original execution contract. It is a human-readable summary.

## 6. Summary restrictions

Do not remove or weaken high-risk gates when summarizing.

```text
D禁止削除禁止
RT:v条件削除禁止
NEXT/COMMIT権限分離削除禁止
rollback/revert条件削除禁止
public履歴/公開済tag/Release Assets保護削除禁止
repo安全条件を一般Guardへ丸めすぎること禁止
```

## 7. Boundary examples

### 7.1 KDSL-CP is enough

```text
KDSL-CP:
役: 小説編集者/批評者
目: novel材→多角review+改善提案
材: novel_text
出: 総評/魅力/弱点/改善案
守: 材外設定追加禁止, 不→断定禁止
確: 根拠あり, 抽象論のみ禁止
```

Reason:

```text
repo操作なし
実装なし
R1/RT不要
```

### 7.2 CP-Lift required

```text
KDSL-CP:
Goal: QuickAccessDialogのTab順を修正
Input: repo path / target file / observed UI bug
```

Reason:

```text
実装/改修を含む
file/pathを含む
AI coding toolへ渡す可能性あり
→ KDSL-Packetへ昇格
```

## 8. Non-goals

```text
KDSL-DP/P1/P1L境界変更
R1/KDSL_RESULT意味変更
RT:v条件緩和
KDSL-CPをAI coding tool実装契約として扱うこと
```
