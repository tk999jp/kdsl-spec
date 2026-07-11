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
READ:
  - "src/Example.cs"
TGT:
  - "src/Example.cs"
OBS:
  - "Duplicate entry observed after refresh"
GOAL: "Confirm the cause and apply a different correction"
NON:
  - "Broad refactor prohibited"
  - "Commit/push/release not authorized"
SG:
  registry: kdsl-sg@0.1-draft
  entries:
    - id: SG-SCOPE
      state: hold
      scope: "src/Example.cs"
      reason: "preflight pending"
    - id: SG-EVIDENCE
      state: hold
      scope: "root cause"
      reason: "cause not confirmed"
    - id: SG-AUTHORITY
      state: hold
      scope: "edit/stage/commit/push"
      reason: "authority not established"
    - id: SG-STOP
      state: satisfied
      scope: "unexpected diff"
      reason: "stop condition declared"
STOP:
  - "Unexpected diff outside TGT"
  - "Root cause remains unconfirmed"
FLOW:
  registry: kdsl-packet-flow@0.1-draft
  steps:
    - op: FLOW-READ
      detail: "Inspect exact READ references"
    - op: FLOW-ANALYZE
      detail: "Separate observation from inference"
    - op: FLOW-GATE
      detail: "Evaluate required Safety Gates"
    - op: FLOW-CHANGE
      detail: "Change exact TGT only after approved normalization and authority"
    - op: FLOW-VERIFY
      detail: "Run git diff --check and relevant tests"
    - op: FLOW-REPORT
      detail: "Return KDSL_RESULT using requested schema"
VERIFY:
  - "git diff --check"
  - "relevant tests"
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
