# kdsl-spec

KDSL（漢字圧縮DSL）、軽量Agent実行層、最小R1結果仕様の正本repository。

## 定義

```text
KDSL:=日本語promptを漢字語幹／記号／最小制御語へ再構成する、LLM直投入可能な漢字圧縮DSL
```

第一目的は漢字圧縮。意味保持・判断分岐・明示制約を維持し、英語KEYや非漢字表現は `KDSL-Intl` 派生subsetとして扱う。

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

安全契機は第一目的ではない。Uが明示した重大条件の意味消失を防ぐ限定保護であり、潜在risk推測による自動増殖を禁止する。

## Agent経路

```text
U自然文
→ChatGPT converter
→KDSL dev-prompt／KDSL-DP
→P1L／P1
→PF1適用
→K1
→Codex agent再帰実行
→R1
→ChatGPT
→U
```

```text
P1L:=agent実行契約長形式
P1:=P1L可逆短縮
K1:=agent run状態
PF1:=project既定
```

repo書込、複数step実装、再帰完走、複数tool、中断再開を含む時はAgent層を使用する。通常会話・単発回答・変換のみでは省略可。

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

## 現在状態

```text
branch: canonical/kdsl-kanji
status: canonical
historical-base: 39a51b71950340b83f6e525dd1a76724530bb0df
framework-archive: archive/kdsl-framework-20260718
v2-asset-audit: complete／Agent再審査反映済
agent-layer: kdsl-agent@1
```

PR #1〜#145と旧Core以降309-pathを機能群単位で監査し、採用／簡略移植／Intl分離／不採用を確定。Agent駆動の実運用要件を再審査し、P1L／P1／K1／PF1の機能核だけを軽量再定義した。詳細は `docs/reviews/kdsl-v2-asset-audit.md`。

旧v2 framework系統は回収元。既存実装量・CI実績・Phase完了記録だけで採用しない。

## 運用原則

```text
英語KEY既定禁止
漢字optional化禁止
安全理由scope／Phase／architecture増殖禁止
Agent層はKDSL Core下位
P1L権限rail明示
K1更新によるscope変更禁止
PF1による権限拡張禁止
KDSL_RESULT成果物化禁止
validator非権威
build／lint／test／CI pass != RT:v
command／path／API名保持
KDSL-DP直接実行禁止
```

## 非採用

Agent層v1は次へ依存しない。

```text
Safety Gate Registry
R1C
Packet／Normalization
共通AST／semantic parser
Binding Evidence
runtime evaluator
```

## 検証

```bash
python tools/validator/kdsl_identity_lint.py
python tools/validator/run_canonical_samples.py
```

GitHub Actions `KDSL Validation`でvalidator compile、identity、canonical regression、Agent contract regressionを実行する。
