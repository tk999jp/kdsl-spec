# Phase 7C — P1L/P1 Validator First Slice

status: integrated
review_date: 2026-07-17
repository: tk999jp/kdsl-spec
tracking_issue: 118
implementation_pull_request: 123
implementation_source_head: 497bdd45942caa687c74890cdb2f94ecf36bb8a7
implementation_squash_commit: b808325c957c9f403fed461dfdbb9e3ce5d547b1
workflow_run_id: 29583167723
workflow_run_number: 427
workflow_conclusion: success

## 1. Goal

Add a bounded structural parser/validator/round-trip first slice for adopted canonical P1L/P1 schemas without adding runtime binding or execution authority.

## 2. Implemented

```text
P1L AST v2 raw-envelope parsing under checker-local marker registration
P1 ordered compact JSON segment parsing
P1 canonical rendering
P1L/P1 shared model validation
P1L→P1→P1L structural comparison
CLI targets: p1l / p1 / p1-contract
unified sample runner integration
```

## 3. Verified properties

```text
required top-level/nested order
source/profile evidence shape
profile completion vs inference
context classification separation
Runtime pre-execution values only
all Authority rails explicit
Normalization/Binding non-executable state
pipe inside JSON string handling
Windows path exact preservation
legacy colon P1 rejection
mixed source rejection
```

```text
P1 corpus: 14 / failed 0
Packet Semantic Property: success
existing unified suite: success
```

## 4. Corrective history

```text
run #426: failed in new P1 corpus
cause: legacy colon P1 was rejected generically before the corpus-specific classification marker
correction: bounded bootstrap classifies legacy colon P1 before canonical parser dispatch
run #427: success
```

The corrective did not modify Packet, Normalization, Safety Gate, R1/R1C, shared AST v2 parser core, or canonical schema semantics.

## 5. Boundary

```text
validator pass != executable
validator pass != semantic equivalence
validator pass != complete safety proof
validator pass != runtime binding
validator pass != execution authority
validator pass != U approval
validator pass != RT:v
```

The result surfaces retain:

```text
EXECUTABLE:no
SEMANTIC_EQUIVALENCE:not_proven
EXECUTION_AUTHORITY:none
```

## 6. Parser ownership decision

Shared `kdsl_parser_v2.py` was not changed. P1L marker registration is checker-local in `kdsl_p1_bootstrap.py`.

Reason:

```text
Phase 7C first slice has no existing shared-parser consumer dependency
bounded registration reduces unrelated parser regression risk
shared first-class adoption requires separate compatibility/consumer review
```

This is not evidence that checker-local registration should remain permanent.

## 7. Not implemented

```text
shared AST v2 first-class P1L envelope registration
arbitrary external Profile content verification
P1L/P1 semantic equivalence proof
complete protected-wording proof
K1/PF1 canonical parser/validator
runtime binding
executable transformer
Packet→P1L/P1 mapping/property integration
```

## 8. Next phase boundary

Phase 7D may resolve Packet normalization targets only through non-executable previews:

```text
P1L_PREVIEW != P1L:
P1_PREVIEW != P1|
TARGET.executable:false
AUTHORITY.execution_authority:none
semantic_equivalence:not_proven
```

Schema/validator pass alone must not make Packet normalized or executable.

## 9. Release boundary

No stable/public-ready/tag/release/Release Assets operation was performed.
