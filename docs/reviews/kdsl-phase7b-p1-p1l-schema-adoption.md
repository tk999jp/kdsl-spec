# Phase 7B — P1L/P1 Canonical Schema Adoption

status: integrated core schema slice
review_date: 2026-07-17
repository: tk999jp/kdsl-spec
tracking_issue: 118
implementation_pull_request: 121
implementation_source_head: 84e15427fe7aa7fc8e0bae554c4b40becf7a9cb0
implementation_squash_commit: 80edbce75ad4eb42b8aeeb9c268d47b0523d9311
workflow_run_id: 29581426216
workflow_run_number: 418
workflow_conclusion: success

## 1. Adopted ownership

```text
P1L:=lossless structured normalized contract schema
P1:=compact serialization profile subordinate to P1L
```

```text
Core/Profile/R1/Bridge canonical meaning
> P1L canonical v2-draft contract schema
> P1 compact serialization profile
> P1/P1L lint
> validator/example/tool
```

## 2. Adopted files

```text
spec/adps/kdsl-p1l-contract-schema.md
spec/adps/kdsl-p1-compact-contract-schema.md
spec/lint/kdsl-p1-p1l-lint.md
spec/bridge/kdsl-adps-bridge.md
examples/adps/p1l-investigate.example.md
examples/adps/p1-profile-completed.example.md
examples/adps/p1-unknown-profile-blocked.example.md
examples/adps/p1-authority-missing-blocked.example.md
```

Schema IDs:

```text
kdsl-p1l@0.1-draft
kdsl-p1@0.1-draft
```

## 3. Contract state

```text
STATUS: contract-candidate
P1L/P1 executable: no
BINDING.state default: unbound
BINDING.executable: false
runtime binding specification: absent
```

All eight authority rails are required:

```text
read/edit/stage/commit/push/release/public_repo/destructive_ops
```

## 4. P1 compact decision

Canonical P1 uses ordered JSON segments:

```text
P1|SCHEMA=kdsl-p1@0.1-draft|STATUS=contract-candidate|M=...|SRC=...|PF=...|T=...|S=...|C=...|G=...|P=...|GD=...|X=...|V=...|RT=...|O=...|A=...|N=...|BD=...
```

Reason:

```text
full P1L projection remains reconstructable
exact Unicode/path/command/API strings can be preserved
unknown/repeated/out-of-order fields can be blocked
hidden defaults are not required
```

## 5. Legacy compatibility

Project-local colon syntax remains legacy operational evidence.

```text
loss=P→profile_completed only with exact compatibility evidence
loss=L meaning unresolved→blocked
AP/H meanings unresolved→blocked
Authority rails absent→canonical promotion blocked without exact permission contract
```

No legacy alias was inferred or silently standardized.

## 6. Verification

```text
PR: 121
source head: 84e15427fe7aa7fc8e0bae554c4b40becf7a9cb0
squash commit: 80edbce75ad4eb42b8aeeb9c268d47b0523d9311
workflow: 29581426216 / #418
KDSL Validation: success
Packet Semantic Property: success
```

```text
workflow/validator pass != semantic equivalence
workflow/validator pass != complete safety proof
workflow/validator pass != runtime binding
workflow/validator pass != authority
workflow/validator pass != RT:v
```

## 7. Preserved boundaries

```text
KDSL-DP direct execution prohibited
P1L/P1 valid != executable
P1L/P1 lint/round-trip pass != authority
profile completion != inference
build/diff/lint/test/CI pass != RT:v
NEXT remains proposal only
COMMIT remains non-authoritative unless executed
Packet normalization remains non-executable
stable/public-ready/tag/release/Release Assets:none
```

## 8. Not implemented

```text
P1L/P1 parser/validator
runtime binding
K1/PF1 canonical schema
Packet→P1L/P1 mapping
P1L_PREVIEW/P1_PREVIEW integration
complete semantic equivalence proof
complete safety proof
```

## 9. Closeout boundary

The core schema slice is integrated. Repository index/status/glossary alignment is a documentation closeout responsibility and must not be confused with parser or runtime implementation.
