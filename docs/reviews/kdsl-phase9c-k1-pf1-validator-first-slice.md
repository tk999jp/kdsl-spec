# Phase 9C — K1 / PF1 Validator First-Slice Review

status: implementation-candidate
review_date: 2026-07-18
repository: tk999jp/kdsl-spec
tracking_issue: 132
pull_request: 137
base_main: 09c18c0b419f9f105dda3070bcd0ef771a35eeb3

## Goal

Implement a bounded, non-executable parser/validator and exact K1-reference compatibility check for the canonical Phase 9B K1/PF1 schemas.

## Implemented scope

```text
K1/PF1 first-class shared AST recognition
canonical field and nested-key ordering
required value/type and fixed safety-boundary checks
canonical JSON projection and digest recomputation
K1/PF1 identity validation
PF1 KERNEL_REF exact resolution
project scope and contract-schema compatibility
public validator targets
focused corpus and unified-runner integration
```

## Key files

```text
examples/runtime/k1-canonical.example.md
tools/validator/kdsl_runtime_control.py
tools/validator/kdsl_k1.py
tools/validator/kdsl_pf1.py
tools/validator/kdsl_runtime_control_compatibility.py
tools/validator/run_runtime_control_samples.py
tools/validator/kdsl_parser_v2.py
tools/validator/kdsl_validate.py
tools/validator/run_all_samples.py
tools/validator/kdsl-runtime-control-implementation-notes.md
```

## Result boundary

```text
K1/PF1 valid != executable|authority grant
compatibility valid != P1L binding
compatibility valid != authority sufficient
capability structure valid != capability observed
route structure valid != route invocation
EXECUTABLE:false
SEMANTIC_EQUIVALENCE:not_proven
EXECUTION_AUTHORITY:none
```

## Corpus expectations

The focused corpus contains 16 checks:

```text
canonical K1 parse
canonical generated PF1 parse
shared AST K1 recognition
shared AST PF1 recognition
exact K1/PF1 compatibility
K1 dedicated CLI
PF1 dedicated CLI
compatibility CLI
public k1 target
public pf1 target
public runtime-control target
digest mismatch rejection
KERNEL_REF mismatch rejection
unknown ceiling mode rejection
capability-is-permission rejection
duplicate K1 rejection
```

Focused and unified results must be recorded from the final PR head before merge. Validator pass is heuristic evidence and not a semantic-equivalence, safety, authority, runtime, or release proof.

## Deliberately deferred

```text
P1L request intersection
approval acceptance and issuer/source trust evaluation
capability observation evaluation
preset/alias semantic expansion
binding-evidence schema and generation
runtime binding
execution authorization
route/tool/command execution
Packet normalized-state promotion
stable/public-ready/tag/release/Release Assets operations
```

## Adoption judgment

Candidate is suitable for Phase 9C adoption only when the final PR head passes the focused runtime-control corpus, shared P1L compatibility corpus, unified validator suite, and all repository-required jobs without weakening existing boundaries.
