# Phase 9D — Binding Evidence Schema Review

status: schema-adoption-candidate
review_date: 2026-07-18
repository: tk999jp/kdsl-spec
tracking_issue: 132
base_main: 8c0c8e7dc6bd93234971c2e4f6e720cbdf83bc05

## Goal

Adopt the external content-addressed evidence-record fields referenced by `P1L.BINDING.runtime_control`.

## Candidate

```text
schema: kdsl-binding-evidence@0.1-draft
canonicalization: kdsl-runtime-control-c14n@0.1-draft
P1L reference: compact JSON schema/id/revision/digest
```

## Decisions

```text
record identity independent from P1L identity
record digest precedes P1L reference creation
evaluation dimensions remain separate
all eight authority rails remain explicit
approval content validity != source trust
capability != authority
bound records exact attachment; executable:false remains fixed
aggregate pass/ready/authorized field absent
```

## Deferred

```text
binding evaluator and record generator
approval authentication
capability observation acquisition
route/tool integration
release-state changes
```

Repository validation and closeout alignment are required before adoption. Lint and CI success remain heuristic evidence only.
