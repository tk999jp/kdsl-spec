# KDSL / R1 Project Status

status: canonical-project-status
last_updated: 2026-07-13
phase: phase6c-safety-gate-compatibility-integrated
repository: tk999jp/kdsl-spec
default_branch: main
tracking_issue: 55

この文書は、`kdsl-spec` repository の現在状態を示す運用上の状態正本です。
仕様正本とfile責務は `spec/manifest.md` を参照します。

Phase 5以前の詳細な履歴は次の非正本archiveへ保持します。

```text
docs/project-status-history/project-status-through-phase4-20260712.md
```

```text
current operational status > historical status archive
historical archive:=証跡保持 / 現在状態正本ではない
```

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
operational status:
  docs/project-status.md
specification map:
  spec/manifest.md
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
Lint:
  spec/lint/*
Bridge:
  spec/bridge/*
Registry/Packet:
  spec/registry/*
  spec/packet/*
```

## 3. Current architecture

```text
format: KDSL
profile: compact-prompt|dev-prompt|converter|lint
mode: readable|min|dense|lock
safety: normal|lock-critical|lock-all
lexicon: standard|kanji-v1
envelope: plain|packet-draft|result
```

Named compositions:

```text
KDSL-CP:=profile:compact-prompt
KDSL-CP漢:=profile:compact-prompt + mode:dense + lexicon:kanji-v1
KDSL-R1:=envelope:result / KDSL_RESULT
KDSL-Packet:=v2-draft authoring envelope / non-executable
```

Legacy:

```text
rulebook:=v1.1 legacy profile name
rulebook新規使用禁止
rulebookを正式v2 profile扱い禁止
legacy rulebook入力→用途確認なしに他profileへ自動補正禁止
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
Phase 6B additive typed parser/AST v2 core: integrated
Phase 6C-1 R1C compatibility view/parity: integrated
Phase 6C-2 R1C checker migration: integrated
Phase 6C-3 CompactPrompt compatibility view/parity: integrated
Phase 6C-4 CompactPrompt checker structural migration: integrated
Phase 6C-5 Safety Gate compatibility view/parity: integrated
```

Phase 5 evidence:

```text
PR #50 / 49b6c865af046d44efc04a46d851aed55d222a61
PR #51 / 442d53226c7d0fd000ed1f93efc28ccbb367b129
PR #52 / 88f3d94b0c5915a74f3654e0407bffda3bb9f4c3
experimental preview documentation: ready
public repository navigation: ready
public examples: non-normative
public_ready: no
stable_release: no
```

## 5. Repository enforcement

```yaml
repository_enforcement:
  ruleset_name: Protect main with KDSL Validation
  ruleset_id: 18832171
  enforcement_status: active
  target: default_branch / main
  bypass_list: empty
  restrict_deletions: true
  require_pull_request_before_merging: true
  required_approvals: 0
  allowed_merge_method: squash
  require_status_checks: true
  required_status_check: KDSL Validation
  require_branches_up_to_date: true
  block_force_pushes: true
```

```text
verification PR: 53 / closed without merge
verification workflow: #252 / success
activation record PR: 54
activation record squash: 9434628aefb966d0b66e9d865a956d961b551ef2
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
  workflow_name: KDSL Validation
  unified_command: python tools/validator/run_all_samples.py
  unified_runners: 13
  unified_expectations: 303
  failed: 0
  phase1_parser_cases: 11
  phase6b_parser_v2_cases: 12
  phase6c_r1c_parity_cases: 10
  phase6c_compact_parity_cases: 12
  phase6c_compact_checker_migration_cases: 4
  phase6c_safety_gate_parity_cases: 8
  required_check_activation: active
  required_check_ruleset: Protect main with KDSL Validation
```

Latest verification:

```text
implementation PR: 67
source head: ce0f45852a2d2baf81e09371e8534ea2026051e0
squash commit: 604e4e1f8f8c601f7054b15b38e3c5db40d88056
workflow run: 29230830767 / #301 / success
jobs:
  KDSL Validation: success
  Packet Semantic Property: success
```

Unified output policy:

```text
successful child runner→compact summary
failed/malformed child runner→full stdout/stderr
missing summary or non-zero exit→failure
```

Boundaries:

```text
validator未実行→pass扱禁止
validator pass != semantic equivalence
validator pass != complete safety proof
validator pass != U承認
validator pass != RT:v
validator pass != release readiness
required check active != stable/public-ready approval
```

## 7. Semantic parser status

### Phase 1 compatibility parser

```text
tools/validator/kdsl_parser.py
tools/validator/kdsl_parser_adapter.py
DocumentNode / EnvelopeNode / FieldNode
SourceSpan / ParseIssue / DiagnosticBag
```

Remaining namespace-adapter consumers:

```text
Safety Gate
Packet
Packet Normalization
```

```text
R1C: AST v2 compatibility extraction + legacy parity guard
CompactPrompt: AST v2 compatibility extraction + legacy parity guard
Safety Gate: CompatibilityView integrated / checker remains Phase 1 adapter based
legacy adapter removal: prohibited until remaining checker migration evidence
```

### Phase 6B typed AST v2 core

```text
implementation:
  tools/validator/kdsl_parser_v2.py
  tools/validator/kdsl_parse_v2.py
corpus:
  tools/validator/run_parser_v2_samples.py
  tools/validator/samples/parser-v2/*
review:
  docs/reviews/kdsl-phase6b-semantic-parser-core.md
PR: 57
squash: 54c214587cedfc4af634edba9d3df7cdea30d524
status: integrated / additive
```

Implemented surface:

```text
ordered document children
formal header nodes
multiple envelope exposure
raw + normalized value channels
typed scalar/block/JSON/mapping/sequence/record nodes
nested source spans
duplicate envelope/field/mapping-key diagnostics
invalid JSON/unclosed fence diagnostics
active-document fence isolation
CRLF normalization
UTF-8/Japanese exact wording preservation
unknown header values retained without inference
```

### Phase 6C R1C migration

```text
compatibility view: tools/validator/kdsl_parser_v2_compat.py
parity checker: tools/validator/kdsl_parser_v2_r1c_parity.py
semantic checker: tools/validator/kdsl_r1c.py
reviews:
  docs/reviews/kdsl-phase6c-r1c-compatibility-view.md
  docs/reviews/kdsl-phase6c-r1c-checker-migration.md
PRs: 59 / 61
status: checker migrated under parity guard
```

Current R1C path:

```text
AST v2 compatibility extraction
→ Full R1 fallback when R1C schema absent
→ legacy-v2 parity guard when R1C schema present
→ existing R1C semantic validation
```

Corrective boundaries:

```text
fenced repository example→legacy-compatible scope selection
AST v2 active-document fence isolation remains unchanged
SAFETY_GATES standalone marker/R1C field ambiguity→R1C scope限定処理
marker registry restored in finally
same-marker divergence→semantic validation前にfail
```

### Phase 6C CompactPrompt migration

```text
compatibility view: tools/validator/kdsl_parser_v2_compact_compat.py
parity checker: tools/validator/kdsl_parser_v2_compact_parity.py
semantic checker: tools/validator/kdsl_compact_prompt.py
checker migration suite: tools/validator/run_compact_migration_samples.py
reviews:
  docs/reviews/kdsl-phase6c-compact-compatibility-view.md
  docs/reviews/kdsl-phase6c-compact-checker-migration.md
PRs: 63 / 65
status: checker migrated under parity guard
```

Current CompactPrompt path:

```text
CompactPromptCompatibilityView
→ legacy-v2 structural parity guard
→ mismatch: fail before semantic validation
→ AST v2 scope/header/block/duplicate extraction
→ existing CompactPrompt semantic/safety validation
```

Retained policy:

```text
CP-Lift semantics: unchanged
restricted alias semantics: unchanged
mode/safety/lexicon policy: unchanged
required/empty/mixed/duplicate policy: unchanged
PKT:v1 and Packet non-executable checks: unchanged
```

### Phase 6C Safety Gate compatibility pilot

```text
compatibility view: tools/validator/kdsl_parser_v2_safety_gate_compat.py
parity checker: tools/validator/kdsl_parser_v2_safety_gate_parity.py
parity runner: tools/validator/run_parser_v2_safety_gate_parity_samples.py
review: docs/reviews/kdsl-phase6c-safety-gate-compatibility-view.md
PR: 67
squash: 604e4e1f8f8c601f7054b15b38e3c5db40d88056
status: compatibility view/parity integrated
```

Compared contract:

```text
SAFETY_GATES presence
exact Phase 1 selected scope
registry
entry order
entry field order
entry values
fenced repository example
out-of-scope absence
```

Migration boundary:

```text
Safety Gate checker switch: not performed
Phase 1 adapter: retained
registry/ID/state semantics: unchanged
baseline/composition/protected-wording semantics: unchanged
inheritance/graph semantics: unchanged
```

## 8. R1 / R1C status

```text
canonical R1: spec/r1/r1-result-spec.md
R1C schema: kdsl-r1c@0.1-draft
R1C status: v2-draft adopted serialization profile
R1C extraction: AST v2 compatibility path + legacy parity guard
R1C independent canonical spec: no
R1C stable: no
R1C full semantic equivalence: not_proven
```

```text
RT:v=対象環境runtime確認済のみ
build/diff/lint/test/CI pass != RT:v
NEXT:=提案, 実行許可扱禁止
COMMIT:=実行済commitまたは推奨message, 自動commit許可扱禁止
```

## 9. CompactPrompt status

```text
profile: compact-prompt
standard structure: Goal/Input/Output/Guard/Check
kanji-v1 structure: 目/材/出/守/確
semantic checker: tools/validator/kdsl_compact_prompt.py
AST v2 compatibility view: integrated
checker migration: integrated
legacy-v2 parity guard: active
```

```text
implementation/repo/runtime/public/data/source-of-truth/AI coding trigger→CP-Lift
CP-Lift先:=profile:dev-prompt
restricted kanji alias free-text使用禁止
KDSL-CP漢 alias:=構造KEY位置のみ
Packet draft:=non-executable
```

## 10. Safety Gate status

```text
registry: kdsl-sg@0.1-draft
semantic checker: tools/validator/kdsl_safety_gate.py
AST v2 compatibility view: integrated
checker migration: pending
Phase 1 adapter: active
structural parity: 8 / failed 0
```

Critical boundaries:

```text
hold/blocked gate削除禁止
state:satisfied requires evidence and authority basis
baseline/composition/protected-wording requirements unchanged
inheritance/graph semantics unchanged
```

## 11. Packet status

```text
schema: kdsl-packet@0.1-draft
status: v2-draft adopted
stable: no
executable: no
normalization_required: yes
packet_state: not_normalized
PKT:v1: prohibited
semantic_property_model: kdsl-packet-property@0.1-draft
property_scope: selected bounded properties only
semantic_equivalence: not_proven
normalization_completion: not_proven
execution_authority: none
```

```text
Registry/lint/validator/property pass != Packet executable
normalization preview != executable target
KDSL-Packet直接実行禁止
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
Full R1 compatibility view/migration
Safety Gate checker migration to CompatibilityView
Packet compatibility view/migration
Packet Normalization compatibility view/migration
legacy adapter retirement proof
same-marker multiple-envelope general semantics
broader fence/context semantics beyond current first slice
full YAML/KDSL semantic parser
full natural-language negation/exception reasoning
full semantic equivalence proof
complete safety proof
arbitrary graph/cross-document Safety Gate proof
R1C full semantic equivalence
Packet normalization completion proof
canonical P1/P1L target schema
stable/public-ready U approval
```

## 14. Current positioning

Use as:

```text
public experimental preview
safety-gate-preserving prompt notation draft
Human-AI work contract design
R1 evidence/result-reporting specification
CompactPrompt architecture
experimental heuristic validator helpers
additive typed parser/AST v2 first slice
R1C AST v2 extraction under legacy parity guard
CompactPrompt AST v2 extraction under legacy parity guard
Safety Gate AST v2 structural parity pilot
```

Do not present as:

```text
stable standard
production-ready proof system
approval/runtime/release substitute
executable Packet specification
independent canonical R1C standard
complete semantic parser
semantic equivalence proof
```

## 15. Next safe steps

```text
P0: Phase 6C-6 Safety Gate checker structural migration under parity guard
P1: Packet / Packet Normalization compatibility views and migration
P2: Full R1 compatibility view/migration
P3: Phase 6D mutation/property/repository corpus and adapter-retirement decision
Hold: stable/public-ready/tag/release/Release Assets
```

```text
NEXT:=proposal only
NEXT実行許可扱禁止
stable/public-ready化→別途U明示承認必須
```
