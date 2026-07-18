# Binding Evidence — Non-Executable Example

status: explanatory-only
schema: kdsl-binding-evidence@0.1-draft

This example illustrates field relationships. Placeholder digests are not canonical identity proof.

```yaml
BINDING_EVIDENCE:
SCHEMA: kdsl-binding-evidence@0.1-draft
STATUS: external-content-addressed-record
IDENTITY:
  id: kdsl.reference.binding.docs-review
  revision: 0.1.0
  canonicalization: kdsl-runtime-control-c14n@0.1-draft
  digest: "sha256:<record-digest>"
  source_ref: "example:binding-evidence-non-executable"
SUBJECT:
  contract_schema: kdsl-p1l@0.1-draft
  contract_id: docs-review-001
  contract_digest: "sha256:<contract-digest>"
  project_id: kdsl-spec
  repository: tk999jp/kdsl-spec
  task_kind: review
RUNTIME_CONTROL:
  k1_ref:
    id: kdsl.reference.kernel
    revision: 0.1.0
    digest: "sha256:<k1-digest>"
    source_ref: "example:k1-canonical"
  pf1_state: resolved
  pf1_ref:
    id: kdsl.reference.profile
    revision: 0.1.0
    digest: "sha256:<pf1-digest>"
    source_ref: "example:pf1-reference"
  compatibility_state: valid
EVALUATION:
  evaluated_at: "2026-07-18T00:00:00Z"
  evaluator_ref:
    id: kdsl.reference.evaluator
    revision: 0.1.0
    digest: "sha256:<evaluator-digest>"
    immutable_ref: none
  repository_state_ref: "commit:<exact-commit>"
  environment_state_ref: none
COMPLETION:
  state: explicit
  completed_fields: []
  expansions: []
  unresolved: []
RESTRICTIONS:
  state: applied
  applied: []
  conflicts: []
AUTHORITY:
  state: sufficient
  rails:
    read: &read_rail
      requested: allow
      k1_disposition: preserve
      pf1_mode: allow_max
      pf1_scope: any
      pf1_cardinality: any
      approval_requirement: not_required
      approval_evidence_id: none
      targets: []
      operation_instance: none
      effective_value: allow
      effective_scope: any
      effective_cardinality: any
      state: sufficient
    edit: &forbid_rail
      requested: forbid
      k1_disposition: preserve
      pf1_mode: forbid
      pf1_scope: any
      pf1_cardinality: any
      approval_requirement: not_required
      approval_evidence_id: none
      targets: []
      operation_instance: none
      effective_value: forbid
      effective_scope: none
      effective_cardinality: none
      state: sufficient
    stage: *forbid_rail
    commit: *forbid_rail
    push: *forbid_rail
    release: *forbid_rail
    public_repo: *forbid_rail
    destructive_ops: *forbid_rail
APPROVALS:
  state: not_required
  requirements: []
  evidence: []
CAPABILITIES:
  state: not_required
  requirements: []
  observations: []
STOP:
  state: clear
  rules_checked: []
  matches: []
PRECONDITIONS:
  state: satisfied
  requirements: []
  evidence: []
BINDING:
  state: bound
  identity_state: resolved
  profile_state: resolved
  completion_state: explicit
  restriction_state: applied
  authority_state: sufficient
  capability_state: not_required
  stop_state: clear
  precondition_state: satisfied
  executable: false
  semantic_equivalence: not_proven
  execution_authority: none
PROVENANCE:
  generated_at: "2026-07-18T00:00:00Z"
  source_records:
    - kind: contract
      id: docs-review-001
      revision: 0.1
      digest: "sha256:<contract-digest>"
      source_ref: "example:p1l-contract"
    - kind: k1
      id: kdsl.reference.kernel
      revision: 0.1.0
      digest: "sha256:<k1-digest>"
      source_ref: "example:k1-canonical"
    - kind: pf1
      id: kdsl.reference.profile
      revision: 0.1.0
      digest: "sha256:<pf1-digest>"
      source_ref: "example:pf1-reference"
  notes:
    - "bound records exact evidence; it does not change executable:false"
```

Corresponding P1L scalar reference after a real digest is computed:

```text
{"schema":"kdsl-binding-evidence@0.1-draft","id":"kdsl.reference.binding.docs-review","revision":"0.1.0","digest":"sha256:<64 lowercase hex>"}
```

```text
example != canonical digest proof
bound != permission expansion
bound != runtime result
validator/lint pass != RT:v
```
