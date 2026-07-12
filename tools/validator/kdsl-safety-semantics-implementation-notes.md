# Safety Semantics / Multi-Generation Inheritance First Slice

status: implementation-candidate
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
