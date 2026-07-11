# KDSL R1C Validator First-Slice Review

status: implementation-review / merge-pending
review_date: 2026-07-11
branch: agent/kdsl-r1c-validator
target: main
pull_request: 7

## Goal

Implement a non-authoritative heuristic validator for the integrated R1C design candidate without promoting R1C to canonical/stable status.

## Implemented scope

```text
script: tools/validator/kdsl_r1c.py
wrapper target: r1c
all target integration: yes
schema: kdsl-r1c@0.1-draft
required field presence/order
short alias rejection
JSON-compatible structured fields
VERIFY class separation
RT state/basis heuristic
NEXT proposal_only
COMMIT actual/proposed/permission_basis
Full R1 fallback/out-of-scope
```

## Sample expansion

```text
previous total: 34
new total: 49
```

Coverage:

```text
3 repository R1C examples
unknown schema
missing field
short alias
invalid JSON
invalid RT:v basis
invalid NEXT authority
invalid COMMIT authority
VERIFY contradiction
field order mismatch
Full R1 fallback
wrapper valid/invalid
```

## Initial CI

```text
workflow: Validator CI
source_head: 5a48aa3a81789a4406c75820f9389be50b291118
workflow_run_id: 29144103000
run_number: 44
status: completed
conclusion: success
expected summary: total 49 / failed 0
```

Final immutable head/run evidence is recorded in PR #7 after documentation commits.

## Accepted design choices

### R1C detection

```text
KDSL_RESULT + exact SCHEMA marker→R1C
KDSL_RESULT without SCHEMA→Full R1 fallback/out-of-scope
unknown SCHEMA→fail
```

### No short aliases

```text
ST/PH/F/W/C/V/RK/NX/CM→未定義
```

### Structured values

```text
one-line JSON-compatible arrays/objects
commands/paths preserved as quoted strings
```

### Authority separation

```text
NEXT.authority:=proposal_only
COMMIT.proposed != commit authority
automatic commit authority→fail
```

## Known limitations

```text
line-based parser
first KDSL_RESULT block only
multi-line JSON未対応
full JSON/YAML/KDSL parserなし
semantic equivalence proofなし
runtime evidence authenticity判断なし
execution evidence authenticity判断なし
optional EVIDENCE/AUTHORITY deep lint限定
```

## Status split

```text
R1C design candidate: main integrated
R1C validator candidate: this PR
R1C canonical adoption: no
manifest/Bridge/glossary promotion: pending
```

Reason:

```text
validator実装 != canonical promotion
CI pass != specification approval
正本参照変更は独立approval/review対象
```

## Safety boundaries

```text
validator pass != semantic equivalence
validator pass != safety proof
validator pass != RT:v
validator pass != U承認
validator pass != execution authority
validator pass != release readiness
validator pass != R1C canonical/stable promotion
validator pass != Packet readiness
KDSL-Packet:=draft-non-executable
PKT:v1使用禁止
```

## Merge gate

```text
final Validator CI success
PR ready for review
squash merge
post-merge project-status/README/CHANGELOG synchronization
```

## Non-actions

```text
canonical R1変更なし
manifest/Bridge/glossary R1C adoptionなし
R1C stable/canonical化なし
Packet executable化なし
tag/release/Release Assets操作なし
branch deletionなし
```
