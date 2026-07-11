# KDSL Packet Schema v0.1 Draft Candidate

status: design-candidate
canonical: no
schema_id: kdsl-packet@0.1-draft
executable: no
normalization_required: yes

## 1. Purpose

This candidate defines a compact authoring envelope for development work contracts while preserving KDSL safety, evidence, authority, and result boundaries.

```text
KDSL-Packet:=authoring/transport candidate
KDSL-Packet != direct execution contract
KDSL-Packet != authority grant
KDSL-Packet != P1/P1L
KDSL-Packet != KDSL_RESULT
```

Priority:

```text
meaning/safety/evidence/authority > reversibility > compactness
```

## 2. Current boundary

```text
schema: kdsl-packet@0.1-draft
status: design-candidate
executable: no
PKT:v1使用禁止
AI coding tool直接投入禁止
normalization未完了→実行指示扱禁止
```

This candidate may be reviewed, linted, summarized, or normalized. It must not be executed as written.

## 3. Source-of-truth relation

```text
Core/Profile/R1/Bridge canonical meaning
> adopted Safety Gate/R1C mappings
> Packet candidate
> Packet lint candidate
> Example/Tool
```

Conflict handling:

```text
Packet×canonical source→canonical source優先
unknown schema/registry/ID→blocked
meaning conflict→Packet使用禁止 / Full KDSL or P1/P1Lへfallback
```

## 4. Required envelope

Required opening:

```text
PACKET_DRAFT:
SCHEMA: kdsl-packet@0.1-draft
STATUS: non-executable
```

Required field order:

```text
PACKET_DRAFT
SCHEMA
STATUS
BASE
TASK
SRC
READ
TGT
OBS
GOAL
NON
SG
STOP
FLOW
VERIFY
OUT
AUTHORITY
NORMALIZE
```

All required fields must be present. No implicit defaults are defined.

## 5. Candidate record shape

```yaml
PACKET_DRAFT:
SCHEMA: kdsl-packet@0.1-draft
STATUS: non-executable
BASE:
  registry: kdsl-packet-base@0.1-draft
  id: BASE-KDSL-DEV
TASK:
  registry: kdsl-packet-task@0.1-draft
  id: TASK-CHANGE
SRC: []
READ: []
TGT: []
OBS: []
GOAL: ""
NON: []
SG:
  registry: kdsl-sg@0.1-draft
  entries: []
STOP: []
FLOW:
  registry: kdsl-packet-flow@0.1-draft
  steps: []
VERIFY: []
OUT:
  result_schema: kdsl-r1c@0.1-draft
AUTHORITY:
  read: not_requested
  edit: not_requested
  stage: not_requested
  commit: not_requested
  push: forbid
  release: forbid
NORMALIZE:
  required: true
  target: full-kdsl-dev-prompt
  state: not_normalized
```

The example shape is illustrative. Registry adoption and Packet lint implementation are separate phases.

## 6. Field semantics

### 6.1 BASE

`BASE` selects a declared normalization baseline.

```text
BASE ID != permission
BASE ID != executable state
BASE ID != environment confirmation
```

Registry source candidate:

```text
spec/registry/kdsl-packet-base-registry.md
```

### 6.2 TASK

`TASK` selects one declared task class.

```text
TASK ID:=work classification
TASK ID != authority
TASK ID != completion claim
TASK ID != Safety Gate satisfaction
```

Registry source candidate:

```text
spec/registry/kdsl-packet-task-registry.md
```

### 6.3 SRC / READ / TGT

```text
SRC:=source-of-truth references supplied or confirmed
READ:=required inspection references
TGT:=allowed target scope
```

Rules:

```text
repo/path/file/branch/tag/API/command exact strings保持
unknown source-of-truth推測禁止
TGT外変更禁止
READ済扱い→実際の読取/evidence必要
```

### 6.4 OBS

`OBS` records observations available at authoring time.

```text
observed != inferred
unverified != confirmed
not_observed != absent
```

Packet authoring must not turn inference into observation.

### 6.5 GOAL / NON

```text
GOAL:=required outcome
NON:=explicit non-goals/prohibited scope
```

`NON` must retain D禁止, destructive-operation prohibitions, runtime separation, public-history protection, and other applicable safety boundaries.

### 6.6 SG

`SG` references the adopted Safety Gate Registry.

```text
registry: kdsl-sg@0.1-draft
```

Rules:

```text
SG ID:=supplemental reference
SG ID-only compression禁止
hold/blocked gate削除禁止
state:satisfied != unrelated authority
complete critical natural-language wording保持
```

### 6.7 STOP

`STOP` contains explicit stop conditions.

```text
STOP entry省略による継続許可推測禁止
stop発火→remaining change flow禁止
stop解除→evidence/authority再評価必須
```

### 6.8 FLOW

`FLOW` is an ordered list of declared flow opcodes plus explicit details.

```text
FLOW opcode != permission
FLOW opcode != command
FLOW opcode != success claim
```

Registry source candidate:

```text
spec/registry/kdsl-packet-flow-registry.md
```

Commands, paths, APIs, and exact operation details remain uncompressed strings in each step payload.

### 6.9 VERIFY

`VERIFY` describes required verification, not completed evidence.

```text
verify requirement != verify executed
validator/CI pass != RT:v
not_run→pass扱禁止
```

Executed verification belongs in R1/R1C output evidence.

### 6.10 OUT

`OUT.result_schema` selects the requested result serialization.

Candidate value:

```text
kdsl-r1c@0.1-draft
```

Rules:

```text
OUT selection != result success
R1C validator pass != semantic equivalence
R1C round-trip不成立→Full R1 fallback
NEXT/COMMIT authority境界保持
```

### 6.11 AUTHORITY

`AUTHORITY` remains explicit and operation-specific.

Candidate values align with canonical R1 authority vocabulary:

```text
allow|forbid|target_only|allow_once|propose_only|not_requested|not_applicable
```

Rules:

```text
read許可 != edit許可
edit許可 != stage/commit/push許可
commit許可 != push/release許可
NEXT/COMMIT.proposed != authority
Registry ID/opcode != authority
```

### 6.12 NORMALIZE

`NORMALIZE` prevents direct execution.

Required candidate shape:

```yaml
NORMALIZE:
  required: true
  target: design-only|full-kdsl-dev-prompt|P1|P1L
  state: not_normalized
```

Rules:

```text
required:=true固定
state:=not_normalized固定 in Packet candidate
state normalizedをPacket内で自己申告禁止
normalization artifactを別途生成/検証必須
KDSL-DP→P1/P1L正規化必須
```

## 7. Candidate invariants

```text
PACKET_DRAFT先頭固定
SCHEMA exact
STATUS:non-executable固定
all required fields保持
unknown registry/ID/opcode推測禁止
implicit default禁止
exact strings保持
Safety Gate保持
Authority分離保持
R1C result boundary保持
normalization前実行禁止
PKT:v1使用禁止
```

## 8. Round-trip and expansion

A valid Packet candidate must expand without inventing meaning to one of:

```text
design-only review artifact
Full KDSL profile:dev-prompt
ADPS normalization input followed by P1/P1L
```

Required preservation:

```text
source/read/target scope
observed vs inferred separation
goal/non-goals
all applicable Safety Gates and stop conditions
flow order and exact operation details
verify requirements
authority rails
result schema request
normalization target
```

When preservation cannot be guaranteed:

```text
Packet使用禁止
Full KDSLまたはP1/P1L authoringへfallback
```

## 9. High-risk handling

High-risk triggers include:

```text
rollback/revert/restore/clean/未push破棄
public/tag/release/Release Assets
migration/data deletion/schema change
runtime/RT:v claim
source-of-truth change
commit/push/destructive action
KDSL-DP/ADPS execution boundary
```

Required response:

```text
applicable SG entries必須
complete protected wording必須
exact AUTHORITY必須
explicit STOP必須
unknown/insufficient evidence→hold|blocked
```

## 10. Invalid conditions

```text
PKT:v1使用
STATUS executable相当
NORMALIZE.required != true
NORMALIZE.state != not_normalized
unknown BASE/TASK/FLOW/SG/R1C
missing required field
implicit permission/default
SG ID-only safety compression
TGT外operation
unexecuted VERIFYをpass扱
PacketからRT:vを自己認定
NEXT/COMMITをauthority扱
command/path/API alteration
```

Any invalid condition blocks Packet use.

## 11. Design-only example

See:

```text
examples/packet/packet-design.example.md
```

The example remains non-executable even when structurally valid.

## 12. Promotion gate

Before any adopted/canonical/executable promotion:

```text
manifest/Bridge/glossary ownership review
BASE/TASK/FLOW registry adoption review
Packet lint implementation
validator sample suite
normalization round-trip tests
Safety Gate completeness tests
Authority non-substitution tests
R1C output integration tests
U明示承認
```

## 13. Non-goals

```text
Packet直接実行
PKT:v1有効化
Core/R1/KDSL-DP境界変更
Safety Gate弱化
authority自動推測
command mini-language化
one-character opcode化
stable/public-ready化
tag/release/Release Assets操作
```
