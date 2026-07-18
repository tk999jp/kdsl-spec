# KDSL / Agent Bridge v3.0-minimal

## 境界

```text
KDSL:=LLM直投入可能な漢字圧縮prompt
KDSL-DP:=Agent向けAuthoring形式
P1L:=agent実行契約の正規長形式
P1:=P1Lの可逆短縮
K1:=1回のagent run状態
PF1:=project固有既定
R1／KDSL_RESULT:=結果報告
```

## 使用

```text
通常会話／単発回答／変換のみ→Agent層省略可
repo書込／複数step実装／再帰完走／複数tool／中断再開→Agent層必須
```

```text
KDSL_PROMPT
→KDSL-DP
→P1L
→P1
→PF1適用
→K1初期化
→Codex agent実行
→R1
```

## 保持

```text
KDSL-DP直接実行禁止
KDSL-DP→P1L／P1正規化必須
P1L／P1 valid != 全操作許可
実行許可:=P1L権限rail
K1更新→目的／scope／権限変更禁止
PF1→P1L権限拡張禁止
build／lint／test／CI pass != RT:v
```

## identity境界

```text
Agent層はKDSL Core下位
Agent層→漢字圧縮解除禁止
英語schema必要→KDSL-Intlへ分離
Agent層!=汎用安全framework
```

KDSL本体は漢字圧縮の直投入prompt。Agent層はChatGPT／Codex実行の安定化を担い、KDSLの第一目的を変更しない。

## 除外

Agent層v1は次へ依存しない。

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
