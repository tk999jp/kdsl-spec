# KDSL Packet Design Example

status: design-candidate example
canonical: no
executable: no

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
SRC:
  - "repository: tk999jp/example"
  - "branch: main"
READ:
  - "src/Example.cs"
  - "tests/ExampleTests.cs"
TGT:
  - "src/Example.cs"
  - "tests/ExampleTests.cs"
OBS:
  - "User reports duplicate entry after refresh"
  - "Root cause not yet confirmed"
GOAL: "Confirm the cause and apply the smallest safe correction within TGT"
NON:
  - "Broad refactor prohibited"
  - "Unrelated diff modification prohibited"
  - "Commit/push/release not authorized by this Packet"
SG:
  registry: kdsl-sg@0.1-draft
  entries:
    - id: SG-SCOPE
      state: hold
      scope: "TGT files"
      reason: "preflight and existing diff ownership not yet confirmed"
      evidence: "none"
      authority: "none"
    - id: SG-EVIDENCE
      state: hold
      scope: "duplicate entry cause"
      reason: "root cause not yet observed"
      evidence: "user observation only"
      authority: "not_required"
    - id: SG-AUTHORITY
      state: hold
      scope: "edit/stage/commit/push"
      reason: "operation-specific authority not established"
      evidence: "none"
      authority: "none"
    - id: SG-STOP
      state: satisfied
      scope: "unexpected diff or TGT expansion"
      reason: "stop conditions explicitly declared"
      evidence: "STOP block"
      authority: "not_required"
STOP:
  - "Unexpected tracked or untracked changes outside TGT"
  - "Root cause remains unconfirmed after inspection"
  - "Required change expands outside TGT"
FLOW:
  registry: kdsl-packet-flow@0.1-draft
  steps:
    - op: FLOW-READ
      detail: "Inspect exact SRC/READ references and repository state"
    - op: FLOW-ANALYZE
      detail: "Separate observed behavior from inferred causes"
    - op: FLOW-GATE
      detail: "Evaluate SG-SCOPE/SG-EVIDENCE/SG-AUTHORITY/SG-STOP"
    - op: FLOW-CHANGE
      detail: "Only after normalization and satisfied edit authority, change exact TGT"
    - op: FLOW-VERIFY
      detail: "Run declared static/tests; runtime remains separate"
    - op: FLOW-REPORT
      detail: "Return canonical R1C result without implying NEXT/COMMIT authority"
VERIFY:
  - "git diff --check"
  - "relevant tests"
  - "target runtime only when separately authorized and available"
OUT:
  result_schema: kdsl-r1c@0.1-draft
AUTHORITY:
  read: target_only
  edit: not_requested
  stage: not_requested
  commit: propose_only
  push: forbid
  release: forbid
NORMALIZE:
  required: true
  target: full-kdsl-dev-prompt
  state: not_normalized
```

Boundary:

```text
This example is not executable.
FLOW-CHANGE does not grant edit permission.
SG state records do not replace complete protected wording.
NORMALIZE.state:not_normalized means an executable Full KDSL prompt does not yet exist.
PKT:v1使用禁止.
```
