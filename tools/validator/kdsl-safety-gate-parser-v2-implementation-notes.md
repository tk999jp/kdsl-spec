# Safety Gate Parser v2 Compatibility Notes

status: phase6c-compatibility-view-integrated / checker-migration-pending
compatibility_view: tools/validator/kdsl_parser_v2_safety_gate_compat.py
parity_checker: tools/validator/kdsl_parser_v2_safety_gate_parity.py
parity_runner: tools/validator/run_parser_v2_safety_gate_parity_samples.py
implementation_pull_request: 67
implementation_squash_commit: 604e4e1f8f8c601f7054b15b38e3c5db40d88056
workflow: 29230830767 / 301 / success
validator_authority: non-authoritative

## Purpose

Provide a source-spanned Safety Gate structural view that matches the Phase 1 parser contract before the active checker is migrated.

```text
parser parity != Safety Gate semantic equivalence
parser parity != safety proof
parser parity != authority
```

## Current active checker path

```text
tools/validator/kdsl_safety_gate.py
→ tools/validator/kdsl_parser_adapter.py
→ extract_gate_block_legacy / parse_registry_legacy
→ existing semantic checks
```

The active checker has not switched to the v2 view.

## Compatibility view path

```text
input
→ independent legacy-compatible SAFETY_GATES scope selection
→ exact original scope retained
→ view-local dedent
→ DocumentNodeV2 raw-envelope parse
→ registry and typed record extraction
→ Phase 1 output parity comparison
```

## Compared structural contract

```text
block presence
exact block text
registry
record order
record field order
record values
```

The comparison uses Phase 1 functions directly:

```text
extract_gate_block_legacy
parse_registry_legacy
```

## AST v2 data used

```text
DocumentNodeV2
EnvelopeNodeV2
FieldNodeV2
RecordSequenceNode
MappingNode
SourceSpanV2
```

`SafetyGateEntryNodeV2` retains ordered key/value pairs, raw text, span and relative line.

## Fenced example boundary

The active repository example is inside a Markdown fence.

```text
AST v2 active-document: fenced example inactive
Phase 1 Safety Gate parser: first marker selected
CompatibilityView: independently selects that same first scope
```

The selected scope is parsed through `raw-envelope` only after a local dedent. General parser fence and indentation behavior is unchanged.

## Semantic checks intentionally excluded

```text
registry/ID/state validity
required field rules
state:satisfied evidence and authority basis
state:blocked warning
state:na reason
baseline gate composition
operation-triggered composition
protected wording
inheritance and graph rules
aggregate state meaning
```

## Verification

```text
Safety Gate parity: 8 / failed 0
unified runners: 13
unified expectations: 303 / failed 0
workflow run: 29230830767 / #301
KDSL Validation: success
Packet Semantic Property: success
```

## Exit codes

```text
0: structural parity pass
2: structural parity failure or usage failure
```

## Migration boundary

```text
CompatibilityView: integrated
parity corpus: integrated
checker switch: pending
Phase 1 adapter removal: prohibited
```

## Next step

```text
Safety Gate checker structural extraction→CompatibilityView
in-process legacy-v2 parity guard required
semantic/composition/protected-wording/inheritance policy unchanged
```
