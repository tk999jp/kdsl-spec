# KDSL / R1 Project Status

status: canonical-project-status
last_updated: 2026-07-17
phase: phase6d-adapter-retirement-readiness-integrated
repository: tk999jp/kdsl-spec
default_branch: main
tracking_issue: 55
verified_main_head: ed928bfddd7a412acd420ba1622addd788cd6f50

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
Phase 6A/6B semantic parser foundation/core: integrated
Phase 6C active-checker structural migrations: complete
Phase 6D-1 adapter/helper inventory: integrated
Phase 6D-2 consumer decision matrix: integrated
Phase 6D unified-runner corrective: integrated
Phase 6D-3 Normalization consumer contract/migration: integrated
Phase 6D-4 Normalization installer removal: integrated
Phase 6D-5 Packet normalize consumer contract/migration: integrated
Phase 6D-6 Packet semantic consumer contract/migration: integrated
Phase 6D-7A Packet installer readiness: integrated
Phase 6D-7B Packet installer removal: integrated
Phase 6D-8A Safety Gate consumer contract/inventory: integrated
Phase 6D-8B Safety semantics structural migration: integrated
Phase 6D-8C Safety Gate inheritance/graph structural migration: integrated
Phase 6D-8D R1C optional Safety Gate structural migration: integrated
Phase 6D-9A parser adapter retirement readiness: integrated
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
PR: 114
source head: f31ecb5d0626644a6b1867c5390ca246adf2b3bd
squash commit: ed928bfddd7a412acd420ba1622addd788cd6f50
workflow run: 29545316817 / #406
KDSL Validation: success
Packet Semantic Property: success
```

Verified suites:

```text
adapter retirement readiness: 7 / failed 0
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

Corrective record:

```text
run #400: semantic utilities misclassified as structural
run #401/#402/#403: readiness passed; stale repository matrix expectation remained
semantic classification and repository matrix expectation corrected
temporary diagnostic artifact workflow removed before final verification
run #406: success
```

```text
validator未実行→pass扱禁止
validator pass != semantic equivalence
validator pass != complete safety proof
validator pass != U承認
validator pass != RT:v
validator pass != release readiness
readiness pass != adapter deletion/post-deletion proof
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

## 8. Dependency and adapter state

```text
direct kdsl_parser_adapter imports: none
installer function consumers outside adapter: none
legacy structural helper consumers: none
parity modules depending on adapter: none
key runtime modules import with adapter denied: pass
```

Normalization family:

```text
checker/consumer: NormalizationCompatibilityView
direct installer: removed
local parity helpers: retained
```

Packet family:

```text
normalize/semantic consumers: PacketCompatibilityView
install_packet: removed
runtime structural consumers from kdsl_packet: none
local legacy helpers: parity evidence only
```

Safety Gate family:

```text
active checker and known structural consumers: SafetyGateCompatibilityView
direct installer: absent
legacy structural consumers: none
```

Retained semantic internal API:

```text
KNOWN_IDS
KNOWN_STATES
REGISTRY
REQUIRED_FIELDS
aggregate_state
authority_is_unverified
is_blank
```

Parity strategy:

```text
direct legacy-parser/checker-local comparison paths retained
kdsl_parser_adapter.py is not parity evidence
```

Adapter file:

```text
path: tools/validator/kdsl_parser_adapter.py
exports: install_r1c/install_packet/install_normalization/install_safety_gate
runtime consumers: none
state: bounded-removal-trial-candidate
file removal: not performed
```

## 9. Adapter retirement gates

```text
G1 active checker independence: satisfied
G2 direct installer inventory: satisfied
G3 consumer decision matrix: satisfied / blocking_records:0
G4 Normalization family migration/removal: satisfied
G5 Packet family migration/removal: satisfied
G6 Safety Gate structural consumers migrated: satisfied
G7 semantic utility retention decision: satisfied / bounded internal API
G8 parity strategy: satisfied / adapter-independent
G9 zero-reference/readiness corpus: satisfied
G10 bounded adapter deletion trial: pending
G11 post-deletion full repository proof: pending
G12 adapter retirement completion: blocked
```

Current decision:

```text
readiness state: bounded-removal-trial-candidate
kdsl_parser_adapter.py file: retained
adapter deletion: not performed
adapter retirement: blocked until post-deletion proof
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
```

```text
Registry/lint/validator/property/parity/readiness/contract/migration/removal pass != Packet executable
normalization preview != executable target
KDSL-Packet直接実行禁止
FLOW-CHANGE != edit authority
```

## 13. Known gaps

```text
bounded kdsl_parser_adapter.py deletion trial
post-deletion full repository proof
adapter retirement closeout decision
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
all active checker structural inputs migrated to AST v2 CompatibilityViews
known runtime structural consumers migrated
Normalization and Packet direct installers removed
adapter zero-reference readiness proven
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
adapter removal completed
```

## 15. Next safe steps

```text
P0: Phase 6D-9B delete only tools/validator/kdsl_parser_adapter.py
P1: replace readiness corpus with post-deletion corpus
P2: preserve semantic internal API and parity paths
P3: run complete unified suite
P4: record adapter retirement only after post-deletion success
Hold: stable/public-ready/tag/release/Release Assets
```

Stop when:

```text
hidden adapter import appears
parity evidence is lost
semantic utility behavior changes
RT/NEXT/COMMIT meaning changes
Packet/Normalization/Safety/CP-Lift boundaries weaken
unknown schema/default inference is required
```
