# Parser Adapter Consumer Decision Matrix Notes

status: phase6d-consumer-matrix-integrated / unified-ci-verified / retirement-blocked
matrix_tool: tools/validator/kdsl_parser_adapter_matrix.py
matrix_runner: tools/validator/run_parser_adapter_matrix_samples.py
inventory_tool: tools/validator/kdsl_parser_adapter_inventory.py
implementation_pull_request: 85
implementation_squash_commit: 330f79694a50b509b02d9a43a7160ad8ab2650cb
corrective_pull_request: 87
corrective_squash_commit: 724d31dfb1adbbba7488db4cb444c65047492d5d
verified_workflow: 29288377720 / 345 / success
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

## Verification

PR #85 integrated the matrix tool and dedicated runner. PR #87 connected it to the unified suite and corrected the direct-installer inventory.

```text
adapter inventory: 4 / failed 0
consumer matrix: 5 / failed 0
unified runners: 22
unified expectations: 362 / failed 0
workflow run: 29288377720 / #345
KDSL Validation: success
Packet Semantic Property: success
```

Previous run #337 succeeded for the then-current 20-runner suite; it was not the unified proof for the inventory/matrix corpora.

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
add consumer-specific mutation/property evidence
migrate or replace imports
re-run inventory and matrix
attempt installer removal only after blocking records are cleared per family
```
