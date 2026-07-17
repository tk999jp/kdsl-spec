# P1L Investigate Example

This example is explanatory and not a specification source.

```yaml
P1L:
SCHEMA: kdsl-p1l@0.1-draft
STATUS: contract-candidate
META:
  contract_rev: "0.1"
  contract_id: "example-investigate-001"
  parent_id: "none"
SOURCE:
  kind: manual
  digest: "sha256:0000000000000000000000000000000000000000000000000000000000000000"
  references:
    - "spec/bridge/kdsl-adps-bridge.md"
PROFILE:
  id: "none"
  revision: "none"
  digest: "none"
  completion: explicit
  completed_fields: []
TASK:
  kind: investigate
  declared: "investigate"
SCOPE:
  source:
    - "spec/bridge/kdsl-adps-bridge.md"
  read:
    - "spec/bridge/kdsl-adps-bridge.md"
  target: []
  non_target:
    - "implementation"
    - "runtime binding"
CONTEXT:
  background:
    - "Review the current KDSL-DP/P1/P1L boundary"
  observed: []
  inferred: []
  unverified:
    - "No runtime environment was inspected"
GOAL:
  expected:
    - "Report the current boundary without implementation"
  questions:
    - "Is direct KDSL-DP execution prohibited?"
PLAN:
  strategy:
    - "Read-only canonical review"
  steps:
    - "Read the Bridge"
    - "Separate authoring, normalization, binding, execution, and result states"
GUARD:
  constraints:
    - "KDSL-DP direct execution prohibited"
    - "Unknown profile/alias/preset inference prohibited"
  safety_gates: []
  protected_wording:
    - "未確認を確認済扱い禁止"
    - "P1/P1L valid != executable"
STOP:
  - "A required source cannot be read"
  - "An unknown schema meaning would need inference"
VERIFY:
  requirements:
    - "Compare the conclusion with spec/bridge/kdsl-adps-bridge.md"
  unavailable_policy: report_not_run
RUNTIME:
  disposition: not_applicable
  required_evidence: []
OUTPUT:
  result_schema: kdsl-r1c@0.1-draft
  report_requirements:
    - "NEXT remains proposal only"
    - "COMMIT remains non-authoritative"
AUTHORITY:
  read: target_only
  edit: forbid
  stage: forbid
  commit: propose_only
  push: forbid
  release: forbid
  public_repo: forbid
  destructive_ops: forbid
NORMALIZATION:
  state: explicit
  unresolved: []
  loss: []
  round_trip: not_tested
  semantic_equivalence: not_proven
BINDING:
  runtime_control: "unresolved"
  state: unbound
  executable: false
```

```text
structurally reviewable != executable
RT:not_applicable here is a contract disposition, not RT:v evidence
```
