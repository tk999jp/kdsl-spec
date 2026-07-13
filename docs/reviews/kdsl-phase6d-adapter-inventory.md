# Phase 6D-1 — Parser Adapter Dependency Inventory

status: completed / integrated / unified-CI-verified-after-corrective
review_date: 2026-07-14
repository: tk999jp/kdsl-spec
tracking_issue: 55
implementation_pull_request: 83
corrective_pull_request: 87
corrective_squash_commit: 724d31dfb1adbbba7488db4cb444c65047492d5d
verified_workflow: 29288377720 / 345 / success
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
tools/validator/run_all_samples.py
```

`run_all_samples.py` integration and direct-installer correction were completed by PR #87.

## 3. Inventory classes

```text
A. direct kdsl_parser_adapter installer importer
B. legacy structural helper consumer
C. nonstructural module consumer
D. prohibited installer recurrence
```

Verified direct installer boundary:

```text
kdsl_packet.py -> install_packet
kdsl_packet_normalization.py -> install_normalization
```

Safety Gate:

```text
kdsl_safety_gate.py direct installer: absent
Safety Gate helper-consumer symbols: still inventoried
```

Unknown direct importers fail. `install_r1c` recurrence fails.

## 4. Evidence correction

PR #83 integrated the inventory tool and dedicated runner but did not connect the runner to the unified suite. Its original inventory also expected a stale Safety Gate direct installer.

PR #87 corrected both issues.

```text
run #341: failure exposed stale installer expectation
run #342: isolated inventory failure
run #344: corrected inventory runner success
run #345: inventory + matrix unified success
```

## 5. Verified corpus

```text
repository dependency inventory is known
unauthorized direct adapter importer is rejected
install_r1c recurrence is rejected
legacy structural helper consumer is classified
```

```text
inventory corpus: 4 / failed 0
consumer matrix corpus: 5 / failed 0
unified runners: 22
unified expectations: 362 / failed 0
KDSL Validation: success
Packet Semantic Property: success
```

## 6. Retirement gates

```text
G1 active checker independence: satisfied
G2 direct installer inventory: integrated / unified-CI-verified
G3 helper-consumer decision matrix: integrated / unified-CI-verified
G4 mutation/property/repository corpus: incomplete
G5 replacement API or explicit retention: incomplete
G6 per-family post-removal proof: absent
G7 adapter file retirement: blocked
```

## 7. Current decision

```text
adapter_retirement: blocked
adapter_removal: not performed
```

Reasons:

```text
direct installer compatibility exports remain
legacy structural helper consumers remain
consumer-specific mutation/property evidence incomplete
post-removal proof absent
```

## 8. Safety and authority boundary

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

## 9. Next safe step

```text
Phase 6D-3A: Packet Normalization round-trip/property consumer contract corpus
Phase 6D-3B: consumer migration after contract proof
```

## 10. Closeout decision

```text
Phase 6D-1 inventory: integrated and unified-CI-verified
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
