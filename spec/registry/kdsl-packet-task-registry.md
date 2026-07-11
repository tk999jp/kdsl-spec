# KDSL Packet TASK Registry v0.1 Draft

status: v2-draft adopted
canonical: v2-draft
registry: kdsl-packet-task
version: 0.1-draft
executable_effect: none

## 1. Purpose

This v2-draft registry classifies intended work represented by KDSL-Packet authoring.

```text
TASK:=work-class reference
TASK != command
TASK != authority
TASK != completion claim
TASK != Safety Gate satisfaction
```

## 2. Current boundary

```text
registry: kdsl-packet-task@0.1-draft
status: v2-draft adopted
adopted: yes
stable/public-ready: no
Packet executable effect: none
unknown TASK ID推測禁止
```

## 3. Record model

Each TASK entry defines:

```text
id
purpose
minimum_flow
required_gates
authority_expectation
stop_expectation
non_substitutes
```

`required_gates` is additive. Specialized gates do not remove broader gates.

## 4. Adopted entries

### TASK-INSPECT

Purpose:

```text
read/inspect/compare/summarize without changing target state
```

Minimum flow:

```text
FLOW-READ/FLOW-ANALYZE/FLOW-REPORT
```

Required gates:

```text
SG-SCOPE
SG-EVIDENCE
SG-STOP
```

Authority expectation:

```text
read exact scope required
edit/stage/commit/push/release not implied
```

### TASK-PLAN

Purpose:

```text
phase/slice/design/implementation plan without target modification
```

Minimum flow:

```text
FLOW-READ/FLOW-ANALYZE/FLOW-GATE/FLOW-DECIDE/FLOW-REPORT
```

Required gates:

```text
SG-DESIGN when design/policy changes are proposed
SG-SCOPE
SG-EVIDENCE
SG-STOP
```

Non-substitutes:

```text
plan accepted-looking != U承認
NEXT proposal != execution authority
```

### TASK-CHANGE

Purpose:

```text
file/code/config/docs change within exact target scope
```

Minimum flow:

```text
FLOW-READ/FLOW-ANALYZE/FLOW-GATE/FLOW-CHANGE/FLOW-VERIFY/FLOW-REPORT
```

Required gates:

```text
SG-SCOPE
SG-EVIDENCE
SG-AUTHORITY
SG-STOP
SG-DESIGN when requirements/policy/source-of-truth changes
```

Authority expectation:

```text
edit exact target required
stage/commit/push separately evaluated
```

Stop expectation:

```text
unexpected diff/source/preflight mismatch→stop
TGT外変更必要→stop
```

### TASK-VERIFY

Purpose:

```text
build/diff/lint/test/CI/runtime verification or evidence review
```

Minimum flow:

```text
FLOW-READ/FLOW-GATE/FLOW-VERIFY/FLOW-REPORT
```

Required gates:

```text
SG-EVIDENCE
SG-STOP
SG-RUNTIME when runtime/RT:v is involved
SG-AUTHORITY when verification changes state or invokes restricted operations
```

Non-substitutes:

```text
build/diff/lint/test/CI pass != RT:v
validator pass != semantic equivalence/safety proof
```

### TASK-CLOSEOUT

Purpose:

```text
record final state, evidence, remaining risks, and result contract after completed work
```

Minimum flow:

```text
FLOW-READ/FLOW-GATE/FLOW-VERIFY/FLOW-REPORT
```

Required gates:

```text
SG-EVIDENCE
SG-AUTHORITY
SG-STOP
SG-RUNTIME when RT:v is claimed
```

Authority expectation:

```text
commit/push/release remain operation-specific
closeout report itself does not grant authority
```

### TASK-PUBLIC

Purpose:

```text
public history/tag/release/Release Assets/publication operation candidate
```

Minimum flow:

```text
FLOW-READ/FLOW-ANALYZE/FLOW-GATE/FLOW-DECIDE/FLOW-CHANGE/FLOW-VERIFY/FLOW-REPORT
```

Required gates:

```text
SG-PUBLIC
SG-AUTHORITY
SG-EVIDENCE
SG-SCOPE
SG-STOP
SG-DESIGN when release policy changes
```

Stop expectation:

```text
public target/permission/hash/assets未確認→stop
stable/public-ready未承認→stop
```

Non-substitutes:

```text
CI pass != release authority
existing tag != tag movement permission
```

### TASK-DATA

Purpose:

```text
data migration/schema/storage/destructive data operation candidate
```

Minimum flow:

```text
FLOW-READ/FLOW-ANALYZE/FLOW-GATE/FLOW-DECIDE/FLOW-CHANGE/FLOW-VERIFY/FLOW-REPORT
```

Required gates:

```text
SG-DATA
SG-ROLLBACK
SG-AUTHORITY
SG-EVIDENCE
SG-SCOPE
SG-STOP
SG-DESIGN when data contract changes
```

Stop expectation:

```text
backup/rollback/data ownership未確認→stop
irreversible effect未承認→stop
```

## 5. Selection rules

```text
TASK exactly one in v0.1 candidate
unknown ID→blocked
multiple task intentions→split Packet or choose dominant class with all gates
TASK classより危険なoperation検出→追加gate必須
TASK IDでFLOW/AUTHORITY/VERIFY省略禁止
```

## 6. Additive gate matrix

```text
TASK-INSPECT  → SG-SCOPE/SG-EVIDENCE/SG-STOP
TASK-PLAN     → SG-SCOPE/SG-EVIDENCE/SG-STOP + conditional SG-DESIGN
TASK-CHANGE   → SG-SCOPE/SG-EVIDENCE/SG-AUTHORITY/SG-STOP + conditional gates
TASK-VERIFY   → SG-EVIDENCE/SG-STOP + conditional SG-RUNTIME/SG-AUTHORITY
TASK-CLOSEOUT → SG-EVIDENCE/SG-AUTHORITY/SG-STOP + conditional SG-RUNTIME
TASK-PUBLIC   → SG-PUBLIC/SG-AUTHORITY/SG-EVIDENCE/SG-SCOPE/SG-STOP
TASK-DATA     → SG-DATA/SG-ROLLBACK/SG-AUTHORITY/SG-EVIDENCE/SG-SCOPE/SG-STOP
```

This matrix is a minimum, not a complete safety proof.

## 7. Compatibility

```text
new TASK ID追加→compatible candidate
existing TASK purpose/gate weakening→breaking/prohibited
required gate追加→compatible safety strengthening candidate
permission meaning追加→禁止
```

## 8. Promotion gate

```text
manifest/Bridge ownership review
TASK-FLOW compatibility lint
trigger-to-gate tests
Authority non-substitution tests
high-risk sample matrix
U明示承認
```

## 9. Non-goals

```text
individual command registry
project-specific task preset
success/status vocabulary
execution authority
automatic gate satisfaction
PKT:v1有効化
```
