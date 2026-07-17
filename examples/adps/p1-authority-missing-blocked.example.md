# P1L Authority-Missing Blocked Example

This example is intentionally invalid because authority is implicit and incomplete.

```yaml
P1L:
SCHEMA: kdsl-p1l@0.1-draft
STATUS: contract-candidate
META:
  contract_rev: "0.1"
  contract_id: "blocked-authority-001"
  parent_id: "none"
SOURCE:
  kind: manual
  digest: "sha256:4444444444444444444444444444444444444444444444444444444444444444"
  references: []
PROFILE:
  id: "none"
  revision: "none"
  digest: "none"
  completion: explicit
  completed_fields: []
TASK:
  kind: implement
  declared: "implement"
SCOPE:
  source: []
  read:
    - "src/Feature.cs"
  target:
    - "src/Feature.cs"
  non_target:
    - "release"
CONTEXT:
  background: []
  observed: []
  inferred: []
  unverified: []
GOAL:
  expected:
    - "Change the target file"
  questions: []
PLAN:
  strategy: []
  steps:
    - "Edit src/Feature.cs"
    - "Commit and push"
GUARD:
  constraints: []
  safety_gates: []
  protected_wording: []
STOP: []
VERIFY:
  requirements: []
  unavailable_policy: report_not_run
RUNTIME:
  disposition: pending
  required_evidence: []
OUTPUT:
  result_schema: kdsl-r1c@0.1-draft
  report_requirements: []
AUTHORITY:
  read: allow
  edit: target_only
  commit: allow_once
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

Blocked reasons:

```text
stage/push/release/public_repo/destructive_ops rails missing
PLAN includes commit/push but PLAN != authority
commit allow_once does not imply push
protected wording and Stop conditions are absent for a write contract
NORMALIZATION.state cannot remain explicit when critical authority is unresolved
```

Required handling:

```text
missing Authority rail→blocked
NORMALIZATION.state:blocked
BINDING.state:blocked|unbound
BINDING.executable:false
```
