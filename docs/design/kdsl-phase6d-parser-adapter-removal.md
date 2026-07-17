# Phase 6D-9B — Parser Adapter Removal Trial

status: bounded implementation trial
repository: tk999jp/kdsl-spec
tracking_issue: 55

## Goal

Delete only:

```text
tools/validator/kdsl_parser_adapter.py
```

and replace the pre-deletion readiness runner with post-deletion proof.

## Preconditions

Phase 6D-9A established:

```text
direct adapter imports: none
installer consumers: none
legacy structural helper consumers: none
parity dependency on adapter: none
consumer matrix blocking records: 0
key runtime modules import with adapter denied
```

## Exact change

```text
delete kdsl_parser_adapter.py
delete run_parser_adapter_retirement_readiness_samples.py
add run_parser_adapter_removal_samples.py
replace unified runner entry
```

## Post-deletion corpus

```text
adapter file absent
no top-level adapter imports
no installer names loaded
parity modules remain adapter-independent
inventory remains direct/legacy empty
consumer matrix remains semantic-only/nonblocking
key runtime modules import after deletion under adapter-deny guard
```

## Preserved

```text
Safety Gate semantic internal API
checker-local and direct legacy-parser parity paths
all active CompatibilityView paths
all existing validator suites and exits
Packet/Normalization non-executable boundaries
RT/NEXT/COMMIT authority boundaries
```

## Non-target

```text
semantic utility relocation
parity helper removal
checker behavior changes
specification canonical files
stable/public-ready/tag/release/Release Assets
```

## Completion gate

```text
adapter removal corpus: 7 / failed 0
unified runners: 35
unified expectations: 442 / failed 0
KDSL Validation: success
Packet Semantic Property: success
```

## Boundary

```text
post-deletion pass != semantic equivalence
post-deletion pass != complete safety proof
post-deletion pass != U approval
post-deletion pass != RT:v
post-deletion pass != execution authority
post-deletion pass != release readiness
```
