# KDSL Packet Validator First Slice

status: implementation-candidate
schema: kdsl-packet@0.1-draft
checker: tools/validator/kdsl_packet.py
validator_authority: non-authoritative

## Implemented checks

```text
PACKET_DRAFT detection / out-of-scope pass
required top-level field presence/order
SCHEMA/STATUS exact values
BASE/TASK/FLOW/SG registry and known ID checks
TASK minimum FLOW and Safety Gate matrices
FLOW-CHANGE ordering around FLOW-GATE/FLOW-STOP
AUTHORITY required rails and allowed values
NORMALIZE.required/target/state and BASE target compatibility
OUT.result_schema representative values
PKT:v1 rejection
representative rollback/runtime/public/data/KDSL-DP trigger gates
```

## Boundaries

```text
line-based heuristic parser
first PACKET_DRAFT block only
full YAML parserなし
full natural-language trigger parserなし
Safety Gate entry state/evidence deep lintなし
protected wording semantic equivalence proofなし
normalization transformer/round-trip proofなし
Packet validator pass != executable/normalized/authority/safety proof
```

## Exit codes

```text
0: pass/out-of-scope
1: warning
2: fail
```
