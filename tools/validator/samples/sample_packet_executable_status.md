PACKET_DRAFT:
SCHEMA: kdsl-packet@0.1-draft
STATUS: executable
BASE:
  registry: kdsl-packet-base@0.1-draft
  id: BASE-KDSL-DEV
TASK:
  registry: kdsl-packet-task@0.1-draft
  id: TASK-CHANGE
SRC:
  - "repository: tk999jp/example"
READ:
  - "src/Example.cs"
TGT:
  - "src/Example.cs"
OBS:
  - "Duplicate entry observed"
GOAL: "Apply the smallest safe correction"
NON:
  - "Broad refactor prohibited"
SG:
  registry: kdsl-sg@0.1-draft
  entries:
    - id: SG-SCOPE
      state: hold
      scope: target
      reason: pending
    - id: SG-EVIDENCE
      state: hold
      scope: cause
      reason: pending
    - id: SG-AUTHORITY
      state: hold
      scope: edit
      reason: pending
    - id: SG-STOP
      state: satisfied
      scope: stop
      reason: declared
STOP:
  - "Unexpected diff"
FLOW:
  registry: kdsl-packet-flow@0.1-draft
  steps:
    - op: FLOW-READ
      detail: "Read"
    - op: FLOW-ANALYZE
      detail: "Analyze"
    - op: FLOW-GATE
      detail: "Gate"
    - op: FLOW-CHANGE
      detail: "Change after normalization"
    - op: FLOW-VERIFY
      detail: "Verify"
    - op: FLOW-REPORT
      detail: "Report"
VERIFY:
  - "git diff --check"
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
