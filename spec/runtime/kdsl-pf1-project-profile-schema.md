# KDSL PF1 Project Runtime-Control Profile Schema v0.1 Draft

status: v2-draft adopted
canonical: v2-draft
schema_id: kdsl-pf1@0.1-draft
canonicalization: kdsl-runtime-control-c14n@0.1-draft
executable: no
authority_grant: no

## 1. Purpose

PF1 defines exact project-scoped defaults, presets, restrictions, authority ceilings, capability requirements, aliases, and routing references under one exact K1 instance.

```text
PF1 valid != executable
PF1 valid != authority grant
PF1 ceiling != task permission
PF1 route != task approval
```

PF1 may narrow a P1L contract. It must never widen P1L authority or weaken K1/Core/R1/Bridge boundaries.

## 2. Required envelope and order

```text
PF1:
SCHEMA: kdsl-pf1@0.1-draft
STATUS: project-runtime-control-profile
```

Required order:

```text
PF1
SCHEMA
STATUS
IDENTITY
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

No implicit defaults exist.

## 3. Record shape

```yaml
PF1:
SCHEMA: kdsl-pf1@0.1-draft
STATUS: project-runtime-control-profile
IDENTITY:
  id: "<exact profile id>"
  revision: "<exact revision>"
  canonicalization: kdsl-runtime-control-c14n@0.1-draft
  digest: "sha256:<hex>"
  source_ref: "<exact source reference>"
KERNEL_REF:
  id: "<exact K1 id>"
  revision: "<exact K1 revision>"
  digest: "sha256:<hex>"
PROJECT:
  id: "<exact project id>"
  repository: "<exact repository or none>"
  root_ref: "<exact project/repository reference>"
APPLIES_TO:
  contract_schemas:
    - kdsl-p1l@0.1-draft
    - kdsl-p1@0.1-draft
  task_kinds: []
  excluded_task_kinds: []
DEFAULTS:
  guard: none
  verify: none
  stop: none
  output: none
  runtime_disposition: none
  result_schema: none
PRESETS:
  guard: []
  verify: []
  stop: []
  output: []
  runtime: []
ALIASES: []
RESTRICTIONS: []
AUTHORITY_CEILING:
  read: {mode: allow_max, scope: any, cardinality: any}
  edit: {mode: forbid, scope: any, cardinality: any}
  stage: {mode: forbid, scope: any, cardinality: any}
  commit: {mode: forbid, scope: any, cardinality: any}
  push: {mode: forbid, scope: any, cardinality: any}
  release: {mode: forbid, scope: any, cardinality: any}
  public_repo: {mode: forbid, scope: any, cardinality: any}
  destructive_ops: {mode: forbid, scope: any, cardinality: any}
CAPABILITY_REQUIREMENTS: []
ROUTING: []
RUNTIME_POLICY:
  code_change_default: user_required
  docs_only_default: not_applicable
  state_only_default: not_applicable
RESULT_POLICY:
  result_schema: kdsl-r1c@0.1-draft|full-r1
  report_requirements: []
COMPATIBILITY:
  legacy_profile_ids: []
  legacy_aliases: []
  migration_notes: []
```

The example ceiling values above are structural placeholders, not universal defaults. Every canonical PF1 must explicitly declare every rail.

## 4. Exact identity

PF1 identity and K1 reference require exact `id/revision/digest`.

```text
PF1 name only→blocked
K1 reference mismatch→blocked
unsupported canonicalization→blocked
project/repository mismatch→blocked
```

A project-local file path is reviewable evidence, not immutable identity.

## 5. Defaults

Allowed default categories:

```text
Guard preset
Verify preset
Stop preset
Output preset
pre-execution Runtime disposition
result schema
```

Defaults are profile-completion inputs only.

```text
default != inference
default != authority grant
default allow for critical authority rail→prohibited
expanded value/provenance must be visible in binding evidence
```

`none` means no PF1 default is supplied. It does not mean an empty semantic value.

## 6. Presets

Each preset record requires:

```yaml
- id: "<exact preset id>"
  category: guard|verify|stop|output|runtime
  expansion: []
  ordered: true|false
```

Rules:

```text
unknown nested preset→blocked
cyclic preset→blocked
category mismatch→blocked
ordered expansion reordering→blocked
preset ID may not replace protected wording
```

Category boundaries:

```text
Guard preset != Authority
Verify preset != Verify result
Stop continuation != Authority
Output preset != Result validity
Runtime preset != R1 runtime result
```

## 7. Aliases

Alias record:

```yaml
- id: "<exact alias>"
  category: task|strategy|guard|verify|stop|output|runtime|route
  expands_to: "<exact declared value or reference>"
```

```text
unknown alias→blocked
similar-name alias→blocked
cross-category alias→blocked
alias expansion provenance required
protected wording one-character shortening prohibited
```

Repo/path/command/API/file/branch/tag/package/class/method/property strings remain exact.

## 8. Restrictions

Restriction record:

```yaml
- id: "<exact restriction id>"
  applies_to:
    task_kinds: []
    rails: []
  effect: forbid|approval_required|stop
  scope: "<exact scope or any>"
  protected_wording: "<complete wording>"
```

Restrictions are conjunctive and non-widening.

```text
PF1 restriction cannot be weakened by P1L wording
restriction conflict/unknown scope→blocked
approval_required != approval granted
```

## 9. Authority ceiling vocabulary

Each rail uses three independent dimensions:

```yaml
mode: allow_max|propose_only_max|forbid|approval_required|not_applicable_only
scope: any|target_only
cardinality: any|once
```

Meanings:

```text
allow_max:=PF1 does not add an operation-class prohibition
propose_only_max:=operation itself prohibited; proposal may remain possible
forbid:=operation prohibited
approval_required:=explicit valid approval_ref required before authority can be sufficient
not_applicable_only:=rail may only be P1L not_applicable
scope:target_only:=exact P1L target/scope required
cardinality:once:=one exact operation instance only
```

Ceilings never create permission. They only preserve or narrow the explicit P1L request.

## 10. Deterministic authority evaluation

Evaluation order per rail:

```text
1. require explicit P1L rail
2. apply K1 absolute prohibition
3. apply PF1 mode
4. apply PF1 scope/cardinality constraints
5. validate exact target/operation instance
6. validate approval_ref when required
7. emit effective request constraints and authority state
```

Rail-level outcomes:

| P1L value | PF1 mode | Result |
|---|---|---|
| `forbid` | any valid mode | `forbid` |
| `not_requested` | any mode except `not_applicable_only` | `not_requested` |
| `propose_only` | `allow_max`/`propose_only_max`/`approval_required` | `propose_only` |
| `allow` | `allow_max` | `allow` plus PF1 scope/cardinality constraints |
| `target_only` | `allow_max` | `target_only` plus PF1 cardinality constraint |
| `allow_once` | `allow_max` | `allow_once` plus PF1 scope constraint |
| any operational request | `propose_only_max` | `propose_only` |
| any operational request | `forbid` | `forbid` |
| any operational request | `approval_required` + valid exact approval | preserve request plus PF1 constraints |
| any operational request | `approval_required` + missing/invalid approval | `blocked` |
| `not_applicable` | `not_applicable_only` | `not_applicable` |
| non-`not_applicable` | `not_applicable_only` | `blocked` |

Additional rules:

```text
K1 forbid always→forbid
P1L allow_once + missing exact operation instance→blocked
scope:target_only + missing/empty target→blocked
scope conflict→blocked
approval scope/operation mismatch→blocked
```

The effective evidence must preserve independent facets when the scalar P1L vocabulary is insufficient:

```yaml
request_value: allow_once
effective_scope: target_only
effective_cardinality: once
authority_state: sufficient|insufficient|conflict|blocked
```

Capability does not participate in this table.

## 11. Capability requirements

Requirement record:

```yaml
- id: "<exact requirement id>"
  capability: "<exact capability id>"
  task_kinds: []
  scope: "<exact environment/target>"
  max_age_seconds: <positive integer>
  required_state: observed
  invalidation:
    - time_expired
    - scope_changed
    - environment_digest_changed
    - credential_rotated
    - repository_state_changed
    - explicit_revocation
```

Rules:

```text
requirement != observation
capability observed != authority
missing observation→insufficient
inferred|unverified|stale→insufficient
not_available→insufficient or blocked according to task requirement
```

An observation is current only when:

```text
state=observed
scope exact match
observed_at + max_age_seconds >= binding evaluation time
valid_until >= binding evaluation time
environment_digest still matches
no invalidation condition active
```

## 12. Routing

Route record:

```yaml
- id: "<exact route id>"
  task_kinds: []
  kind: skill|tool|workflow
  target_id: "<exact target id>"
  revision: "<exact revision>"
  digest: "sha256:<hex> or none"
  immutable_ref: "<exact immutable reference or none>"
```

At least one of `digest` or `immutable_ref` is required.

```text
route resolved != authority
route available != capability for unrelated operations
route procedure cannot weaken K1/PF1/P1L
unknown route→blocked or explicit no_route disposition
```

## 13. Approval references

PF1 may declare which restrictions require approval and the expected operation/scope. Actual approval evidence remains a separate binding input.

```text
approval rule declaration != approval evidence
conversation memory != approval evidence
approval digest valid != executable
```

Minimum approval reference validity follows the K1 schema.

## 14. PF1 not_applicable

PF1 may be omitted only when exact K1 policy permits no-profile binding and every no-profile condition is satisfied.

```text
implicit project default/preset/alias/restriction/capability dependency→blocked
```

## 15. Compatibility

Project-local PF1 files are compatibility evidence only until migrated.

Migration requires:

```text
exact identity/canonical digest
all fields categorized
all aliases/presets expanded
implicit permission removed
Stop continuation separated from authority
authority ceilings explicit for all eight rails
commands/paths preserved exactly
lint pass
human review/approval
```

## 16. Non-goals

```text
runtime-binding resolver implementation
binding-evidence schema
execution authorization
BINDING.executable:true
actual route invocation
actual command/credential use
Packet normalized-state promotion
stable/public-ready/tag/release/Release Assets operation
```
