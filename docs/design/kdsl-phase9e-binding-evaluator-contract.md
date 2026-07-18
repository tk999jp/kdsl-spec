# Phase 9E Slice B — Binding Evaluator Contract

status: candidate
tracking: #144

## Inputs

```text
P1L/P1 contract
validated K1
validated PF1 or explicit not_applicable
supplied approval/capability/Stop/precondition records
evaluation time and repository/environment references
```

## Evaluation order

```text
identity→K1/PF1 compatibility→completion provenance→restrictions
→rail-level non-widening calculation→approval classification
→capability classification→Stop/preconditions→binding consistency
→canonical evidence record and compact reference
```

## Fixed output boundary

```text
kdsl-binding-evidence@0.1-draft candidate
BINDING.executable:false
semantic_equivalence:not_proven
execution_authority:none
```

No live evidence acquisition, credential use, route invocation, runtime binding, or operation execution is included.
