# KDSL / R1 Project Status

status: canonical-project-status
last_updated: 2026-07-14
phase: phase6d-normalization-installer-removal-integrated
repository: tk999jp/kdsl-spec
default_branch: main
tracking_issue: 55
verified_main_head: 1e488c6fedb792cd1a40a003b68c374af93b7dae

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
v0.1.0-draft tag:=履歴として維持
v1.1.0-rc1:=experimental historical baseline
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
Phase 6C active-checker structural migrations: complete
Phase 6D-1 parser adapter/helper inventory: integrated
Phase 6D-2 helper consumer decision matrix: integrated
Phase 6D unified-runner corrective: integrated
Phase 6D-3A Normalization consumer contract: integrated
Phase 6D-3B Normalization round-trip consumer migration: integrated
Phase 6D-4 Normalization direct-installer removal: integrated
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
required_check_activation: confirmed
workflow success != semantic equivalence/safety proof/RT:v/release readiness
```

## 6. Latest verified implementation

```text
PR: 92
source head: 6c0a27f5374e9374a0b698f2501ff7060218e69f
squash commit: 1e488c6fedb792cd1a40a003b68c374af93b7dae
workflow run: 29290086908 / #355
KDSL Validation: success
Packet Semantic Property: success
```

Verified suites:

```text
Normalization installer-removal: 4 / failed 0
Normalization consumer contract: 10 / failed 0
Normalization consumer migration: 3 / failed 0
adapter inventory: 4 / failed 0
consumer matrix: 5 / failed 0
unified runners: 25
unified expectations: 379 / failed 0
```

```text
validator未実行→pass扱禁止
validator pass != semantic equivalence
validator pass != complete safety proof
validator pass != U承認
validator pass != RT:v
validator pass != release readiness
inventory/matrix/contract/migration/removal pass != adapter file retirement proof
```

## 7. Parser/checker migration state

Typed AST core:

```text
tools/validator/kdsl_parser_v2.py
tools/validator/kdsl_parse_v2.py
```

Migrated active checker structural paths:

```text
Full R1 required blocks / RT basis / authority
R1C
CompactPrompt
Safety Gate
Packet
Packet Normalization
```

Common checker pattern:

```text
input
→ checker-specific AST v2 CompatibilityView
→ legacy/AST v2 structural parity guard
→ mismatch: semantic validation前にfail
→ match: existing semantic validation
```

No active checker remains solely on the Phase 1 structural path.

## 8. Phase 6D dependency state

Decision vocabulary:

```text
retain-temporarily
migrate-or-replace
retain-parity-only
retain-semantic-api
```

Current direct installer boundary:

```text
kdsl_packet.py -> install_packet
kdsl_packet_normalization.py -> none
kdsl_safety_gate.py -> none
```

Normalization family:

```text
active checker: NormalizationCompatibilityView
round-trip consumer: NormalizationCompatibilityView
property consumer: indirect parse_normalization API
Normalization direct installer: removed
local legacy helpers: retained for parity evidence
```

Safety Gate family:

```text
direct adapter installer: absent
helper-consumer inventory/decision: retained for Phase 6D review
```

Packet family:

```text
direct adapter installer: retained
helper consumers: remain
consumer-specific migration proof: pending
```

## 9. Adapter retirement gates

```text
G1 active checker independence: satisfied
G2 direct installer inventory: integrated / unified-CI-verified
G3 helper-consumer decision matrix: integrated / unified-CI-verified
G4 Normalization consumer mutation/property corpus: satisfied
G5 Normalization consumer migration: satisfied
G6 Normalization installer removal proof: satisfied
G7 Packet/Safety helper-family decisions: incomplete
G8 adapter file retirement proof: blocked
```

Current decision:

```text
Normalization installer removal: complete
Packet installer removal: not started
adapter file retirement: blocked
adapter file removal: not performed
```

## 10. R1 / R1C boundaries

```text
canonical R1: spec/r1/r1-result-spec.md
R1C schema: kdsl-r1c@0.1-draft
Full R1 / R1C AST v2 checker migration: integrated
Full R1 whole-document scan compatibility: retained
semantic equivalence: not_proven
```

```text
RT:v=対象環境runtime確認済のみ
build/diff/lint/test/CI pass != RT:v
NEXT:=提案, 実行許可扱禁止
COMMIT:=実行済commitまたは推奨message, 自動commit許可扱禁止
未確認/未実行→確認済/実行済扱禁止
```

## 11. CompactPrompt boundaries

```text
standard: Goal/Input/Output/Guard/Check
kanji-v1: 目/材/出/守/確
AST v2 checker migration: integrated
CP-Lift/restricted-alias rules: unchanged
```

```text
implementation/repo/runtime/public/data/source-of-truth/AI coding trigger→CP-Lift
CP-Lift先:=profile:dev-prompt
KDSL-CP漢 alias:=構造KEY位置のみ
```

## 12. Safety Gate boundaries

```text
registry: kdsl-sg@0.1-draft
AST v2 checker migration: integrated
hold/blocked gate削除禁止
state:satisfied requires evidence and authority basis
baseline/composition/protected-wording unchanged
inheritance/graph semantics unchanged
```

## 13. Packet / Normalization boundaries

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
Registry/lint/validator/property/parity/contract/migration/removal pass != Packet executable
normalization preview != executable target
KDSL-Packet直接実行禁止
FLOW-CHANGE != edit authority
```

## 14. Safety and authority boundaries

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

## 15. Known gaps

```text
Packet helper-consumer contract/migration
Packet installer removal proof
Safety Gate inheritance/graph/optional helper decision
parity-only legacy helper strategy
legacy adapter file retirement proof
same-marker multi-envelope semantics
complete semantic equivalence proof
complete Safety Gate proof
canonical P1/P1L target schema
stable/public-ready U approval
```

## 16. Current positioning

Use as:

```text
KDSL v2-draft specification repository
R1 evidence/result-reporting specification
CompactPrompt architecture
experimental heuristic validator helpers
typed parser/AST v2 first slice
all active checker structural inputs migrated to AST v2 CompatibilityViews
Normalization checker/consumer/installer migration complete under bounded evidence
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

## 17. Next safe steps

```text
P0: Phase 6D-5 Packet helper-consumer contract inventory
P1: Packet consumer-specific mutation/property corpus
P2: Packet consumer migration before install_packet removal
P3: Safety Gate helper-family explicit decision
P4: adapter file retirement decision last
Hold: stable/public-ready/tag/release/Release Assets
```

Stop when:

```text
unknown helper consumer appears
existing checker/consumer exits change
RT/NEXT/COMMIT meaning changes
Packet/Normalization/Safety/CP-Lift boundaries weaken
unknown schema/default inference is required
```
