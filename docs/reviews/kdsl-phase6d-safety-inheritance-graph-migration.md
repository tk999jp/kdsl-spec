# Phase 6D-8C — Safety Gate Inheritance and Graph Migration

status: completed / integrated
review_date: 2026-07-17
repository: tk999jp/kdsl-spec
tracking_issue: 55
implementation_pull_request: 110
implementation_source_head: 01abc0d87ee26ca4b6dc53e57ad432a30a6f5098
implementation_squash_commit: 01d9de06f6af12ae7b06ba35a83405457a447817
workflow_run_id: 29543232320
workflow_run_number: 392
workflow_conclusion: success

## 1. Goal

Move only structural Safety Gate extraction in inheritance and graph consumers to `SafetyGateCompatibilityView`.

```text
extract_gate_block + parse_registry
=> SafetyGateCompatibilityView.from_text(...)
=> view.present / view.registry / view.entry_dicts
```

## 2. Integrated changes

Modified:

```text
tools/validator/kdsl_safety_gate_inheritance.py
tools/validator/kdsl_safety_gate_graph.py
tools/validator/run_safety_gate_consumer_contract_samples.py
tools/validator/run_all_samples.py
```

Added:

```text
docs/design/kdsl-phase6d-safety-inheritance-graph-migration.md
tools/validator/run_safety_inheritance_graph_migration_samples.py
```

Unchanged:

```text
tools/validator/kdsl_r1c_optional.py
tools/validator/kdsl_safety_gate.py
tools/validator/kdsl_parser_adapter.py
specification canonical files
```

## 3. Preserved inheritance contract

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

## 4. Preserved graph contract

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

## 5. Retained semantic utilities

The following imports remain temporarily from `kdsl_safety_gate`:

```text
REGISTRY
aggregate_state
authority_is_unverified
is_blank
```

They are semantic utilities/constants, not structural parser-adapter dependencies.

## 6. Corpus and corrective

Migration corpus:

```text
CompatibilityView import boundary
inheritance hold preserved
inheritance hold->satisfied missing evidence/authority rejected
repository multi-generation graph pass
graph cycle rejected
graph missing inherited hold gate rejected
```

Initial run:

```text
run #391: KDSL Validation failure
cause: fixture used evidence:none, which is intentionally nonblank
implementation semantics: unchanged
```

Corrective:

```text
fixture evidence:none => actual blank value
```

Final verification:

```text
workflow run: 29543232320 / #392
KDSL Validation: success
Packet Semantic Property: success
Safety Gate consumer contract: 8 / failed 0
Safety semantics migration: 4 / failed 0
inheritance/graph migration: 6 / failed 0
unified runners: 33
unified expectations: 429 / failed 0
```

## 7. Remaining structural consumer

```text
kdsl_r1c_optional.py:
  parse_registry structural dependency remains
  constants/authority_is_unverified/is_blank retained
```

After this phase, R1C optional is the only direct legacy Safety Gate structural-helper consumer.

## 8. Safety and authority boundary

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

## 9. Next safe step

Phase 6D-8D:

```text
freeze R1C optional embedded SAFETY_GATES contract
migrate parse_safety_gates_model() to SafetyGateCompatibilityView
retain constants and semantic utilities temporarily
preserve R1C optional output/exit/evidence/authority behavior
```

Then:

```text
semantic utility location/retention decision
→ parity-only helper strategy
→ kdsl_parser_adapter.py retirement or explicit retention decision last
```

## 10. Closeout decision

```text
Phase 6D-8C inheritance/graph structural migration: integrated
remaining Safety Gate structural consumers: 1
kdsl_parser_adapter.py: retained
adapter retirement: blocked
Issue #55: remain open
semantic equivalence: not_proven
complete safety proof: not_proven
RT:v: not granted
execution authority: none
public_ready: no
stable_release: none
Release Assets: none
```
