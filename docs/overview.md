# KDSL Overview

```text
状態:=canonical
KDSL:=日本語prompt向け漢字圧縮DSL
Agent:=明示scope完走用軽量実行層
R1:=短い作業結果報告
```

## 目的

KDSLは自然文promptを次へ再構成する。

```text
自然文
=> 助詞削減
 + 重複統合
 + 漢字語幹化
 + 条件／遷移記号化
 + 最小制御語化
```

第一目的は漢字圧縮。安全契機は、入力で明示された禁止・未確認・rollback等を圧縮時に落とさないための限定保護である。

## 構成

```text
Core:=identity／記法／mode
Profile:=dev-prompt／compact-prompt／converter／Intl
Agent:=KDSL_PROMPT＋K1／条件付きP1L・P1・PF1
R1:=簡潔KDSL_RESULT
Lint:=漢字退行／意味欠落／過剰安全／Agent契約検出
Bridge:=KDSL-DP／Agent／R1境界
Prompt:=単独投入用compiled配布物
Template／Example:=非正本の実用部品
Validator:=非権威的lint／回帰
```

## 非漢字言語

```text
KDSL本体:=漢字圧縮
KDSL-Intl:=非漢字言語向け派生subset
```

英語KEYは無指定の既定にしない。

## 安全契機

保持:

```text
明示禁止
明示未確認／未実行
明示承認待
明示rollback／revert
明示data／public保護
明示RT:v
```

追加禁止:

```text
潜在risk推測
未指定承認gate
安全理由scope／Phase／architecture拡張
未依頼hardening
```

## Agent

```text
目的:=ユーザー明示scopeを必要最小契約で調査→実装→検証→完了
通常:=KDSL_PROMPT＋K1
厳密handoff／中断再開:=PF1参照＋P1L＋識別付きK1
P1:=任意短縮／P1Lと併記禁止／可逆性保証なし
```

Agent層はKDSL Core下位。K1更新で目的／対象／権限を変更しない。

## 使用配置

```text
現在Task意味／判断分岐→KDSL_PROMPT
repo常設規則→AGENTS.md等
反復procedure→Skill
決定論検査→Hook／script
外部tool／data→MCP等
独立探索／大量分業→Agent／subagent
長期仕様→Spec／SDD
```

KDSLはAgent framework／workflow engine／repo常設instructionの代替ではない。単体LLMへ直接投入可能な高密度意味伝達層を維持する。

詳細: `docs/usage-placement.md`

Pilot記録: `docs/reviews/kdsl-eval-pilot-01.md`

## R1

```text
KDSL_RESULT:
状態:
局面:
要約:
変更:
理由:
実行:
検証:
実機:
危険:
次:
commit:
```

R1は成果物ではなく一時報告。build／test／CI passはRT:vではない。

## 単独投入

```text
prompts/kdsl-converter-standalone.md
```

Core／mode／converter／lintを統合した非正本compiled prompt。正本競合時は`spec/`を優先する。

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

validatorは補助であり、意味同等、ユーザー承認、Agent実効性、runtime、release readinessを証明しない。

## 履歴

```text
初期draft: tag v0.1.0-draft
旧framework: archive/kdsl-framework-20260718
初期draft要約: docs/history/v0.1.0-draft.md
旧v2採否: docs/reviews/kdsl-v2-asset-audit.md
```

Safety Gate Registry、R1C、Packet、Normalization、semantic parser、旧重P1／K1／PF1、Binding Evidenceは現行正本ではない。
