# Phase 6D-2 — Parser Helper Consumer Decision Matrix

status: completed / integrated / unified-CI-verified-after-corrective
review_date: 2026-07-14
repository: tk999jp/kdsl-spec
tracking_issue: 55
implementation_pull_request: 85
implementation_source_head: 62743085b2ea1b4708f69c02e97d6085afa750a9
implementation_squash_commit: 330f79694a50b509b02d9a43a7160ad8ab2650cb
corrective_pull_request: 87
corrective_source_head: 20cce60e459bbb379599d69e5a1e1b1bae66f202
corrective_squash_commit: 724d31dfb1adbbba7488db4cb444c65047492d5d
verified_workflow_run_id: 29288377720
verified_workflow_run_number: 345
verified_workflow_conclusion: success
validator_authority: non-authoritative

## 1. Goal

Assign every discovered parser-adapter or helper-module dependency an explicit action before changing imports or attempting adapter retirement.

```text
inventory:=what depends on the compatibility surface
decision matrix:=what must happen next
```

## 2. Integrated files

```text
docs/design/kdsl-phase6d-consumer-matrix.md
tools/validator/kdsl_parser_adapter_matrix.py
tools/validator/run_parser_adapter_matrix_samples.py
tools/validator/samples/adapter-inventory/parity_consumer.py
tools/validator/samples/adapter-inventory/semantic_consumer.py
tools/validator/samples/adapter-inventory/allowed/kdsl_packet.py
tools/validator/run_all_samples.py
```

PR #87 completed the unified runner integration.

## 3. Decision vocabulary

```text
retain-temporarily:
  direct installer remains while dependent helper API is unresolved

migrate-or-replace:
  legacy structural helper consumer needs a CompatibilityView/direct API or dedicated replacement

retain-parity-only:
  legacy helper is limited to prior-contract comparison

retain-semantic-api:
  imported symbol is outside the bounded structural-helper set
```

Unclassified records fail.

## 4. Classification order

```text
direct adapter installer→retain-temporarily
legacy structural helper in parity-named consumer→retain-parity-only
legacy structural helper in other consumer→migrate-or-replace
nonstructural helper-module import→retain-semantic-api
```

The classification is deterministic and emitted as text or JSON.

## 5. Evidence correction and verification

PR #85 integrated the matrix tool and dedicated runner, but did not connect it to `run_all_samples.py`. Therefore run #337 did not prove the matrix corpus inside the unified suite.

PR #87 connected both Phase 6D runners and corrected a stale Safety Gate direct-installer expectation.

```text
run #341: initial unified connection exposed stale inventory assumption
run #342: isolated inventory failure
run #344: corrected inventory-only unified success
run #345: inventory + matrix unified success
```

Final verified corpus:

```text
adapter inventory: 4 / failed 0
consumer matrix: 5 / failed 0
unified runners: 22
unified expectations: 362 / failed 0
KDSL Validation: success
Packet Semantic Property: success
```

Cases:

```text
repository matrix assigns all decisions and remains blocked
legacy helper consumer→migrate-or-replace
parity consumer→retain-parity-only
semantic-only consumer→retain-semantic-api
known direct installer→retain-temporarily
```

## 6. Retirement interpretation

Blocking decisions:

```text
retain-temporarily
migrate-or-replace
```

Nonblocking by classification alone:

```text
retain-parity-only
retain-semantic-api
```

But:

```text
no blocking record != adapter retirement proof
```

Post-change consumer corpus and full CI remain mandatory.

## 7. Current decision

```text
adapter_retirement: blocked
consumer migration: not performed
adapter removal: not performed
```

The matrix makes the remaining work explicit; it does not authorize it.

## 8. Safety and authority boundary

```text
matrix pass != consumer migration
matrix pass != semantic equivalence
matrix pass != complete safety proof
matrix pass != adapter retirement proof
matrix pass != U approval
matrix pass != RT:v
matrix pass != execution authority
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

## 9. Known limitations

```text
classification is based on static ImportFrom analysis
runtime/dynamic imports are not proven absent
retain-semantic-api does not declare a canonical public API
consumer-specific behavior has not yet been migrated or mutation-tested
```

## 10. Next safe step

Phase 6D-3A:

```text
select Packet Normalization round-trip/property helper family
record exact consumer contract
add mutation/property tests before changing imports
```

Phase 6D-3B:

```text
migrate kdsl_packet_roundtrip.parse_normalization to NormalizationCompatibilityView
retain non-executable/not_proven/none boundaries
re-run inventory/matrix and full suite
```

## 11. Closeout decision

```text
Phase 6D-2 consumer matrix: integrated and unified-CI-verified
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
