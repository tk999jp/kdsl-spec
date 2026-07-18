# KDSL Binding Evidence Schema v0.1 Draft

status: v2-draft adopted
canonical: v2-draft
schema_id: kdsl-binding-evidence@0.1-draft
canonicalization: kdsl-runtime-control-c14n@0.1-draft
executable: no
authority_grant: no

## 1. Purpose

Define the external content-addressed record referenced by `P1L.BINDING.runtime_control`.

```text
valid record != authority grant
valid record != approval authenticity proof
valid record != capability truth proof
valid record != semantic equivalence|complete safety proof|RT:v
```

Identity, profile, completion, restriction, authority, capability, Stop, and precondition states remain independent.

## 2. Ownership

```text
Core/R1/Bridge
> P1L/P1
> K1/PF1
> binding-evidence schema
> lint
> future resolver
> example/tool
```

## 3. Envelope and field order

```text
BINDING_EVIDENCE:
SCHEMA: kdsl-binding-evidence@0.1-draft
STATUS: external-content-addressed-record
```

```text
BINDING_EVIDENCE
SCHEMA
STATUS
IDENTITY
SUBJECT
RUNTIME_CONTROL
EVALUATION
COMPLETION
RESTRICTIONS
AUTHORITY
APPROVALS
CAPABILITIES
STOP
PRECONDITIONS
BINDING
PROVENANCE
```

Unknown, duplicate, missing, or reordered required fields are blocked. No implicit defaults exist.

## 4. Record shape

```yaml
BINDING_EVIDENCE:
SCHEMA: kdsl-binding-evidence@0.1-draft
STATUS: external-content-addressed-record
IDENTITY:
  id: "<exact record id>"
  revision: "<exact revision>"
  canonicalization: kdsl-runtime-control-c14n@0.1-draft
  digest: "sha256:<hex>"
  source_ref: "<exact source reference>"
SUBJECT:
  contract_schema: kdsl-p1l@0.1-draft|kdsl-p1@0.1-draft
  contract_id: "<exact contract id>"
  contract_digest: "sha256:<hex>"
  project_id: "<exact id or none>"
  repository: "<exact repository or none>"
  task_kind: "<exact task kind>"
RUNTIME_CONTROL:
  k1_ref:
    id: "<exact K1 id>"
    revision: "<exact revision>"
    digest: "sha256:<hex>"
    source_ref: "<exact source reference>"
  pf1_state: resolved|not_applicable|blocked
  pf1_ref:
    id: "<exact PF1 id or none>"
    revision: "<exact revision or none>"
    digest: "sha256:<hex> or none"
    source_ref: "<exact source reference or none>"
  compatibility_state: valid|blocked
EVALUATION:
  evaluated_at: "<UTC RFC3339 timestamp>"
  evaluator_ref:
    id: "<exact evaluator id>"
    revision: "<exact revision>"
    digest: "sha256:<hex> or none"
    immutable_ref: "<exact immutable reference or none>"
  repository_state_ref: "<exact immutable reference or none>"
  environment_state_ref: "<exact immutable reference or none>"
COMPLETION:
  state: explicit|profile_completed|blocked
  completed_fields: []
  expansions: []
  unresolved: []
RESTRICTIONS:
  state: applied|conflict|blocked
  applied: []
  conflicts: []
AUTHORITY:
  state: sufficient|insufficient|conflict|blocked
  rails:
    read: {}
    edit: {}
    stage: {}
    commit: {}
    push: {}
    release: {}
    public_repo: {}
    destructive_ops: {}
APPROVALS:
  state: sufficient|insufficient|unverified|not_required|blocked
  requirements: []
  evidence: []
CAPABILITIES:
  state: sufficient|insufficient|stale|unverified|not_required|blocked
  requirements: []
  observations: []
STOP:
  state: clear|active|unknown|blocked
  rules_checked: []
  matches: []
PRECONDITIONS:
  state: satisfied|unsatisfied|unknown|blocked
  requirements: []
  evidence: []
BINDING:
  state: unbound|bound|blocked
  identity_state: resolved|blocked
  profile_state: resolved|not_applicable|blocked
  completion_state: explicit|profile_completed|blocked
  restriction_state: applied|conflict|blocked
  authority_state: sufficient|insufficient|conflict|blocked
  capability_state: sufficient|insufficient|stale|unverified|not_required|blocked
  stop_state: clear|active|unknown|blocked
  precondition_state: satisfied|unsatisfied|unknown|blocked
  executable: false
  semantic_equivalence: not_proven
  execution_authority: none
PROVENANCE:
  generated_at: "<UTC RFC3339 timestamp>"
  source_records: []
  notes: []
```

`evaluator_ref` requires `digest` or `immutable_ref`. `none` is explicit only where declared.

## 5. P1L reference form

A resolved `P1L.BINDING.runtime_control` uses this compact JSON string:

```text
{"schema":"kdsl-binding-evidence@0.1-draft","id":"<exact id>","revision":"<exact revision>","digest":"sha256:<64 lowercase hex>"}
```

```text
key order:=schema,id,revision,digest
whitespace:=none
encoding:=JSON escaping / UTF-8
unknown|missing key→blocked
name-only|source_ref-only reference→blocked
digest mismatch→blocked
`unresolved` allowed only with P1L state unbound|blocked
```

The reference is created after record digest calculation and is not included in the record.

## 6. Canonical identity

Use schema-ordered semantic projection and self-digest substitution:

```text
IDENTITY.digest=`sha256:SELF` during calculation
compact JSON→UTF-8→SHA-256
stored digest:=sha256:<64 lowercase hex>
```

Digest agreement proves content identity only.

## 7. Completion and restrictions

Completion expansion record:

```yaml
- field_path: "<exact P1L field path>"
  source_kind: default|preset|alias
  source_id: "<exact id>"
  source_revision: "<exact revision>"
  source_digest: "sha256:<hex>"
  category: guard|verify|stop|output|runtime|task|strategy|route
  ordered: true|false
  expanded_value_digest: "sha256:<hex>"
```

Restriction record:

```yaml
- id: "<exact restriction id>"
  source_revision: "<exact PF1 revision>"
  source_digest: "sha256:<hex>"
  effect: forbid|approval_required|stop
  rails: []
  task_kinds: []
  scope: "<exact scope or any>"
```

```text
profile_completed + missing provenance→blocked
unknown|cyclic|ambiguous|category mismatch→blocked
restriction conflict|unknown scope→blocked
completion|restriction evidence != authority grant
```

## 8. Authority rail record

Every rail uses:

```yaml
requested: allow|forbid|target_only|allow_once|propose_only|not_requested|not_applicable
k1_disposition: preserve|forbid|blocked
pf1_mode: allow_max|propose_only_max|forbid|approval_required|not_applicable_only
pf1_scope: any|target_only
pf1_cardinality: any|once
approval_requirement: required|not_required
approval_evidence_id: "<exact id or none>"
targets: []
operation_instance: "<exact instance or none>"
effective_value: allow|forbid|target_only|allow_once|propose_only|not_requested|not_applicable|blocked
effective_scope: any|target_only|none|blocked
effective_cardinality: any|once|none|blocked
state: sufficient|insufficient|conflict|blocked
```

```text
P1L forbid remains forbid
not_requested never becomes allow
K1/PF1 cannot widen P1L
allow_once requires exact operation_instance
target_only requires exact targets
capability is not an authority input
```

`AUTHORITY.state` is derived; the eight rail records remain controlling evidence.

## 9. Approval evidence

Approval record:

```yaml
- id: "<exact approval id>"
  revision: "<exact revision>"
  digest: "sha256:<hex>"
  source_ref: "<exact reviewable source>"
  issuer: "<explicit issuer identity>"
  issued_at: "<UTC RFC3339 timestamp>"
  operation: "<exact rail/operation>"
  scope: "<exact target/scope>"
  valid_until: "<UTC RFC3339 timestamp or none>"
  revoked: false
  content_state: valid|invalid|blocked
  trust_state: verified|unverified|blocked
  trust_policy_ref: "<exact immutable reference or none>"
```

```text
content validity != source trust
digest match != issuer authenticity
operation|scope|time mismatch→invalid|blocked
revoked:true→invalid
unverified source leaves approval requirement unsatisfied
approval accepted != executable
```

Signer authentication is outside this draft.

## 10. Capability evidence

Requirement record:

```yaml
- id: "<exact requirement id>"
  capability: "<exact capability id>"
  scope: "<exact environment/target>"
  max_age_seconds: <positive integer>
  required_state: observed
```

Observation record:

```yaml
- id: "<exact observation id>"
  revision: "<exact revision>"
  digest: "sha256:<hex>"
  capability: "<exact capability id>"
  state: observed|inferred|unverified|not_available
  scope: "<exact environment/target>"
  observed_at: "<UTC RFC3339 timestamp>"
  valid_until: "<UTC RFC3339 timestamp>"
  environment_digest: "sha256:<hex>"
  evidence_ref: "<exact evidence reference>"
  invalidation: []
  current_state: current|stale|invalidated|blocked
```

```text
requirement != observation
stale|inferred|unverified|not_available→insufficient
capability sufficient != authority sufficient
capability evidence != RT:v
```

Known insufficiency may coexist with `BINDING.state:bound`; unresolved identity mismatch is blocked.

## 11. Stop, preconditions, and binding

```text
Stop clear != authority grant
Stop active→cannot proceed
Stop unknown|blocked→binding blocked
precondition unsatisfied→not ready
precondition unknown|blocked→binding blocked
```

Binding meanings:

```text
unbound:=no complete exact record attached
bound:=subject and runtime-control identities are exact; all dimensions are recorded; no binding-level conflict exists
blocked:=critical identity, structure, provenance, Stop, or precondition conflict prevents binding
```

`bound` may coexist with authority insufficiency, capability insufficiency/staleness, active Stop, or unsatisfied precondition.

Fixed values:

```text
executable:false
semantic_equivalence:not_proven
execution_authority:none
```

No aggregate `pass`, `ready`, `authorized`, or equivalent field is defined.

## 12. Provenance

Source record:

```yaml
- kind: contract|k1|pf1|preset|alias|restriction|approval|capability|stop|precondition|evaluator
  id: "<exact id>"
  revision: "<exact revision or none>"
  digest: "sha256:<hex> or none"
  source_ref: "<exact source reference>"
```

Every source affecting a dimension must be listed. Provenance presence does not prove source trust.

## 13. Blocked conditions

```text
unknown|duplicate|required-field-order error
invalid self-digest
contract/K1/PF1 identity mismatch
unresolved exact reference
implicit profile completion
missing authority rail
restriction conflict
approval operation/scope mismatch
unknown critical Stop/precondition state
critical exact-string mutation
protected-wording weakening
```

Insufficient evidence must not be rewritten as success.

## 14. Non-goals

```text
runtime evaluator implementation
record generation implementation
approval authentication implementation
capability observation acquisition
route/tool invocation
execution authorization
executable promotion
Packet normalized-state promotion
stable/public-ready/tag/release/Release Assets operation
```
