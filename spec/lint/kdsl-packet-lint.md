# KDSL Packet Lint v0.1 Draft Candidate

status: design-candidate
canonical: no
validator: not implemented
scope: kdsl-packet@0.1-draft / BASE / TASK / FLOW

## 1. Purpose

This candidate defines semantic and structural checks for Packet design artifacts.

```text
lint pass != executable
lint pass != normalization complete
lint pass != authority
lint pass != safety proof
lint pass != semantic equivalence
```

## 2. Detection

In scope when the document contains:

```text
PACKET_DRAFT:
SCHEMA: kdsl-packet@0.1-draft
```

Out of scope:

```text
Full KDSL
KDSL-DP
P1/P1L
KDSL_RESULT/R1C
KDSL-CP
```

Mixed envelopes without an explicit bridge are errors.

## 3. Required envelope checks

Errors:

```text
PACKET_DRAFT not first significant line
SCHEMA missing or unknown
STATUS missing
STATUS != non-executable
PKT:v1 present
executable/ready/run/direct-execute state present
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

Missing, duplicate, or reordered required fields are errors in v0.1 candidate.

## 4. Registry checks

### BASE

```text
registry must equal kdsl-packet-base@0.1-draft
known IDs:
  BASE-DESIGN-ONLY
  BASE-KDSL-DEV
  BASE-ADPS-P1
unknown ID→error
multiple IDs→error
```

### TASK

```text
registry must equal kdsl-packet-task@0.1-draft
known IDs:
  TASK-INSPECT
  TASK-PLAN
  TASK-CHANGE
  TASK-VERIFY
  TASK-CLOSEOUT
  TASK-PUBLIC
  TASK-DATA
unknown ID→error
multiple IDs→error
```

### FLOW

```text
registry must equal kdsl-packet-flow@0.1-draft
known opcodes:
  FLOW-READ
  FLOW-ANALYZE
  FLOW-GATE
  FLOW-DECIDE
  FLOW-CHANGE
  FLOW-VERIFY
  FLOW-REPORT
  FLOW-STOP
  FLOW-ASK
unknown opcode→error
one-character opcode→error
```

### SG / OUT

```text
SG.registry must equal kdsl-sg@0.1-draft
OUT.result_schema must be kdsl-r1c@0.1-draft or explicit Full R1 request
unknown SG/R1C→error
```

Registry ID presence never satisfies authority or safety wording checks.

## 5. Non-execution and normalization checks

Required:

```text
NORMALIZE.required:true
NORMALIZE.state:not_normalized
NORMALIZE.target one of:
  design-only
  full-kdsl-dev-prompt
  P1
  P1L
```

Errors:

```text
required false/missing
state normalized/executable/ready
Packet self-claims successful normalization
BASE and NORMALIZE.target mismatch
AI coding tool direct execution instruction
```

Mappings:

```text
BASE-DESIGN-ONLY → design-only
BASE-KDSL-DEV → full-kdsl-dev-prompt
BASE-ADPS-P1 → P1|P1L
```

## 6. Required content checks

```text
GOAL non-empty
SRC/READ/TGT/OBS/NON/STOP/VERIFY arrays or declared structured values
FLOW.steps present
AUTHORITY all operation rails explicit
```

Warnings:

```text
SRC empty for source-dependent task
READ empty for TASK-CHANGE/TASK-VERIFY
TGT empty for state-changing task
OBS empty while causal claim exists
NON empty for high-risk task
STOP empty for TASK-CHANGE/TASK-PUBLIC/TASK-DATA
VERIFY empty for TASK-CHANGE/TASK-VERIFY/TASK-CLOSEOUT
```

## 7. Safety Gate minimum checks

Minimum matrix:

```text
TASK-INSPECT:
  SG-SCOPE/SG-EVIDENCE/SG-STOP

TASK-PLAN:
  SG-SCOPE/SG-EVIDENCE/SG-STOP
  + SG-DESIGN when requirements/policy/source-of-truth changes

TASK-CHANGE:
  SG-SCOPE/SG-EVIDENCE/SG-AUTHORITY/SG-STOP
  + conditional gates

TASK-VERIFY:
  SG-EVIDENCE/SG-STOP
  + SG-RUNTIME for runtime/RT:v
  + SG-AUTHORITY for restricted/state-changing verify

TASK-CLOSEOUT:
  SG-EVIDENCE/SG-AUTHORITY/SG-STOP
  + SG-RUNTIME when RT:v claimed

TASK-PUBLIC:
  SG-PUBLIC/SG-AUTHORITY/SG-EVIDENCE/SG-SCOPE/SG-STOP

TASK-DATA:
  SG-DATA/SG-ROLLBACK/SG-AUTHORITY/SG-EVIDENCE/SG-SCOPE/SG-STOP
```

Errors:

```text
required SG missing
hold/blocked gate omitted from summary/view
SG ID-only critical safety wording
state:satisfied without required evidence/authority
specialized gate used to remove broader gate
```

## 8. Trigger checks

Representative trigger-to-gate requirements:

```text
rollback/revert/restore/clean/未push破棄→SG-ROLLBACK
runtime/実機/RT:v→SG-RUNTIME
public/tag/release/Release Assets→SG-PUBLIC
migration/data delete/schema/storage→SG-DATA
commit/push/edit/destructive→SG-AUTHORITY
requirement/policy/source-of-truth change→SG-DESIGN
KDSL-DP/ADPS/P1/P1L→SG-KDSL-DP
```

Natural-language trigger parsing is heuristic until a validator exists.

## 9. FLOW sequencing checks

Errors:

```text
FLOW-CHANGE before FLOW-GATE
FLOW-CHANGE without compatible TASK
FLOW-CHANGE after FLOW-STOP
FLOW-CHANGE dependent on unresolved FLOW-ASK
FLOW-REPORT before required VERIFY classification
empty detail
opcode used as command replacement
```

Warnings:

```text
FLOW-ANALYZE missing before causal change
FLOW-DECIDE missing for approved design alternative
FLOW-REPORT missing as terminal step
```

## 10. Authority checks

Required rails:

```text
read
edit
stage
commit
push
release
```

Errors:

```text
implicit/missing authority value
BASE/TASK/FLOW/SG treated as permission
read authority expanded to edit
edit expanded to stage/commit/push
commit proposed treated as commit permission
NEXT treated as execution permission
release not forbid/not_requested for non-public task without basis
```

## 11. Evidence and verification checks

Errors:

```text
READ済 claim without evidence
OBS inference recorded as observation
VERIFY requirement recorded as completed pass
build/diff/lint/test/CI pass treated as RT:v
Packet self-reports success/completion
```

Warnings:

```text
high-risk claim without evidence references
runtime not applicable without reason
```

## 12. Exact-string checks

Must remain exact:

```text
repo names
paths
branches
tags
commit hashes
commands
package/class/method/property/API names
file names/extensions
URLs
Windows paths
```

Transformation or abbreviation is an error.

## 13. Result integration checks

```text
OUT selection != result success
R1C required field/RT/NEXT/COMMIT meanings remain canonical
R1C round-trip uncertain→Full R1 fallback declared
Packet NEXT/COMMIT authority shortcuts prohibited
```

## 14. Validator boundary

Current state:

```text
Packet validator: not implemented
sample runner coverage: not implemented
Packet lint pass claim: prohibited until implementation/execution evidence
```

Future validator success will still not prove:

```text
semantic equivalence
safety completeness
normalization correctness
RT:v
U approval
execution authority
release readiness
```

## 15. Promotion checks

Before adopted/canonical/executable promotion:

```text
manifest/Bridge/glossary ownership alignment
registry ID freeze
Packet parser/lint implementation
positive/negative sample matrix
normalization round-trip tests
Safety Gate inheritance/composition tests
Authority non-substitution tests
R1C integration tests
U明示承認
```
