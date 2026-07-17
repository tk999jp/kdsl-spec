# Phase 6D-8D — R1C Optional Safety Gate Migration

status: completed / integrated
review_date: 2026-07-17
repository: tk999jp/kdsl-spec
tracking_issue: 55
implementation_pull_request: 112
implementation_source_head: f675f2bd6187a1717175110d8a4d6cd3d8a01a4d
implementation_squash_commit: dfbaaa40580c43d563650acbf21b5ece75bc3fb7
workflow_run_id: 29543907368
workflow_run_number: 396
workflow_conclusion: success

## 1. Goal

Move embedded `SAFETY_GATES` structural parsing in `kdsl_r1c_optional.py` to `SafetyGateCompatibilityView`.

```text
safety_gate_standalone(value)
→ SafetyGateCompatibilityView.from_text(...)
→ view.registry / view.entry_dicts / view.entry_field_orders
```

## 2. Integrated changes

Modified:

```text
tools/validator/kdsl_r1c_optional.py
tools/validator/run_safety_gate_consumer_contract_samples.py
tools/validator/run_all_samples.py
```

Added:

```text
docs/design/kdsl-phase6d-r1c-optional-safety-migration.md
tools/validator/run_r1c_optional_safety_migration_samples.py
```

Unchanged:

```text
R1C base parser
EVIDENCE/AUTHORITY/ANNUNCIATOR schemas
Safety Gate semantic utility definitions
kdsl_parser_adapter.py
specification canonical files
```

## 3. Preserved model

```text
registry
entries as ordered dictionaries
entry_field_order as ordered key lists
duplicate records retained for semantic rejection
```

## 4. Preserved deep-lint contract

```text
known registry/ID/state checks
required field checks
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

## 5. Corpus

```text
CompatibilityView import boundary
model shape and field-order preservation
duplicate entry-order preservation
repository deep optional example pass
unknown state rejection
satisfied evidence/authority rejection
```

Verification:

```text
workflow run: 29543907368 / #396
KDSL Validation: success
Packet Semantic Property: success
Safety Gate consumer contract: 8 / failed 0
Safety semantics migration: 4 / failed 0
inheritance/graph migration: 6 / failed 0
R1C optional Safety Gate migration: 6 / failed 0
unified runners: 34
unified expectations: 435 / failed 0
```

## 6. Structural dependency result

After this phase:

```text
direct kdsl_parser_adapter imports: none
legacy Safety Gate structural helper consumers: none
active checkers and migrated runtime consumers: CompatibilityViews
```

Remaining imports from `kdsl_safety_gate` are semantic utilities/constants:

```text
KNOWN_IDS
KNOWN_STATES
REGISTRY
REQUIRED_FIELDS
aggregate_state
authority_is_unverified
is_blank
```

## 7. Safety and authority boundary

```text
hold/blocked gate deletion prohibited
state:satisfied requires evidence and authority basis
build/diff/lint/test/CI pass != RT:v
NEXT:=proposal, not execution authority
COMMIT:=actual/proposed record, not auto-commit authority
```

```text
migration pass != semantic equivalence
migration pass != complete safety proof
migration pass != U approval
migration pass != RT:v
migration pass != execution authority
migration pass != adapter retirement proof
CI pass != release readiness
```

## 8. Remaining Phase 6D decisions

```text
semantic utility location/retention decision
parity-only legacy helper strategy
kdsl_parser_adapter.py retirement or explicit retention decision
post-decision full repository proof
```

The absence of structural consumers does not by itself authorize adapter-file deletion.

## 9. Next safe step

Phase 6D-9:

```text
inventory actual imports/references to kdsl_parser_adapter.py
inventory parity-only helper requirements
classify semantic utilities as stable internal API or dedicated module candidates
add adapter-retirement readiness corpus
remove adapter file only after zero-reference proof and full CI
```

## 10. Closeout decision

```text
Phase 6D-8D R1C optional Safety Gate migration: integrated
legacy Safety Gate structural consumers: none
kdsl_parser_adapter.py: retained
adapter retirement: blocked pending readiness proof
Issue #55: remain open
semantic equivalence: not_proven
complete safety proof: not_proven
RT:v: not granted
execution authority: none
public_ready: no
stable_release: none
Release Assets: none
```
