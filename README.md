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
Safety Semantics: kdsl-safety-language@0.1-draft / Phase 2 bounded first slice integrated
Safety Gate multi-generation graph/deep-scope first slice: integrated
R1C: kdsl-r1c@0.1-draft / v2-draft adopted serialization profile
R1C validator: first heuristic slice integrated
R1C deep optional-block validator/round-trip: Phase 3 first slice integrated
R1C independent canonical/stable status: no
Packet schema: kdsl-packet@0.1-draft / v2-draft adopted / non-executable
Packet BASE/TASK/FLOW registries: v2-draft adopted
Packet validator: first heuristic slice integrated
Packet normalization contract: kdsl-packet-normalization@0.1-draft / v2-draft adopted / non-executable
Packet normalization validator/mapper: first-slice integrated / non-executable preview only
Packet normalization structural round-trip: first-slice integrated / selected structural properties only
Packet semantic/property contract: kdsl-packet-property@0.1-draft / Phase 4 strict first slice integrated / non-executable
Common parser/AST: Phase 1 integrated / source-spanned first slice
major parser adapters: R1C / Packet / Packet Normalization / Safety Gate
KDSL Validation unified suite: 257 expectations / failed 0
required check activation: pending / issue #39
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
  spec/registry/kdsl-safety-semantics.md
  spec/registry/kdsl-packet-base-registry.md
  spec/registry/kdsl-packet-task-registry.md
  spec/registry/kdsl-packet-flow-registry.md

Packet:
  spec/packet/kdsl-packet-schema.md
  spec/packet/kdsl-packet-normalization-contract.md
  spec/packet/kdsl-packet-semantic-property-contract.md

R1 / KDSL_RESULT:
  spec/r1/r1-result-spec.md
  spec/r1/r1c-compact-result-schema.md
  spec/r1/r1c-optional-block-contract.md

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
  tools/validator/kdsl_packet_roundtrip.py
  tools/validator/kdsl_packet_semantic.py
  tools/validator/kdsl_packet_normalize_semantic.py
  tools/validator/kdsl_packet_property.py
  tools/validator/kdsl_parser.py
  tools/validator/kdsl_parse.py
  tools/validator/kdsl_parser_adapter.py
  tools/validator/run_all_samples.py
  tools/validator/run_parser_samples.py
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
bounded semantic match != full semantic equivalence
multi-generation graph pass != complete safety proof
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
semantic/property contract: kdsl-packet-property@0.1-draft
semantic/property spec: spec/packet/kdsl-packet-semantic-property-contract.md
status: non-executable
```

Current unresolved execution dependencies:

```text
full Packet/Normalization semantic equivalence proof
complete Safety Gate completeness/inheritance proof across arbitrary documents
canonical P1/P1L target schema
stable/canonical execution dependency
explicit executable transformer specification/review/U承認
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
python tools/validator/kdsl_validate.py --target safety-semantics <file>
python tools/validator/kdsl_safety_gate_graph.py <graph.json>
python tools/validator/kdsl_validate.py --target r1c <file>
python tools/validator/kdsl_r1c_roundtrip.py <file>
python tools/validator/kdsl_validate.py --target packet <file>
python tools/validator/kdsl_validate.py --target packet-semantic <file>
python tools/validator/kdsl_validate.py --target normalization <file>
python tools/validator/kdsl_packet_normalize.py <packet-file>
python tools/validator/kdsl_packet_roundtrip.py <packet-file> [normalization-file]
python tools/validator/kdsl_packet_normalize_semantic.py <packet-file>
python tools/validator/kdsl_packet_property.py <packet-file> [normalization-file]
python tools/validator/kdsl_parse.py --envelope <MARKER> [--json] <file>
python tools/validator/kdsl_validate.py --target all <file>
```

Current unified runner:

```text
python tools/validator/run_all_samples.py

component runners:
  run_samples.py: 108
  run_safety_gate_samples.py: 14
  run_r1c_roundtrip_samples.py: 14
  run_parser_samples.py: 11
  run_safety_semantics_samples.py: 32
  run_safety_semantics_examples.py: 2
  run_r1c_optional_samples.py: 34
  run_packet_semantic_property_samples.py: 42
```

Latest CI evidence:

```text
pull_request: 48
source_head: ea982099bd5b99862191e0792e15cd501c4cc4f4
squash_commit: 47b15f9af3496dc36e14673cf0a681e3c333b098
workflow/check: KDSL Validation + Packet Semantic Property
workflow_run: #224 / success
unified expectations: 257
failed: 0
required-check repository setting: pending / issue #39
```

Repository examples included:

```text
examples/safety-gates/dev-prompt-safety-gates.example.md
examples/safety-gates/bounded-semantics.example.md
examples/safety-gates/multigeneration/graph.json
examples/r1c/r1c-success.example.md
examples/r1c/r1c-blocked.example.md
examples/r1c/r1c-needs-user.example.md
examples/packet/packet-design.example.md
examples/packet/packet-semantic-property.example.md
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
common source-spanned parser/AST first slice:=main integrated
full YAML/KDSL semantic parserなし
bounded Safety Semantics first slice:=main integrated
full natural-language semantic parserなし
full negation/exception reasoningなし
protected wording full semantic equivalence proofなし
Safety Gate multi-generation DAG/deep-scope first slice:=integrated; arbitrary graph/full scope proof未実装
R1C multiline JSON input:=common parser adapter integrated
R1C deep optional-block structural round-trip:=Phase 3 integrated
R1C round-trip full semantic proofなし
Packet validator first slice:=main integrated / 69 expectations verified
Packet strict bounded semantic/property first slice:=Phase 4 integrated / 42 expectations / 257 unified verified
Packet full YAML/natural-language semantic equivalence proofなし
Packet normalization validator/mapper first slice:=main integrated / 93 expectations verified
Packet normalization structural round-trip first slice:=main integrated / 108 expectations verified
Packet selected semantic/property comparison:=Phase 4 integrated
Packet complete Safety Gate completeness/inheritance proofなし
required KDSL Validation check:=workflow ready / repository setting pending issue #39
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
  required KDSL Validation check activation / issue #39

P1:
  Phase 5 public-facing v2 hardening / release-readiness review

Hold:
  v1.1.0 stable release
  tag/release/Release Assets操作
```
