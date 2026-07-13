# KDSL / R1 Project Status

status: canonical-project-status
last_updated: 2026-07-13
phase: phase6c-full-r1-compatibility-integrated
repository: tk999jp/kdsl-spec
default_branch: main
tracking_issue: 55

この文書は、`kdsl-spec` repository の現在状態を示す運用上の状態正本です。
仕様正本とfile責務は `spec/manifest.md` を参照します。
詳細なphase証跡は `docs/reviews/*` と各validator implementation notesへ保持します。

## 1. Current public state

```yaml
current_public_state:
  repository_visibility: public
  published_release: v1.1.0-rc1
  release_class: experimental_preview
  release_type: prerelease
  public_ready: no
  stable_release: none
  release_assets: none
  license: MIT
```

```text
public: yes
public-ready: no
stable: no
v0.1.0-draft tag:=履歴として維持
v1.1.0-rc1:=experimental historical baseline
v1.1.0 stable:=保留
既存tag移動禁止
Release Assets操作禁止
stable/public-ready化→別途U明示承認必須
```

## 2. Canonical reference map

```text
operational status: docs/project-status.md
specification map: spec/manifest.md
Core:
  spec/core/kdsl-spec.md
  spec/core/kdsl-core.md
  spec/core/kdsl-modes.md
Profiles:
  spec/profiles/kdsl-profile-dev-prompt.md
  spec/profiles/kdsl-converter-prompt.md
  spec/profiles/kdsl-profile-compact-prompt.md
R1:
  spec/r1/r1-result-spec.md
  spec/r1/r1c-compact-result-schema.md
  spec/r1/r1c-optional-block-contract.md
Lint: spec/lint/*
Bridge: spec/bridge/*
Registry/Packet:
  spec/registry/*
  spec/packet/*
```

```text
Core/Profile/R1/Lint/Bridge canonical指定file:=仕様正本
docs/project-status.md:=運用状態正本
Design/Template/Example/Tool:=補助資料
validator結果:=非権威的heuristic evidence
```

## 3. Architecture

```text
format: KDSL
profile: compact-prompt|dev-prompt|converter|lint
mode: readable|min|dense|lock
safety: normal|lock-critical|lock-all
lexicon: standard|kanji-v1
envelope: plain|packet-draft|result
```

```text
KDSL-CP:=profile:compact-prompt
KDSL-CP漢:=profile:compact-prompt + mode:dense + lexicon:kanji-v1
KDSL-R1:=envelope:result / KDSL_RESULT
KDSL-Packet:=v2-draft authoring envelope / non-executable
rulebook:=v1.1 legacy profile name / 新規使用禁止
```

## 4. Integrated phase summary

```text
Foundation / v2 architecture: integrated
Phase 1 Common parser / unified validation: integrated
Phase 2 Safety Semantics bounded slice: integrated
Phase 3 R1C deep optional-block round-trip: integrated
Phase 4 Packet / Normalization semantic properties: integrated
Phase 5 Public-facing v2 hardening: complete
Phase 6A Semantic Parser Foundation design: integrated
Phase 6B typed parser/AST v2 core: integrated
Phase 6C-1 R1C compatibility view/parity: integrated
Phase 6C-2 R1C checker migration: integrated
Phase 6C-3 CompactPrompt compatibility view/parity: integrated
Phase 6C-4 CompactPrompt checker migration: integrated
Phase 6C-5 Safety Gate compatibility view/parity: integrated
Phase 6C-6 Safety Gate checker migration: integrated
Phase 6C-7 Packet compatibility view/parity: integrated
Phase 6C-8 Packet base checker migration: integrated
Phase 6C-9 Packet Normalization compatibility view/parity: integrated
Phase 6C-10 Packet Normalization checker migration: integrated
Phase 6C-11 Full R1 compatibility view/parity: integrated
```

## 5. Repository enforcement

```yaml
repository_enforcement:
  ruleset_name: Protect main with KDSL Validation
  ruleset_id: 18832171
  enforcement_status: active
  target: default_branch / main
  bypass_list: empty
  require_pull_request_before_merging: true
  required_approvals: 0
  allowed_merge_method: squash
  required_status_check: KDSL Validation
  require_branches_up_to_date: true
  restrict_deletions: true
  block_force_pushes: true
```

```text
verification PR: 53 / closed without merge
activation record PR: 54
activation squash: 9434628aefb966d0b66e9d865a956d961b551ef2
issue #39: closed / completed
required_check_activation: confirmed
workflow success != semantic equivalence/safety proof/RT:v/release readiness
```

## 6. Validator status

```yaml
validator:
  maturity: experimental_heuristic_helpers
  implementation: partial
  authority: non_authoritative
  workflow: .github/workflows/validator.yml
  unified_command: python tools/validator/run_all_samples.py
  unified_runners: 19
  unified_expectations: 344
  failed: 0
  phase1_parser_cases: 11
  phase6b_parser_v2_cases: 12
  r1c_parity_cases: 10
  compact_parity_cases: 12
  compact_migration_cases: 4
  safety_gate_parity_cases: 8
  safety_gate_migration_cases: 4
  packet_parity_cases: 8
  packet_migration_cases: 6
  normalization_parity_cases: 8
  normalization_migration_cases: 7
  full_r1_parity_cases: 8
```

Latest verification:

```text
implementation PR: 79
source head: 1b2cd34bf6623c660f062207fb06ebaa96d2c2b8
squash commit: 191e7315482934fc474022f3a21d02f2457793be
workflow run: 29234411316 / #325 / success
KDSL Validation: success
Packet Semantic Property: success
```

```text
validator未実行→pass扱禁止
validator pass != semantic equivalence
validator pass != complete safety proof
validator pass != U承認
validator pass != RT:v
validator pass != release readiness
```

## 7. Parser/checker migration state

Typed AST core:

```text
tools/validator/kdsl_parser_v2.py
tools/validator/kdsl_parse_v2.py
DocumentNodeV2 / HeaderNode / EnvelopeNodeV2 / FieldNodeV2
SourceSpanV2 / DiagnosticV2
typed scalar/block/JSON/mapping/sequence/record nodes
active-document fence isolation
raw-envelope compatibility contexts
```

Migrated active checker paths:

```text
R1C:
  tools/validator/kdsl_parser_v2_compat.py
  tools/validator/kdsl_r1c.py
CompactPrompt:
  tools/validator/kdsl_parser_v2_compact_compat.py
  tools/validator/kdsl_compact_prompt.py
Safety Gate:
  tools/validator/kdsl_parser_v2_safety_gate_compat.py
  tools/validator/kdsl_safety_gate.py
Packet:
  tools/validator/kdsl_parser_v2_packet_compat.py
  tools/validator/kdsl_packet.py
Packet Normalization:
  tools/validator/kdsl_parser_v2_normalization_compat.py
  tools/validator/kdsl_packet_normalization.py
```

Compatibility pilot without checker switch:

```text
Full R1:
  tools/validator/kdsl_parser_v2_full_r1_compat.py
  tools/validator/kdsl_parser_v2_full_r1_parity.py
  r1_required_blocks.py / r1_rt_basis.py / r1_authority_guard.py unchanged
```

Common migrated runtime pattern:

```text
input
→ AST v2 CompatibilityView
→ Phase 1/AST v2 parity guard
→ mismatch: semantic validation前にfail
→ match: existing semantic validation
```

Full R1 compatibility boundary:

```text
current three checkers scan whole document
CompatibilityView preserves whole-document scan
bounded-envelope tightening: not introduced
checker migration: pending
```

Retained helper compatibility:

```text
Packet helper exports→semantic/property/normalization modules
Normalization helper exports→round-trip/property modules
Safety Gate helper exports→inheritance/graph/R1C optional/semantic modules
```

```text
helper exports retained != active checker Phase 1 path
legacy adapter removal: prohibited until Full R1 and helper-consumer evidence
```

## 8. R1 / R1C status

```text
canonical R1: spec/r1/r1-result-spec.md
R1C schema: kdsl-r1c@0.1-draft
R1C extraction: AST v2 + parity guard
R1C stable: no
R1C semantic equivalence: not_proven
Full R1 CompatibilityView/parity: integrated
Full R1 checker migration: pending
Full R1 structural parity: 8 / failed 0
```

Critical boundaries:

```text
RT:v=対象環境runtime確認済のみ
build/diff/lint/test/CI pass != RT:v
NEXT:=提案, 実行許可扱禁止
COMMIT:=実行済commitまたは推奨message, 自動commit許可扱禁止
未確認/未実行→確認済/実行済扱禁止
```

## 9. CompactPrompt status

```text
standard: Goal/Input/Output/Guard/Check
kanji-v1: 目/材/出/守/確
AST v2 checker migration: integrated
legacy-v2 parity guard: active
CP-Lift/restricted-alias rules: unchanged
```

```text
implementation/repo/runtime/public/data/source-of-truth/AI coding trigger→CP-Lift
CP-Lift先:=profile:dev-prompt
KDSL-CP漢 alias:=構造KEY位置のみ
```

## 10. Safety Gate status

```text
registry: kdsl-sg@0.1-draft
AST v2 checker migration: integrated
legacy-v2 parity guard: active
structural parity: 8 / failed 0
migration corpus: 4 / failed 0
```

```text
hold/blocked gate削除禁止
state:satisfied requires evidence and authority basis
baseline/composition/protected-wording unchanged
inheritance/graph semantics unchanged
```

## 11. Packet / Normalization status

Packet:

```text
schema: kdsl-packet@0.1-draft
status: v2-draft adopted
executable: no
normalization_required: yes
packet_state: not_normalized
PKT:v1: prohibited
semantic_equivalence: not_proven
normalization_completion: not_proven
execution_authority: none
AST v2 checker migration: integrated
```

Normalization:

```text
schema: kdsl-packet-normalization@0.1-draft
status: non-executable
AST v2 checker migration: integrated
TARGET.executable: false
ROUND_TRIP.semantic_equivalence: not_proven
AUTHORITY.execution_authority: none
normalization completion: not_proven
```

```text
Registry/lint/validator/property/parity pass != Packet executable
normalization preview != executable target
KDSL-Packet直接実行禁止
FLOW-CHANGE != edit authority
```

## 12. Safety and authority boundaries

```text
意味保持 > safety gate保持 > 判断分岐保持 > 誤実装防止 > 文字数削減
safety > high-risk判定 > mode > profile > lexicon > envelope
KDSL-DP直接実行禁止
KDSL-DP→P1/P1L正規化必須
P1/P1L valid != executable
build/diff/lint/test/CI pass != RT:v
NEXT実行許可扱禁止
COMMIT自動commit許可扱禁止
public履歴/公開済tag/Release Assets保護
unknown profile/mode/safety/lexicon/envelope/schema/registry/ID推測禁止
hold/blocked gate削除禁止
```

## 13. Known gaps

```text
Full R1 checker migration
Packet/Normalization helper-consumer migration decision
Safety Gate inheritance/graph helper migration decision
legacy adapter retirement proof
same-marker multi-envelope semantics
complete semantic equivalence proof
complete Safety Gate proof
canonical P1/P1L target schema
stable/public-ready U approval
```

## 14. Current positioning

Use as:

```text
KDSL v2-draft specification repository
R1 evidence/result-reporting specification
CompactPrompt architecture
experimental heuristic validator helpers
typed parser/AST v2 first slice
R1C/CompactPrompt/Safety Gate/Packet/Normalization AST v2 extraction under parity guards
Full R1 AST v2 structural parity pilot
```

Do not present as:

```text
stable KDSL release
public-ready guarantee
Packet executable runtime contract
normalization-complete target
complete semantic parser
semantic equivalence proof
complete safety proof
```

## 15. Next safe steps

```text
P0: Phase 6C-12 Full R1 checker migration under parity guard
P1: helper-consumer migration decision
P2: Phase 6D mutation/property/repository corpus
P3: legacy adapter retirement decision
Hold: stable/public-ready/tag/release/Release Assets
```

Stop when:

```text
existing checker exits change without specification approval
whole-document Full R1 scan changes
RT/NEXT/COMMIT meaning changes
Packet/Normalization/Safety/CP-Lift boundaries weaken
unknown schema/default inference is required
```
