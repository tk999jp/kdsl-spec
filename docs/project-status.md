# KDSL / R1 Project Status

status: canonical-project-status
last_updated: 2026-07-18
phase: phase9d-binding-evidence-schema-complete
repository: tk999jp/kdsl-spec
default_branch: main
tracking_issue: 132
verified_main_head: b4fbec0d0be3bd2a06bf61afa4cac0e409c19571

この文書は、`kdsl-spec` repository の現在状態を示す運用上の状態正本です。
仕様正本とfile責務は `spec/manifest.md` を参照します。
詳細証跡は `docs/reviews/*` と各validator implementation notesへ保持します。

## 1. Public / release state

```text
repository_visibility: public
published_release: v1.1.0-rc1
release_class: experimental_preview
public_ready: no
stable_release: none
Release Assets: none
license: MIT
```

```text
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
Packet/Normalization: spec/packet/*
R1: spec/r1/*
Lint: spec/lint/*
Bridge: spec/bridge/*
Registry: spec/registry/*
Runtime Control: spec/runtime/*
Glossary: spec/glossary.md / spec/glossary-v2-draft.md
```

```text
P1L:=spec/adps/kdsl-p1l-contract-schema.md
P1:=spec/adps/kdsl-p1-compact-contract-schema.md
Packet→P1L/P1:=spec/packet/kdsl-packet-p1-normalization-contract.md
P1L/P1 lint:=spec/lint/kdsl-p1-p1l-lint.md
Packet→P1L/P1 lint:=spec/lint/kdsl-packet-p1-normalization-lint.md
K1:=spec/runtime/kdsl-k1-runtime-kernel-schema.md
PF1:=spec/runtime/kdsl-pf1-project-profile-schema.md
K1/PF1 lint:=spec/lint/kdsl-k1-pf1-lint.md
Binding evidence:=spec/runtime/kdsl-binding-evidence-schema.md
Binding evidence lint:=spec/lint/kdsl-binding-evidence-lint.md
validator結果:=非権威的heuristic evidence
```

## 3. Architecture and boundaries

```text
KDSL:=LLM直投入可能な安全gate保持型半構造化prompt記法
KDSL-DP:=ADPS authoring form / direct execution prohibited
P1L:=lossless structured normalized contract / non-executable
P1:=P1L subordinate reversible compact serialization / non-executable
KDSL-Packet:=non-executable authoring/transport envelope
R1/KDSL_RESULT:=execution evidence/result reporting
```

```text
KDSL-DP直接実行禁止
KDSL-DP→P1L/P1正規化必須
P1L/P1 valid|lint|round-trip pass != executable|authority
Packet valid|property pass != normalized|executable
build/diff/lint/test/CI pass != RT:v
NEXT:=提案, 実行許可扱禁止
COMMIT:=実行済commitまたは推奨message, 自動commit許可扱禁止
```

## 4. Integrated phase summary

```text
Foundation / v2 architecture: integrated
Phase 1 Common parser / unified validation: integrated
Phase 2 Safety Semantics: integrated bounded slice
Phase 3 R1C optional-block round-trip: integrated
Phase 4 Packet / Normalization semantic properties: integrated
Phase 5 Public-facing v2 hardening: complete
Phase 6 Semantic Parser Foundation / adapter retirement: complete
Phase 7A P1/P1L ownership and contract design: integrated
Phase 7B canonical P1L/P1 schema/lint/examples/alignment: integrated
Phase 7C P1L/P1 parser/validator/round-trip first slice: integrated
Phase 7D Packet→P1L/P1 target-specific normalization preview: integrated
Phase 7D manifest/glossary/index/review/status alignment: integrated
Phase 7 canonical P1/P1L contract scope: complete
Phase 8 shared AST v2 P1L first-class integration: complete
Phase 9A K1/PF1 runtime-control design: complete
Phase 9B K1/PF1 schema/lint/examples: complete
Phase 9C K1/PF1 parser/validator compatibility first slice: complete
Phase 9D binding-evidence schema/lint/example: complete
```

## 5. Repository enforcement

```text
ruleset: Protect main with KDSL Validation
ruleset_id: 18832171
status: active
PR required: yes
merge method: squash
required check: KDSL Validation
branch up-to-date: required
force push: blocked
deletions: restricted
```

## 6. Latest verified design / implementation

Phase 9D schema proof:

```text
PR: 142
source head: dc090a26593e920a550545957dce092e6fed1e7d
squash commit: b4fbec0d0be3bd2a06bf61afa4cac0e409c19571
workflow run: 29639314207 / #524
KDSL Validation: success
Packet Semantic Property: success
Packet P1 Normalization Property: success
scope: binding-evidence schema/lint/example/canonical alignment
binding-evidence parser/validator/evaluator: not implemented
```

Phase 9C validator proof:

```text
PR: 137
source head: 0b66ba14279063c2069591569482ce96b0251a42
squash commit: c2d6e8be0e8f54b73db6ba410ada1b93260c70cb
workflow run: 29636378733 / #500
KDSL Validation: success
Packet Semantic Property: success
Packet P1 Normalization Property: success
focused runtime-control corpus: 16 / failed 0
scope: bounded parser/validator/canonical digest/exact K1-PF1 compatibility
runtime binding: not implemented
```

Phase 9B schema proof:

```text
PR: 135
source head: 63980b24c106ee0a62c13c9f7d56100d95bcd8aa
squash commit: f779ce38e9e37fafec4de72832edd138a5da7bbc
workflow run: 29634153852 / #489
KDSL Validation: success
Packet Semantic Property: success
Packet P1 Normalization Property: success
scope: schema/lint/examples/canonical alignment
K1/PF1 resolver/parser/validator: not implemented
```

Phase 9A design proof:

```text
PR: 133
source head: b0ec16600686b1b372ab71236df794e03ee23267
squash commit: d65c6eae6947b251246946bfafb9e51636efb145
workflow run: 29630096451 / #465
KDSL Validation: success
Packet Semantic Property: success
Packet P1 Normalization Property: success
scope: design documents only
```

Phase 8 implementation proof:

```text
PR: 129
source head: 3285995a4c31c749537e190956f53c38bf35c627
squash commit: a9e27531b7dc2d9bca68de5284a76616956a7242
workflow run: 29613070208 / #449
KDSL Validation: success
Packet Semantic Property: success
Packet P1 Normalization Property: success
Phase 8 shared P1L compatibility corpus: 10 / failed 0
```

Phase 8 closeout proof:

```text
PR: 130
source head: 9613cc1d4943da9be446104dd740f705d3dd5b97
squash commit: cdb907d139bf562bc6cca9c4fdb436d12d802ea6
workflow run: 29613621345 / #455
KDSL Validation: success
Packet Semantic Property: success
Packet P1 Normalization Property: success
```

Phase 7 Packet→P1L/P1 implementation proof:

```text
PR: 125
squash commit: 222b8483ec12e09d5316a7124f3f611dbb5e507c
workflow run: 29585279349 / #433
all required jobs: success
```

Closeout alignment proof:

```text
PR: 126
source head: e6061bf730ebfe1b5eeb45582e03f8c30181f99d
squash commit: 729f2000e1341dd9624f5d0f60cb9c0abcf040f0
workflow run: 29592332244 / #435
KDSL Validation: success
Packet Semantic Property: success
Packet P1 Normalization Property: success
preservation audit: pass-with-correction
canonical glossary: unchanged from verified pre-closeout main
```

Verified current additions:

```text
P1L/P1 contract corpus: 14 / failed 0
P1L shared AST compatibility corpus: 10 / failed 0
Packet→P1L/P1 normalization corpus: 17 / failed 0
K1/PF1 runtime-control corpus: 16 / failed 0
unified runners: 39
unified expectations: 499 / failed 0
```

Corrective record:

```text
Phase 7C run #426 failed→legacy colon classification correction→run #427 success
Phase 7D run #430/#431 unified failure→legacy structural helper import detected
property checker migrated to NormalizationCompatibilityView→run #433 all jobs success
Phase 7 closeout audit detected canonical glossary over-compression→canonical glossary restored / v2 detailed terms preserved→run #435 success
Phase 8 branch diagnostics exposed runner self-match/newline/indentation generation defects before commit→clean runner generation and final cleanup→run #449 success
Phase 9A design self-audit separated authority from capability and reduced unresolved schema decisions to five
Phase 9B adoption self-audit removed digest self-reference and separated approval content integrity from source verification before merge
Phase 9C shared-parser registration was validated before storage; final parser diff added only K1/PF1 markers
Phase 9D self-audit separated bound state from authority/capability sufficiency and aligned candidate/adopted status before merge
```

```text
validator/property/CI pass != semantic equivalence
validator/property/CI pass != complete safety proof
validator/property/CI pass != runtime binding
validator/property/CI pass != execution authority
validator/property/CI pass != RT:v
validator/property/CI pass != release readiness
```

## 7. P1L / P1 state

```text
P1L schema: kdsl-p1l@0.1-draft / adopted v2-draft
P1 schema: kdsl-p1@0.1-draft / adopted subordinate serialization
P1L/P1 parser/validator: first bounded slice integrated
P1L→P1→P1L structural round-trip: integrated first slice
shared AST v2 P1L marker registration: first-class integrated / bootstrap removed / compatibility corpus 10 failed 0
runtime binding: not implemented
K1/PF1 canonical schema: adopted v2-draft
K1/PF1 parser/validator: bounded first slice integrated
K1/PF1 exact compatibility: id/revision/digest/project_scope/contract_schemas
Binding evidence schema: kdsl-binding-evidence@0.1-draft / adopted v2-draft
Binding evidence parser/validator/evaluator: not implemented
P1L runtime_control reference: compact JSON schema/id/revision/digest
BINDING.state: unbound
BINDING.executable: false
```

Required authority rails:

```text
read/edit/stage/commit/push/release/public_repo/destructive_ops
```

Legacy boundary:

```text
project-local colon P1:=legacy operational evidence
loss=P→exact compatibility evidence時のみprofile_completed候補
loss=L意味推測禁止
AP/H意味推測禁止
missing Authority rails→canonical promotion blocked
```

## 8. Packet→P1L/P1 normalization state

Integrated target-specific path:

```text
BASE: BASE-ADPS-P1
NORMALIZE.target: P1L|P1
TARGET.resolution: resolved
TARGET.executable: false
OUTPUT.marker: P1L_PREVIEW|P1_PREVIEW
SOURCE.packet_status: non-executable
SOURCE.normalize_state: not_normalized
ROUND_TRIP.structural_equivalence: pass
ROUND_TRIP.semantic_equivalence: not_proven
AUTHORITY.execution_authority: none
```

Preview boundary:

```text
P1L_PREVIEW != P1L:
P1_PREVIEW != P1|
normalization preview != executable target
```

Authority mapping:

```text
read/edit/stage/commit/push/release:=source rails copied exactly
public_repo:=forbid
destructive_ops:=forbid
```

The two added rails are explicit non-widening safety floors, not hidden defaults or permission grants.

Parser ownership:

```text
Packet P1 property checker uses NormalizationCompatibilityView
legacy normalization structural helper consumers: none
P1L shared parser registration: first-class integrated
P1L checker-local bootstrap consumers: none
shared parser adapter retirement remains complete
```

## 9. Phase 7 completion interpretation

Completed:

```text
P1L/P1 ownership and contract design
canonical P1L structured schema
canonical subordinate P1 serialization
P1L/P1 lint and examples
P1L/P1 bounded parser/validator/round-trip first slice
Packet→P1L/P1 target-specific mapper/property
P1L_PREVIEW/P1_PREVIEW non-executable boundary
manifest/glossary/index/review/status alignment
preservation audit and canonical glossary restoration
```

Not included:

```text
Packet normalized-state promotion
P1L/P1 runtime binding
K1/PF1 canonical runtime-control schema
executable transformer
AI coding tool direct execution from P1L/P1/preview
complete semantic equivalence
complete natural-language interpretation
complete safety proof
stable/public-ready promotion
```

## 10. Current positioning

Use as:

```text
KDSL v2-draft specification repository
R1 evidence/result-reporting specification
CompactPrompt architecture
typed AST v2 structural foundation
P1L shared first-class AST envelope recognition
P1L canonical v2-draft structured contract schema
P1 subordinate compact serialization
P1L/P1 bounded validator/round-trip first slice
Packet→P1L/P1 non-executable preview normalization first slice
K1/PF1 non-executable runtime-control design
K1/PF1 canonical schema/lint/manual examples
K1/PF1 bounded non-executable validator/compatibility first slice
Binding-evidence canonical schema/lint/non-executable example
experimental heuristic validator helpers
```

Do not present as:

```text
stable KDSL release
public-ready guarantee
P1L/P1 executable runtime contract
K1/PF1 executable runtime contract
Binding-evidence parser/evaluator and runtime binding implementation
Packet normalized/executable runtime contract
semantic equivalence proof
complete safety proof
complete semantic parser
```

## 11. Next safe steps

```text
P0: Phase 9E binding-evidence parser/validator first slice only under separate approval
P1: future P1L→K1/PF1 binding evaluator only under separate approval
Hold: runtime binding/executable promotion/stable/public-ready/tag/release/Release Assets
```

Stop when:

```text
unknown legacy alias/profile/preset meaning must be inferred
critical authority rail becomes implicit
profile defaults lack exact revision/digest evidence
P1 round-trip loses protected wording or exact strings
preview emits canonical executable-looking P1L:/P1| marker
Packet source becomes normalized/executable
RT/NEXT/COMMIT meaning changes
Packet/Normalization/Safety/CP-Lift boundaries weaken
```
