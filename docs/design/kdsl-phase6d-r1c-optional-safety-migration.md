# Phase 6D-8D — R1C Optional Safety Gate Migration

status: implementation-plan / bounded migration
repository: tk999jp/kdsl-spec
tracking_issue: 55

## Goal

Move only embedded `SAFETY_GATES` structural parsing in `kdsl_r1c_optional.py` from `parse_registry` to `SafetyGateCompatibilityView`.

## Exact change

```text
safety_gate_standalone(value)
→ SafetyGateCompatibilityView.from_text(...)
→ view.registry / view.entry_dicts / view.entry_field_orders
```

## Preserved model

```text
registry
entries as ordered dictionaries
entry_field_order as ordered key lists
duplicate records retained for semantic rejection
```

## Preserved deep-lint contract

```text
known registry/ID/state checks
required fields
unknown field rejection
duplicate ID rejection
state:satisfied evidence requirement
state:satisfied authority requirement
state:blocked evidence warning
state:na reason requirement
EVIDENCE/AUTHORITY/ANNUNCIATOR behavior
R1C optional output and exit codes
SEMANTIC_EQUIVALENCE:not_proven
EXECUTION_AUTHORITY:none
```

## Retained semantic utilities/constants

```text
KNOWN_IDS
KNOWN_STATES
REGISTRY
REQUIRED_FIELDS
authority_is_unverified
is_blank
```

These remain temporarily in `kdsl_safety_gate`; they are not structural parser dependencies.

## Migration corpus

```text
CompatibilityView import boundary
model shape and field-order preservation
duplicate entry-order preservation
repository deep optional example pass
unknown state rejection
satisfied evidence/authority rejection
```

## Non-target

```text
R1C base parser
EVIDENCE/AUTHORITY/ANNUNCIATOR schemas
Safety Gate semantic utility location
parity-only helper strategy
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
