# Phase 5 — Public README / R1 Quickstart / Public Examples

status: reviewed-integration-candidate
review_date: 2026-07-12
branch: agent/kdsl-phase5-public-readme-r1-quickstart
target: main
base: 49b6c865af046d44efc04a46d851aed55d222a61
pull_request: 51

## Scope

```text
root README public-facing simplification
docs/overview.md v2 public overview
docs/r1-quickstart.md creation
examples/public/README.md non-normative boundary hardening
public R1 examples current-contract alignment
KDSL-DP public example normalization-path correction
obsolete public-facing README draft retirement
docs/public-readiness.md candidate checklist update
```

## Public entry design

```text
README.md:=short public entry and navigation
docs/overview.md:=architecture and maturity explanation
docs/r1-quickstart.md:=R1 usage guide
examples/public/README.md:=non-normative example authority boundary
spec/manifest.md:=canonical responsibility map
docs/project-status.md:=operational status canonical
```

## R1 example corrections

Previous public R1 examples used ambiguous `RT: not_v` and listed validator commands as if they were executed evidence.

Corrected contract:

```text
documentation-only→RT:na
unexecuted command→CMD記載禁止 / CMD:[]
VERIFY:=illustrated executed review only
NEXT:=proposal_only
COMMIT.proposed != commit authority
AUTHORITY.commit:propose_only != commit permission
```

## KDSL-DP correction

Previous public example implied:

```text
KDSL-DP normalization→KDSL_PROMPT creation
```

This mixed separate layers. Corrected flow:

```text
KDSL-DP
→ canonical P1/P1L normalization
→ Runtime binding/control after validity and authority
→ execution within bound contract
→ R1/KDSL_RESULT
```

```text
KDSL_PROMPT != automatic KDSL-DP normalization output
KDSL-DP valid != executable
P1/P1L valid != executable
```

## Public example authority

```text
examples/public/* != Core specification
examples/public/* != execution contract
examples/public/* != approval
examples/public/* != RT:v evidence
examples/public/* != commit/push/release authority
```

## Manual review

```text
changed paths limited to public entry/guide/example/readiness/review files
README relative links resolved to existing repository paths
public examples contain no MidFD/private project dependency
public example listing clarified as representative, not exhaustive
obsolete public-facing README draft retained through Git history and replaced by superseded pointer
RT/NEXT/COMMIT/KDSL-DP/Packet boundaries retained
```

## Validation evidence

```text
workflow: KDSL Validation
candidate_pr: 51
run_number: 241
conclusion: success
jobs:
  KDSL Validation: success
  Packet Semantic Property: success
unified_expected_total: 257
```

Final-head rerun remains required after review-record updates.

## Validator/release boundaries

```text
validator pass != semantic equivalence
validator pass != complete safety proof
validator pass != U approval
validator pass != RT:v
validator pass != release readiness
stable/public-ready promotion:none
tag/release/Release Assets operation:none
Packet executable effect:none
required-check activation:none / issue #39 pending
```

## Non-actions

```text
main direct updateなし
existing tag movementなし
Release Assets操作なし
stable release creationなし
public-ready宣言なし
KDSL-Packet executable化なし
canonical P1/P1L schema推測なし
```

## Remaining Phase 5 work

```text
final-head CI
required KDSL Validation check activation / issue #39
final release-readiness review
operational status closeout
```
