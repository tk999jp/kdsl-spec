# Example — K1 / PF1 Non-Executable Runtime Control

This example is explanatory only.

```text
example != specification source
example digest != verified content identity
K1/PF1 valid != executable|authority
binding reference != execution instruction
```

## 1. K1 instance example

```yaml
K1:
SCHEMA: kdsl-k1@0.1-draft
STATUS: runtime-control-definition
IDENTITY:
  id: example.safe-kernel
  revision: "2026-07-18"
  canonicalization: kdsl-runtime-control-c14n@0.1-draft
  digest: "sha256:1111111111111111111111111111111111111111111111111111111111111111"
  source_ref: "examples/runtime/k1-pf1-non-executable.example.md#k1"
APPLIES_TO:
  contract_schemas: [kdsl-p1l@0.1-draft, kdsl-p1@0.1-draft]
  project_scope: "repository:example/project"
  no_profile_task_kinds: [review]
STATE_MODEL:
  required_states: [authoring_valid, contract_valid, profile_resolved, runtime_control_valid, binding_valid, authority_sufficient, capability_sufficient, stop_clear, executable, executed, verified, runtime_verified]
  executable_under_current_contract: false
COMPLETION_POLICY:
  exact_identity_required: true
  inference_prohibited: true
  provenance_required: true
  cyclic_expansion: blocked
  ambiguous_expansion: blocked
AUTHORITY_POLICY:
  rails: [read, edit, stage, commit, push, release, public_repo, destructive_ops]
  p1l_values: [allow, forbid, target_only, allow_once, propose_only, not_requested, not_applicable]
  non_widening: true
  missing_rail: blocked
  approval_reference_required_when_declared: true
CAPABILITY_POLICY:
  sufficient_claim: observed_current
  inferred_claim: insufficient
  unverified_claim: insufficient
  stale_claim: insufficient
  capability_is_permission: false
STOP_POLICY:
  continuation_is_authority: false
  active_for_requested_operation: blocked
  unknown_state: blocked
VERIFY_POLICY:
  requirement_is_result: false
  unavailable_is_pass: false
  not_run_is_pass: false
RUNTIME_POLICY:
  pre_execution_values: [pending, user_required, not_applicable]
  result_values_reserved_for_r1: [v, fail, blk]
  build_test_ci_is_rt_v: false
RESULT_POLICY:
  next_is_authority: false
  commit_field_is_commit_authority: false
  required_result_schema: [kdsl-r1c@0.1-draft, full-r1]
CONFLICT_POLICY:
  unknown_definition: blocked
  identity_mismatch: blocked
  category_mismatch: blocked
  protected_wording_weakening: blocked
  critical_exact_string_change: blocked
BINDING_REQUIREMENTS:
  evidence_representation: external_content_addressed_record
  evidence_schema: deferred_phase9d
  reference_from_p1l_binding: required
  executable: false
  semantic_equivalence: not_proven
  execution_authority: none
```

## 2. PF1 instance example

```yaml
PF1:
SCHEMA: kdsl-pf1@0.1-draft
STATUS: project-runtime-control-profile
IDENTITY:
  id: Example.safe.v1
  revision: "2026-07-18"
  canonicalization: kdsl-runtime-control-c14n@0.1-draft
  digest: "sha256:2222222222222222222222222222222222222222222222222222222222222222"
  source_ref: "examples/runtime/k1-pf1-non-executable.example.md#pf1"
KERNEL_REF:
  id: example.safe-kernel
  revision: "2026-07-18"
  digest: "sha256:1111111111111111111111111111111111111111111111111111111111111111"
PROJECT:
  id: Example
  repository: example/project
  root_ref: "repository:example/project"
APPLIES_TO:
  contract_schemas: [kdsl-p1l@0.1-draft, kdsl-p1@0.1-draft]
  task_kinds: [investigate, fix, docs, closeout]
  excluded_task_kinds: [release]
DEFAULTS:
  guard: safe
  verify: build_diff
  stop: narrow_unknown
  output: standard
  runtime_disposition: user_required
  result_schema: kdsl-r1c@0.1-draft
PRESETS:
  guard:
    - id: safe
      category: guard
      expansion: [narrow_scope, preserve_existing_behavior, no_public_history_rewrite]
      ordered: true
  verify:
    - id: build_diff
      category: verify
      expansion: ["dotnet build", "git diff --check"]
      ordered: true
  stop:
    - id: narrow_unknown
      category: stop
      expansion: [wide_scope_change, cause_unknown]
      ordered: true
  output:
    - id: standard
      category: output
      expansion: [summary, files, commands, verify, runtime, risk, next, commit]
      ordered: true
  runtime: []
ALIASES:
  - id: inv
    category: strategy
    expands_to: preserve_invariant
RESTRICTIONS:
  - id: no-public-history-rewrite
    applies_to:
      task_kinds: [investigate, fix, docs, closeout]
      rails: [public_repo]
    effect: forbid
    scope: any
    protected_wording: "public履歴のrewrite禁止"
AUTHORITY_CEILING:
  read: {mode: allow_max, scope: any, cardinality: any}
  edit: {mode: allow_max, scope: target_only, cardinality: any}
  stage: {mode: approval_required, scope: target_only, cardinality: once}
  commit: {mode: approval_required, scope: target_only, cardinality: once}
  push: {mode: approval_required, scope: target_only, cardinality: once}
  release: {mode: forbid, scope: any, cardinality: any}
  public_repo: {mode: forbid, scope: any, cardinality: any}
  destructive_ops: {mode: approval_required, scope: target_only, cardinality: once}
CAPABILITY_REQUIREMENTS:
  - id: repository-readable
    capability: repository_read
    task_kinds: [investigate, fix, docs, closeout]
    scope: "repository:example/project"
    max_age_seconds: 300
    required_state: observed
    invalidation: [time_expired, scope_changed, environment_digest_changed, repository_state_changed, explicit_revocation]
ROUTING:
  - id: fix-route
    task_kinds: [fix]
    kind: skill
    target_id: example-safe-fix
    revision: "1"
    digest: "sha256:3333333333333333333333333333333333333333333333333333333333333333"
    immutable_ref: none
RUNTIME_POLICY:
  code_change_default: user_required
  docs_only_default: not_applicable
  state_only_default: not_applicable
RESULT_POLICY:
  result_schema: kdsl-r1c@0.1-draft
  report_requirements: [KDSL_RESULT, RT_boundary, NEXT_proposal_only, COMMIT_non_authoritative]
COMPATIBILITY:
  legacy_profile_ids: [Example.safe.legacy]
  legacy_aliases: []
  migration_notes: ["legacy profile requires explicit canonical migration"]
```

## 3. P1L binding reference example

The current P1L schema remains non-executable:

```yaml
BINDING:
  runtime_control: "sha256:4444444444444444444444444444444444444444444444444444444444444444"
  state: bound
  executable: false
```

The referenced record is external and content-addressed. Its field schema is deferred to Phase 9D.

```text
bound != executable|approved|executed
```

## 4. Authority evaluation examples

### 4.1 Non-widening

```text
P1L.edit: target_only
PF1.edit: mode=allow_max/scope=target_only/cardinality=any
→ effective request: target_only
```

### 4.2 Composite constraint

```text
P1L.commit: allow_once
PF1.commit: mode=approval_required/scope=target_only/cardinality=once
valid exact approval_ref: present
→ request_value: allow_once
→ effective_scope: target_only
→ effective_cardinality: once
→ authority_state: sufficient
→ executable: false
```

### 4.3 Missing approval

```text
P1L.push: allow_once
PF1.push: approval_required
approval_ref: missing
→ authority_state: blocked
→ executable: false
```

### 4.4 Capability is separate

```text
repository_write capability: observed/current
P1L.push: not_requested
PF1.push: approval_required
→ authority remains not_requested
→ capability does not create push permission
```

## 5. Capability observation example

```yaml
capability_observation:
  id: example-repository-read-1
  capability: repository_read
  state: observed
  scope: "repository:example/project"
  observed_at: "2026-07-18T00:00:00Z"
  valid_until: "2026-07-18T00:05:00Z"
  environment_digest: "sha256:5555555555555555555555555555555555555555555555555555555555555555"
  evidence_ref: "example-observation-record"
  invalidation: [time_expired, scope_changed, environment_digest_changed, repository_state_changed, explicit_revocation]
```

After `valid_until`, this observation is stale and cannot satisfy the requirement.

## 6. Approval reference example

```yaml
approval_ref:
  id: example-commit-approval-1
  revision: "1"
  digest: "sha256:6666666666666666666666666666666666666666666666666666666666666666"
  source_ref: "example-review-record"
  issuer: "user:example"
  issued_at: "2026-07-18T00:00:00Z"
  operation: commit
  scope: "repository:example/project/target:file.txt"
  valid_until: "2026-07-18T01:00:00Z"
  revoked: false
```

```text
approval_ref valid != executable
digest match != issuer authenticity proof
```
