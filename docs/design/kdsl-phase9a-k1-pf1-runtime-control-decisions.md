# Phase 9A — K1 / PF1 Runtime-Control Decision Addendum

status: design-decision-addendum
tracking_issue: 132
applies_to: docs/design/kdsl-phase9a-k1-pf1-runtime-control-design.md
base_design_commit: d80e91ec78a63eeda86fb9281ec6dda7f02e647e

## 1. Purpose

Clarify authority/capability separation and resolve design questions that can be decided from the verified Phase 8 contract boundary and project-local K1/PF1 evidence.

This addendum controls Phase 9A interpretation when wording in the base design could be read more broadly.

## 2. Authority and capability are separate evaluations

The base design Section 7.3 phrase that included runtime capability in an `actual permitted ceiling` intersection must not be interpreted as capability participating in permission semantics.

Correct model:

```text
authority_effective
:= P1L explicit authority rails
∩ K1 absolute prohibitions/invariants
∩ PF1 project ceilings/restrictions
∩ explicit approval evidence when required
```

```text
capability_sufficient
:= every required capability has current observed evidence
```

```text
stop_clear
:= no active Stop trigger prohibits the requested operation class
```

```text
execution_ready_candidate
:= binding_valid
∧ authority_sufficient
∧ capability_sufficient
∧ stop_clear
∧ required preconditions satisfied
```

Mandatory separation:

```text
capability_sufficient != authority_sufficient
capability observed != permission granted
authority sufficient != capability available
execution_ready_candidate != executable under kdsl-p1l@0.1-draft
```

Under the current P1L/P1 schemas:

```text
BINDING.executable:false
```

remains fixed even when all four evaluation dimensions pass.

## 3. Resolved design decisions

### 3.1 K1 schema and instances

Decision:

```text
canonical K1 schema
+ exact project/repository K1 instances
```

The canonical specification defines K1 semantics and required fields. A project may supply a local K1 instance conforming to that schema.

```text
project-local K1 instance != canonical specification source
project-local K1 valid != executable
```

A future repository-wide reference K1 instance may be added separately, but is not required for Phase 9B schema adoption.

### 3.2 PF1 not_applicable

Decision:

`PF1 not_applicable` may be permitted only when all are true:

```text
K1 policy explicitly permits no-profile binding for the task class
P1L PROFILE.id/revision/digest are explicitly none/not_applicable
no profile completion is required
no project preset/alias/default is referenced
no project restriction or capability requirement is required
all P1L authority rails remain explicit
```

Any implicit profile dependency makes `PF1 not_applicable` blocked.

### 3.3 Skill/tool route identity

Decision:

A canonical PF1 route requires:

```text
route kind
exact target id
exact revision
exact digest or immutable reference
applicable TASK.kind
```

```text
route resolution != authority
route target availability != capability evidence for unrelated operations
```

### 3.4 Binding state terminology

Decision:

For `kdsl-p1l@0.1-draft`, retain:

```text
BINDING.state: bound
BINDING.executable: false
```

A future P1L schema revision should prefer an explicit state such as:

```text
bound_non_executable
```

The current schema must not be retroactively changed without a new schema ID or explicit compatibility revision.

## 4. Remaining Phase 9B decisions

The following remain unresolved and block canonical schema adoption until decided or explicitly deferred in the schema:

1. Binding evidence representation:
   - separate canonical envelope; or
   - separately hashed record referenced by `P1L.BINDING.runtime_control`.
2. Canonical serialization and digest algorithm for structured K1/PF1 definitions.
3. PF1 authority-ceiling vocabulary and deterministic intersection table.
4. Immutable user-approval evidence representation.
5. Capability observation freshness, scope, expiry, and invalidation rules.

## 5. Binding evidence dimensions

Phase 9B must keep these dimensions separate:

```text
identity_state: resolved|blocked
profile_state: resolved|not_applicable|blocked
completion_state: explicit|profile_completed|blocked
restriction_state: applied|conflict|blocked
authority_state: sufficient|insufficient|conflict|blocked
capability_state: sufficient|insufficient|stale|unverified|blocked
stop_state: clear|active|unknown|blocked
precondition_state: satisfied|unsatisfied|unknown|blocked
binding_state: unbound|bound|blocked
executable: false
semantic_equivalence: not_proven
```

No aggregate `pass` value may erase the individual dimensions.

## 6. Non-widening authority table requirement

Phase 9B must provide a complete rail-level table covering at least:

```text
P1L value
PF1 ceiling/restriction
K1 absolute rule
approval evidence requirement
resulting authority state
```

Required examples:

```text
P1L allow × PF1 forbid → forbid
P1L forbid × PF1 allow-ceiling → forbid
P1L propose_only × PF1 allow-ceiling → propose_only
P1L not_requested × PF1 allow-ceiling → not_requested
P1L allow_once × missing exact target → blocked
approval_required × missing approval evidence → blocked
```

Capability must not appear as an input column in this authority table. It is evaluated separately.

## 7. Phase 9A final design position

```text
K1:=canonical runtime-control semantics + exact conforming instance
PF1:=project-scoped exact definitions and non-widening restrictions
binding resolves identity/completion/restriction/authority/capability/Stop/preconditions separately
authority != capability
binding valid != executable
BINDING.executable:false remains fixed
unknown/conflict/stale critical evidence→blocked
```

No runtime binding, execution authorization artifact, executable transformer, or automatic AI tool execution is adopted by this addendum.
