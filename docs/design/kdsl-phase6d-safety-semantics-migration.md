# Phase 6D-8B — Safety Semantics Consumer Migration

status: implementation-plan / bounded migration
repository: tk999jp/kdsl-spec
tracking_issue: 55

## Goal

Move only `kdsl_safety_semantics.gate_ids_from_text()` from `kdsl_safety_gate` structural helpers to `SafetyGateCompatibilityView`.

## Exact change

```text
extract_gate_block + parse_registry
=> SafetyGateCompatibilityView.from_text(...).entry_dicts
```

## Preserved

```text
semantic requirement registry
semantic atom analysis
weakening detection
scope relation helpers
exit codes and output markers
FULL_SEMANTIC_EQUIVALENCE:not_proven
EXECUTION_AUTHORITY:none
```

## Contract

```text
Safety Gate ID order retained
duplicate IDs retained for downstream set normalization
absent entries remain out of scope
valid bounded-semantics example remains pass
weakened protected concept remains fail
```

## Non-target

```text
kdsl_safety_gate_inheritance.py
kdsl_safety_gate_graph.py
kdsl_r1c_optional.py
kdsl_safety_gate.py
kdsl_parser_adapter.py
specification canonical files
```

## Boundary

```text
migration pass != semantic equivalence
migration pass != complete safety proof
migration pass != RT:v
migration pass != execution authority
migration pass != adapter retirement proof
CI pass != release readiness
```
