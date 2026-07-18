# Canonical K1 machine sample

K1:
SCHEMA: "kdsl-k1@0.1-draft"
STATUS: "runtime-control-definition"
IDENTITY:
  id: "kdsl.reference.kernel"
  revision: "0.1.0"
  canonicalization: "kdsl-runtime-control-c14n@0.1-draft"
  digest: "sha256:b916d5884b6d25e0a00ca8ad490247b02e5e588a0f1a4af4894fba4057c4d5ae"
  source_ref: "examples/runtime/k1-canonical.example.md"
APPLIES_TO:
  contract_schemas: ["kdsl-p1l@0.1-draft","kdsl-p1@0.1-draft"]
  project_scope: "repository:tk999jp/kdsl-spec"
  no_profile_task_kinds: ["review"]
STATE_MODEL:
  required_states: ["authoring_valid","contract_valid","profile_resolved","runtime_control_valid","binding_valid","authority_sufficient","capability_sufficient","stop_clear","executable","executed","verified","runtime_verified"]
  executable_under_current_contract: false
COMPLETION_POLICY:
  exact_identity_required: true
  inference_prohibited: true
  provenance_required: true
  cyclic_expansion: "blocked"
  ambiguous_expansion: "blocked"
AUTHORITY_POLICY:
  rails: ["read","edit","stage","commit","push","release","public_repo","destructive_ops"]
  p1l_values: ["allow","forbid","target_only","allow_once","propose_only","not_requested","not_applicable"]
  non_widening: true
  missing_rail: "blocked"
  approval_reference_required_when_declared: true
CAPABILITY_POLICY:
  sufficient_claim: "observed_current"
  inferred_claim: "insufficient"
  unverified_claim: "insufficient"
  stale_claim: "insufficient"
  capability_is_permission: false
STOP_POLICY:
  continuation_is_authority: false
  active_for_requested_operation: "blocked"
  unknown_state: "blocked"
VERIFY_POLICY:
  requirement_is_result: false
  unavailable_is_pass: false
  not_run_is_pass: false
RUNTIME_POLICY:
  pre_execution_values: ["pending","user_required","not_applicable"]
  result_values_reserved_for_r1: ["v","fail","blk"]
  build_test_ci_is_rt_v: false
RESULT_POLICY:
  next_is_authority: false
  commit_field_is_commit_authority: false
  required_result_schema: ["kdsl-r1c@0.1-draft","full-r1"]
CONFLICT_POLICY:
  unknown_definition: "blocked"
  identity_mismatch: "blocked"
  category_mismatch: "blocked"
  protected_wording_weakening: "blocked"
  critical_exact_string_change: "blocked"
BINDING_REQUIREMENTS:
  evidence_representation: "external_content_addressed_record"
  evidence_schema: "deferred_phase9d"
  reference_from_p1l_binding: "required"
  executable: false
  semantic_equivalence: "not_proven"
  execution_authority: "none"
