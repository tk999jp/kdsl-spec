# KDSL / R1 Project Status

status: canonical-project-status
last_updated: 2026-07-12
phase: phase5-public-hardening-complete
repository: tk999jp/kdsl-spec
default_branch: main

この文書は、`kdsl-spec` repository の現在状態を示す運用上の状態正本です。
仕様正本とfile責務は `spec/manifest.md` を参照します。

Phase 5以前の詳細なPR/CI履歴は次の非正本archiveへ保持します。

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
```

Policy:

```text
v0.1.0-draft tag:=履歴として維持
v1.1.0-rc1:=experimental historical baseline
v1.1.0 stable:=保留
v2-draft設計/validator改善:=継続
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

Legacy:

```text
rulebook:=v1.1 legacy profile name
rulebook新規使用禁止
rulebookを正式v2 profile扱い禁止
legacy rulebook入力→用途確認なしに他profileへ自動補正禁止
```

Named compositions:

```text
KDSL-CP:=profile:compact-prompt
KDSL-CP漢:=profile:compact-prompt + mode:dense + lexicon:kanji-v1
KDSL-R1:=envelope:result / KDSL_RESULT
KDSL-Packet:=v2-draft authoring envelope / non-executable
```

## 4. Integrated phase summary

### Foundation / v2 architecture

```text
CompactPrompt architecture: integrated
kanji-v1 lexicon: integrated
CP-Lift boundary: integrated
Validator CI baseline: integrated
Safety Gate Registry: v2-draft integrated
R1C serialization profile: v2-draft adopted / canonical R1 subordinate
Packet schema/registries: v2-draft adopted / non-executable
```

### Phase 1 — Common parser / unified validation

```text
pull_request: 38
squash_commit: 701c1c6901bdf471ce979513da6dd2f215fd3b58
status: integrated
unified_expectations: 147
failed: 0
```

### Phase 2 — Safety Semantics

```text
pull_request: 42
squash_commit: 66191b6b97bab720ffd14d5732aa6f5bc0d92a44
status: integrated
unified_expectations: 181
failed: 0
full_semantic_equivalence: not_proven
full_safety_proof: not_proven
```

### Phase 3 — R1C deep optional-block round-trip

```text
pull_request: 45
squash_commit: 24f08a4397f22555e73469099014b6ba502760c3
status: integrated
unified_expectations: 215
failed: 0
semantic_equivalence: not_proven
execution_authority: none
```

### Phase 4 — Packet / Normalization semantic properties

```text
pull_request: 48
squash_commit: 47b15f9af3496dc36e14673cf0a681e3c333b098
status: integrated
unified_expectations: 257
failed: 0
semantic_equivalence: not_proven
full_safety_proof: not_proven
normalization_completion: not_proven
execution_authority: none
```

### Phase 5 — Public-facing v2 hardening

```text
slice1_pull_request: 50
slice1_squash_commit: 49b6c865af046d44efc04a46d851aed55d222a61
slice1_workflow_run: 239 / success

slice2_pull_request: 51
slice2_squash_commit: 442d53226c7d0fd000ed1f93efc28ccbb367b129
slice2_workflow_run: 246 / success

closeout_pull_request: 52
status: public-facing hardening complete
```

Scope:

```text
Core/Profile/Glossary formal axes synchronization
Converter GitHub source priority / A-G / CP-Lift synchronization
public README / overview
R1 quickstart
public example separation and authority boundary
KDSL-DP normalization-path correction
public-readiness review
```

Decision:

```text
experimental preview documentation: ready
public repository navigation: ready
R1 introduction: ready
public examples: non-normative
public_ready: no
stable_release: no
```

## 5. Validator status

```yaml
validator:
  maturity: experimental_heuristic_helpers
  implementation: partial
  authority: non_authoritative
  workflow: .github/workflows/validator.yml
  workflow_name: KDSL Validation
  unified_command: python tools/validator/run_all_samples.py
  unified_expectations: 257
  failed: 0
  required_check_activation: pending
  required_check_issue: 39
```

Current wrapper targets:

```text
r1
prompt
compact
safety-gate
safety-semantics
r1c
packet
packet-semantic
normalization
all
```

Boundaries:

```text
validator未実行→pass扱禁止
validator pass != semantic equivalence
validator pass != complete safety proof
validator pass != U承認
validator pass != RT:v
validator pass != release readiness
workflow success != required-check activation
```

## 6. R1 / R1C status

```text
canonical R1: spec/r1/r1-result-spec.md
R1C schema: kdsl-r1c@0.1-draft
R1C status: v2-draft adopted serialization profile
R1C independent canonical spec: no
R1C stable: no
R1C full semantic equivalence: not_proven
```

Critical boundaries:

```text
RT:v=対象環境runtime確認済のみ
build/diff/lint/test/CI pass != RT:v
NEXT:=提案, 実行許可扱禁止
COMMIT:=実行済commitまたは推奨message, 自動commit許可扱禁止
```

## 7. Packet status

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

## 8. Safety and authority boundaries

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

## 9. Known gaps

```text
required KDSL Validation repository ruleset activation / issue #39
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

## 10. Current positioning

Use as:

```text
public experimental preview
safety-gate-preserving prompt notation draft
Human-AI work contract design
R1 evidence/result-reporting specification
CompactPrompt architecture
experimental heuristic validator helpers
```

Do not present as:

```text
stable standard
production-ready proof system
approval/runtime/release substitute
executable Packet specification
independent canonical R1C standard
```

## 11. Next safe steps

```text
P0: activate and verify required KDSL Validation check / issue #39
P1: continue semantic/parser/safety proof maturation as separate phases
Hold: stable/public-ready/tag/release/Release Assets
```

```text
NEXT:=proposal only
NEXT実行許可扱禁止
stable/public-ready化→別途U明示承認必須
```
