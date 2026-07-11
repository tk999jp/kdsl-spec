# KDSL / R1 Project Status

status: canonical-project-status
last_updated: 2026-07-11

この文書は、`kdsl-spec` repository の現在状態を示す運用上の状態正本です。
仕様正本は `spec/manifest.md` と `spec/core/*` / `spec/profiles/*` / `spec/r1/*` / `spec/lint/*` / `spec/bridge/*` / `spec/registry/*` を参照します。

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

## 2. Integrated workstreams

### PR #1 — v2 CompactPrompt architecture

```yaml
pull_request: 1
merge_method: squash
merge_status: merged
squash_commit: ae55f845018c0e8208d9e07c9814bc48035b2ef8
scope:
  - CompactPrompt profile
  - kanji-v1 lexicon
  - CompactPrompt lint
  - CP-Lift boundary
  - Packet draft-non-executable boundary
stable_effect: none
```

### PR #2 — CompactPrompt validator first slice

```yaml
pull_request: 2
merge_status: merged
squash_commit: c9e6dc5d8aaf4f5860fe2bab9d69247b41fc3b82
scope:
  - CompactPrompt structure/value lint
  - kanji-v1 alias lint
  - representative CP-Lift lint
  - wrapper target compact
```

### PR #3 — Validator CI baseline

```yaml
pull_request: 3
merge_status: merged
squash_commit: 8505c16b44b4a95892e8d2f3f44119a2ad31afde
workflow: .github/workflows/validator.yml
runner: ubuntu-latest
python: "3.11"
permissions: contents-read
command: python tools/validator/run_samples.py
```

### PR #4 — Safety Gate Registry v0.1 draft

```yaml
pull_request: 4
merge_status: merged
registry: kdsl-sg@0.1-draft
squash_commit: e1ab32e398751dcb5bc38bec8325aeded798d843
states:
  - hold
  - satisfied
  - blocked
  - na
ids:
  - SG-DESIGN
  - SG-SCOPE
  - SG-EVIDENCE
  - SG-RUNTIME
  - SG-AUTHORITY
  - SG-ROLLBACK
  - SG-PUBLIC
  - SG-DATA
  - SG-KDSL-DP
  - SG-STOP
stable_effect: none
```

### PR #5 — Safety Gate validator first slice

```yaml
pull_request: 5
merge_status: merged
squash_commit: 05773b4426481b783f2aeb55f1bcbcc50c17ee93
workflow_run_id: 29143048337
workflow_run_number: 33
workflow_conclusion: success
sample_total: 34
sample_failed: 0
```

### PR #6 — R1C compact-result design candidate

```yaml
pull_request: 6
merge_status: merged
merge_method: squash
source_head: d2460fa656d017963c34e382dddf4faa0248b68e
squash_commit: 34d95a78aa1012662b3f2f68aac678686c95bdf0
integration_record_commit: 24298c072aca75bba76da74766c66530e4649b83
schema_id: kdsl-r1c@0.1-draft
status: design_candidate_integrated
canonical: no
validator_at_merge: not_implemented
scope:
  - KDSL_RESULT envelope retained
  - canonical 11 required field names retained
  - JSON-compatible structured values
  - no short aliases
  - no implicit defaults
  - round-trip requirement
  - Full R1 fallback requirement
stable_effect: none
```

### PR #7 — R1C design-candidate validator first slice

```yaml
pull_request: 7
merge_status: merged
merge_method: squash
source_head: 7e79a4db2e8800f5ba73f6ea8318ebd2f3c5f0bc
squash_commit: 49957fe530d028738cea94d3b6ab1f473f8b176d
workflow: Validator CI
workflow_run_id: 29144196401
workflow_run_number: 50
workflow_status: completed
workflow_conclusion: success
sample_total: 49
sample_failed: 0
status: design_candidate_validator_integrated
canonical_effect: none
```

### PR #8 — R1C v2-draft ownership alignment

```yaml
pull_request: 8
merge_status: merged
merge_method: squash
source_branch: agent/kdsl-r1c-ownership
source_head: fbe92dd69125321977e3fbb971bed8fcc54edd39
base_commit: 4011599a5f3bbd81a97ac87fb3e2e6f0e90fe585
squash_commit: 87965cf7ff4284a2e53bc035ab38e611adc03287
closeout_pull_request: 9
schema_id: kdsl-r1c@0.1-draft
status: v2_draft_adopted_serialization_profile
canonical_parent: spec/r1/r1-result-spec.md
canonical_r1_replacement: none
packet_execution_effect: none
alignment_workflow_run_id: 29145044694
alignment_workflow_run_number: 67
alignment_job_conclusion: success
sample_total: 49
sample_failed: 0
substantive_ci_run_id: 29145390191
substantive_ci_run_number: 72
substantive_ci_conclusion: success
final_head_ci_run_id: 29145458879
final_head_ci_run_number: 74
final_head_ci_conclusion: action_required
final_head_ci_jobs: none
final_head_ci_note: workflow-history approval state; not a sample failure
stable_effect: none
```

### PR #10 — Packet registry and schema design candidate

```yaml
pull_request: 10
merge_status: merged
merge_method: squash
source_branch: agent/kdsl-packet-design
source_head: 5c8d16ed8f49e7263f870e95f928772b689f4137
squash_commit: 49cfdc665b4bf74e5324df019073aefbf786c383
schema_id: kdsl-packet@0.1-draft
base_registry: kdsl-packet-base@0.1-draft
task_registry: kdsl-packet-task@0.1-draft
flow_registry: kdsl-packet-flow@0.1-draft
status: design_candidate_integrated
executable: no
workflow_run_id: 29147274104
workflow_run_number: 78
workflow_conclusion: success
sample_total: 49
sample_failed: 0
stable_effect: none
```

### PR #11 — Packet v2-draft ownership alignment

```yaml
pull_request: 11
merge_status: pending
source_branch: agent/kdsl-packet-ownership
target_status: v2_draft_adopted_non_executable
canonical_effect: none
execution_effect: none
stable_effect: none
```

## 3. Current architecture direction

```text
v2-draft architecture:=main統合済み
CompactPrompt validator first slice:=main統合済み
Validator CI baseline:=main統合済み
Safety Gate Registry:=v2-draft integrated
Safety Gate validator first slice:=main統合済み
R1C design candidate:=main統合済み
R1C design-candidate validator first slice:=main統合済み
R1C ownership:=v2-draft adopted serialization profile
R1C canonical R1 replacement:=なし
Packet design candidate:=main統合済み
Packet ownership:=v2-draft adopted authoring schema/registries/lint
KDSL-Packet:=non-executable / normalization required
stable/tag/release/Release Assets操作:=別途U明示承認必須
```

## 4. R1C current status

```yaml
r1c:
  schema_id: kdsl-r1c@0.1-draft
  design_candidate: integrated
  v2_draft_adopted_serialization_profile: yes
  canonical_parent: spec/r1/r1-result-spec.md
  independent_canonical_spec: no
  stable: no
  envelope: KDSL_RESULT
  required_field_names: canonical R1 names retained
  structured_values: JSON-compatible inline arrays/objects
  short_aliases: prohibited
  implicit_defaults: prohibited
  round_trip_to_full_r1: required by candidate
  full_r1_fallback: required by candidate
  validator: first heuristic slice integrated
  manifest_bridge_glossary_alignment: integrated by PR #8
```

R1Cは現時点で、canonical R1を置換しません。

```text
canonical R1 > R1C v2-draft serialization profile
R1C validator pass != canonical R1適合証明
R1C adoption/validator存在 != Packet executable
```

## 5. Packet current status

```yaml
packet:
  schema_id: kdsl-packet@0.1-draft
  status: v2_draft_adopted
  canonical: v2_draft_only
  stable: no
  executable: no
  base_registry: kdsl-packet-base@0.1-draft
  task_registry: kdsl-packet-task@0.1-draft
  flow_registry: kdsl-packet-flow@0.1-draft
  lint: adopted
  validator: not_implemented
  normalize_required: true
  packet_state: not_normalized
  pkt_v1: prohibited
```

```text
Registry/opcode != authority
valid-looking/lint-looking != executable
normalization artifact未生成/未検証→実行禁止
KDSL-DP→P1/P1L正規化必須
```

## 6. Validator maturity

```yaml
validator:
  maturity: experimental_heuristic_helpers
  implementation: partial
  authority: non_authoritative
  wrapper_targets:
    - r1
    - prompt
    - compact
    - safety-gate
    - r1c
    - all
  current_main_scope:
    - KDSL_RESULT required block presence lint
    - RT:v basis wording heuristic lint
    - NEXT/COMMIT authority-shape heuristic lint
    - template reference/expansion evidence lint
    - CompactPrompt structure/value/alias/CP-Lift lint
    - Safety Gate registry/ID/state/field/composition lint
    - R1C schema/field/order/JSON shape lint
    - R1C VERIFY class separation lint
    - R1C RT/NEXT/COMMIT boundary lint
    - Full R1 fallback/out-of-scope separation
  ci:
    workflow: .github/workflows/validator.yml
    command: python tools/validator/run_samples.py
    expected_sample_total: 49
    latest_pr_validation:
      pull_request: 7
      run_id: 29144196401
      run_number: 50
      conclusion: success
```

Specified or designed but not fully implemented:

```text
protected wording semantic equivalence lint
Safety Gate parent-child inheritance lint
Safety Gate aggregate composite state calculation
full natural-language trigger context parser
R1C multi-line JSON parsing
R1C round-trip semantic proof
R1C optional EVIDENCE/AUTHORITY deep lint
Packet validator/sample matrix
Packet normalization transformer/round-trip proof
Packet Safety Gate completeness/inheritance proof
Packet OUT/R1C integration lint
```

## 7. Safety and authority boundaries

```text
意味保持 > safety gate保持
safety > high-risk判定 > mode > profile
KDSL-DP直接実行禁止
KDSL-DP→P1/P1L正規化必須
RT:v=対象環境runtime確認済のみ
build/diff/lint/test/CI pass != RT:v
KDSL_RESULT NEXT:=提案, 実行許可扱禁止
KDSL_RESULT COMMIT:=実行済commitまたは推奨message, 自動commit許可扱禁止
public履歴/公開済tag/Release Assets保護
unknown profile/mode/safety/lexicon/envelope/schema/registry/ID推測禁止
Registry ID != permission
state:satisfied != unrelated authority
hold/blocked gate削除禁止
SG ID-only compression禁止
R1C short field alias未定義
R1C required field省略禁止
R1C NEXT.authority:=proposal_only
R1C COMMIT.proposed != commit authority
KDSL-Packet直接実行禁止
PKT:v1使用禁止
```

Validator/CI boundaries:

```text
validator未実行→pass扱禁止
validator pass != U承認
validator pass != RT:v
validator pass != semantic equivalence
validator pass != safety proof
validator pass != execution authority
validator pass != release readiness
validator pass != canonical/stable promotion
CI pass != tag/release/Release Assets許可
```

## 8. Validation evidence

### CompactPrompt local verification

```yaml
date: 2026-07-11
environment: Windows PowerShell 5.1
sample_total: 23
failed: 0
compact_examples: 4/4 pass
worktree: clean
diff_check: pass
```

### Safety Gate validator

```yaml
pull_request: 5
workflow_run_id: 29143048337
run_number: 33
conclusion: success
sample_total: 34
failed: 0
```

### R1C design regression

```yaml
pull_request: 6
workflow_run_id: 29143936842
run_number: 41
conclusion: success
sample_total: 34
failed: 0
meaning: design-only regression evidence; not R1C lint pass
```

### Packet design candidate regression

```yaml
pull_request: 10
source_head: 5c8d16ed8f49e7263f870e95f928772b689f4137
workflow_run_id: 29147274104
run_number: 78
conclusion: success
sample_total: 49
failed: 0
meaning: existing validator regression evidence; not Packet lint pass
```

### R1C validator

```yaml
pull_request: 7
source_head: 7e79a4db2e8800f5ba73f6ea8318ebd2f3c5f0bc
workflow_run_id: 29144196401
run_number: 50
conclusion: success
sample_total: 49
failed: 0
repository_examples:
  - examples/r1c/r1c-success.example.md
  - examples/r1c/r1c-blocked.example.md
  - examples/r1c/r1c-needs-user.example.md
```

Verification records:

```text
tools/validator/verification/kdsl_compact_prompt_verify.md
tools/validator/verification/kdsl_safety_gate_verify.md
tools/validator/verification/kdsl_r1c_verify.md
docs/reviews/kdsl-r1c-design-integration.md
docs/reviews/kdsl-r1c-validator-first-slice.md
```

## 9. Known gaps before stable

```text
full YAML/JSON/KDSL parserなし
full natural-language semantic parserなし
full negation parserなし
protected wording semantic equivalence lintなし
Safety Gate parent-child inheritance lintなし
Safety Gate aggregate state lintなし
R1C round-trip semantic proofなし
Packet validator/sample matrix未実装
Packet normalization transformer/round-trip proofなし
Packet Safety Gate completeness/inheritance proofなし
KDSL-Packetはv2-draft adopted / non-executable
v2 public-facing overview未確定
CI required check/branch protection未設定
```

## 10. Recommended positioning

```text
Use as:
  experimental preview
  safety-gate-preserving prompt notation draft
  CompactPrompt architecture draft
  Safety Gate Registry v2-draft
  R1C v2-draft adopted compact serialization profile
  Packet v2-draft adopted non-executable authoring schema
  experimental heuristic validator helpers
  validator sample CI baseline

Do not present as:
  stable standard
  production-ready validator suite
  proof system
  approval/runtime/release substitute
  independent canonical R1C standard
  executable Packet specification
```

## 11. Next safe steps

```text
P0: PR #11 CI確認 / squash merge / ownership closeout
P1: Packet validator first slice / sample matrix
P2: Packet normalization round-trip tooling/tests
P3: Safety Gate protected wording/inheritance validator拡張
P4: R1C round-trip/property-based validator検討
P5: public-facing v2 overview / CI required check検討
Hold: v1.1.0 stable / tag / release / Release Assets
```
