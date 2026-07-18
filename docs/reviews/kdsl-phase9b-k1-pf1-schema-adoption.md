# Phase 9B — K1 / PF1 Schema Adoption Review

status: schema-candidate / alignment-pending
review_date: 2026-07-18
repository: tk999jp/kdsl-spec
tracking_issue: 132
pull_request: 135
base_main: 86b064133a5b83877f56a0d71eadabd3c1a7c8e1

## 1. Goal

Adopt canonical, non-executable K1/PF1 runtime-control schemas, deterministic identity rules, lint, and explanatory examples without implementing runtime binding or execution authorization.

## 2. Adopted candidates

```text
kdsl-k1@0.1-draft
kdsl-pf1@0.1-draft
kdsl-runtime-control-c14n@0.1-draft
```

## 3. Resolved Phase 9B decisions

```text
binding evidence:=external content-addressed record referenced by P1L.BINDING.runtime_control
canonicalization:=schema-ordered semantic projection→compact JSON→UTF-8→SHA-256
PF1 ceiling:=mode/scope/cardinality independent dimensions
approval evidence:=explicit content-addressed reference with exact operation/scope/time/revocation
capability evidence:=scoped observed record with freshness/expiry/invalidation
```

## 4. Authority model

```text
authority_effective
:= P1L explicit request
 ∩ K1 absolute rules
 ∩ PF1 restrictions/ceilings
 ∩ exact approval evidence when required
```

```text
capability_sufficient
:= required capability has current observed scope-matching evidence
```

Capability is evaluated separately and never creates permission.

## 5. Composite authority preservation

PF1 ceiling uses:

```text
mode: allow_max|propose_only_max|forbid|approval_required|not_applicable_only
scope: any|target_only
cardinality: any|once
```

This preserves combinations such as:

```text
P1L allow_once + PF1 target_only
→ request_value: allow_once
→ effective_scope: target_only
→ effective_cardinality: once
```

## 6. Files

```text
spec/runtime/README.md
spec/runtime/kdsl-runtime-control-canonicalization.md
spec/runtime/kdsl-k1-runtime-kernel-schema.md
spec/runtime/kdsl-pf1-project-profile-schema.md
spec/lint/kdsl-k1-pf1-lint.md
examples/runtime/k1-pf1-non-executable.example.md
```

Canonical alignment files are updated in the same PR.

## 7. Preserved boundaries

```text
K1/PF1 valid|lint pass != executable|authority grant
PF1 may narrow but never widen P1L authority
capability != permission
Stop continuation != authority
routing != authority
BINDING.executable:false
binding evidence != executable instruction
build/diff/lint/test/CI pass != RT:v
NEXT != execution authority
COMMIT != commit authority
Packet remains non-executable/not_normalized
```

## 8. Not implemented / not proven

```text
K1/PF1 parser/resolver/validator
canonical binding-evidence field schema
runtime binding
execution authorization artifact
BINDING.executable:true
executable transformer
automatic AI coding tool execution
approval issuer cryptographic authentication
semantic equivalence proof
complete safety proof
stable/public-ready promotion
```

No tag, release, or Release Assets operation is authorized by this phase.
