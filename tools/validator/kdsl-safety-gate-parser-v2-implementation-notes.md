# Safety Gate Parser v2 Compatibility Notes

status: phase6c-compatibility-view-integrated / checker-migrated-under-parity-guard
compatibility_view: tools/validator/kdsl_parser_v2_safety_gate_compat.py
parity_checker: tools/validator/kdsl_parser_v2_safety_gate_parity.py
parity_runner: tools/validator/run_parser_v2_safety_gate_parity_samples.py
active_checker: tools/validator/kdsl_safety_gate.py
migration_runner: tools/validator/run_safety_gate_migration_samples.py
compatibility_pull_request: 67
compatibility_squash_commit: 604e4e1f8f8c601f7054b15b38e3c5db40d88056
migration_pull_request: 69
migration_squash_commit: bfc034c44473232cee5107c53483a0b080e25a46
latest_workflow: 29231502084 / 305 / success
tracking_issue: 55
validator_authority: non-authoritative

## Purpose

Provide a source-spanned Safety Gate structural view and use it in the active checker without changing canonical Safety Gate semantics.

```text
parser parity != Safety Gate semantic equivalence
parser parity != safety proof
parser parity != authority
parser parity != RT:v
```

## Active checker path

```text
input
→ SafetyGateCompatibilityView
→ compare_safety_gate_legacy_v2
→ mismatch: fail before semantic validation
→ match: existing registry/state/composition/protected-wording checks
```

The active checker no longer installs the Phase 1 namespace adapter.

```text
install_safety_gate(globals()): removed from kdsl_safety_gate.py
```

## Compatibility view path

```text
first legacy-compatible SAFETY_GATES scope selection
→ exact original scope retained
→ view-local dedent
→ DocumentNodeV2 raw-envelope parse
→ registry and typed record extraction
→ Phase 1 output parity comparison
```

Compared contract:

```text
block presence
exact block text
registry
record order
record field order
record values
```

AST v2 data:

```text
DocumentNodeV2
EnvelopeNodeV2
FieldNodeV2
RecordSequenceNode
MappingNode
SourceSpanV2
SafetyGateEntryNodeV2
```

## Fenced example boundary

The repository example is inside a Markdown fence.

```text
AST v2 active-document: fenced example inactive
Phase 1 parser: first SAFETY_GATES marker selected
CompatibilityView: independently selects the same legacy-compatible scope
```

The selected copy is locally dedented and parsed as `raw-envelope`. General AST v2 fence and indentation behavior is unchanged.

## Checker-consumed values

```text
view.block_text
view.registry
view.entry_dicts
```

Legacy-v2 guard:

```text
compare_safety_gate_legacy_v2(text)
```

Output markers:

```text
Safety Gate parser parity guard: pass
Safety Gate structural extraction: AST v2 compatibility view
```

## Retained helper API

The following module-level helpers remain because inheritance, graph, R1C optional-block, and semantic modules import them:

```text
extract_gate_block
parse_registry
aggregate_state
authority_is_unverified
is_blank
```

Retention of these helpers does not restore namespace-adapter use in the active checker. Their separate migration is not claimed by Phase 6C-6.

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
```

## Fail-closed divergence case

A structure with records but no `entries:` field is accepted by loose Phase 1 line scanning but cannot be represented by the typed Safety Gate record field.

```text
legacy-v2 mismatch→parity guard failure
semantic validation→not entered
```

This is a structural stop condition, not schema inference or automatic correction.

## Verification

```text
Safety Gate parity: 8 / failed 0
Safety Gate checker migration: 4 / failed 0
unified runners: 14
unified expectations: 307 / failed 0
workflow run: 29231502084 / #305
KDSL Validation: success
Packet Semantic Property: success
```

## Exit codes

```text
0: pass
1: semantic warning
2: parser parity or semantic failure
```

## Current boundary

```text
CompatibilityView: integrated
active checker switch: integrated
legacy-v2 parity guard: active
Safety Gate semantic policy: unchanged
inheritance/graph helper migration: not claimed
remaining namespace-adapter consumers: Packet / Packet Normalization
legacy adapter removal: prohibited
```

## Next step

```text
Packet compatibility view/parity pilot
Packet executable:no保持
Packet state:not_normalized保持
checker switchはparity成立後
```
