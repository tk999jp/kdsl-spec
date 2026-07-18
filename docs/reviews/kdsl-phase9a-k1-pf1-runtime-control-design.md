# Phase 9A — K1 / PF1 Runtime-Control Design Review

status: design-integrated / closeout-candidate
review_date: 2026-07-18
repository: tk999jp/kdsl-spec
tracking_issue: 132
design_pull_request: 133
design_source_head: b0ec16600686b1b372ab71236df794e03ee23267
design_squash_commit: d65c6eae6947b251246946bfafb9e51636efb145
workflow_run_id: 29630096451
workflow_run_number: 465
workflow_conclusion: success

## 1. Goal

Define canonical K1/PF1 runtime-control ownership and binding boundaries without implementing runtime binding or weakening the existing P1L/P1 non-executable contract.

## 2. Reviewed sources

Canonical sources:

```text
spec/bridge/kdsl-adps-bridge.md
spec/adps/kdsl-p1l-contract-schema.md
spec/glossary.md
docs/overview.md
docs/project-status.md
```

Operational evidence only:

```text
tk999jp/MidFD-dev/.codex/adps/kernel.k1.md
tk999jp/MidFD-dev/.codex/adps/profiles/MidFD.safe.v2.pf1.md
tk999jp/MidFD-dev/.codex/adps/profiles/MidFD.closeout.v1.pf1.md
tk999jp/MidFD-dev/.codex/adps/examples/safe-fix.p1.md
```

The MidFD files were not treated as canonical specification sources.

## 3. Integrated design files

```text
docs/design/kdsl-phase9a-k1-pf1-runtime-control-design.md
docs/design/kdsl-phase9a-k1-pf1-runtime-control-decisions.md
```

## 4. Adopted Phase 9A direction

```text
K1:=canonical runtime-control semantics + exact conforming project/repository instance
PF1:=project-scoped exact defaults/presets/restrictions/capability requirements/routing definitions
K1 + PF1 + P1L→binding evidence candidate
binding evidence != executable instruction
```

## 5. Core decisions

```text
K1/PF1 valid != executable
K1/PF1 valid != authority grant
PF1 may narrow but never widen P1L authority
capability and authority are separate evaluations
Stop continuation class != operation authority
skill/tool routing != authority
profile completion requires exact id/revision/digest and visible provenance
unknown/conflict/missing/stale critical evidence→blocked
BINDING.executable:false remains fixed under kdsl-p1l@0.1-draft
```

Authority model:

```text
authority_effective
:= P1L explicit rails
∩ K1 absolute prohibitions/invariants
∩ PF1 project ceilings/restrictions
∩ explicit approval evidence when required
```

Capability model:

```text
capability_sufficient
:= every required capability has current observed evidence
```

Readiness model:

```text
execution_ready_candidate
:= binding_valid
∧ authority_sufficient
∧ capability_sufficient
∧ stop_clear
∧ required preconditions satisfied
```

```text
execution_ready_candidate != executable under current P1L/P1 schemas
```

## 6. State separation

The design keeps these dimensions independent:

```text
identity_state
profile_state
completion_state
restriction_state
authority_state
capability_state
stop_state
precondition_state
binding_state
executable
semantic_equivalence
```

No aggregate `pass` may erase blocked, insufficient, stale, unverified, or conflict states.

## 7. Resolved design questions

```text
K1 uses a canonical schema with exact project/repository instances
PF1 not_applicable is allowed only under explicit no-profile conditions
skill/tool routes require exact id/revision/digest or immutable reference
current P1L keeps BINDING.state:bound + executable:false
future P1L revision should prefer bound_non_executable wording
```

## 8. Remaining Phase 9B decisions

1. Binding-evidence representation:
   - separate canonical envelope; or
   - separately hashed record referenced by `P1L.BINDING.runtime_control`.
2. Canonical serialization and digest algorithm for K1/PF1.
3. PF1 authority-ceiling vocabulary and deterministic intersection table.
4. Immutable user-approval evidence representation.
5. Capability observation freshness, scope, expiry, and invalidation.

These decisions block canonical K1/PF1 schema adoption until resolved or explicitly deferred in the schema.

## 9. Compatibility interpretation

Existing project-local K1/PF1 files are compatibility evidence only.

```text
runtime_control_rev:0.1 != canonical schema id
G/V/X/O/RT defaults:=profile-completion candidates, not inferred values
Stop allow lists:=continuation classes, not permissions
Skill Routing:=route selection, not authority
Approval Required list:=precondition declaration, not approval evidence
RT:u default:=pre-execution/runtime disposition, not result RT:v
```

## 10. Verification

```text
workflow run: 29630096451 / #465
KDSL Validation: success
Packet Semantic Property: success
Packet P1 Normalization Property: success
```

PR #133 changed design documents only. No schema, validator, runtime-control implementation, Packet state, tag, release, or Release Assets operation was changed.

## 11. Not implemented / not adopted

```text
canonical K1/PF1 schema id
binding-evidence schema
runtime-binding implementation
BINDING.executable:true
execution-authorization artifact
executable transformer
automatic AI coding tool execution
KDSL_PROMPT auto-generation from P1L validity alone
Packet normalized-state promotion
complete semantic equivalence
complete safety proof
stable/public-ready promotion
```

## 12. Next gate

Phase 9B may begin only after separate approval to resolve the five remaining decisions and draft:

```text
canonical K1 schema
canonical PF1 schema
K1/PF1 lint
non-executable examples
manifest/glossary/bridge alignment
```

No tag, release, or Release Assets operation was performed.
