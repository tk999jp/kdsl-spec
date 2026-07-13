# Parser Adapter Consumer Decision Matrix Notes

status: phase6d-consumer-matrix-integrated / retirement-blocked
matrix_tool: tools/validator/kdsl_parser_adapter_matrix.py
matrix_runner: tools/validator/run_parser_adapter_matrix_samples.py
inventory_tool: tools/validator/kdsl_parser_adapter_inventory.py
tracking_issue: 55
validator_authority: non-authoritative

## Purpose

Convert discovered adapter/helper dependencies into deterministic actions before any import rewrite or adapter removal.

## Decisions

```text
retain-temporarily
migrate-or-replace
retain-parity-only
retain-semantic-api
```

## Rule order

```text
direct installer→retain-temporarily
legacy structural helper + parity-named file→retain-parity-only
legacy structural helper + other file→migrate-or-replace
nonstructural helper-module import→retain-semantic-api
```

Unknown decision values fail.

## Text output

```text
PARSER_ADAPTER_CONSUMER_MATRIX_RESULT:
STATUS:
MODE:
RECORDS:
COUNTS:
ERRORS:
RETIREMENT:
BOUNDARY:
```

## JSON output

```text
python tools/validator/kdsl_parser_adapter_matrix.py --json
```

JSON records contain:

```text
path
module
symbols
decision
reason
```

## Retirement state

Blocking records:

```text
retain-temporarily
migrate-or-replace
```

Current result:

```text
state: blocked
```

A future `candidate` result remains insufficient without consumer-specific tests and post-removal full CI.

## Corpus

```text
repository decision matrix
migrate-or-replace fixture
retain-parity-only fixture
retain-semantic-api fixture
retain-temporarily fixture
```

## Boundaries

```text
matrix pass != consumer migration
matrix pass != semantic equivalence
matrix pass != adapter retirement proof
matrix pass != U approval
matrix pass != RT:v
matrix pass != execution authority
matrix pass != release readiness
```

## Next work

```text
select one migrate-or-replace family
add mutation/property evidence
migrate or replace imports
re-run inventory and matrix
attempt installer removal only after blocking records are cleared per family
```
