# KDSL / R1 Project Status

status: canonical-project-status
last_updated: 2026-07-17
phase: phase7a-p1-p1l-contract-design-integrated
repository: tk999jp/kdsl-spec
default_branch: main
tracking_issue: 118
verified_main_head: 32b663132941138f8fe6e45d017f6c18046a671e

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
R1: spec/r1/*
Lint: spec/lint/*
Bridge: spec/bridge/*
Registry/Packet: spec/registry/* / spec/packet/*
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
PR: 119
source head: 2347725e1fea1323be00e153ff42a4bfa1bdd6de
squash commit: 32b663132941138f8fe6e45d017f6c18046a671e
workflow run: 29579900564 / #414
KDSL Validation: success
Packet Semantic Property: success
```

Verified suites remain:

```text
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
unified runners: 35
unified expectations: 442 / failed 0
```

```text
validator未実行→pass扱禁止
validator pass != semantic equivalence
validator pass != complete safety proof
validator pass != U承認
validator pass != RT:v
validator pass != release readiness
design integration pass != canonical schema adoption
```

## 7. Parser/checker state

All active checker structural inputs use checker-specific AST v2 CompatibilityViews under legacy parity guards:

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

No active checker remains solely on the Phase 1 structural path.

P1/P1L parser/checker is not yet implemented.

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

Retained bounded semantic internal API:

```text
KNOWN_IDS
KNOWN_STATES
REGISTRY
REQUIRED_FIELDS
aggregate_state
authority_is_unverified
is_blank
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

Parity strategy:

```text
direct legacy-parser/checker-local comparison paths retained
local parity helpers retained where required
adapter removal did not remove parity evidence
```

## 10. R1 / authority boundaries

```text
RT:v=対象環境runtime確認済のみ
build/diff/lint/test/CI pass != RT:v
NEXT:=提案, 実行許可扱禁止
COMMIT:=実行済commitまたは推奨message, 自動commit許可扱禁止
未確認/未実行→確認済/実行済扱禁止
```

## 11. CompactPrompt / Safety boundaries

```text
CP-Lift trigger保持
KDSL-CP漢 alias:=構造KEY位置のみ
hold/blocked gate削除禁止
state:satisfied requires evidence and authority basis
baseline/composition/protected-wording unchanged
inheritance/graph semantics unchanged
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
P1/P1L target resolution: blocked until canonical schema adoption and separate integration
```

```text
Registry/lint/validator/property/parity/readiness/contract/migration/removal pass != Packet executable
normalization preview != executable target
KDSL-Packet直接実行禁止
FLOW-CHANGE != edit authority
```

## 13. Phase 7A design state

Integrated design direction:

```text
P1L:=lossless structured normalized contract schema candidate
P1:=compact serialization profile subordinate to P1L candidate
P1/P1L valid != executable
profile completion != inference
authority/runtime binding separate from structural validity
```

Phase 7A recorded:

```text
candidate schema IDs: kdsl-p1l@0.1-draft / kdsl-p1@0.1-draft
P1L candidate envelope and required fields
P1 compact field-map candidate
explicit/profile_completed/lossy/blocked normalization states
mandatory authority rails
runtime requirement vs R1 result-state separation
P1↔P1L structural round-trip model
legacy MidFD P1 compatibility boundary
Packet normalization dependency
```

Unresolved evidence retained:

```text
legacy loss=L meaning
legacy AP/H abbreviations
operational P1 explicit authority rails
operational P1L concrete syntax
K1/PF1 canonical runtime-control schema
```

Not proven / not adopted:

```text
canonical P1L schema
canonical P1 compact schema
P1/P1L parser/validator
P1/P1L runtime binding
complete semantic equivalence
complete natural-language interpretation
complete safety proof
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
experimental heuristic validator helpers
typed AST v2 structural foundation
all active checker and known runtime structural consumers migrated
legacy namespace adapter retired
P1/P1L canonical contract design completed
```

Do not present as:

```text
stable KDSL release
public-ready guarantee
canonical P1/P1L schema already adopted
P1/P1L executable runtime contract
Packet executable runtime contract
normalization-complete target
complete semantic parser
semantic equivalence proof
complete safety proof
```

## 15. Next safe steps

```text
P0: obtain explicit U approval to adopt the Phase 7A ownership direction as canonical v2-draft schemas
P1: Phase 7B canonical P1L schema + subordinate P1 compact schema + lint/examples
P2: Phase 7C parser/validator first slice and round-trip corpus
P3: Phase 7D Packet normalization integration under non-executable preview boundary
Hold: K1/PF1 invention, executable promotion, stable/public-ready/tag/release/Release Assets
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
