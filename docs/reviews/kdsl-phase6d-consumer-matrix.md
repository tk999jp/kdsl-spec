# Phase 6D-2 — Parser Helper Consumer Decision Matrix

status: completed / integrated
review_date: 2026-07-13
repository: tk999jp/kdsl-spec
tracking_issue: 55
implementation_pull_request: 85
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
```

Unified runner integration:

```text
tools/validator/run_all_samples.py
```

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

## 5. Corpus

```text
repository matrix assigns all decisions and remains blocked
legacy helper consumer→migrate-or-replace
parity consumer→retain-parity-only
semantic-only consumer→retain-semantic-api
known direct installer→retain-temporarily
```

Expected integrated state:

```text
inventory corpus: 4 / failed 0
consumer matrix corpus: 5 / failed 0
unified runners: 22
unified expectations: 362 / failed 0
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

Phase 6D-3:

```text
select one migrate-or-replace helper family
record exact consumer files/symbols
add consumer-specific mutation/property tests
migrate imports only after those tests exist
```

Recommended first target:

```text
Packet Normalization round-trip/property consumers
```

Selection reasons:

```text
existing NormalizationCompatibilityView
bounded helper surface
strong non-executable/not_proven/none invariants
existing round-trip/property corpus
```

## 11. Closeout decision

```text
Phase 6D-2 consumer matrix: integrated
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
