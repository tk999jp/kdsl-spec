# Phase 6D-1 — Parser Adapter Dependency Inventory

status: completed / integrated
review_date: 2026-07-13
repository: tk999jp/kdsl-spec
tracking_issue: 55
implementation_pull_request: 83
validator_authority: non-authoritative

## 1. Goal

Freeze the remaining parser-adapter and structural-helper dependency surface before any removal attempt.

```text
active checker migration complete != adapter retirement proof
helper exports retained != active checker Phase 1 path
unknown dependency drift must fail before removal work
```

## 2. Integrated files

```text
docs/design/kdsl-phase6d-adapter-retirement.md
tools/validator/kdsl_parser_adapter_inventory.py
tools/validator/run_parser_adapter_inventory_samples.py
tools/validator/samples/adapter-inventory/unauthorized_direct.py
tools/validator/samples/adapter-inventory/prohibited_r1c.py
tools/validator/samples/adapter-inventory/helper_consumer.py
```

Unified runner integration:

```text
tools/validator/run_all_samples.py
```

## 3. Inventory classes

```text
A. direct kdsl_parser_adapter installer importer
B. legacy structural helper consumer
C. nonstructural module consumer
D. prohibited installer recurrence
```

Known direct installer boundary:

```text
kdsl_packet.py -> install_packet
kdsl_packet_normalization.py -> install_normalization
kdsl_safety_gate.py -> install_safety_gate
```

Unknown direct importers fail. `install_r1c` recurrence fails.

## 4. Current decision

```text
adapter_retirement: blocked
```

Reasons:

```text
direct installer compatibility exports remain
legacy structural helper consumers remain
per-consumer migrate/replace/retain decisions are incomplete
post-removal mutation/property corpus is absent
```

This is an expected safe progression state, not a regression.

## 5. Corpus

```text
repository dependency inventory is known
unauthorized direct adapter importer is rejected
install_r1c recurrence is rejected
legacy structural helper consumer is classified
```

Expected integrated validation state:

```text
inventory corpus: 4 / failed 0
unified runners: 21
unified expectations: 357 / failed 0
```

## 6. Retirement gates

```text
G1 active checker independence: satisfied
G2 direct installer inventory: integrated
G3 helper-consumer inventory: first bounded slice integrated
G4 mutation/property/repository corpus: incomplete
G5 replacement API or explicit retention: incomplete
G6 per-family post-removal proof: absent
G7 adapter file retirement: blocked
```

## 7. Safety and authority boundary

```text
inventory pass != adapter retirement proof
inventory pass != semantic equivalence
inventory pass != complete safety proof
inventory pass != U approval
inventory pass != RT:v
inventory pass != execution authority
CI pass != release readiness
```

Retained:

```text
build/diff/lint/test/CI pass != RT:v
NEXT:=proposal, not execution authority
COMMIT:=actual/proposed record, not auto-commit authority
Packet executable:no
Packet state:not_normalized
Normalization semantic_equivalence:not_proven
Normalization execution_authority:none
stable/public-ready/tag/release/Release Assets操作なし
```

## 8. Known limitations

```text
inventory recognizes a bounded known structural-helper symbol set
runtime/dynamic imports are not proven absent
consumer semantic dependence is not inferred
mutation/property evidence is incomplete
adapter removal was not attempted
```

## 9. Next safe step

Phase 6D-2:

```text
record the exact helper-consumer matrix
classify each consumer as migrate|replace|retain-with-reason
select one low-risk helper family for additive direct-CompatibilityView migration
add consumer-specific mutation/property cases before changing imports
```

Recommended first family:

```text
Packet Normalization round-trip/property helper consumers
```

Alternative:

```text
Safety Gate inheritance/graph helpers if consumer contracts are more self-contained
```

## 10. Closeout decision

```text
Phase 6D-1 inventory: integrated
adapter retirement: blocked
adapter removal: not performed
Issue #55: remain open
semantic equivalence: not_proven
complete safety proof: not_proven
RT:v: not granted
execution authority: none
public_ready: no
stable_release: none
Release Assets: none
```
