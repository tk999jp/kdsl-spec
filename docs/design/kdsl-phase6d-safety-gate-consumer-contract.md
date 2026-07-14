# Phase 6D-8A — Safety Gate Helper Consumer Contract

status: implementation-candidate / non-canonical design evidence
review_date: 2026-07-14
repository: tk999jp/kdsl-spec
base_ref: main
tracking_issue: 55

## 1. Goal

Freeze the exact Safety Gate helper-consumer surface before changing any imports from `kdsl_safety_gate`.

```text
inventory first
→ classify structural vs semantic utility use
→ freeze per-consumer return/exit contract
→ migrate structural input only
→ decide helper retention last
```

This phase does not change Safety Gate parsing, inheritance, graph, R1C optional semantics, protected wording, authority, or exit behavior.

## 2. Runtime consumers

### `kdsl_safety_semantics.py`

```text
structural:
  extract_gate_block
  parse_registry

decision:
  migrate structural extraction to SafetyGateCompatibilityView
```

### `kdsl_safety_gate_inheritance.py`

```text
structural:
  extract_gate_block
  parse_registry

semantic utility:
  REGISTRY
  aggregate_state
  authority_is_unverified
  is_blank

decision:
  migrate structural extraction
  retain semantic utility imports until a separate utility-location decision
```

### `kdsl_safety_gate_graph.py`

```text
structural:
  extract_gate_block
  parse_registry

semantic utility:
  REGISTRY
  aggregate_state
  authority_is_unverified
  is_blank

decision:
  migrate structural extraction
  retain semantic utility imports until a separate utility-location decision
```

### `kdsl_r1c_optional.py`

```text
structural:
  parse_registry

semantic/constants:
  KNOWN_IDS
  KNOWN_STATES
  REGISTRY
  REQUIRED_FIELDS
  authority_is_unverified
  is_blank

decision:
  migrate embedded SAFETY_GATES parsing to SafetyGateCompatibilityView
  retain semantic/constants until a separate utility-location decision
```

## 3. Non-consumers

The following are not direct helper consumers:

```text
run_safety_semantics_samples.py
run_safety_semantics_examples.py
kdsl_validate.py
```

They invoke consumer modules or subprocess checkers and must not be classified as runtime structural helper consumers.

## 4. Structural compatibility target

Migration target:

```text
tools/validator/kdsl_parser_v2_safety_gate_compat.py
SafetyGateCompatibilityView
```

Required view channels:

```text
present
block_text
registry
entry_dicts
entry_field_orders
```

The CompatibilityView does not decide:

```text
registry validity
known IDs
state validity
inheritance
scope relation
protected wording
composition
authority
safety proof
execution authority
```

## 5. Frozen consumer contracts

### Safety semantics

```text
no SAFETY_GATES block → unchanged not-applicable result
valid block → same semantic atoms/concept checks
invalid registry or entries → same downstream rejection
```

### Inheritance

```text
parent/child entry maps preserve gate order/value mapping
hold/blocked propagation unchanged
satisfied scope re-evaluation unchanged
aggregate state output unchanged
```

### Graph

```text
node file parsing unchanged
topological/cycle behavior unchanged
multi-parent aggregate behavior unchanged
transition evidence/authority checks unchanged
```

### R1C optional SAFETY_GATES

```text
registry/entry model unchanged
entry field order unchanged
required/unknown field checks unchanged
state/evidence/authority checks unchanged
```

## 6. Contract corpus

```text
1. exact runtime consumer set
2. exact structural import set per consumer
3. exact semantic utility import set per consumer
4. graph/inheritance shared helper boundary
5. R1C optional embedded parser boundary
6. CompatibilityView migration channels exist
7. no direct kdsl_parser_adapter import
8. runner/wrapper modules are not misclassified
```

## 7. Migration order

```text
6D-8A: consumer contract/inventory
6D-8B: safety semantics structural migration
6D-8C: inheritance and graph structural migration
6D-8D: R1C optional SAFETY_GATES structural migration
6D-8E: semantic utility location/retention decision
```

Each migration requires its own corpus and full unified validation.

## 8. Safety and authority boundary

```text
Safety Gate contract pass != semantic equivalence
Safety Gate contract pass != complete safety proof
Safety Gate contract pass != U approval
Safety Gate contract pass != RT:v
Safety Gate contract pass != execution authority
Safety Gate contract pass != adapter-file retirement proof
CI pass != release readiness
```

```text
hold/blocked gate deletion prohibited
state:satisfied requires evidence and authority basis
inheritance/graph semantics unchanged
build/diff/lint/test/CI pass != RT:v
NEXT proposal != execution permission
COMMIT recommendation != automatic commit permission
```

## 9. Stop conditions

Stop before migration when:

```text
consumer set differs from the frozen inventory
unknown structural helper use appears
entry order/value contract is unclear
inheritance/graph exit behavior would change
R1C optional field-order behavior would change
Safety/Authority/RT boundaries would weaken
```

## 10. Non-goals

```text
kdsl_parser_adapter.py deletion
legacy parity helper removal
Safety Gate semantic utility relocation
canonical specification change
stable/public-ready/tag/release/Release Assets operations
complete semantic equivalence or safety proof
```
