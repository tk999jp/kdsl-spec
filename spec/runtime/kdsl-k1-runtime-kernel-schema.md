# KDSL K1 Runtime Kernel Schema v0.1 Draft

status: v2-draft adopted
canonical: v2-draft
schema_id: kdsl-k1@0.1-draft
canonicalization: kdsl-runtime-control-c14n@0.1-draft
executable: no
authority_grant: no

## 1. Purpose

K1 defines canonical runtime-control semantics and state separation. A project or repository may provide an exact K1 instance conforming to this schema.

```text
K1 valid != executable
K1 valid != authority grant
K1 valid != runtime binding
K1 valid != RT:v
```

K1 contains cross-project semantics. Project commands, paths, aliases, presets, skill routes, and project defaults belong in PF1.

## 2. Ownership

```text
Core/R1/Bridge canonical meaning
> P1L/P1 canonical contract meaning
> K1 runtime-control semantics
> PF1 project definitions
> resolver/lint
> skill/tool routing
> example/template/tool
```

K1 may add prohibitions and state-separation rules but may not weaken upper canonical sources.

## 3. Required envelope and order

```text
K1:
SCHEMA: kdsl-k1@0.1-draft
STATUS: runtime-control-definition
```

Required order:

```text
K1
SCHEMA
STATUS
IDENTITY
APPLIES_TO
STATE_MODEL
COMPLETION_POLICY
AUTHORITY_POLICY
CAPABILITY_POLICY
STOP_POLICY
VERIFY_POLICY
RUNTIME_POLICY
RESULT_POLICY
CONFLICT_POLICY
BINDING_REQUIREMENTS
```

No implicit defaults exist.

## 4. Record shape

```yaml
K1:
SCHEMA: kdsl-k1@0.1-draft
STATUS: runtime-control-definition
IDENTITY:
  id: "<exact kernel id>"
  revision: "<exact revision>"
  canonicalization: kdsl-runtime-control-c14n@0.1-draft
  digest: "sha256:<hex>"
  source_ref: "<exact source reference>"
APPLIES_TO:
  contract_schemas:
    - kdsl-p1l@0.1-draft
    - kdsl-p1@0.1-draft
  project_scope: "global|repository:<exact>|project:<exact>"
  no_profile_task_kinds: []
STATE_MODEL:
  required_states:
    - authoring_valid
    - contract_valid
    - profile_resolved
    - runtime_control_valid
    - binding_valid
    - authority_sufficient
    - capability_sufficient
    - stop_clear
    - executable
    - executed
    - verified
    - runtime_verified
  executable_under_current_contract: false
COMPLETION_POLICY:
  exact_identity_required: true
  inference_prohibited: true
  provenance_required: true
  cyclic_expansion: blocked
  ambiguous_expansion: blocked
AUTHORITY_POLICY:
  rails:
    - read
    - edit
    - stage
    - commit
    - push
    - release
    - public_repo
    - destructive_ops
  p1l_values:
    - allow
    - forbid
    - target_only
    - allow_once
    - propose_only
    - not_requested
    - not_applicable
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
  pre_execution_values:
    - pending
    - user_required
    - not_applicable
  result_values_reserved_for_r1:
    - v
    - fail
    - blk
  build_test_ci_is_rt_v: false
RESULT_POLICY:
  next_is_authority: false
  commit_field_is_commit_authority: false
  required_result_schema:
    - kdsl-r1c@0.1-draft
    - full-r1
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

## 5. State separation

The following states are distinct:

```text
authoring_valid
contract_valid
profile_resolved
runtime_control_valid
binding_valid
authority_sufficient
capability_sufficient
stop_clear
executable
executed
verified
runtime_verified
```

Forbidden equivalence:

```text
contract_valid = executable
runtime_control_valid = executable
binding_valid = authority_sufficient
authority_sufficient = capability_sufficient
authority_sufficient = executed
capability_sufficient = permission
verified = runtime_verified
build/diff/lint/test/CI pass = RT:v
```

Under `kdsl-p1l@0.1-draft` and `kdsl-p1@0.1-draft`:

```text
BINDING.state may become bound
BINDING.executable:false remains fixed
bound != executable|approved|executed
```

## 6. Completion versus inference

```text
completion:=mechanical expansion from exact id+revision+digest
inference:=meaning guessed from name/memory/conversation/convention/similarity
```

Completion requires:

```text
exact source identity
field-specific declared default/preset/alias
category match
acyclic resolution
visible expanded value
provenance in binding evidence
```

Unknown, similar-name, cyclic, ambiguous, or category-mismatched expansion results in `blocked`.

## 7. Authority semantics

K1 defines evaluation semantics, not project permission.

```text
authority_effective
:= P1L explicit request
 ∩ K1 absolute prohibitions/invariants
 ∩ PF1 ceilings/restrictions
 ∩ required approval evidence
```

Capability is not an authority input.

```text
capability observed != permission
credential available != push/release authority
route resolved != authority
Stop continuation allowed != authority
```

All eight P1L authority rails remain mandatory.

## 8. Approval evidence reference

K1 recognizes explicit content-addressed approval references as binding inputs. It does not define an execution-authorization artifact.

Minimum reference:

```yaml
approval_ref:
  id: "<exact approval id>"
  revision: "<exact revision>"
  digest: "sha256:<hex>"
  source_ref: "<exact reviewable source>"
  issuer: "<explicit issuer identity>"
  issued_at: "<UTC timestamp>"
  operation: "<exact rail/operation>"
  scope: "<exact target/scope>"
  valid_until: "<UTC timestamp or none>"
  revoked: false
```

Approval handling separates structural integrity from trusted-source acceptance.

Structural validity requires:

```text
exact operation/scope match
current time validity
revoked:false
digest recomputation match
```

Authority sufficiency additionally requires trusted-source verification of the issuer/source under an explicit repository/project trust policy or immutable platform record.

```text
remembered conversation approval→invalid
structurally valid approval without trusted-source verification→blocked
approval accepted != executable
digest match != issuer authenticity proof
```

Cryptographic signer authentication is outside v0.1 draft. When no independently trusted source can verify issuer identity, the approval requirement remains unsatisfied and authority is `blocked`.

## 9. Capability observations

Capability requirements and observations remain separate.

Minimum observation:

```yaml
capability_observation:
  id: "<exact observation id>"
  capability: "<exact capability id>"
  state: observed|inferred|unverified|not_available
  scope: "<exact environment/target>"
  observed_at: "<UTC timestamp>"
  valid_until: "<UTC timestamp>"
  environment_digest: "sha256:<hex>"
  evidence_ref: "<exact evidence reference>"
  invalidation:
    - time_expired
    - scope_changed
    - environment_digest_changed
    - credential_rotated
    - repository_state_changed
    - explicit_revocation
```

Only `observed` and current, scope-matching evidence may satisfy a requirement.

```text
missing valid_until→stale
stale|inferred|unverified→insufficient
runtime available != RT:v
```

## 10. PF1 not_applicable

No-profile binding is allowed only when:

```text
TASK.kind is listed in APPLIES_TO.no_profile_task_kinds
P1L PROFILE identity is explicit none/not_applicable
no profile completion/preset/alias/default is referenced
no project restriction/capability requirement is required
all P1L authority rails remain explicit
```

Any implicit profile dependency results in `blocked`.

## 11. Binding evidence representation

Phase 9B adopts this representation decision:

```text
binding evidence:=external content-addressed record
P1L.BINDING.runtime_control:=exact reference to that record
```

The record schema and resolver implementation remain Phase 9D/9C work. No executable-looking canonical envelope is introduced in Phase 9B.

## 12. Non-goals

```text
runtime-binding resolver implementation
binding-evidence field schema
BINDING.executable:true
execution authorization artifact
executable transformer
automatic AI coding tool execution
actual credential or command use
Packet normalized-state promotion
stable/public-ready/tag/release/Release Assets operation
```
