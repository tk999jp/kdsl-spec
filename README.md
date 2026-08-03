# kdsl-spec

KDSL（漢字圧縮DSL）、軽量Agent実行層、最小R1結果仕様の正本repository。

## 定義

```text
KDSL:=日本語promptを漢字語幹／記号／最小制御語へ再構成する、LLM直投入可能な漢字圧縮DSL
```

```text
KDSL本体:=漢字圧縮
KDSL-Intl:=非漢字言語／ASCII／英語KEY向け互換subset
KDSL本体 > KDSL-Intl
```

## 設計順位

```text
漢字圧縮
> 意味保持
> LLM直投入可能
> 判断分岐保持
> 明示制約保持
> Agent完走
> 出力安定
> 人間修正可能
```

安全契機はU明示重大条件の限定保護。潜在risk推測による自動増殖を禁止する。

## Agent goal

```text
U明示scopeを必要最小契約で調査→実装→検証→完了
```

通常のCodex開発run:

```text
U自然文
→ChatGPT converter
→KDSL_PROMPT＋K1
→Codex再帰実行
→R1
→ChatGPT
→U
```

厳密handoff／中断再開時だけ:

```text
U指示＋PF1
→P1L
→識別付きK1
→Codex再帰実行
```

```text
K1:=標準run状態
P1L:=条件付き厳密契約
P1:=任意短縮／P1Lと併記禁止／可逆性保証なし
PF1:=継続project既定
```

Agent駆動は必須でも、P1L／P1／PF1全量を毎回展開しない。

## 正本

```text
全体定義: spec/core/kdsl-spec.md
記法: spec/core/kdsl-core.md
mode／安全契機: spec/core/kdsl-modes.md
dev-prompt: spec/profiles/kdsl-profile-dev-prompt.md
CompactPrompt: spec/profiles/kdsl-profile-compact-prompt.md
converter: spec/profiles/kdsl-converter-prompt.md
Intl subset: spec/profiles/kdsl-profile-intl.md
Agent契約: spec/agent/kdsl-agent-execution.md
R1: spec/r1/r1-result-spec.md
lint: spec/lint/kdsl-lint-checklist.md
Agent lint: spec/lint/kdsl-agent-lint.md
境界: spec/bridge/kdsl-adps-bridge.md
参照地図: spec/manifest.md
用語: spec/glossary.md
```

## 単独Project投入

```text
prompts/kdsl-converter-standalone.md
```

ChatGPT Project instructions／単独instruction向けに、KDSL identity、Core記法、mode、converter、lintを1fileへ統合したcompiled prompt。正本ではなく配布・投入用であり、正本と競合する場合は `spec/` 配下を優先する。

## 現在状態

```text
branch: main
status: canonical
framework-archive: archive/kdsl-framework-20260718
v2-asset-audit: complete／Agent再審査反映済
agent-layer: kdsl-agent@1.1
standalone-converter: prompts/kdsl-converter-standalone.md／非正本
```

## 運用原則

```text
英語KEY既定禁止
漢字optional化禁止
安全理由scope／Phase／architecture増殖禁止
Agent層はKDSL Core下位
通常Agent:=KDSL_PROMPT＋K1
P1L／PF1:=条件付き
P1:=任意／可逆偽装禁止
K1更新によるscope変更禁止
PF1による権限拡張禁止
KDSL_RESULT成果物化禁止
validator非権威
build／lint／test／CI pass != RT:v
command／path／API名保持
```

## 非採用

```text
Safety Gate Registry
R1C
Packet／Normalization
共通AST／semantic parser
Binding Evidence
runtime evaluator
```

## 圧縮評価

2026-07-20の3分類sampleでは、空白除外Unicode文字数で次を確認した。

```text
min本文: 45.1%削減
min投入全体: 30.5%削減
dense本文: 48.0%削減
dense投入全体: 32.3%削減
概念marker: 21/21 pass
```

`dense`は常に`min`より短いとは限らない。通常既定は`mode:min`とし、実投入量が減る場合またはAI直投入密度を優先する場合だけ`dense`を使用する。marker passは完全な意味同等性や応答品質を証明しない。

## 検証

```bash
python tools/validator/kdsl_identity_lint.py
python tools/validator/kdsl_standalone_lint.py
python tools/validator/kdsl_agent_lint.py examples/kanji/agent-codex-run.kdsl.md
python tools/validator/kdsl_agent_operational_regression.py
python tools/validator/kdsl_run_changed_git_regression.py
python tools/validator/kdsl_compression_evaluation.py
python tools/validator/run_canonical_samples.py
```

GitHub Actions `KDSL Validation`でcompile、identity、standalone compiled prompt、Agent contract、状態遷移、Git repository上のRunChanged帰属、圧縮評価、canonical regressionを実行する。形式／自動回帰passは意味同等性、Codex Agent実効性、RT:v、release readinessを証明しない。
