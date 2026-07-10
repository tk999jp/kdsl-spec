# kdsl-spec

KDSL / R1 specification repository.

KDSL（安全gate保持型prompt記法）と R1 Result Specification（AI作業結果の証跡・検収仕様）を管理するexperimental preview repositoryです。

## Current status

```text
status: v1.1.0-rc1 experimental preview published
repository_visibility: public
release: v1.1.0-rc1
release_type: prerelease / experimental preview
public_ready: no
stable_release: none
Release Assets: none
license: MIT
validator: experimental heuristic lint helpers / partial implementation
validator_authority: non_authoritative
```

状態正本:

```text
docs/project-status.md
```

Policy:

```text
v1.1.0-rc1:=experimental historical baseline
v1.1.0 stable:=当面保留
v2-draft設計を優先
既存tag移動禁止
Release Assets操作禁止
stable/public-ready化→別途U明示承認必須
```

## Purpose

KDSL/R1を、単なるprompt圧縮記法ではなく、Human-AI work interface / 作業契約 / 結果証跡として整理します。

```text
意味保持 > safety gate保持 > 判断分岐保持 > 誤実装防止 > 文字数削減
```

Main goals:

- 一般LLM promptの短縮と出力安定
- AI coding tool向けpromptの意味/safety gate保持
- D禁止 / rollback / 未確認 / 未実行 / 承認gate / 実機確認分離の保持
- KDSL_PROMPT / KDSL_RESULT の入出力契約整理
- R1による結果報告の検収可能化
- Profile / Mode / Safety / Lexicon / Envelope の責務分離

## Quick navigation

```text
Project status:
  docs/project-status.md

Overview:
  docs/overview.md

v2 draft direction:
  docs/design/kdsl-v2-direction.md

Core:
  spec/core/kdsl-spec.md
  spec/core/kdsl-core.md
  spec/core/kdsl-modes.md

Manifest / glossary:
  spec/manifest.md
  spec/glossary.md
  spec/glossary-v2-draft.md

Profiles:
  spec/profiles/kdsl-profile-dev-prompt.md
  spec/profiles/kdsl-converter-prompt.md
  spec/profiles/kdsl-profile-compact-prompt.md

Lexicons:
  spec/lexicons/kdsl-lexicon-kanji-v1.md

R1 / KDSL_RESULT:
  spec/r1/r1-result-spec.md

Lint:
  spec/lint/kdsl-lint-checklist.md
  spec/lint/kdsl-compact-prompt-lint.md

Bridge:
  spec/bridge/kdsl-adps-bridge.md
  spec/bridge/kdsl-cp-packet-bridge.md

Templates:
  templates/README.md
  templates/base/kdsl_base_dev.md
  templates/result/r1_result_spec.md
  templates/tasks/*

CompactPrompt examples:
  examples/compact-prompt/README.md
  examples/compact-prompt/blog_meta.kdsl-cp.md
  examples/compact-prompt/blog_meta.kdsl-cp-kanji.md
  examples/compact-prompt/novel_review.kdsl-cp-kanji.md
  examples/compact-prompt/prompt_improver.kdsl-cp.md
  examples/compact-prompt/cp_lift_example.md

AI coding / R1 examples:
  examples/midfd/*
  examples/public/*

Validator helpers:
  tools/validator/README.md
  tools/validator/kdsl_validate.py
  tools/validator/run_samples.py
  tools/validator/*

Public/release planning:
  docs/public-readiness.md
  docs/release/*
  docs/reviews/*
```

## Architecture

KDSL v2 draft uses orthogonal axes.

```text
format:
  KDSL

profile:
  compact-prompt
  dev-prompt
  converter
  lint

mode:
  readable|min|dense|lock

safety:
  normal|lock-critical|lock-all

lexicon:
  standard|kanji-v1

envelope:
  plain|packet-draft|result
```

Named compositions:

```text
KDSL-CP:=profile:compact-prompt

KDSL-CP漢:=profile:compact-prompt + mode:dense + lexicon:kanji-v1

KDSL-Packet:=future packet envelope candidate
  current status: draft-non-executable

KDSL-R1:=result envelope / KDSL_RESULT / Evidence / RT / Authority
```

## Repository structure

```text
spec/
  manifest.md   正本参照関係
  glossary*.md 用語定義
  core/         KDSL Core正本
  profiles/     用途別運用仕様
  lexicons/     宣言済み語彙/alias集合
  r1/           R1 Result Specification
  lint/         KDSL/R1/CompactPrompt lint
  bridge/       KDSL-DP/ADPS/CP-Lift/Packet境界

templates/      再利用部品
experimental/   正本ではない実験案
examples/       正本ではない理解補助
tools/          validator helper
docs/           status/design/review/release planning
```

## Specification levels

```text
Core: operator/保護語/変換禁止/mode/safetyの正本
Profile: 用途別の運用仕様
Lexicon: profile内で使用する宣言済み語彙。Core保護語を上書きしない
R1: AI作業結果の証跡/検収仕様
Lint: 意味/safety gate/構造欠落検査
Bridge: KDSL-DP/ADPS/P1/P1L/CP-Lift/Packet境界
Templates: 実運用向け再利用部品。正本ではない
Examples: 理解補助。正本ではない
Tools: heuristic lint補助。承認/RT:v/release readinessの代替ではない
Design docs: 次期仕様の判断記録。正本ではない
Project status: repository現在状態の運用上の状態正本
```

## CompactPrompt

KDSL-CP is for general LLM prompts, Project files, and standalone instructions.

Required blocks:

```text
Goal / Input / Output / Guard / Check
```

Kanji-v1 required keys:

```text
目 / 材 / 出 / 守 / 確
```

Kanji aliases are structural keys, not permission to reduce protected words.

```text
推奨:
守:
- 入力外事実追加禁止
- 不明→断定禁止
- 推測→推測明記

非推奨:
守:
- 材外実追加禁止
- 不→断定禁止
```

## CP-Lift / Packet boundary

KDSL-CP must lift when implementation or repository operations appear.

```text
CP-Lift triggers:
  実装/改修/削除
  repo/path/branch/commit操作
  file/API/command変更
  rollback/revert
  RT:v/実機確認
  public履歴/tag/Release Assets
  data migration
  正本変更
  AI coding toolへ渡す場合
```

Current lift target:

```text
Full KDSL profile:dev-prompt
```

Future Packet:

```text
KDSL-Packet未正規化→実行指示扱禁止
PKT:v1使用禁止
Packet registry未定義→停止
unknown BASE/TASK/FLOW/SG/R1C推測禁止
```

## Validator helpers

Current validator helpers are experimental and heuristic.

```text
checks:
  required block presence
  RT:v basis wording
  NEXT/COMMIT authority shape
  template reference/expansion evidence

not checks:
  semantic equivalence proof
  runtime execution
  U approval
  release readiness
```

```text
validator pass != RT:v
validator pass != U承認
validator pass != 実装妥当性保証
```

## Operational rules

- Core / R1 / canonical Bridge は慎重に変更する
- Manifest は正本参照関係を示す
- LexiconはCore保護語を上書きしない
- unknown profile / lexicon / alias / preset / template / schema は推測しない
- KDSL-DPはP1/P1Lへ正規化するまで実行指示扱いしない
- KDSL_RESULT NEXTは提案であり実行許可ではない
- KDSL_RESULT COMMITは実行結果または推奨messageであり自動commit許可ではない
- Examples / Templates / Design docs は正本扱いしない
- public履歴 / 公開済tag / Release Assets を保護する

## Next candidates

```text
P0:
  manifest/README/examplesのv2 architecture同期
  CompactPrompt lint運用確認
  kanji-v1 examples review

P1:
  R1C compact schema検討
  Safety Gate registry検討
  Packet registry検討

Hold:
  v1.1.0 stable release
  tag/release/Release Assets操作
```
