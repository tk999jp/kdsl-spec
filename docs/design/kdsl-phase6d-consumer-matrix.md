# Phase 6D-2 — Parser Helper Consumer Decision Matrix

status: design-draft / non-normative implementation plan
repository: tk999jp/kdsl-spec
tracking_issue: 55
review_date: 2026-07-13

## 1. Purpose

Turn the Phase 6D-1 dependency inventory into explicit per-consumer decisions before changing imports or removing compatibility installers.

```text
inventory:=what depends on the compatibility surface
decision matrix:=what must happen before retirement
```

## 2. Decision vocabulary

### `migrate-or-replace`

The consumer imports a bounded legacy structural helper.

Required before retirement:

```text
migrate to a CompatibilityView/helper API
or
replace with a dedicated compatibility module
and
add consumer-specific regression evidence
```

### `retain-parity-only`

The consumer uses a legacy helper solely to compare the prior extraction contract.

```text
retention must remain bounded to parity code
semantic execution must not depend on this path
```

### `retain-semantic-api`

The import is not part of the bounded structural-helper set, such as a constant or semantic function.

```text
semantic module dependency != parser adapter dependency
```

This decision does not prove that the API is stable or canonical.

### `retain-temporarily`

A direct adapter installer remains because downstream helper imports still require installed names.

```text
retention is temporary
removal requires consumer migration evidence
```

## 3. Classification order

```text
direct adapter installer→retain-temporarily
legacy structural helper in parity-named consumer→retain-parity-only
legacy structural helper in other consumer→migrate-or-replace
nonstructural import from helper module→retain-semantic-api
unclassified dependency→failure
```

## 4. Matrix output

```text
path
source module
imported symbols
decision
reason
```

The tool emits text and JSON forms.

```text
tools/validator/kdsl_parser_adapter_matrix.py
tools/validator/kdsl_parser_adapter_matrix.py --json
```

## 5. Retirement interpretation

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

However:

```text
no blocking record != adapter retirement proof
```

Post-change consumer corpus and full CI remain mandatory.

## 6. Safety boundary

The matrix must not:

```text
rewrite imports
remove installers
infer semantic equivalence
infer execution authority
mark adapter retirement complete
weaken Packet/Normalization/Safety/RT/NEXT/COMMIT boundaries
```

## 7. Phase 6D-2 completion criteria

```text
all discovered records receive one allowed decision
unknown direct adapter imports remain failures
install_r1c recurrence remains failure
repository matrix reports current blocking decisions
fixture cases prove each decision class
```

## 8. Next phase

Phase 6D-3 selects one `migrate-or-replace` family and adds consumer-specific mutation/property evidence before changing imports.

Recommended selection criteria:

```text
few consumers
self-contained structural contract
existing CompatibilityView coverage
no authority widening
clear rollback
```

## 9. Authority and release boundary

```text
matrix pass != consumer migration
matrix pass != semantic equivalence
matrix pass != adapter retirement proof
matrix pass != U approval
matrix pass != RT:v
matrix pass != execution authority
CI pass != release readiness
stable/public-ready/tag/release/Release Assets操作なし
```
