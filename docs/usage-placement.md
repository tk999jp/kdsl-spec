# KDSL Usage Placement Guide

```text
状態:=operational guide
正本性:=Core補助
目的:=KDSLと外部AI coding層の責務重複防止
Core変更:=なし
```

## 基本

```text
KDSL:=現在Taskの意味／判断分岐／明示制約を高密度化する層
KDSL!=Agent framework
KDSL!=repo常設instruction
KDSL!=procedure registry
KDSL!=deterministic policy engine
KDSL!=tool protocol
KDSL!=長期Spec管理
```

KDSLは単体LLMへ直接投入可能であることを維持する。Agent／Skill／Hook／MCP／SDDをKDSL成立条件にしない。

## 配置

| 情報／処理 | 推奨配置 | KDSLとの関係 |
|---|---|---|
| 現在Taskの目的／成功条件／判断分岐／明示制約 | `KDSL_PROMPT` | 主対象 |
| repo全体で常時有効な規則 | `AGENTS.md`等 | 常設側へ置き、Taskごとに再掲しない |
| path／component固有の常設規則 | path-scoped instruction | 対象pathで必要時適用 |
| 反復可能なprocedure／専門作業 | Skill | KDSLから必要時利用 |
| 決定論的検査／遮断／format強制 | Hook／script | 自然言語判断へ戻さない |
| 外部tool／data access | MCP等 | transport/tool層 |
| 独立探索／大量分業／context分離 | Agent／subagent | 必要時のみ |
| 長期要件／設計artifact | Spec／SDD | KDSLへ全文複製しない |
| Agent run状態 | K1 | Task意味と分離 |
| 厳密handoff／中断再開 | P1L／PF1 | 条件付き |
| 作業結果 | R1／KDSL_RESULT | 簡潔一時報告 |

## 選択規則

```text
現在Task意味?→KDSL
repo常時不変?→AGENTS等
反復procedure?→Skill
決定論条件?→Hook/script
外部tool/data?→MCP等
独立探索／並列化利益?→Agent/subagent
長期仕様?→Spec/SDD
```

同一意味を複数層へ全文複製しない。

## KDSL＋Agent

既定:

```text
U要求→KDSL_PROMPT→単体LLM実行可
```

Agent利用価値がある場合:

```text
U要求
→KDSL_PROMPT
→orchestrator
→局所Task
→必要Agent
→統合／検証
```

Agent利用候補:

```text
独立探索あり
複数領域を分離可能
大量context分離利益あり
並列化利益あり
専門role分離利益あり
```

次だけを理由にAgentを必須化しない。

```text
AI codingである
Taskが長文である
安全性を上げたい
Agent機能が利用可能
```

単体高性能LLMで十分なTaskに不要なorchestrationを追加しない。

## KDSL＋AGENTS.md

```text
AGENTS.md:=repo常設契約
KDSL_PROMPT:=今回Task契約
```

例:

```text
AGENTS.md:
- build/test標準command
- repo共通編集規則
- 常時禁止操作

KDSL_PROMPT:
- 今回目的
- 今回対象
- 今回保持条件
- 今回作業／検証
```

Task固有値をAGENTSへ移して比較・再利用性を壊さない。常設規則を毎回KDSLへ複製しない。

## KDSL＋Skill

```text
Skill:=再利用procedure
KDSL:=今回procedureへ渡す目的／条件／値
```

Skill内部procedureをKDSL Core syntaxへ吸収しない。SkillがなくてもKDSL自体はLLM直投入可能とする。

## KDSL＋Hook/script

次は自然言語より決定論処理を優先する。

```text
format check
lint
固定command実行
禁止path検査
機械判定可能なthreshold
再現可能なartifact検査
```

KDSLはHookの代替ではない。Hookで確定できる事実を長い禁止文へ変換しない。

## KDSL＋Spec/SDD

長期仕様全文をKDSLへ複製しない。

```text
Spec:=長期正本
KDSL:=今回Taskに必要な部分を意味保持して圧縮
```

正本競合時は、KDSL自身が正本を変更したことにはしない。上位契約の優先関係は既存Core／profileに従う。

## 非推奨

```text
KDSL CoreへAgent orchestration syntax追加
AGENTS全文をKDSLへ毎回複製
Skill procedure全文をTask promptへ展開
Hookで可能な検査を自然文gate化
MCP/tool schemaをKDSL syntax化
Spec Kit等workflow全体をKDSLへ吸収
利用可能な全層を常時併用
```

## 運用原則

```text
必要最小層
責務一意
意味重複最小
KDSL単独成立維持
問題実測→必要箇所だけ改修
```

Pilot根拠は`docs/reviews/kdsl-eval-pilot-01.md`。Pilotは方向性確認であり、全環境への一般保証ではない。
