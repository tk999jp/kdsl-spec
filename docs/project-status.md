# KDSL / R1 Project Status

status: canonical-project-status
last_updated: 2026-07-17
phase: phase6d-safety-semantics-migration-integrated
repository: tk999jp/kdsl-spec
default_branch: main
tracking_issue: 55
verified_main_head: 36dcdbedb717772dda618972d7c4eca09b41aa07

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

## 6. Latest integrated implementation

```text
PR: 108
source head: 5f429dc94078cb7af51da0162fb1a57bc76e1516
squash commit: 36dcdbedb717772dda618972d7c4eca09b41aa07
required check: KDSL Validation
required check evidence: active Ruleset accepted squash merge
workflow run ID: unavailable / GitHub connector repeated HTTP 502
individual workflow job payload: unconfirmed
```

Expected integrated suites under the required unified job:

```text
Safety Gate consumer contract: 8 / failed 0
Safety semantics migration: 4 / failed 0
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
unified runners: 32
unified expectations: 423 / failed 0
```

Evidence interpretation:

```text
run_all_samples.py includes 32 runners
new migration runner contributes 4 expectations
unified runner fails on missing summary/nonzero/failed case
Ruleset-required KDSL Validation accepted before merge
exact run number and separate job payload are not inferred
```

```text
validator未実行→pass扱禁止
validator pass != semantic equivalence
validator pass != complete safety proof
validator pass != U承認
validator pass != RT:v
validator pass != release readiness
contract/migration/removal pass != adapter file retirement proof
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

## 8. Phase 6D dependency state

Direct adapter installer boundary:

```text
none
```

Any future direct import from `kdsl_parser_adapter` is an inventory failure.

Normalization family:

```text
checker: NormalizationCompatibilityView
round-trip consumer: NormalizationCompatibilityView
property consumer: indirect parse_normalization API
direct installer: removed
local parity helpers: retained
```

Packet family:

```text
normalize consumer: PacketCompatibilityView
semantic consumer: PacketCompatibilityView
legacy structural imports from kdsl_packet: removed
nonstructural/constants imports retained
install_packet import/call: removed
runtime structural consumers from kdsl_packet: none
local legacy helper functions: parity evidence only
```

Safety Gate family:

```text
active checker: SafetyGateCompatibilityView + parity guard
direct adapter installer: absent
consumer contract/inventory: integrated
```

Safety semantics consumer:

```text
file: kdsl_safety_semantics.py
structural extraction: SafetyGateCompatibilityView
legacy structural imports from kdsl_safety_gate: removed
semantic requirement/atom/scope logic: unchanged
migration corpus: integrated
```

Remaining helper consumers:

```text
kdsl_safety_gate_inheritance.py:
  extract_gate_block/parse_registry → pending migration
  REGISTRY/aggregate_state/authority_is_unverified/is_blank → retain temporarily

kdsl_safety_gate_graph.py:
  extract_gate_block/parse_registry → pending migration
  REGISTRY/aggregate_state/authority_is_unverified/is_blank → retain temporarily

kdsl_r1c_optional.py:
  embedded parse_registry → pending migration
  constants/authority_is_unverified/is_blank → retain temporarily
```

## 9. Adapter retirement gates

```text
G1 active checker independence: satisfied
G2 direct installer inventory: satisfied / direct imports none
G3 consumer decision matrix: integrated / CI-verified
G4 Normalization family contract/migration: satisfied
G5 Normalization installer removal: satisfied
G6 Packet normalize contract/migration: satisfied
G7 Packet semantic contract/migration: satisfied
G8 Packet installer readiness: satisfied
G9 Packet installer removal: satisfied
G10 Safety Gate consumer contract/inventory: satisfied
G11 Safety semantics structural migration: satisfied
G12 Safety Gate inheritance/graph structural migration: pending
G13 R1C optional SAFETY_GATES structural migration: pending
G14 semantic utility location/retention decision: pending
G15 parity-only legacy helper strategy: pending
G16 adapter file retirement proof: blocked
```

Current decision:

```text
Normalization installer removal: complete
Packet installer removal: complete
direct adapter imports: none
Safety semantics migration: complete
remaining Safety Gate structural consumers: 3
kdsl_parser_adapter.py file: retained
adapter file retirement: blocked
adapter file removal: not performed
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
Safety Gate inheritance/graph structural migration
R1C optional SAFETY_GATES structural migration
Safety Gate semantic utility location/retention decision
parity-only legacy helper strategy
legacy adapter file retirement or explicit retention decision
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
Normalization and Packet runtime consumers migrated
Normalization and Packet direct installers removed
Safety Gate consumer contract frozen
Safety semantics structural consumer migrated
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
adapter-retirement-ready repository
```

## 15. Next safe steps

```text
P0: Phase 6D-8C add inheritance/graph consumer contract evidence
P1: migrate only inheritance/graph structural extraction
P2: retain semantic utility/constants temporarily
P3: Phase 6D-8D migrate R1C optional embedded SAFETY_GATES parsing
P4: decide semantic utility location/retention
P5: decide parity-only helpers and adapter-file retirement last
Hold: stable/public-ready/tag/release/Release Assets
```

Stop when:

```text
Safety Gate inheritance/graph/optional behavior changes
unknown structural consumer appears
semantic/property exit behavior changes
RT/NEXT/COMMIT meaning changes
Packet/Normalization/Safety/CP-Lift boundaries weaken
unknown schema/default inference is required
```
