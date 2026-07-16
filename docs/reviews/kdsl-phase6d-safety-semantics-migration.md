# Phase 6D-8B — Safety Semantics Consumer Migration

status: completed / integrated
review_date: 2026-07-17
repository: tk999jp/kdsl-spec
tracking_issue: 55
implementation_pull_request: 108
implementation_source_head: 5f429dc94078cb7af51da0162fb1a57bc76e1516
implementation_squash_commit: 36dcdbedb717772dda618972d7c4eca09b41aa07
required_check: KDSL Validation
required_check_enforcement: Ruleset merge accepted
workflow_metadata: unavailable / GitHub connector returned repeated 502
validator_authority: non-authoritative

## 1. Goal

Move only the structural input of `kdsl_safety_semantics.gate_ids_from_text()` to `SafetyGateCompatibilityView`.

```text
extract_gate_block + parse_registry
=> SafetyGateCompatibilityView.from_text(...).entry_dicts
```

## 2. Integrated changes

Modified:

```text
tools/validator/kdsl_safety_semantics.py
tools/validator/run_safety_gate_consumer_contract_samples.py
tools/validator/run_all_samples.py
```

Added:

```text
docs/design/kdsl-phase6d-safety-semantics-migration.md
tools/validator/run_safety_semantics_migration_samples.py
```

Unchanged:

```text
tools/validator/kdsl_safety_gate.py
tools/validator/kdsl_safety_gate_inheritance.py
tools/validator/kdsl_safety_gate_graph.py
tools/validator/kdsl_r1c_optional.py
tools/validator/kdsl_parser_adapter.py
specification canonical files
```

## 3. Preserved contract

```text
Safety Gate ID order retained
duplicate IDs retained
absent Safety Gate entries remain out of scope
semantic requirement registry unchanged
semantic atom analysis unchanged
weakening detection unchanged
scope relation helpers unchanged
exit codes unchanged
FULL_SEMANTIC_EQUIVALENCE:not_proven
EXECUTION_AUTHORITY:none
```

## 4. Migration corpus

```text
compatibility-view import boundary
Safety Gate ID order and duplicate preservation
repository bounded-semantics example remains pass
weakened evidence boundary remains fail
```

Expected integrated unified state:

```text
Safety Gate consumer contract: 8 / failed 0
Safety semantics migration: 4 / failed 0
unified runners: 32
unified expectations: 423 / failed 0
```

Evidence basis:

```text
PR #108 merged under active Ruleset
required check context: KDSL Validation
run_all_samples.py includes all 32 runners and fails on missing summary/nonzero/failed case
```

Exact workflow run ID and individual job payload were not retrieved because the GitHub connector repeatedly returned HTTP 502. They are not fabricated or treated as independently confirmed.

## 5. Remaining Safety Gate consumers

```text
kdsl_safety_gate_inheritance.py:
  structural helpers pending migration
  semantic utilities retained temporarily

kdsl_safety_gate_graph.py:
  structural helpers pending migration
  semantic utilities retained temporarily

kdsl_r1c_optional.py:
  embedded SAFETY_GATES parser pending migration
  constants/semantic utilities retained temporarily
```

## 6. Safety and authority boundary

```text
hold/blocked gate deletion prohibited
state:satisfied requires evidence and authority basis
inheritance/graph semantics unchanged
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

## 7. Next safe step

Phase 6D-8C:

```text
add inheritance/graph consumer-specific contract evidence
migrate only structural extraction to SafetyGateCompatibilityView
retain aggregate_state/authority_is_unverified/is_blank/REGISTRY temporarily
preserve transition, scope, evidence, authority, graph-order, and exit behavior
```

Then:

```text
Phase 6D-8D R1C optional embedded SAFETY_GATES migration
→ semantic utility location/retention decision
→ parity-only helper strategy
→ adapter-file retirement or explicit retention decision last
```

## 8. Closeout decision

```text
Phase 6D-8B Safety semantics structural migration: integrated
Safety semantics direct kdsl_safety_gate import: removed
remaining Safety Gate structural consumers: 3
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
