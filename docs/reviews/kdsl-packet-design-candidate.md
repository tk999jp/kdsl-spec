# KDSL Packet Design Candidate Review

status: design-candidate
review_date: 2026-07-11
branch: agent/kdsl-packet-design
target: main
canonical_effect: none
execution_effect: none

## 1. Scope

```text
spec/packet/kdsl-packet-schema.md
spec/registry/kdsl-packet-base-registry.md
spec/registry/kdsl-packet-task-registry.md
spec/registry/kdsl-packet-flow-registry.md
spec/lint/kdsl-packet-lint.md
examples/packet/README.md
examples/packet/packet-design.example.md
spec/registry/README.md
```

## 2. Selected model

```text
schema: kdsl-packet@0.1-draft
BASE registry: kdsl-packet-base@0.1-draft
TASK registry: kdsl-packet-task@0.1-draft
FLOW registry: kdsl-packet-flow@0.1-draft
status: design-candidate
executable: no
normalization required: yes
```

Packet is an authoring/transport candidate. It does not replace Full KDSL, KDSL-DP, P1/P1L, or R1/R1C.

## 3. Required field model

```text
PACKET_DRAFT/SCHEMA/STATUS
BASE/TASK
SRC/READ/TGT/OBS/GOAL/NON
SG/STOP/FLOW/VERIFY
OUT/AUTHORITY/NORMALIZE
```

The field model preserves the existing Bridge draft vocabulary while making safety, authority, and normalization explicit.

## 4. Registry rationale

### BASE

Separates normalization destination from task intent.

```text
BASE-DESIGN-ONLY
BASE-KDSL-DEV
BASE-ADPS-P1
```

### TASK

Classifies risk and minimum Safety Gate composition.

```text
TASK-INSPECT
TASK-PLAN
TASK-CHANGE
TASK-VERIFY
TASK-CLOSEOUT
TASK-PUBLIC
TASK-DATA
```

### FLOW

Defines semantic order without replacing commands or granting permission.

```text
FLOW-READ
FLOW-ANALYZE
FLOW-GATE
FLOW-DECIDE
FLOW-CHANGE
FLOW-VERIFY
FLOW-REPORT
FLOW-STOP
FLOW-ASK
```

## 5. Safety decisions

Adopted in the candidate:

```text
STATUS:non-executable固定
NORMALIZE.required:true固定
NORMALIZE.state:not_normalized固定
PKT:v1使用禁止
unknown registry/ID/opcode推測禁止
Registry/opcode != authority
SG ID-only compression禁止
hold/blocked gate削除禁止
exact command/path/API strings保持
build/diff/lint/test/CI pass != RT:v
NEXT/COMMIT authority separation保持
KDSL-DP→P1/P1L正規化必須
```

## 6. Rejected alternatives

### Executable `PKT:v1`

Rejected because schema/registry/lint/normalization proof are not mature or adopted.

### One-character opcodes

Rejected because identity and safety semantics become difficult to review and lint.

### Implicit defaults

Rejected because missing scope, authority, gates, or normalization state could be interpreted as permission.

### Registry IDs as permission presets

Rejected because classification and authority must remain orthogonal.

### Commands encoded as opcodes

Rejected because exact command/path/API preservation is mandatory.

### Packet self-declared normalization success

Rejected because normalization must create and validate a separate target artifact.

## 7. Compatibility classification

```text
new design candidate files: compatible experimental addition
canonical Core/Profile/R1/Bridge change: none
adopted registry change: none
stable/public-ready change: none
Packet execution change: none
```

## 8. Split-phase decision

This PR is design-only.

Separate future phases:

```text
P1: manifest/Bridge/glossary ownership adoption review
P2: Packet validator first slice and sample runner integration
P3: normalization round-trip tooling/tests
P4: executable promotion review, only after explicit approval
```

The design and validator are separated so an unadopted schema cannot self-validate into authority.

## 9. Merge gate

```text
existing Validator CI regression: total 49 / failed 0
new files reviewed for protected wording and boundary preservation
no workflow changes
no validator implementation
squash merge
post-merge project-status closeout
```

## 10. Non-actions

```text
Packet adopted/canonical/executable化なし
PKT:v1有効化なし
canonical R1変更なし
KDSL-DP/P1/P1L境界変更なし
tag/release/Release Assets操作なし
stable/public-ready化なし
source branch削除なし
```
