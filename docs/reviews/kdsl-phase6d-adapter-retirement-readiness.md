# Phase 6D-9A — Parser Adapter Retirement Readiness

status: completed / integrated
review_date: 2026-07-17
repository: tk999jp/kdsl-spec
tracking_issue: 55
implementation_pull_request: 114
implementation_source_head: f31ecb5d0626644a6b1867c5390ca246adf2b3bd
implementation_squash_commit: ed928bfddd7a412acd420ba1622addd788cd6f50
workflow_run_id: 29545316817
workflow_run_number: 406
workflow_conclusion: success

## 1. Goal

Prove that `tools/validator/kdsl_parser_adapter.py` has no runtime importer, installer consumer, structural-helper consumer, or parity dependency before a separate deletion trial.

## 2. Readiness corpus

```text
adapter file exposes only four known installer functions
no top-level validator module imports kdsl_parser_adapter
no installer function is loaded outside the adapter module
parity modules are adapter-independent
repository inventory has no direct or legacy structural consumers
consumer matrix has no blocking records and retains semantic APIs only
key runtime modules import while adapter imports are denied
```

## 3. Semantic utility decision

The following symbols remain in `kdsl_safety_gate.py` as a bounded internal semantic API:

```text
KNOWN_IDS
KNOWN_STATES
REGISTRY
REQUIRED_FIELDS
aggregate_state
authority_is_unverified
is_blank
```

They are not structural parser helpers and do not depend on `kdsl_parser_adapter.py`.

## 4. Parity strategy

```text
parity modules use direct legacy-parser or checker-local comparison paths
kdsl_parser_adapter.py is not parity evidence
local legacy helpers remain where required by parity guards
```

Adapter deletion must not remove or weaken those parity paths.

## 5. Corrective record

Initial failures:

```text
run #400:
  Safety Gate semantic utilities were still classified as structural helpers

run #401/#402/#403:
  readiness runner passed
  unified suite exposed stale repository matrix expectation
```

Corrections:

```text
Safety Gate structural set:=extract_gate_block/parse_registry only
semantic utilities/constants:=retain-semantic-api
repository matrix:
  migrate-or-replace:0
  retain-temporarily:0
  blocking_records:0
```

A temporary diagnostic artifact step was used to retrieve the complete readiness output and removed before final verification.

Final verification:

```text
workflow run: 29545316817 / #406
KDSL Validation: success
Packet Semantic Property: success
adapter retirement readiness: 7 / failed 0
unified runners: 35
unified expectations: 442 / failed 0
```

## 6. Current decision

```text
kdsl_parser_adapter.py: retained
readiness state: bounded-removal-trial-candidate
adapter deletion: not performed
post-deletion proof: absent
```

Readiness success authorizes only a bounded deletion trial in the next isolated phase.

## 7. Safety and authority boundary

```text
readiness pass != adapter deletion
readiness pass != post-deletion proof
readiness pass != semantic equivalence
readiness pass != complete safety proof
readiness pass != U approval
readiness pass != RT:v
readiness pass != execution authority
CI pass != release readiness
```

No stable/public-ready/tag/release/Release Assets operation was performed.

## 8. Next safe step

Phase 6D-9B:

```text
delete only tools/validator/kdsl_parser_adapter.py
replace readiness corpus with post-deletion corpus
retain inventory/matrix/semantic utilities/parity paths
run the complete unified suite
record exact deletion and CI evidence
```

## 9. Closeout decision

```text
Phase 6D-9A readiness: integrated
bounded deletion trial candidate: yes
adapter file removal: not performed
Issue #55: remain open
semantic equivalence: not_proven
complete safety proof: not_proven
RT:v: not granted
execution authority: none
public_ready: no
stable_release: none
Release Assets: none
```
