# KDSL / R1 Project Status

status: canonical-project-status
last_updated: 2026-07-17
phase: phase7c-p1-p1l-validator-first-slice-complete
repository: tk999jp/kdsl-spec
default_branch: main
tracking_issue: 118
verified_main_head: b808325c957c9f403fed461dfdbb9e3ce5d547b1

この文書は、`kdsl-spec` repository の現在状態を示す運用上の状態正本です。
仕様正本とfile責務は `spec/manifest.md` を参照します。
詳細証跡は `docs/reviews/*` と各validator implementation notesへ保持します。

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
既存tag移動禁止
Release Assets操作禁止
stable/public-ready化→別途U明示承認必須
```

## 2. Canonical reference map

```text
operational status: docs/project-status.md
specification map: spec/manifest.md
Core: spec/core/*
Profiles: spec/profiles/*
ADPS/P1L/P1: spec/adps/*
R1: spec/r1/*
Lint: spec/lint/*
Bridge: spec/bridge/*
Registry/Packet: spec/registry/* / spec/packet/*
Glossary: spec/glossary.md / spec/glossary-v2-draft.md
```

```text
Core/Profile/ADPS/R1/Lint/Bridge canonical指定file:=仕様正本
P1L:=spec/adps/kdsl-p1l-contract-schema.md
P1:=spec/adps/kdsl-p1-compact-contract-schema.md
P1/P1L index:=spec/adps/README.md
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
P1L:=lossless structured normalized contract / non-executable
P1:=P1L subordinate compact serialization / non-executable
```

## 4. Integrated phase summary

```text
Foundation / v2 architecture: integrated
Phase 1 Common parser / unified validation: integrated
Phase 2 Safety Semantics: integrated bounded slice
Phase 3 R1C optional-block round-trip: integrated
Phase 4 Packet / Normalization semantic properties: integrated
Phase 5 Public-facing v2 hardening: complete
Phase 6A contract/compatibility design: integrated
Phase 6B typed AST v2 core: integrated
Phase 6C active-checker structural migrations: complete
Phase 6D consumer/property/repository migration and proof: complete
Phase 6D-9A adapter zero-reference readiness: integrated
Phase 6D-9B parser adapter removal/post-deletion proof: integrated
Phase 7A P1/P1L ownership and contract design: integrated
Phase 7B P1L/P1 canonical schema/lint/examples/Bridge: integrated
Phase 7B manifest/glossary/index/review/status alignment: integrated
Phase 7C P1L/P1 parser/validator/round-trip first slice: integrated
```

## 5. Repository enforcement

```text
ruleset: Protect main with KDSL Validation
ruleset_id: 18832171
status: active
target: main
PR required: yes
merge method: squash
required check: KDSL Validation
branch up-to-date: required
force push: blocked
deletions: restricted
```

```text
workflow success != semantic equivalence/safety proof/RT:v/release readiness
```

## 6. Latest verified implementation

```text
PR: 123
source head: 497bdd45942caa687c74890cdb2f94ecf36bb8a7
squash commit: b808325c957c9f403fed461dfdbb9e3ce5d547b1
workflow run: 29583167723 / #427
KDSL Validation: success
Packet Semantic Property: success
```

Verified suites:

```text
P1L/P1 contract corpus: 14 / failed 0
adapter removal: 7 / failed 0
Safety Gate consumer contract: 8 / failed 0
Safety semantics migration: 4 / failed 0
Safety inheritance/graph migration: 6 / failed 0
R1C optional Safety Gate migration: 6 / failed 0
Packet installer removal: 4 / failed 0
Packet semantic consumer contract: 10 / failed 0
Packet semantic consumer migration: 4 / failed 0
Packet normalize contract: 10 / failed 0
Packet normalize migration: 4 / failed 0
Normalization installer removal: 4 / failed 0
Normalization consumer contract: 10 / failed 0
Normalization consumer migration: 3 / failed 0
adapter inventory: 4 / failed 0
consumer matrix: 5 / failed 0
unified runners: 36
unified expectations: 456 / failed 0
```

Corrective record:

```text
run #426: new P1 corpus failed
cause: legacy colon P1 classification marker mismatch
correction: checker-local bootstrap classifies legacy colon P1 before canonical dispatch
run #427: success
```

```text
validator未実行→pass扱禁止
validator pass != semantic equivalence
validator pass != complete safety proof
validator pass != U承認
validator pass != RT:v
validator pass != release readiness
P1L/P1 validator pass != runtime binding/execution authority
```

## 7. Parser/checker state

Pre-Phase-7 active checker structural inputs use checker-specific AST v2 CompatibilityViews under legacy parity guards:

```text
Full R1 required blocks / RT basis / authority
R1C
CompactPrompt
Safety Gate
Packet
Packet Normalization
```

```text
input
→ AST v2 CompatibilityView
→ legacy/AST v2 structural parity guard
→ mismatch: semantic validation前にfail
→ match: existing semantic validation
```

P1L/P1 first slice:

```text
P1L parser: DocumentNodeV2 raw-envelope parse under checker-local marker registration
P1 parser: dedicated ordered JSON segment scanner
shared AST v2 P1L marker registration: not integrated
P1L/P1 schema checker: integrated first slice
P1L→P1→P1L round-trip: integrated first slice
CLI targets: p1l|p1|p1-contract
unified runner: integrated
```

First-slice coverage:

```text
top-level/nested field order
source/profile evidence shape
profile completion vs inference
scope/context classification
Runtime pre-execution disposition
all eight Authority rails
Normalization/Binding boundaries
pipe inside JSON strings
Windows path exact preservation
legacy colon P1 rejection
mixed P1L/P1 rejection
```

## 8. Runtime consumer state

Normalization:

```text
checker/round-trip consumer: NormalizationCompatibilityView
property consumer: indirect parse_normalization API
install_normalization: removed
```

Packet:

```text
normalize/semantic consumers: PacketCompatibilityView
install_packet: removed
runtime structural consumers from kdsl_packet: none
local legacy helpers: parity evidence only
```

Safety Gate:

```text
active checker: SafetyGateCompatibilityView + parity guard
safety semantics: SafetyGateCompatibilityView
inheritance: SafetyGateCompatibilityView
graph: SafetyGateCompatibilityView
R1C optional embedded SAFETY_GATES: SafetyGateCompatibilityView
install_safety_gate: removed
legacy structural consumers: none
```

P1L/P1:

```text
runtime binding implementation: none
K1/PF1 canonical schema: absent
BINDING.state default: unbound
BINDING.executable: false
runtime consumers: none
validator/round-trip pass does not change binding
```

## 9. Adapter retirement state

```text
tools/validator/kdsl_parser_adapter.py: removed
direct adapter imports: none
installer function consumers: none
legacy structural helper consumers: none
parity modules depending on adapter: none
consumer matrix blocking_records: 0
post-deletion key runtime import guard: pass
post-deletion full unified suite: pass
adapter retirement: complete
```

## 10. R1 / authority boundaries

```text
RT:v=対象環境runtime確認済のみ
build/diff/lint/test/CI pass != RT:v
NEXT:=提案, 実行許可扱禁止
COMMIT:=実行済commitまたは推奨message, 自動commit許可扱禁止
未確認/未実行→確認済/実行済扱禁止
```

P1L/P1 pre-execution runtime values:

```text
pending|user_required|not_applicable
```

```text
P1L/P1でRT:v/fail/blk結果claim禁止
P1L/P1 AUTHORITY missing/implicit→blocked
read/edit/stage/commit/push/release/public_repo/destructive_ops全rail必須
PLAN/step/opcode != authority
```

Validator output remains:

```text
EXECUTABLE:no
SEMANTIC_EQUIVALENCE:not_proven
EXECUTION_AUTHORITY:none
```

## 11. CompactPrompt / Safety boundaries

```text
CP-Lift trigger保持
KDSL-CP漢 alias:=構造KEY位置のみ
hold/blocked gate削除禁止
state:satisfied requires evidence and authority basis
baseline/composition/protected-wording unchanged
inheritance/graph semantics unchanged
P1 profile completion != inference
Safety Gate ID/presetのみでprotected wording置換禁止
```

## 12. Packet / Normalization boundaries

Packet:

```text
schema: kdsl-packet@0.1-draft
status: non-executable
normalization_required: yes
packet_state: not_normalized
PKT:v1: prohibited
semantic_equivalence: not_proven
execution_authority: none
```

Normalization:

```text
schema: kdsl-packet-normalization@0.1-draft
status: non-executable
TARGET.executable: false
ROUND_TRIP.semantic_equivalence: not_proven
AUTHORITY.execution_authority: none
normalization completion: not_proven
P1/P1L target schema: present
P1/P1L validator first slice: present
Packet→P1L/P1 mapping/integration: not implemented
P1L_PREVIEW/P1_PREVIEW: not adopted
```

```text
P1/P1L schema/validator adoption alone != Packet target resolution complete
Registry/lint/validator/property/parity/readiness/contract/migration/removal pass != Packet executable
normalization preview != executable target
KDSL-Packet直接実行禁止
FLOW-CHANGE != edit authority
```

## 13. Phase 7C state

Integrated:

```text
tools/validator/kdsl_p1_contract.py
tools/validator/kdsl_p1_bootstrap.py
tools/validator/kdsl_p1l.py
tools/validator/kdsl_p1.py
tools/validator/kdsl_p1_auto.py
tools/validator/kdsl_p1_roundtrip.py
tools/validator/run_p1_contract_samples.py
kdsl_validate targets: p1l|p1|p1-contract
unified runner integration
implementation notes
review evidence
```

Parser ownership:

```text
shared AST v2 core unchanged
P1L marker registered only in bounded checker process
P1 dedicated scanner handles JSON nesting/string escaping
checker-local registration is transitional, not permanent proof
```

Not implemented / not proven:

```text
shared AST v2 first-class P1L integration
arbitrary external Profile content verification
complete protected-wording semantic proof
P1L/P1 semantic equivalence
complete natural-language interpretation
complete safety proof
runtime binding
K1/PF1 canonical schema
Packet→P1L/P1 normalization mapping
Packet normalization completion
Packet executable promotion
stable/public-ready promotion
```

## 14. Current positioning

Use as:

```text
KDSL v2-draft specification repository
R1 evidence/result-reporting specification
CompactPrompt architecture
typed AST v2 structural foundation
legacy namespace adapter retired
P1L canonical v2-draft structured contract schema
P1 canonical v2-draft subordinate compact serialization
P1/P1L bounded parser/validator/round-trip first slice
experimental heuristic validator helpers
```

Do not present as:

```text
stable KDSL release
public-ready guarantee
P1L/P1 executable runtime contract
P1L/P1 semantic-equivalence proof
P1L/P1 complete safety proof
Packet executable runtime contract
normalization-complete target
complete semantic parser
```

## 15. Next safe steps

```text
P0: Phase 7D Packet normalization integration under P1L_PREVIEW/P1_PREVIEW non-executable boundary
P1: shared AST v2 first-class P1L integration only after compatibility/consumer review
P2: K1/PF1 canonical runtime-control design only under separate approval
Hold: runtime binding/executable promotion/stable/public-ready/tag/release/Release Assets
```

Stop when:

```text
P1L/P1 ownership becomes ambiguous
unknown legacy alias/profile/preset meaning must be inferred
critical authority rail becomes implicit
profile defaults lack exact revision/digest evidence
P1 compact round-trip loses protected wording or exact strings
RUNTIME contract field claims RT:v without evidence
Packet normalization becomes executable
RT/NEXT/COMMIT meaning changes
Packet/Normalization/Safety/CP-Lift boundaries weaken
```
