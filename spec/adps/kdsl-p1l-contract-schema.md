# KDSL P1L Contract Schema v0.1 Draft

status: v2-draft adopted
canonical: v2-draft
schema_id: kdsl-p1l@0.1-draft
executable: no
runtime_binding: separate

## 1. Purpose

P1L is the lossless structured normalized contract schema for KDSL-DP and other approved authoring inputs.

```text
KDSL-DP
→ normalization
P1L
→ optional compact serialization
P1
→ separate runtime binding / authority evaluation
execution candidate
→ execution
R1 / KDSL_RESULT
```

```text
P1L:=lossless structured normalized contract schema
P1L != direct execution instruction
P1L != authority grant
P1L valid != executable
P1L lint pass != executable
P1L round-trip pass != semantic equivalence/safety proof/authority
```

Priority:

```text
meaning/safety/scope/evidence/authority preservation > reversibility > compactness
```

## 2. Ownership

```text
Core/Profile/R1/Bridge canonical meaning
> P1L canonical v2-draft contract schema
> P1 compact serialization profile
> P1/P1L lint
> validator/example/tool
```

Conflict handling:

```text
P1L×Core/Profile/R1/Bridge→upper canonical source wins
unknown profile/alias/preset/schema→blocked
meaning/safety/scope/authority loss→blocked
```

## 3. Required envelope

```text
P1L:
SCHEMA: kdsl-p1l@0.1-draft
STATUS: contract-candidate
```

Required field order:

```text
P1L
SCHEMA
STATUS
META
SOURCE
PROFILE
TASK
SCOPE
CONTEXT
GOAL
PLAN
GUARD
STOP
VERIFY
RUNTIME
OUTPUT
AUTHORITY
NORMALIZATION
BINDING
```

All required fields must be present. The schema defines no implicit defaults.

## 4. Record shape

```yaml
P1L:
SCHEMA: kdsl-p1l@0.1-draft
STATUS: contract-candidate
META:
  contract_rev: "0.1"
  contract_id: "<stable task/contract id>"
  parent_id: "<optional parent id or none>"
SOURCE:
  kind: kdsl-dp|packet|manual
  digest: "sha256:<hex>"
  references: []
PROFILE:
  id: "<profile id or none>"
  revision: "<exact revision or none>"
  digest: "sha256:<hex> or none"
  completion: explicit|profile_completed|blocked
  completed_fields: []
TASK:
  kind: investigate|plan|implement|fix|add|refactor|closeout|docs|state|review|other
  declared: "<original task value>"
SCOPE:
  source: []
  read: []
  target: []
  non_target: []
CONTEXT:
  background: []
  observed: []
  inferred: []
  unverified: []
GOAL:
  expected: []
  questions: []
PLAN:
  strategy: []
  steps: []
GUARD:
  constraints: []
  safety_gates: []
  protected_wording: []
STOP: []
VERIFY:
  requirements: []
  unavailable_policy: report_not_run
RUNTIME:
  disposition: pending|user_required|not_applicable
  required_evidence: []
OUTPUT:
  result_schema: kdsl-r1c@0.1-draft|full-r1
  report_requirements: []
AUTHORITY:
  read: allow|forbid|target_only|allow_once|propose_only|not_requested|not_applicable
  edit: allow|forbid|target_only|allow_once|propose_only|not_requested|not_applicable
  stage: allow|forbid|target_only|allow_once|propose_only|not_requested|not_applicable
  commit: allow|forbid|target_only|allow_once|propose_only|not_requested|not_applicable
  push: allow|forbid|target_only|allow_once|propose_only|not_requested|not_applicable
  release: allow|forbid|target_only|allow_once|propose_only|not_requested|not_applicable
  public_repo: allow|forbid|target_only|allow_once|propose_only|not_requested|not_applicable
  destructive_ops: allow|forbid|target_only|allow_once|propose_only|not_requested|not_applicable
NORMALIZATION:
  state: explicit|profile_completed|lossy|blocked
  unresolved: []
  loss: []
  round_trip: not_tested|structural_pass|loss_detected|blocked
  semantic_equivalence: not_proven
BINDING:
  runtime_control: "<compact kdsl-binding-evidence reference or unresolved>"
  state: unbound|bound|blocked
  executable: false
```

## 5. META / SOURCE

```text
contract_id missing→binding blocked
parent_id != authority
contract_rev mismatch→blocked or explicit compatibility path
source digest:=source identity evidence only
source digest != semantic equivalence
multiple unresolved source identities→blocked
```

Repo/path/file/branch/tag/commit/URL/command/package/class/method/property/API and Windows path strings must remain exact.

## 6. PROFILE completion

Profile completion is permitted only when all are available:

```text
exact profile id
exact profile revision
profile content or digest
field-specific declared default
completed_fields evidence
```

```text
explicit:=all required values explicit in normalized source
profile_completed:=verified profile supplied one or more values
blocked:=required profile/default cannot be verified
```

Forbidden:

```text
similar-name completion
memory/conversation/convention completion
unknown alias/preset inference
critical authority completion from unstated defaults
```

`profile_completed` may not hide completed values; the canonical P1L projection must contain the expanded values.

## 7. TASK / SCOPE / CONTEXT

```text
project task code→expanded TASK.kind required
unknown task code→other inference prohibited
read scope != edit scope
empty target + edit/stage/commit authority→blocked
TGT外operation prohibited
observed != inferred
unverified != absent
inferred→observed promotion prohibited
```

## 8. GOAL / PLAN / GUARD / STOP

```text
PLAN step != authority
PLAN step != executed command
strategy proposal != approved design change
STOP activation→prohibited remaining flow must stop
```

Complete applicable wording must be preserved for:

```text
禁止/必須/未確認/未実行/承認/承認待
rollback/revert/data protection
public履歴/公開済tag/Release Assets
D禁止/停止条件
KDSL-DP直接実行禁止/P1/P1L正規化必須
RT:v/NEXT/COMMIT authority boundaries
```

Safety Gate IDs and presets may supplement but never replace protected wording.

## 9. VERIFY / RUNTIME

`VERIFY` contains requirements, not results.

```text
verify requirement != verify executed
not_run/unavailable/user_required→pass扱禁止
build/diff/lint/test/CI pass != RT:v
```

P1L is pre-execution. `RUNTIME.disposition` is limited to:

```text
pending
user_required
not_applicable
```

Compact compatibility:

```text
pending        ↔ RT:p
user_required  ↔ RT:u
not_applicable ↔ RT:na
```

Result values belong only in R1/R1C:

```text
RT:v
RT:fail
RT:blk
```

A contract may require eventual runtime evidence but must not claim `RT:v` before that evidence exists.

## 10. OUTPUT

```text
OUTPUT.result_schema:=requested result serialization
result-schema selection != result validity/success
NEXT:=proposal, not execution authority
COMMIT:=actual/proposed record, not commit authority
```

## 11. AUTHORITY

All eight rails are required:

```text
read/edit/stage/commit/push/release/public_repo/destructive_ops
```

```text
read allow != edit allow
edit allow != stage allow
commit allow != push allow
push allow != release allow
public_repo allow != history rewrite allow
destructive_ops allow_once→exact target/scope required
missing rail→blocked
```

`not_requested` is not `allow`. `propose_only` permits proposal, not operation.

## 12. NORMALIZATION

Allowed states:

```text
explicit
profile_completed
lossy
blocked
```

```text
critical unresolved/loss→blocked
lossy→runtime binding prohibited
profile_completed→exact profile evidence required
semantic_equivalence:not_proven fixed in v0.1 draft
structural_pass != semantic equivalence/safety proof/authority
```

Critical classes include scope, non-target, observation classification, goal, plan order, Guard/protected wording, Stop, Verify, Runtime disposition, Output requirements, Authority rails, source/profile identity, and exact strings.

## 13. BINDING

`kdsl-binding-evidence@0.1-draft` defines the external evidence-record fields. P1L stores only this compact JSON scalar reference:

```text
{"schema":"kdsl-binding-evidence@0.1-draft","id":"<exact id>","revision":"<exact revision>","digest":"sha256:<64 lowercase hex>"}
```

The fixed key order is `schema,id,revision,digest` with no insignificant whitespace. A resolved reference must match the exact external record. This reference form does not define a runtime evaluator.

```text
BINDING.state default: unbound
BINDING.executable fixed: false
P1L parser/lint pass→BINDING unchanged
K1/PF1 missing→unbound|blocked
runtime control valid != authority sufficient
authority sufficient != executed
```

`BINDING.executable:true` is prohibited under `kdsl-p1l@0.1-draft` until a separately approved runtime-binding specification exists.

## 14. P1 relation and round-trip

```text
P1L canonical projection
→ P1 compact serialization
→ parse P1
→ bind exact profile definitions
→ reconstruct P1L canonical projection
→ compare required fields/order/exact strings/authority rails
```

Required preservation:

```text
source/profile identity
scope/non-target
observed/inferred/unverified classification
goal/questions
plan order
Guard/protected wording
Stop/Verify/Runtime/Output
all Authority rails
Normalization/Binding state
exact strings
```

Allowed round-trip states:

```text
not_tested|structural_pass|loss_detected|blocked
```

`structural_pass` does not prove semantic equivalence, complete safety, runtime binding, or execution authority.

## 15. Legacy operational P1

Existing project-local `P1|...` forms are compatibility evidence, not automatic conformance.

```text
loss=P may be recognized only by an explicit compatibility rule as profile completion
loss=L meaning remains unknown and must be blocked
AP/H meanings remain unknown and must be blocked
missing explicit Authority rails→canonical promotion blocked unless an exact profile/base permission contract supplies every rail with evidence
```

## 16. Validity

A P1L document is structurally valid only when:

```text
exact envelope/schema/status/order
all fields present
source/profile identity consistent
no unknown inference
all critical values explicit or verified profile-completed
all Authority rails present
no critical unresolved/loss
RUNTIME contains no result-only claim
NORMALIZATION evidence consistent
BINDING.executable:false
```

Structural validity does not authorize execution.

## 17. Invalid conditions

```text
STATUS executable-equivalent
BINDING.executable:true
unknown schema/profile/alias/preset inferred
missing field or Authority rail
edit authority with empty target
lossy contract marked bound
RT:v/fail/blk used as pre-execution result claim
protected wording/Stop/non-target deletion
exact string alteration
NEXT/COMMIT treated as authority
KDSL-DP direct execution
```

Any invalid condition blocks contract use.

## 18. Non-goals

```text
executable transformer
runtime binding implementation
K1/PF1 canonical schema
automatic AI tool execution
complete semantic equivalence proof
complete safety proof
project-specific profile standardization
Packet executable promotion
stable/public-ready/tag/release/Release Assets operation
```
