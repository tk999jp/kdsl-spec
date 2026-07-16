# Safety Gate Parser v2 Compatibility Notes

status: active-checker-and-safety-semantics-consumer-migrated
compatibility_view: tools/validator/kdsl_parser_v2_safety_gate_compat.py
parity_checker: tools/validator/kdsl_parser_v2_safety_gate_parity.py
parity_runner: tools/validator/run_parser_v2_safety_gate_parity_samples.py
active_checker: tools/validator/kdsl_safety_gate.py
checker_migration_runner: tools/validator/run_safety_gate_migration_samples.py
consumer_contract_runner: tools/validator/run_safety_gate_consumer_contract_samples.py
safety_semantics_consumer: tools/validator/kdsl_safety_semantics.py
safety_semantics_migration_runner: tools/validator/run_safety_semantics_migration_samples.py
checker_migration_pull_request: 69
safety_semantics_migration_pull_request: 108
safety_semantics_migration_squash_commit: 36dcdbedb717772dda618972d7c4eca09b41aa07
required_check: KDSL Validation / Ruleset-enforced merge accepted
workflow_metadata: unavailable / repeated GitHub connector 502
tracking_issue: 55
validator_authority: non-authoritative

## Purpose

Provide a source-spanned Safety Gate structural view for the active checker and migrated consumers without changing canonical Safety Gate semantics, authority, or runtime evidence rules.

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

The active checker does not install the Phase 1 namespace adapter.

```text
install_safety_gate(globals()): removed
```

## Safety semantics consumer path

Phase 6D-8B moved only gate-ID extraction:

```text
input
→ SafetyGateCompatibilityView.from_text(text)
→ view.entry_dicts
→ ordered gate ID list
→ existing bounded semantic analysis
```

Removed from `kdsl_safety_semantics.py`:

```text
extract_gate_block
parse_registry
```

Retained unchanged:

```text
semantic requirement registry
semantic atom model
weakening detection
scope relation helpers
exit codes/output markers
FULL_SEMANTIC_EQUIVALENCE:not_proven
EXECUTION_AUTHORITY:none
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

Compared checker contract:

```text
block presence
exact block text
registry
record order
record field order
record values
```

## Fenced example boundary

```text
AST v2 active-document: fenced example inactive
Phase 1 parser: first SAFETY_GATES marker selected
CompatibilityView: independently selects the same legacy-compatible scope
```

The selected copy is locally dedented and parsed as `raw-envelope`. General AST v2 fence behavior is unchanged.

## Remaining helper consumers

### Inheritance

```text
file: tools/validator/kdsl_safety_gate_inheritance.py
structural pending:
  extract_gate_block
  parse_registry
semantic utilities retained temporarily:
  REGISTRY
  aggregate_state
  authority_is_unverified
  is_blank
```

### Graph

```text
file: tools/validator/kdsl_safety_gate_graph.py
structural pending:
  extract_gate_block
  parse_registry
semantic utilities retained temporarily:
  REGISTRY
  aggregate_state
  authority_is_unverified
  is_blank
```

### R1C optional

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

Retention of semantic utilities does not restore namespace-adapter use. There are no direct `kdsl_parser_adapter` imports.

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
aggregate state
inheritance transitions
graph semantics
R1C optional Safety Gate deep lint
```

## Migration corpus

```text
Safety Gate consumer contract: 8 cases
Safety semantics migration: 4 cases
```

Safety semantics cases:

```text
CompatibilityView import boundary
ID order and duplicate preservation
repository bounded-semantics pass
weakened evidence boundary fail
```

Expected unified state:

```text
unified runners: 32
unified expectations: 423 / failed 0
```

Evidence basis:

```text
PR #108 merged under active Ruleset
required status context: KDSL Validation
run_all_samples.py fails on missing summary/nonzero/failed case
```

Exact workflow run ID and individual job payload remain unconfirmed because the GitHub connector repeatedly returned HTTP 502. No run number is inferred or fabricated.

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
inheritance/graph structural migration: pending
R1C optional embedded SAFETY_GATES migration: pending
semantic utility location/retention decision: pending
parity-only helper strategy: pending
kdsl_parser_adapter.py retirement: blocked
```

## Next step

```text
Phase 6D-8C inheritance/graph contract and structural migration
→ Phase 6D-8D R1C optional embedded SAFETY_GATES migration
→ semantic utility retention/location decision
→ parity-only helper strategy
→ adapter file retirement or explicit retention last
```
