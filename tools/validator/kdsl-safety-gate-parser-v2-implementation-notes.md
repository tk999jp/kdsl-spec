# Safety Gate Parser v2 Compatibility Notes

status: active-checker-and-three-runtime-consumers-migrated
compatibility_view: tools/validator/kdsl_parser_v2_safety_gate_compat.py
parity_checker: tools/validator/kdsl_parser_v2_safety_gate_parity.py
parity_runner: tools/validator/run_parser_v2_safety_gate_parity_samples.py
active_checker: tools/validator/kdsl_safety_gate.py
consumer_contract_runner: tools/validator/run_safety_gate_consumer_contract_samples.py
safety_semantics_migration_runner: tools/validator/run_safety_semantics_migration_samples.py
inheritance_graph_migration_runner: tools/validator/run_safety_inheritance_graph_migration_samples.py
latest_implementation_pull_request: 110
latest_implementation_squash_commit: 01d9de06f6af12ae7b06ba35a83405457a447817
latest_workflow: 29543232320 / 392 / success
tracking_issue: 55
validator_authority: non-authoritative

## Purpose

Provide a source-spanned Safety Gate structural view for the active checker and migrated runtime consumers without changing canonical Safety Gate semantics, authority, or runtime-evidence rules.

```text
parser/consumer migration != Safety Gate semantic equivalence
parser/consumer migration != complete safety proof
parser/consumer migration != authority
parser/consumer migration != RT:v
```

## Active checker path

```text
input
→ SafetyGateCompatibilityView
→ compare_safety_gate_legacy_v2
→ mismatch: fail before semantic validation
→ match: existing registry/state/composition/protected-wording checks
```

```text
install_safety_gate(globals()): removed
```

## Migrated consumer paths

### Safety semantics

```text
input
→ SafetyGateCompatibilityView.from_text(text)
→ view.entry_dicts
→ ordered gate ID list
→ existing bounded semantic analysis
```

### Inheritance

```text
parent/child text
→ SafetyGateCompatibilityView.from_text(text)
→ view.present / view.registry / view.entry_dicts
→ existing transition/scope/evidence/authority checks
```

### Graph

```text
node text
→ SafetyGateCompatibilityView.from_text(text)
→ view.present / view.registry / view.entry_dicts
→ existing graph-order/transition/scope/evidence/authority checks
```

Removed structural imports from these consumers:

```text
extract_gate_block
parse_registry
```

## Compatibility view contract

```text
first legacy-compatible SAFETY_GATES scope selection
exact original scope retained
view-local dedent
DocumentNodeV2 raw-envelope parse
registry and typed record extraction
```

Consumed channels:

```text
view.present
view.block_text
view.registry
view.entry_dicts
view.entry_field_orders
```

Compared active-checker contract:

```text
block presence
exact block text
registry
record order
record field order
record values
```

## Retained semantic utilities

Inheritance and graph continue to import:

```text
REGISTRY
aggregate_state
authority_is_unverified
is_blank
```

These are semantic utilities/constants, not structural parser-adapter dependencies.

## Remaining structural helper consumer

```text
file: tools/validator/kdsl_r1c_optional.py
structural pending:
  parse_registry
semantic/constants retained temporarily:
  KNOWN_IDS
  KNOWN_STATES
  REGISTRY
  REQUIRED_FIELDS
  authority_is_unverified
  is_blank
```

R1C optional is now the only direct legacy Safety Gate structural-helper consumer.

## Semantic checks retained

```text
registry/ID/state validity
required field rules
state:satisfied evidence and authority basis
state:blocked warning
state:na reason
dev-prompt baseline gate composition
operation-triggered composition
protected wording
bounded semantic atoms/weakening detection
aggregate state
inheritance transitions
graph semantics and topological ordering
R1C optional Safety Gate deep lint
```

## Migration corpus

```text
Safety Gate consumer contract: 8 cases
Safety semantics migration: 4 cases
inheritance/graph migration: 6 cases
```

Inheritance/graph cases:

```text
CompatibilityView import boundary
inheritance hold preserved
hold->satisfied missing evidence/authority rejected
repository multi-generation graph pass
graph cycle rejected
graph missing inherited hold gate rejected
```

Corrective evidence:

```text
run #391: fixture failure because evidence:none is nonblank by contract
fixture corrected to actual empty value
implementation semantics unchanged
run #392: success
```

Verified state:

```text
workflow run: 29543232320 / #392
KDSL Validation: success
Packet Semantic Property: success
unified runners: 33
unified expectations: 429 / failed 0
```

## Exit codes

```text
0: pass
1: semantic warning
2: structural or semantic failure
```

## Current boundary

```text
CompatibilityView: integrated
active checker migration: integrated
Safety semantics structural migration: integrated
inheritance/graph structural migration: integrated
R1C optional embedded SAFETY_GATES migration: pending
semantic utility location/retention decision: pending
parity-only helper strategy: pending
kdsl_parser_adapter.py retirement: blocked
```

## Next step

```text
Phase 6D-8D R1C optional embedded SAFETY_GATES migration
→ semantic utility retention/location decision
→ parity-only helper strategy
→ adapter file retirement or explicit retention last
```
