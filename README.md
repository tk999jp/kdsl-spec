# kdsl-spec

KDSL / R1 specification repository.

KDSL（安全gate保持型prompt記法）とR1 Result Specification（AI作業結果の証跡・検収仕様）を管理するexperimental preview repositoryです。

## Current status

```text
repository_visibility: public
published_release: v1.1.0-rc1
release_type: prerelease / experimental preview
public_ready: no
stable_release: none
Release Assets: none
license: MIT

v2 architecture: main integrated
CompactPrompt validator: first slice integrated
Validator CI: integrated
Safety Gate Registry: kdsl-sg@0.1-draft / v2-draft integrated
Safety Gate validator: first heuristic slice integrated
validator sample suite: 34 expectations
validator_authority: non_authoritative
```

状態正本:

```text
docs/project-status.md
```

仕様参照関係:

```text
spec/manifest.md
```

Policy:

```text
v0.1.0-draft tag:=履歴として維持
v1.1.0-rc1:=experimental historical baseline
v1.1.0 stable:=当面保留
v2-draft設計/validator改善:=継続
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
- Safety Gateの参照ID / state / composition整理
- heuristic validatorによる形式・欠落・代表的衝突検査

## Quick navigation

```text
Project status:
  docs/project-status.md

Overview / direction:
  docs/overview.md
  docs/design/kdsl-v2-direction.md

Manifest / glossary:
  spec/manifest.md
  spec/glossary.md
  spec/glossary-v2-draft.md

Core:
  spec/core/kdsl-spec.md
  spec/core/kdsl-core.md
  spec/core/kdsl-modes.md

Profiles:
  spec/profiles/kdsl-profile-dev-prompt.md
  spec/profiles/kdsl-converter-prompt.md
  spec/profiles/kdsl-profile-compact-prompt.md

Lexicons:
  spec/lexicons/kdsl-lexicon-kanji-v1.md

Registries:
  spec/registry/README.md
  spec/registry/kdsl-safety-gate-registry.md
  spec/registry/kdsl-safety-gate-composition.md

R1 / KDSL_RESULT:
  spec/r1/r1-result-spec.md

Lint:
  spec/lint/kdsl-lint-checklist.md
  spec/lint/kdsl-compact-prompt-lint.md
  spec/lint/kdsl-safety-gate-registry-lint.md

Bridge:
  spec/bridge/kdsl-adps-bridge.md
  spec/bridge/kdsl-cp-packet-bridge.md

Examples:
  examples/compact-prompt/*
  examples/safety-gates/dev-prompt-safety-gates.example.md
  examples/midfd/*
  examples/public/*

Validator:
  tools/validator/README.md
  tools/validator/kdsl_validate.py
  tools/validator/kdsl_compact_prompt.py
  tools/validator/kdsl_safety_gate.py
  tools/validator/run_samples.py
  tools/validator/samples/*
  tools/validator/verification/*

Review / release planning:
  docs/reviews/*
  docs/public-readiness.md
  docs/release/*
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
KDSL-R1:=result envelope / KDSL_RESULT / Evidence / RT / Authority
KDSL-Packet:=future packet envelope candidate / draft-non-executable
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
構造aliasはKEY位置のみ
禁止/未確認/未実行/承認待/断定禁止等の保護語弱化禁止
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

Current executable lift target:

```text
Full KDSL profile:dev-prompt
```

Packet boundary:

```text
KDSL-Packet未正規化→実行指示扱禁止
PKT:v1使用禁止
Packet schema/BASE/TASK/FLOW/R1C/Packet lint未定義→停止
unknown BASE/TASK/FLOW/SG/R1C推測禁止
Safety Gate Registry/validator実装 != Packet executable
```

## Safety Gate Registry

Current v2-draft registry:

```text
registry: kdsl-sg@0.1-draft
states: hold|satisfied|blocked|na
```

IDs:

```text
SG-DESIGN
SG-SCOPE
SG-EVIDENCE
SG-RUNTIME
SG-AUTHORITY
SG-ROLLBACK
SG-PUBLIC
SG-DATA
SG-KDSL-DP
SG-STOP
```

Boundary:

```text
Core/R1/Bridge safety meaning > Registry mapping
Registry ID != permission
state:satisfied != unrelated authority
unknown registry/SG ID推測禁止
hold/blocked gate削除禁止
specialized gate != broader gate解除
current Full KDSL:=SG ID + complete protected wording
SG ID-only compression禁止
```

Typed non-substitution:

```text
U承認 != runtime evidence
runtime evidence != commit/push/release authority
CI/validator pass != semantic equivalence
NEXT != execution authority
COMMIT.proposed != commit authority
```

## Validator helpers

Current validator helpers are experimental and heuristic.

Targets:

```text
python tools/validator/kdsl_validate.py --target r1 <file>
python tools/validator/kdsl_validate.py --target prompt <file>
python tools/validator/kdsl_validate.py --target compact <file>
python tools/validator/kdsl_validate.py --target safety-gate <file>
python tools/validator/kdsl_validate.py --target all <file>
```

Safety Gate first slice checks:

```text
known registry / known ID / known state
id/state/scope/reason required fields
state:satisfied evidence/authority
state:blocked evidence warning
state:na reason
dev-prompt baseline gates
representative rollback/data/public/runtime/KDSL-DP composition
```

Sample runner:

```text
python tools/validator/run_samples.py
```

Current CI evidence:

```text
sample expectations: 34
failed: 0
actual Safety Gate repository example: included
workflow: .github/workflows/validator.yml
```

Validator boundaries:

```text
validator pass != RT:v
validator pass != U承認
validator pass != 実装妥当性保証
validator pass != semantic equivalence
validator pass != safety proof
validator pass != execution authority
validator pass != release readiness
CI pass != stable/public-ready判断
```

## Repository structure

```text
spec/          Core/Profile/Lexicon/Registry/R1/Lint/Bridge
examples/      理解補助。正本ではない
templates/     再利用部品。正本ではない
tools/         experimental validator helpers
docs/          status/design/review/release planning
experimental/  正本ではない実験案
```

## Known limitations

```text
full YAML parserなし
full natural-language semantic parserなし
full negation parserなし
protected wording semantic equivalence lintなし
Safety Gate parent-child inheritance lintなし
Safety Gate aggregate state lintなし
R1C schema未定義
Packet schema/BASE/TASK/FLOW registry未定義
Packet lint未定義
KDSL-Packet:=draft-non-executable
```

## Operational rules

- Core / R1 / canonical Bridge は慎重に変更する
- Manifest は正本参照関係を示す
- LexiconはCore保護語を上書きしない
- RegistryはCore/R1/Bridge意味を変更せず、権限を付与しない
- unknown profile / mode / safety / lexicon / alias / schema / registry / ID は推測しない
- KDSL-DPはP1/P1Lへ正規化するまで実行指示扱いしない
- KDSL_RESULT NEXTは提案であり実行許可ではない
- KDSL_RESULT COMMITは実行結果または推奨messageであり自動commit許可ではない
- Examples / Templates / Design docs は正本扱いしない
- public履歴 / 公開済tag / Release Assets を保護する

## Next candidates

```text
P0:
  local mainをorigin/mainへ同期
  34 sample runner再確認

P1:
  R1C compact schema設計

P2:
  Packet BASE/TASK/FLOW registry
  Packet schema/lint

P3:
  Safety Gate protected wording/inheritance validator拡張

P4:
  public-facing v2 overview
  CI required check / branch protection検討

Hold:
  v1.1.0 stable release
  tag/release/Release Assets操作
```
