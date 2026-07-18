# KDSL / Agent Bridge v3.1-minimal

## 境界

```text
KDSL:=LLM直投入可能な漢字圧縮prompt
KDSL-DP:=Agent向けAuthoring形式
K1:=標準agent run状態
P1L:=厳密handoff／中断再開用長形式契約
P1:=任意短縮転送表現
PF1:=継続project既定
R1／KDSL_RESULT:=結果報告
```

## 目的

```text
Agent目的:=U明示scopeを必要最小契約で調査→実装→検証→完了
```

## 正規経路

通常:

```text
KDSL_PROMPT
→K1初期化
→Codex再帰実行
→R1
```

厳密handoff／中断再開:

```text
U指示＋PF1
→P1L生成
→K1識別付き初期化
→Codex再帰実行
→R1
```

短縮転送が必要な場合:

```text
P1LまたはKDSL_PROMPT
→P1
```

P1LとP1を同一promptへ併記しない。

## 保持

```text
KDSL-DP直接実行禁止
K1更新→目的／scope／権限変更禁止
PF1→権限拡張禁止
P1L／P1 valid != 全操作許可
build／lint／test／CI pass != RT:v
形式lint pass != Codex Agent実効性
```

## identity境界

```text
Agent層はKDSL Core下位
Agent層→漢字圧縮解除禁止
英語schema必要→KDSL-Intlへ分離
Agent層!=汎用安全framework
```

## 除外

```text
Safety Gate Registry
R1C
Packet／Normalization
共通AST／semantic parser
Binding Evidence
runtime evaluator
```

## 正本

```text
Agent契約: spec/agent/kdsl-agent-execution.md
Agent lint: spec/lint/kdsl-agent-lint.md
Agent validator: tools/validator/kdsl_agent_lint.py
```