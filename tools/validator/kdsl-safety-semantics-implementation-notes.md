# Safety Semantics / Multi-Generation Inheritance First Slice

status: first-slice integrated
model: kdsl-safety-language@0.1-draft
validator_authority: non-authoritative

## Implemented tools

```text
tools/validator/kdsl_safety_semantics.py
tools/validator/kdsl_safety_gate_graph.py
tools/validator/run_safety_semantics_samples.py
tools/validator/run_safety_semantics_examples.py
```

## Bounded semantic checks

```text
protected concepts by Safety Gate ID
strong wording alternatives
weakening/negation patterns
condition/exception atom capture
FULL_SEMANTIC_EQUIVALENCE:not_proven
EXECUTION_AUTHORITY:none
```

## Graph checks

```text
JSON node/edge manifest
cycle detection
unknown/duplicate node detection
multi-generation hold/blocked preservation
multi-parent aggregate conflict
unsafe state transition rejection
deep scope equal/narrowed/widened/overlap/disjoint/unknown
independent na re-evaluation
```

## Property suite

```text
semantic cases: 16
graph cases: 16
Phase 2 property total: 32
repository examples: 2
existing Phase 1 unified total: 147
expected unified total: 181
```

## Integration evidence

```text
pull_request: 42
source_head: f11fe00da04f25ae5fe7855535b9634e645a901e
squash_commit: 66191b6b97bab720ffd14d5732aa6f5bc0d92a44
workflow_run_id: 29180355132
run_number: 200
unified_total: 181
failed: 0
```

## Boundaries

```text
bounded patterns only
full natural-language parserなし
full negation/exception reasoningなし
scope relation uses normalized exact-item heuristic
semantic lint pass != semantic equivalence
inheritance graph pass != complete safety proof
validator pass != U承認/RT:v/authority/release readiness
```
