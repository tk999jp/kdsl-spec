# Phase 6D-9A — Parser Adapter Retirement Readiness

status: implementation-plan / removal-not-performed
repository: tk999jp/kdsl-spec
tracking_issue: 55

## 1. Goal

Prove that `tools/validator/kdsl_parser_adapter.py` has no runtime importer or parity dependency before a separate deletion trial.

```text
zero direct imports
+ zero installer-symbol consumers
+ zero legacy structural helper consumers
+ parity evidence independent of adapter
+ key runtime modules import under adapter-deny guard
=> bounded removal trial candidate
```

This phase does not delete the adapter file.

## 2. Adapter surface

The retained file exports:

```text
install_r1c
install_packet
install_normalization
install_safety_gate
```

All direct installers were removed from active checker modules in earlier Phase 6D slices.

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

Decision:

```text
retain in kdsl_safety_gate.py for Phase 6D closeout
```

Reason:

```text
shared semantic contract remains stable
moving symbols provides no parser-adapter retirement benefit
relocation would enlarge change scope and require separate API migration evidence
```

This retention does not restore or depend on `kdsl_parser_adapter.py`.

## 4. Parity-only helper strategy

```text
Compatibility/parity modules retain their direct legacy-parser or checker-local comparison paths.
kdsl_parser_adapter.py is not parity evidence.
Local legacy helpers may remain where a parity guard compares the former contract.
```

Adapter-file deletion must not delete or weaken parity comparisons.

## 5. Readiness corpus

```text
1. adapter file exposes only the four known installer functions
2. no top-level validator module imports kdsl_parser_adapter
3. no installer function is loaded/called outside the adapter module
4. parity modules do not import kdsl_parser_adapter
5. repository inventory has no direct or legacy structural consumers
6. consumer matrix has no blocking records
7. key runtime modules import while kdsl_parser_adapter imports are denied
```

## 6. Readiness interpretation

```text
readiness pass => bounded deletion trial may begin
readiness pass != adapter deletion complete
readiness pass != post-deletion proof
```

A separate Phase 6D-9B must:

```text
delete only kdsl_parser_adapter.py
update inventory/readiness expectations
run full unified suite
verify no import/runtime failure
record exact diff and CI evidence
```

## 7. Non-target

```text
semantic utility relocation
parity helper removal
checker behavior changes
specification canonical files
stable/public-ready/tag/release/Release Assets
```

## 8. Boundary

```text
readiness pass != semantic equivalence
readiness pass != complete safety proof
readiness pass != U approval
readiness pass != RT:v
readiness pass != execution authority
readiness pass != adapter removal proof
CI pass != release readiness
```
