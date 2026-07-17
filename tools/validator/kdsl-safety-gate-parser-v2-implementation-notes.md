# Safety Gate Parser v2 Compatibility Notes

status: active-checker-and-all-known-structural-consumers-migrated
compatibility_view: tools/validator/kdsl_parser_v2_safety_gate_compat.py
parity_checker: tools/validator/kdsl_parser_v2_safety_gate_parity.py
parity_runner: tools/validator/run_parser_v2_safety_gate_parity_samples.py
active_checker: tools/validator/kdsl_safety_gate.py
consumer_contract_runner: tools/validator/run_safety_gate_consumer_contract_samples.py
safety_semantics_migration_runner: tools/validator/run_safety_semantics_migration_samples.py
inheritance_graph_migration_runner: tools/validator/run_safety_inheritance_graph_migration_samples.py
r1c_optional_migration_runner: tools/validator/run_r1c_optional_safety_migration_samples.py
latest_implementation_pull_request: 112
latest_implementation_squash_commit: dfbaaa40580c43d563650acbf21b5ece75bc3fb7
latest_workflow: 29543907368 / 396 / success
tracking_issue: 55
validator_authority: non-authoritative

## Purpose

Provide a source-spanned Safety Gate structural view for the active checker and known runtime consumers without changing canonical Safety Gate semantics, authority, or runtime-evidence rules.

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

### R1C optional

```text
embedded SAFETY_GATES value
→ standalone SAFETY_GATES envelope
→ SafetyGateCompatibilityView.from_text(...)
→ view.registry / view.entry_dicts / view.entry_field_orders
→ existing optional deep-lint checks
```

Removed structural imports from known consumers:

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

## Retained semantic utilities and constants

Known consumers continue to import a bounded semantic API from `kdsl_safety_gate`:

```text
KNOWN_IDS
KNOWN_STATES
REGISTRY
REQUIRED_FIELDS
aggregate_state
authority_is_unverified
is_blank
```

These are semantic utilities/constants, not structural parser-adapter dependencies.

Current structural dependency result:

```text
direct kdsl_parser_adapter imports: none
legacy Safety Gate structural helper consumers: none
```

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
R1C optional EVIDENCE/AUTHORITY/ANNUNCIATOR/Safety Gate deep lint
```

## Migration corpus

```text
Safety Gate consumer contract: 8 cases
Safety semantics migration: 4 cases
inheritance/graph migration: 6 cases
R1C optional Safety Gate migration: 6 cases
```

R1C optional cases:

```text
CompatibilityView import boundary
model shape and field-order preservation
duplicate entry-order preservation
repository deep optional example pass
unknown state rejection
satisfied evidence/authority rejection
```

Verified state:

```text
workflow run: 29543907368 / #396
KDSL Validation: success
Packet Semantic Property: success
unified runners: 34
unified expectations: 435 / failed 0
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
R1C optional embedded SAFETY_GATES migration: integrated
legacy Safety Gate structural helper consumers: none
semantic utility location/retention decision: pending
parity-only helper strategy: pending
kdsl_parser_adapter.py retirement: blocked pending readiness proof
```

## Next step

```text
Phase 6D-9 adapter and parity readiness inventory
→ semantic utility retention/location decision
→ parity-only helper strategy
→ adapter file retirement or explicit retention last
```
