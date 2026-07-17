# Phase 7A — Canonical P1/P1L Contract Design

status: design-candidate
review_date: 2026-07-17
repository: tk999jp/kdsl-spec
base_ref: main
base_commit: aa6530dd7a288b65e98c50ce01a1cbc8863454b2
tracking_issue: 118

## 1. Goal

Define the ownership, structure, compatibility, and authority boundaries required to adopt a canonical v2-draft P1/P1L contract schema in a later specification phase.

```text
KDSL-DP
→ normalization
P1L canonical structured contract
→ optional compact serialization
P1
→ runtime binding / authority evaluation
execution candidate
→ execution
R1 / KDSL_RESULT
```

This design does not create an executable transformer and does not authorize execution.

## 2. Confirmed sources

Canonical repository sources:

```text
spec/bridge/kdsl-adps-bridge.md
spec/manifest.md
spec/glossary.md
spec/packet/kdsl-packet-schema.md
spec/packet/kdsl-packet-normalization-contract.md
spec/r1/r1-result-spec.md
```

Operational evidence inspected from `tk999jp/MidFD-dev`:

```text
.codex/adps/README.md
.codex/adps/kernel.k1.md
.codex/adps/profiles/MidFD.safe.v2.pf1.md
.codex/adps/examples/safe-fix.p1.md
.codex/adps/examples/investigate.p1.md
.codex/adps/examples/closeout.p1.md
.codex/prompt_templates/kdsl_base_dev.md
```

Evidence boundary:

```text
MidFD ADPS files:=current operational evidence
MidFD ADPS files != kdsl-spec canonical specification
example/profile behavior not defined in canonical repository→automatic adoption prohibited
unknown alias/preset/profile meaning→inference prohibited
```

## 3. Current gap

The repository currently defines only:

```text
P1/P1L:=KDSL-DPから正規化された実行契約候補
KDSL-DP直接実行禁止
P1/P1L正規化必須
P1/P1L valid != executable
```

It does not define:

```text
P1L marker/schema/required fields
P1 marker/serialization grammar
P1↔P1L ownership
profile completion evidence
loss classification
authority field requirements
runtime requirement semantics
round-trip acceptance
runtime binding gate
```

Therefore Packet normalization correctly remains blocked for P1/P1L targets.

## 4. Decision

Adopt this ownership direction for Phase 7B specification work:

```text
P1L:=lossless structured normalized contract schema
P1:=compact serialization profile subordinate to P1L
```

Candidate schema IDs:

```text
P1L: kdsl-p1l@0.1-draft
P1:  kdsl-p1@0.1-draft
```

Candidate ownership:

```text
Core/Profile/R1/Bridge canonical meaning
> P1L canonical v2-draft contract schema
> P1 compact serialization profile
> P1/P1L lint
> validator/example/tool
```

### 4.1 Why P1L is the structured canonical form

Existing operational `P1|...` examples are compact, profile-dependent, and omit expanded defaults. They are useful transport forms but are not sufficient as a self-contained canonical contract.

P1L provides:

```text
explicit required fields
expanded profile defaults
full authority rails
source/profile identity
observed/inferred separation
unresolved/loss evidence
round-trip basis
```

P1 then becomes a reversible compact representation rather than a second independent contract language.

### 4.2 Rejected alternatives

Alternative A:

```text
P1 compact syntax:=sole canonical contract
P1L:=undefined alias
```

Rejected because profile-dependent omissions would make canonical meaning depend on external unstated defaults.

Alternative B:

```text
P1 and P1L:=independent canonical schemas
```

Rejected because two independently authoritative execution-contract schemas would create ownership conflicts and semantic drift.

Alternative C:

```text
P1L:=human-readable example only
P1:=canonical compact schema
```

Rejected because round-trip and loss evidence require a structured authoritative projection.

## 5. State separation

Required state model:

```text
KDSL-DP valid
P1L structurally valid
P1 serialization valid
profile binding valid
runtime binding valid
execution authority sufficient
executable
executed
verified
runtime verified
```

Forbidden equivalences:

```text
KDSL-DP valid = P1L valid
P1L valid = executable
P1 valid = executable
P1/P1L lint pass = authority
P1/P1L round-trip pass = semantic equivalence
build/test/CI pass = RT:v
```

Candidate contract status:

```text
STATUS: contract-candidate
BINDING.state: unbound|bound|blocked
BINDING.executable: false|true
```

Phase 7B must keep the adopted schema default at:

```text
BINDING.state: unbound
BINDING.executable: false
```

`true` requires a separate runtime-control and authority specification. P1/P1L schema adoption alone must not enable it.

## 6. P1L candidate envelope

Candidate opening:

```text
P1L:
SCHEMA: kdsl-p1l@0.1-draft
STATUS: contract-candidate
```

Candidate required field order:

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

No implicit defaults are defined by the schema itself.

## 7. P1L candidate record shape

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
  runtime_control: "<K1/PF1 reference or unresolved>"
  state: unbound|bound|blocked
  executable: false
```

This is a Phase 7A candidate, not yet a canonical field schema.

## 8. Field semantics

### 8.1 META

`META` identifies the contract revision and lineage.

```text
contract_id missing→blocked for executable binding
parent_id does not grant authority
contract_rev mismatch→blocked or explicit compatibility path
```

### 8.2 SOURCE

`SOURCE` binds the normalized contract to exact authoring input.

```text
source digest:=identity evidence only
source digest != semantic equivalence
source references may include repo/path/file/URL exact strings
multiple unresolved sources→blocked
```

### 8.3 PROFILE

Profile completion is allowed only when all of the following are available:

```text
exact profile id
exact profile revision
profile content or digest
field-specific declared default
completion evidence listing completed fields
```

Forbidden:

```text
profile name similarity completion
past-memory completion
project convention completion without declared profile
unknown alias/preset inference
critical authority completion from unstated defaults
```

`PROFILE.completion` meanings:

```text
explicit:=all required values are explicit in normalized source
profile_completed:=declared profile supplied one or more values
blocked:=required profile/default cannot be verified
```

### 8.4 TASK

Canonical `TASK.kind` uses expanded values. Project-specific task codes remain profile aliases and must be expanded during normalization.

```text
T:I without known profile/alias definition→blocked
T:F without known profile/alias definition→blocked
unknown task code→otherへ自動補正禁止
```

### 8.5 SCOPE

`SCOPE` separates source, required reads, allowed targets, and explicit non-targets.

```text
read target != edit target
TGT外operation禁止
repo/path/file/branch/tag/API/command exact strings保持
empty target with edit authority→blocked
```

### 8.6 CONTEXT

Required separation:

```text
observed != inferred
unverified != absent
not_observed != confirmed absent
```

Inference must not be promoted to observation during normalization.

### 8.7 GOAL / PLAN

`GOAL` defines outcome/questions. `PLAN` defines proposed strategy and ordered steps.

```text
plan step != authority
plan step != command executed
strategy proposal != approved design change
```

### 8.8 GUARD / STOP

Must preserve complete applicable wording for:

```text
禁止
必須
未確認
未実行
承認/承認待
rollback/revert
public履歴/公開済tag/Release Assets
data protection
D禁止
KDSL-DP直接実行禁止
P1/P1L正規化必須
RT:v
NEXT/COMMIT authority boundaries
```

Safety Gate IDs or profile presets may supplement but never replace protected wording.

### 8.9 VERIFY

`VERIFY` records requirements, not completed results.

```text
verify requirement != verify executed
not_run/unavailable/user_required→pass扱禁止
build/diff/lint/test/CI pass != RT:v
```

Executed evidence belongs in R1/R1C.

### 8.10 RUNTIME

P1L is a pre-execution contract. Therefore `RUNTIME` expresses disposition/required evidence, not a completed result state.

Candidate mapping:

```text
pending        → legacy compact RT:p
user_required  → legacy compact RT:u
not_applicable → legacy compact RT:na
```

Result-only values remain in R1/R1C:

```text
RT:v
RT:fail
RT:blk
```

A P1/P1L requirement may require eventual `RT:v`, but it must not claim `RT:v` before evidence exists.

### 8.11 OUTPUT

`OUTPUT.result_schema` requests a result format. It does not claim success.

```text
R1C selection != R1C validity
R1C validity != task success
NEXT remains proposal
COMMIT remains report/proposed message, not authority
```

### 8.12 AUTHORITY

All authority rails are explicit in P1L.

Required rails:

```text
read
edit
stage
commit
push
release
public_repo
destructive_ops
```

Rules:

```text
read allow != edit allow
edit allow != stage allow
commit allow != push allow
push allow != release allow
public_repo allow != history rewrite allow
destructive_ops allow_once requires exact target and scope
missing authority rail→blocked
profile completion of critical authority rail→allowed only from exact declared profile default and recorded evidence
```

### 8.13 NORMALIZATION

Candidate states:

```text
explicit
profile_completed
lossy
blocked
```

Rules:

```text
critical unresolved/loss→blocked
lossy contract→runtime binding prohibited
profile_completed requires exact profile evidence
structural_pass != semantic equivalence/safety proof/authority
semantic_equivalence:not_proven fixed in v0.1 draft
```

### 8.14 BINDING

`BINDING` separates schema validity from execution readiness.

```text
P1L/P1 parser pass→BINDING.state unchanged
K1/PF1 reference missing→unbound|blocked
runtime control valid != authority sufficient
authority sufficient != executed
```

## 9. P1 compact serialization candidate

Candidate opening:

```text
P1|...
```

P1 is valid only when it can reconstruct the required P1L projection without invention.

Candidate field map:

```text
M    → META + SOURCE/PROFILE/NORMALIZATION metadata
T    → TASK
S    → SCOPE.target or declared primary scope
SRC  → SCOPE.source
R    → SCOPE.read
N    → SCOPE.non_target
B    → CONTEXT.background
OBS  → CONTEXT.observed
INF  → CONTEXT.inferred
U    → CONTEXT.unverified
E    → GOAL.expected
Q    → GOAL.questions
P    → PLAN
G    → GUARD
X    → STOP
V    → VERIFY
RT   → RUNTIME disposition only
O    → OUTPUT
A    → AUTHORITY
BD   → BINDING
```

Exact compact grammar is deferred to Phase 7B.

Required compact behavior:

```text
unknown field alias→blocked
unknown task/profile/preset alias→blocked
critical P1L field omitted without exact profile completion→blocked
compact field order fixed
repeated field ownership explicit
escaping/quoting defined
path/command/API exact strings preserved
```

## 10. Existing MidFD P1 compatibility

Confirmed operational evidence:

```text
P1|M:contract_rev=0.1,profile=MidFD.safe.v2,loss=P,conf=high|T:F|S:...|B:...|E:...|G:safe|P:...|V:b+diff|X:...|O:std|RT:u
```

Compatibility interpretation:

```text
existing P1 examples:=legacy operational serialization evidence
existing P1 examples != automatic canonical conformance
```

Known mapping evidence:

```text
loss=P:=profile completion
G/V/X/O profile presets exist in MidFD.safe.v2
T:I/T:F/T:A/T:RF/T:C routing exists in MidFD.safe.v2
RT:u:=user runtime check remains
```

Unresolved evidence:

```text
loss=L meaning is not defined in retrieved canonical kdsl-spec source
P1L concrete operational syntax is absent
AP/H abbreviations mentioned by runtime kernel are not defined as canonical P1 fields
profile digest binding is absent from existing examples
explicit authority rails are absent from existing P1 examples
```

Rules:

```text
loss=L meaning推測禁止
AP/H meaning推測禁止
existing P1 lacking authority rails→canonical P1Lへ自動昇格禁止
compatibility adapter may require project profile + base permission contract
```

Phase 7B must define an explicit legacy compatibility policy rather than silently treating current examples as canonical.

## 11. P1↔P1L round-trip

Candidate structural model:

```text
P1L canonical projection
→ compact P1 serialization
→ parse P1
→ bind exact profile definitions
→ reconstruct P1L canonical projection
→ compare required fields/order/exact strings/authority rails
```

Required preservation:

```text
source/profile identity
scope and non-targets
observed/inferred/unverified classification
goal/questions
plan order
guards/protected wording
stop conditions
verify requirements
runtime disposition
output requirements
authority rails
normalization/binding state
exact strings
```

Allowed result states:

```text
not_tested
structural_pass
loss_detected
blocked
```

Boundary:

```text
structural_pass != semantic equivalence
structural_pass != complete safety proof
structural_pass != execution authority
structural_pass != runtime binding
```

## 12. Packet normalization dependency

After Phase 7B canonical adoption, Packet normalization may change from:

```text
P1/P1L target schema unresolved
resolution: blocked
preview: prohibited
```

to a reviewable non-executable mapping target only after a separate Phase 7D integration.

Required preview markers:

```text
P1L_PREVIEW
P1_PREVIEW
```

Forbidden in Packet normalization output:

```text
P1L:
P1|
KDSL_PROMPT:
executable:true
execution_authority other than none
```

Canonical P1/P1L schema adoption does not itself complete Packet normalization.

## 13. Compatibility classification

Candidate change classification:

```text
new P1L schema adoption: compatible v2-draft addition
new P1 compact schema adoption: compatible v2-draft addition
existing P1 operational syntax declared legacy evidence: documentation-compatible
silently redefining existing project aliases: breaking/prohibited
changing KDSL-DP direct-execution boundary: breaking/prohibited
changing R1 RT/NEXT/COMMIT meaning: breaking/prohibited
```

## 14. Phase 7B required files

Candidate canonical additions:

```text
spec/adps/kdsl-p1l-contract-schema.md
spec/adps/kdsl-p1-compact-contract-schema.md
spec/lint/kdsl-p1-p1l-lint.md
```

Candidate examples:

```text
examples/adps/p1l-investigate.example.md
examples/adps/p1-profile-completed.example.md
examples/adps/p1-unknown-profile-blocked.example.md
examples/adps/p1-authority-missing-blocked.example.md
```

Required synchronization:

```text
spec/bridge/kdsl-adps-bridge.md
spec/manifest.md
spec/glossary.md
spec/glossary-v2-draft.md
docs/project-status.md
```

## 15. Phase 7A acceptance

Phase 7A design is acceptable when:

```text
P1L/P1 ownership is explicit
required P1L fields are enumerated
compact mapping surface is enumerated
profile completion and inference are separated
runtime requirement and R1 result status are separated
authority rails are mandatory
binding/executable state is separate
legacy MidFD evidence is not promoted by inference
Packet normalization remains non-executable
RT/NEXT/COMMIT boundaries remain unchanged
```

## 16. Stop conditions

Stop Phase 7 implementation when:

```text
P1L/P1 ownership becomes ambiguous
unknown legacy alias meaning must be inferred
profile defaults cannot be bound to exact revision/digest
critical authority rail would be implicit
P1 compact round-trip requires protected wording loss
RUNTIME contract field would claim RT:v without evidence
Packet preview would become executable
K1/PF1 runtime control must be invented in this phase
R1/R1C result semantics would change
```

## 17. Non-goals

```text
executable transformer
runtime binding implementation
K1/PF1 canonical schema
automatic AI tool execution
complete semantic equivalence proof
complete safety proof
project-specific profile standardization
Packet executable promotion
stable/public-ready promotion
tag/release/Release Assets operation
```

## 18. Next implementation order

```text
1. review/adopt this ownership design
2. add P1L canonical v2-draft schema
3. add P1 subordinate compact serialization schema
4. add lint and examples
5. synchronize Bridge/manifest/glossary/status
6. implement parser/validator first slice
7. integrate Packet normalization under non-executable preview boundary
```