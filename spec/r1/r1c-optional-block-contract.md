# R1C Deep Optional-Block Contract v0.1 Draft Candidate

status: implementation-candidate
canonical: no
model: kdsl-r1c-optional-blocks@0.1-draft
parent_schema: kdsl-r1c@0.1-draft
base_canonical: spec/r1/r1-result-spec.md
executable: no

## 1. Purpose

This contract defines the Phase 3 bounded validation and structural round-trip rules for optional R1C blocks.

```text
canonical R1 > R1C schema > optional-block contract > validator/example
optional-block pass != Full R1 semantic equivalence
optional-block pass != safety proof
optional-block pass != RT:v
optional-block pass != execution authority
```

## 2. Covered blocks

```text
EVIDENCE
AUTHORITY
ANNUNCIATOR
SAFETY_GATES
```

Phase 3 deep validation applies to `EVIDENCE`, `AUTHORITY`, and `SAFETY_GATES`.
`ANNUNCIATOR` receives structural key validation and exact round-trip preservation only because canonical value semantics are not fully enumerated.

## 3. EVIDENCE exact shape

```json
{
  "observed":[],
  "inferred":[],
  "not_observed":[],
  "unverified":[]
}
```

Rules:

```text
4 key必須
unknown key禁止
各value=array<string>
empty string禁止
同一class内duplicate禁止
class間同一item重複禁止
observed != inferred
not_observed != confirmed
unverified != RT:v basis
VERIFY.pass×not_observed|unverified衝突禁止
```

Normalization is limited to case/whitespace comparison for duplicate and conflict detection. It does not prove linguistic equivalence.

## 4. AUTHORITY exact rails

Required exact keys:

```text
read
edit
stage
commit
push
release
```

Allowed values:

```text
allow|forbid|target_only|allow_once|propose_only|not_requested|not_applicable
```

Cross-field rules:

```text
FILES非空 + edit=forbid|not_requested|not_applicable→fail
executed git add + stage非許可→fail
executed git commit + commit非許可→fail
executed git push + push非許可→fail
executed tag/release/assets操作 + release非許可→fail
COMMIT.actual + commit=forbid|not_requested|not_applicable→fail
COMMIT.actual + commit=propose_only + permission_basisなし→fail
COMMIT.actual + commit=propose_only + separate permission_basis→warn/保持
```

```text
AUTHORITY rail record != authority grant
COMMIT.proposed != commit permission
NEXT != execution permission
```

## 5. ANNUNCIATOR boundary

Allowed canonical keys:

```text
STATUS
PHASE
AUTHORITY
RT
PUBLIC_OPS
DESTRUCTIVE_OPS
```

Rules:

```text
JSON object必須
unknown key禁止
exact structure/order-independent value preservation
value semanticsのimplicit default禁止
Phase 3ではfull consistency proofなし
```

## 6. SAFETY_GATES structure

```text
SAFETY_GATES:
  registry: kdsl-sg@0.1-draft
  entries:
    - id:
      state:
      scope:
      reason:
      evidence:
      authority:
```

Validation:

```text
known registryのみ
entries必須
ID重複禁止
known ID/stateのみ
id/state/scope/reason必須
unknown entry field禁止
state:satisfied→evidence + verified authority/not_required必須
state:blocked→observed evidence推奨
state:na→reason必須
SG ID-only compression禁止
```

Structural projection preserves:

```text
registry
entry order
entry field order
all field values
```

## 7. Round-trip

```text
R1C source
→ canonical Full R1 structural projection
→ R1C reconstruction
→ exact selected-property comparison
```

Required preservation:

```text
optional block order
EVIDENCE class keys/items/order
AUTHORITY rail keys/values
ANNUNCIATOR object structure
SAFETY_GATES registry/entry order/field order/state/scope/reason/evidence/authority
```

Failure:

```text
unknown key/value
implicit default required
classification/authority conflict
Safety Gate loss or mutation
optional block order mutation
```

Fallback:

```text
round-trip不成立→R1C使用禁止→Full R1出力
```

## 8. Non-goals

```text
Full R1 semantic equivalence proof
full natural-language evidence classification
authority grant
RT:v decision
Packet execution
Packet normalization completion
stable/public-ready promotion
```

## 9. Verification target

```text
existing unified suite: 181 / failed 0
Phase 3 optional-block property suite: 34 / failed 0
expected unified total: 215 / failed 0
```
