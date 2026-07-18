# KDSL Spec Manifest — Kanji Core + Agent Layer

## 参照順位

```text
1. U明示指示
2. spec/core/kdsl-spec.md
3. spec/core/kdsl-core.md
4. spec/core/kdsl-modes.md
5. profile／Agent／R1／lint／bridge正本
6. templates／examples
7. tools／validator
8. docs／review
```

## 正本地図

| Path | 責務 |
|---|---|
| `spec/core/kdsl-spec.md` | KDSL identity／第一目的／全体定義 |
| `spec/core/kdsl-core.md` | 演算子／圧縮文型／保護語／変換禁止 |
| `spec/core/kdsl-modes.md` | 圧縮強度／限定安全 |
| `spec/profiles/kdsl-profile-dev-prompt.md` | Codex向け漢字dev-prompt／Agent使用条件 |
| `spec/profiles/kdsl-profile-compact-prompt.md` | 一般LLM／Project向け短縮prompt |
| `spec/profiles/kdsl-converter-prompt.md` | 変換契約 |
| `spec/profiles/kdsl-profile-intl.md` | 非漢字派生subset |
| `spec/agent/kdsl-agent-execution.md` | P1L／P1／K1／PF1最小Agent契約 |
| `spec/r1/r1-result-spec.md` | 簡潔結果報告 |
| `spec/lint/kdsl-lint-checklist.md` | identity／圧縮／過剰安全lint |
| `spec/lint/kdsl-agent-lint.md` | Agent契約lint |
| `spec/bridge/kdsl-adps-bridge.md` | KDSL／Agent／R1境界 |
| `spec/glossary.md` | 用語 |

## 所有

```text
漢字identity:=spec/core/kdsl-spec.md
演算子:=spec/core/kdsl-core.md
mode／safety:=spec/core/kdsl-modes.md
Codex運用:=spec/profiles/kdsl-profile-dev-prompt.md
Agent契約:=spec/agent/kdsl-agent-execution.md
CompactPrompt:=spec/profiles/kdsl-profile-compact-prompt.md
Intl境界:=spec/profiles/kdsl-profile-intl.md
R1:=spec/r1/r1-result-spec.md
```

下位fileが上位正本と競合する場合、上位を優先する。

```text
KDSL Core > Agent層 > profile／R1 > lint／bridge > template／example／tool
```

## 非正本

```text
templates
examples
tools／validator
docs／reviews
archive branch
```

validator pass・CI pass・実装量・Phase完了記録を正本化根拠にしない。

## Agent層

```text
P1L:=agent実行契約長形式
P1:=P1L可逆短縮
K1:=agent run状態
PF1:=project既定
```

Agent層使用条件:

```text
repo書込／複数step実装／再帰完走／複数tool／中断再開
→必須
```

通常会話・単発回答・変換のみでは省略可。

Agent層v1非依存:

```text
Safety Gate Registry
R1C
Packet／Normalization
共通AST／semantic parser
Binding Evidence
runtime evaluator
```

## 旧v2資産

```text
旧Safety Gate Registry／R1C／Packet／Normalization／semantic parser／重P1 schema／旧K1／旧PF1／Binding Evidence
:= archive/kdsl-framework-20260718の回収候補
:= 現Agent層の正本ではない
```

旧P1／K1系統をそのまま復帰せず、agent駆動に必要な機能核だけを `kdsl-agent@1` として再定義した。

採否記録は `docs/reviews/kdsl-v2-asset-audit.md` を参照する。

## 変更分類

breaking:

```text
漢字圧縮を第一目的から外す
漢字をoptional化
英語KEYを既定化
KDSL-Intlを本体化
安全契機を主目的化
Agent層をKDSL Coreより上位化
P1L／P1権限railを暗黙化
K1完了条件を弱化
```

compatible:

```text
圧縮例追加
明示保護語追加
Agent lint追加
PF1項目追加
```

patch:

```text
説明修正
誤記修正
example追加
```
