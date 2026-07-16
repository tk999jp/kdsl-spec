# Phase 6D-8C — Safety Gate Inheritance and Graph Migration

status: implementation-plan / bounded migration
repository: tk999jp/kdsl-spec
tracking_issue: 55

## Goal

Move only structural Safety Gate extraction in:

```text
tools/validator/kdsl_safety_gate_inheritance.py
tools/validator/kdsl_safety_gate_graph.py
```

from module-level legacy helpers to `SafetyGateCompatibilityView`.

## Exact change

```text
extract_gate_block + parse_registry
=> SafetyGateCompatibilityView.from_text(...)
=> view.present / view.registry / view.entry_dicts
```

## Retained semantic utilities

```text
REGISTRY
aggregate_state
authority_is_unverified
is_blank
```

These imports remain temporarily in `kdsl_safety_gate` and are not classified as structural adapter dependencies.

## Preserved inheritance contract

```text
hold/blocked gate propagation
blocked->na prohibition
hold->na prohibition
hold->satisfied evidence requirement
hold->satisfied authority requirement
resolution/satisfaction wording
scope relation re-evaluation
aggregate state reporting
exit codes
inheritance does not grant execution authority
```

## Preserved graph contract

```text
node/file validation
unknown edge rejection
duplicate edge warning
topological ordering
cycle rejection
duplicate gate ID rejection
inherited hold/blocked gate presence
multi-parent aggregate state
scope/evidence/authority transition checks
FULL_SAFETY_PROOF:not_proven
EXECUTION_AUTHORITY:none
```

## Migration corpus

```text
static CompatibilityView import boundary
inheritance hold preserved
inheritance hold->satisfied missing evidence/authority rejected
repository multi-generation graph pass
graph cycle rejected
graph missing inherited hold gate rejected
```

## Non-target

```text
kdsl_r1c_optional.py embedded SAFETY_GATES parser
kdsl_safety_gate.py semantic utility location
kdsl_parser_adapter.py
specification canonical files
stable/public-ready/tag/release/Release Assets
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
