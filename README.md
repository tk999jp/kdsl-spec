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
R1C: kdsl-r1c@0.1-draft / v2-draft adopted serialization profile
R1C validator: first heuristic slice integrated
R1C independent canonical/stable status: no
Packet schema: kdsl-packet@0.1-draft / v2-draft adopted / non-executable
Packet BASE/TASK/FLOW registries: v2-draft adopted
Packet validator: first heuristic slice integrated
Packet normalization contract: kdsl-packet-normalization@0.1-draft / v2-draft adopted / non-executable
Packet normalization validator/mapper: first-slice integrated / non-executable preview only
validator sample suite: 93 expectations / failed 0
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
- CompactPrompt / Lexicon / Safety Gate / R1C の責務分離
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
  spec/registry/kdsl-packet-base-registry.md
  spec/registry/kdsl-packet-task-registry.md
  spec/registry/kdsl-packet-flow-registry.md

Packet:
  spec/packet/kdsl-packet-schema.md
  spec/packet/kdsl-packet-normalization-contract.md

R1 / KDSL_RESULT:
  spec/r1/r1-result-spec.md
  spec/r1/r1c-compact-result-schema.md

Lint:
  spec/lint/kdsl-lint-checklist.md
  spec/lint/kdsl-compact-prompt-lint.md
  spec/lint/kdsl-safety-gate-registry-lint.md
  spec/lint/kdsl-r1c-lint.md
  spec/lint/kdsl-packet-lint.md
  spec/lint/kdsl-packet-normalization-lint.md

Bridge:
  spec/bridge/kdsl-adps-bridge.md
  spec/bridge/kdsl-cp-packet-bridge.md

Examples:
  examples/compact-prompt/*
  examples/safety-gates/dev-prompt-safety-gates.example.md
  examples/r1c/*
  examples/packet/*
  examples/midfd/*
  examples/public/*

Validator:
  tools/validator/README.md
  tools/validator/kdsl_validate.py
  tools/validator/kdsl_compact_prompt.py
  tools/validator/kdsl_safety_gate.py
  tools/validator/kdsl_r1c.py
  tools/validator/kdsl_packet.py
  tools/validator/kdsl_packet_normalization.py
  tools/validator/kdsl_packet_normalize.py
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
KDSL-Packet:=kdsl-packet@0.1-draft authoring envelope / v2-draft adopted / non-executable
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

Boundary:

```text
構造aliasはKEY位置のみ
禁止/未確認/未実行/承認待/断定禁止等の保護語弱化禁止
実装/repo/runtime/public操作を含む→CP-Lift必須
current lift target:=Full KDSL profile:dev-prompt
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

## R1C compact-result serialization profile

Current v2-draft serialization profile:

```text
schema: kdsl-r1c@0.1-draft
status: v2-draft adopted serialization profile
canonical parent: spec/r1/r1-result-spec.md
independent canonical spec: no
stable: no
envelope: KDSL_RESULT
```

Selected model:

```text
canonical 11 required field names保持
structured values:=JSON-compatible inline arrays/objects
short field aliases:=未定義/禁止
required field省略禁止
implicit defaults禁止
Full R1へのround-trip必須
round-trip不成立→Full R1 fallback
```

Required R1C order:

```text
KDSL_RESULT
SCHEMA
STATUS
PHASE
S
FILES
WHY
CMD
VERIFY
RT
RISK
NEXT
COMMIT
```

Critical boundaries:

```text
canonical R1 > R1C v2-draft serialization profile
RT:v=対象環境runtime確認済のみ
build/diff/lint/test/CI pass != RT:v
NEXT.authority:=proposal_only
NEXT実行許可扱禁止
COMMIT.proposed != commit authority
COMMIT自動commit許可扱禁止
path/command exact strings保持
R1C validator pass != canonical/stable promotion
```

R1C examples:

```text
examples/r1c/r1c-success.example.md
examples/r1c/r1c-blocked.example.md
examples/r1c/r1c-needs-user.example.md
```

## CP-Lift / Packet boundary

```text
KDSL-CP単体実装指示禁止
KDSL-Packet未正規化→実行指示扱禁止
PKT:v1使用禁止
unknown BASE/TASK/FLOW/SG/R1C推測禁止
```

Current adopted Packet components:

```text
schema: kdsl-packet@0.1-draft
BASE: kdsl-packet-base@0.1-draft
TASK: kdsl-packet-task@0.1-draft
FLOW: kdsl-packet-flow@0.1-draft
lint: spec/lint/kdsl-packet-lint.md
normalization: kdsl-packet-normalization@0.1-draft
normalization lint: spec/lint/kdsl-packet-normalization-lint.md
status: non-executable
```

Current unresolved execution dependencies:

```text
Packet validator/sample matrix
normalization transformer/round-trip proof
Safety Gate completeness/inheritance proof
stable/canonical execution dependency
explicit executable promotion review/U承認
```

```text
Registry/lint adoption != Packet executable
Safety Gate Registry/validator実装 != Packet executable
R1C adoption/validator実装 != Packet executable
```

## Validator helpers

Current validator helpers are experimental and heuristic.

Targets:

```text
python tools/validator/kdsl_validate.py --target r1 <file>
python tools/validator/kdsl_validate.py --target prompt <file>
python tools/validator/kdsl_validate.py --target compact <file>
python tools/validator/kdsl_validate.py --target safety-gate <file>
python tools/validator/kdsl_validate.py --target r1c <file>
python tools/validator/kdsl_validate.py --target packet <file>
python tools/validator/kdsl_validate.py --target normalization <file>
python tools/validator/kdsl_packet_normalize.py <packet-file>
python tools/validator/kdsl_validate.py --target all <file>
```

Current sample runner:

```text
python tools/validator/run_samples.py
```

Latest CI evidence:

```text
sample expectations: 69
failed: 0
workflow: .github/workflows/validator.yml
latest Packet PR: #14
latest Packet run: #116 / success
```

Repository examples included:

```text
examples/safety-gates/dev-prompt-safety-gates.example.md
examples/r1c/r1c-success.example.md
examples/r1c/r1c-blocked.example.md
examples/r1c/r1c-needs-user.example.md
examples/packet/packet-design.example.md
```

Validator boundaries:

```text
validator未実行→pass扱禁止
validator pass != RT:v
validator pass != U承認
validator pass != 実装妥当性保証
validator pass != semantic equivalence
validator pass != safety proof
validator pass != execution authority
validator pass != release readiness
validator pass != canonical/stable promotion
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
full YAML/JSON/KDSL parserなし
full natural-language semantic parserなし
full negation parserなし
protected wording semantic equivalence lintなし
Safety Gate parent-child inheritance lintなし
Safety Gate aggregate state lintなし
R1C multi-line JSON lintなし
R1C round-trip semantic proofなし
Packet validator first slice:=main integrated / 69 expectations verified
Packet full YAML/semantic parserなし
Packet normalization validator/mapper first slice:=main integrated / 93 expectations verified
Packet normalization round-trip/property proofなし
Packet Safety Gate completeness/inheritance proofなし
KDSL-Packet:=v2-draft adopted / non-executable
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
- R1Cはcanonical R1を置換しない
- Examples / Templates / Design docs は正本扱いしない
- public履歴 / 公開済tag / Release Assets を保護する

## Next candidates

```text
P0:
  normalization round-trip/property tests

P1:
  Safety Gate protected wording/inheritance validator拡張

P2:
  R1C round-trip/property-based validator検討

P3:
  public-facing v2 overview
  CI required check / branch protection検討

Hold:
  v1.1.0 stable release
  tag/release/Release Assets操作
```
