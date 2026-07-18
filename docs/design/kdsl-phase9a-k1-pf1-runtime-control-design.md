# Phase 9A — Canonical K1 / PF1 Runtime-Control Design

status: design-candidate
tracking_issue: 132
repository: tk999jp/kdsl-spec
base: main@951f9344964b91cd175523f0bd8e47d91e170e48
review_class: separate-approval-runtime-control-design

## 1. Purpose

Define the ownership, state model, precedence, identity, completion, restriction, capability, routing, and binding-evidence boundaries for canonical K1/PF1 runtime control.

This phase designs non-executable runtime-control definitions. It does not implement runtime binding or create an executable transformer.

```text
KDSL-DP
→ normalize
P1L
→ optional compact serialization
P1
→ resolve exact K1/PF1 definitions
→ evaluate restrictions/capabilities/authority
→ binding evidence candidate
```

```text
binding evidence candidate != executable instruction
K1/PF1 valid != authority grant
P1L/P1 valid != executable
```

## 2. Verified baseline

```text
main: 951f9344964b91cd175523f0bd8e47d91e170e48
Phase 8: complete
P1L schema: kdsl-p1l@0.1-draft
P1 schema: kdsl-p1@0.1-draft
P1L BINDING.runtime_control: K1/PF1 reference or unresolved
P1L BINDING.state: unbound|bound|blocked
P1L BINDING.executable:false fixed
K1/PF1 canonical schema: absent
runtime-binding implementation: absent
```

Operational evidence:

```text
tk999jp/MidFD-dev/.codex/adps/kernel.k1.md
tk999jp/MidFD-dev/.codex/adps/profiles/MidFD.safe.v2.pf1.md
tk999jp/MidFD-dev/.codex/adps/profiles/MidFD.closeout.v1.pf1.md
```

These files are operational evidence/examples. They are not canonical KDSL specification sources.

## 3. Design goals

```text
separate universal runtime-control semantics from project definitions
preserve P1L/P1 non-executable boundary
make profile completion exact and auditable
make authority evaluation non-widening
separate runtime capability from permission
separate Stop continuation allowances from operation authority
make skill routing descriptive, not authoritative
block unknown/ambiguous/conflicting definitions
support project-local K1/PF1 migration without automatic canonical promotion
```

Priority:

```text
meaning/safety/authority preservation
> exact identity and reproducibility
> deterministic expansion
> compatibility
> compactness
```

## 4. Ownership

### 4.1 K1

```text
K1:=runtime kernel policy and state-separation contract
```

K1 owns runtime-control semantics that must remain stable across projects:

```text
state separation
completion versus inference
non-widening authority evaluation
capability versus permission separation
Stop/Verify/Runtime/Result boundaries
unknown/conflict handling
binding-evidence minimum requirements
```

K1 must not contain project-specific source paths, commands, task aliases, skills, build commands, repository names, or project defaults except in separately declared compatibility examples.

### 4.2 PF1

```text
PF1:=project-scoped named runtime-control profile
```

PF1 may define exact project-scoped values:

```text
project/repository identity
profile identity/revision/digest
non-authority defaults
Guard/Verify/Stop/Output presets
runtime policy
aliases and their exact expansions
capability requirements
skill/task routing references
project restrictions and authority ceilings
compatibility declarations
```

PF1 must not redefine K1 state meanings or weaken Core/P1L/R1/Bridge boundaries.

### 4.3 Binding evidence

```text
binding evidence:=record that exact K1/PF1 definitions were resolved and evaluated against one P1L contract
```

Binding evidence records evaluation. It does not grant authority and does not prove execution.

Phase 9A does not adopt a binding-evidence envelope name or schema ID. Phase 9B must decide whether the evidence is:

```text
a separate canonical envelope
or
a separately hashed record referenced by P1L.BINDING.runtime_control
```

## 5. Canonical source precedence

Specification ownership:

```text
Core/R1/Bridge canonical meaning
> P1L/P1 canonical contract meaning
> K1 canonical runtime-control semantics
> PF1 exact project definitions
> binding resolver/lint
> skill/routing implementation
> example/template/tool
```

Per-task composition is not simple last-writer-wins precedence.

```text
K1 invariant × P1L explicit task value × PF1 mandatory restriction
→ conjunction / most restrictive valid result
```

Rules:

```text
K1 prohibition cannot be weakened by PF1 or P1L
PF1 mandatory restriction cannot be weakened by P1L task wording
P1L explicit value overrides PF1 default only when compatible
PF1 default fills only an allowed missing non-authority field
conflict→blocked
unknown→blocked
```

User approval must be represented as explicit contract/evidence input. An out-of-band remembered approval must not silently override K1/PF1/P1L.

## 6. Identity and reproducibility

Every resolved K1/PF1 definition requires exact identity:

```text
id
revision
digest
source reference
```

Candidate identity requirements:

```text
K1.id
K1.revision
K1.digest
PF1.id
PF1.revision
PF1.digest
PF1.kernel_ref.id
PF1.kernel_ref.revision
PF1.kernel_ref.digest
```

```text
name only != exact identity
revision only != content identity
digest only != semantic equivalence
source path only != immutable identity
```

Unknown or mismatched identity results in `blocked`.

Digest canonicalization rules are unresolved in Phase 9A and must be fixed before schema adoption.

## 7. K1 candidate field groups

Phase 9A recommends the following semantic groups without adopting final field names or a schema ID:

```text
META
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

### 7.1 STATE_MODEL

Required distinct states:

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
authority_sufficient = executed
capability_sufficient = permission
verified = runtime_verified
build/test/CI pass = RT:v
```

### 7.2 COMPLETION_POLICY

```text
completion:=mechanical expansion from an exact resolved definition
inference:=meaning guessed from names, memory, convention, prior conversation, or similar project
```

```text
completion allowed only from exact K1/PF1 id+revision+digest
expanded value must be visible in binding evidence
source preset/alias/default path must be recorded
unknown/cyclic/ambiguous expansion→blocked
```

### 7.3 AUTHORITY_POLICY

K1 defines evaluation semantics, not project permissions.

```text
actual permitted ceiling
:= P1L explicit authority rail
∩ K1 invariant/absolute prohibition
∩ PF1 project ceiling/restriction
∩ current runtime capability
∩ explicit approval evidence when required
```

The intersection is non-widening.

```text
any forbid→forbid
missing explicit P1L rail→blocked
not_requested != allow
propose_only != allow
capability available != allow
PF1 default allow prohibited for critical authority rails
```

Required P1L rails remain:

```text
read/edit/stage/commit/push/release/public_repo/destructive_ops
```

PF1 may declare a stricter ceiling or mandatory `forbid`, but must not convert a P1L `forbid`, `not_requested`, or `propose_only` value into `allow`.

### 7.4 CAPABILITY_POLICY

Capability is an observed runtime/environment fact.

Examples:

```text
repository readable
worktree editable
command available
target runtime available
network available
credentials available
interactive UI available
```

```text
capability evidence != operation permission
credential present != push/release authority
command available != command requested
runtime available != RT:v
```

Capability claims require evidence classification:

```text
observed
inferred
unverified
not_available
```

Only `observed` capability may satisfy a required runtime capability. `inferred` and `unverified` remain insufficient for binding.

### 7.5 STOP_POLICY

Stop entries contain two independent concepts:

```text
stop trigger
allowed continuation class
```

Allowed continuation means the operation may continue only within that class. It is not an authority grant.

Example:

```text
cause unknown
→ confirmed patch stopped
→ investigate/measure/hypothesis/proposal may remain allowed
```

```text
Stop allow: investigate != edit authority
Stop allow: proposal != implementation authority
Stop clear != executable
```

### 7.6 VERIFY / RUNTIME / RESULT policy

```text
Verify requirement != Verify result
not_run/unavailable/user_required→pass扱禁止
build/diff/lint/test/CI pass != RT:v
RT:v requires target-environment runtime evidence
NEXT:=proposal only
COMMIT:=actual/proposed record, not commit authority
```

K1 may define allowed status vocabularies and separation rules. PF1 may define project-specific required checks and commands.

## 8. PF1 candidate field groups

Phase 9A recommends:

```text
META
KERNEL_REF
PROJECT
APPLIES_TO
DEFAULTS
PRESETS
ALIASES
RESTRICTIONS
AUTHORITY_CEILING
CAPABILITY_REQUIREMENTS
ROUTING
RUNTIME_POLICY
RESULT_POLICY
COMPATIBILITY
```

### 8.1 DEFAULTS

PF1 defaults are field-specific and non-authoritative unless a later canonical schema explicitly permits otherwise.

Allowed candidate defaults:

```text
Guard preset
Verify preset
Stop preset
Output preset
pre-execution Runtime disposition
project result schema
```

Critical authority rails must not be silently completed to `allow`.

Every expansion records:

```text
source PF1 identity
source field/preset
expanded target field
exact expanded value
```

### 8.2 PRESETS

Preset definition requirements:

```text
exact name
exact category
exact expansion
ordered expansion where order matters
no cyclic reference
no unknown nested reference
```

Preset categories must not be interchangeable.

```text
Guard preset != Authority
Verify preset != Verify result
Stop preset continuation != Authority
Output preset != Result validity
Runtime preset != Runtime result evidence
```

### 8.3 ALIASES

Aliases are names for exact declared values only.

```text
unknown alias→blocked
similar alias→blocked
alias category mismatch→blocked
alias expansion must be recorded
alias may not replace protected wording
```

### 8.4 RESTRICTIONS / AUTHORITY_CEILING

PF1 restrictions are conjunctive and non-widening.

Examples:

```text
no public history rewrite
no Release Assets overwrite
no destructive operation without approval
no implementation in closeout profile
```

PF1 authority ceiling defines the maximum project-level permission class. It does not itself grant that permission to a task.

```text
PF1 ceiling allow + P1L forbid→forbid
PF1 ceiling forbid + P1L allow→forbid
PF1 ceiling unknown→blocked
```

### 8.5 CAPABILITY_REQUIREMENTS

PF1 may declare capabilities required for a project task class:

```text
required command/tool
required repository access
required target environment
required user runtime confirmation
required credential class
```

The requirement must not claim that the capability exists.

### 8.6 ROUTING

PF1 may map task classes to skill/tool references.

```text
TASK.kind → exact skill id/revision/digest or exact tool route
```

```text
routing resolved != authority granted
skill available != task approved
skill procedure cannot weaken K1/PF1/P1L
unknown route→blocked or explicit no-route disposition
```

## 9. Binding input

Minimum binding inputs:

```text
canonical P1L projection
exact K1 definition
exact PF1 definition or explicit not_applicable
current environment/capability evidence
required approval evidence
resolver version
```

P1 compact input must first reconstruct the canonical P1L projection.

```text
P1→P1L reconstruction failure→blocked
P1L NORMALIZATION.lossy|blocked→binding prohibited
P1L semantic_equivalence:not_proven remains unchanged
```

## 10. Binding evaluation

Candidate deterministic order:

```text
1. verify P1L schema/status/identity
2. verify K1 identity and applicability
3. verify PF1 identity/kernel reference/applicability
4. expand exact PF1 aliases/presets/defaults
5. preserve expanded values and provenance
6. apply K1 invariants
7. apply PF1 mandatory restrictions/ceilings
8. evaluate every explicit P1L authority rail
9. evaluate required capability evidence
10. evaluate Stop state
11. evaluate Verify/Runtime preconditions
12. emit binding evidence state
```

Order is evaluation order, not operation permission.

## 11. Binding states

Candidate states:

```text
unbound
bound_non_executable
blocked
```

`bound` in current P1L vocabulary must mean only that exact runtime-control definitions were resolved and evaluated. Under `kdsl-p1l@0.1-draft`:

```text
BINDING.state: bound
BINDING.executable: false
```

Therefore:

```text
bound != executable
bound != approved
bound != executed
```

A future executable state requires a separately approved schema/version and must not retrofit `kdsl-p1l@0.1-draft`.

## 12. Binding evidence minimum

Candidate evidence fields:

```text
P1L contract id/digest
K1 id/revision/digest
PF1 id/revision/digest or not_applicable
resolver id/revision
expanded defaults/presets/aliases with provenance
applied restrictions
all eight evaluated authority rails
capability requirements and observed evidence
Stop evaluation
Verify/Runtime preconditions
conflicts/unresolved items
binding state
executable:false
semantic_equivalence:not_proven
execution_authority:none unless a separate authority artifact is later approved
```

`execution_authority:none` is the safe Phase 9 design default. Whether a future separate approval artifact may change this is outside Phase 9A.

## 13. Conflict and blocked conditions

Binding must block when any of the following applies:

```text
unknown K1/PF1 id/revision/digest
PF1 kernel reference mismatch
schema applicability mismatch
unknown/cyclic alias or preset
category-mismatched expansion
critical default lacks exact provenance
P1L authority rail missing
PF1 attempts to widen P1L authority
P1L attempts to weaken mandatory PF1 restriction
required capability unobserved
required approval evidence missing
Stop state active for requested operation
critical exact string changed
protected wording weakened
P1L normalization lossy|blocked
```

Blocked binding may still allow explicitly safe analysis/report/proposal paths defined by Stop policy, but those paths remain subject to their own authority rails.

## 14. Compatibility with project-local K1/PF1

Existing project-local files are compatibility evidence.

They may become canonical-profile candidates only after:

```text
exact source identity captured
id/revision/digest added or verified
all presets/aliases expanded and categorized
implicit meanings removed
project restrictions separated from authority grants
Stop continuation allowances separated from permissions
commands/paths preserved exactly
unknown fields blocked
canonical K1/PF1 lint pass
human review/approval
```

Existing `runtime_control_rev: 0.1` is not automatically a canonical schema ID.

Existing project-local colon P1 forms remain legacy operational evidence and must not be used to infer canonical K1/PF1 meanings.

## 15. MidFD evidence interpretation

The MidFD files support these design observations:

```text
kernel.k1.md contains state separation and RT/NEXT rules
MidFD.safe.v2.pf1.md contains defaults/presets/aliases/routing/project restrictions
MidFD.closeout.v1.pf1.md demonstrates a profile that forbids implementation by task class
```

Specific interpretation constraints:

```text
G/V/X/O/RT defaults:=profile completion candidates, not inferred values
X allow lists:=continuation classes, not authority grants
Skill Routing:=route selection, not authority
Approval Required list:=binding precondition, not approval evidence
RT:u default:=pre-execution/runtime disposition, not result RT:v
```

## 16. Candidate schema identifiers

Phase 9A reserves no canonical identifiers.

Possible Phase 9B candidates:

```text
kdsl-k1@0.1-draft
kdsl-pf1@0.1-draft
```

They must not be presented as adopted until canonical schema files, lint, examples, manifest ownership, and review are approved and merged.

No binding-evidence schema identifier is proposed in Phase 9A.

## 17. Open design questions

1. Should K1 be one global canonical kernel schema plus project-local instances, or only a canonical schema with each project supplying its own K1 instance?
2. Should binding evidence use a new envelope or remain an external hashed record referenced by `P1L.BINDING.runtime_control`?
3. What canonical serialization and digest algorithm applies to Markdown/YAML runtime-control definitions?
4. Should PF1 authority ceilings use the P1L rail vocabulary or a smaller `allow_max|forbid|approval_required` vocabulary?
5. How is user approval represented as immutable evidence without turning conversation memory into authority?
6. How are environment capability observations timestamped and invalidated?
7. How are skill/tool route identities versioned and hashed?
8. Should `PF1 not_applicable` be permitted for manual/read-only contracts, and under what K1 policy?
9. Must `BINDING.state: bound` be renamed in a future P1L schema to `bound_non_executable` to reduce misuse?

These questions must be resolved or explicitly deferred before Phase 9B canonical schema adoption.

## 18. Phase plan

```text
Phase 9A: ownership/state/precedence/binding design
Phase 9B: canonical K1/PF1 schema + lint + examples
Phase 9C: resolver/parser/validator first slice
Phase 9D: binding-evidence schema/design, still non-executable
```

Phase 9B requires separate review of the open design questions. Phase 9C/9D must not be treated as runtime execution implementation.

## 19. Non-goals

```text
runtime-binding implementation
BINDING.executable:true
executable transformer
automatic AI coding tool execution
KDSL_PROMPT auto-generation from P1L validity alone
actual credential use
actual command execution
actual commit/push/release/public operation
Packet normalized-state promotion
stable/public-ready/tag/release/Release Assets operations
complete semantic equivalence proof
complete safety proof
```

## 20. Phase 9A decision summary

```text
K1:=universal runtime-control semantics and state-separation policy
PF1:=project-scoped exact defaults/presets/restrictions/capability requirements/routing definitions
K1/PF1 valid != executable|authority grant
PF1 may narrow but never widen P1L authority
capability != permission
Stop continuation != authority
routing != authority
binding evidence records deterministic resolution/evaluation
binding evidence remains non-executable
BINDING.executable:false remains fixed under P1L/P1 v0.1 draft
unknown/conflict/missing critical evidence→blocked
```
