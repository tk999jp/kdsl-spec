# ADPS / P1L / P1 Specification Index

status: v2-draft adopted index

## Canonical and adopted files

```text
Bridge / boundary:
  spec/bridge/kdsl-adps-bridge.md

P1L canonical structured contract:
  spec/adps/kdsl-p1l-contract-schema.md
  schema: kdsl-p1l@0.1-draft

P1 subordinate compact serialization:
  spec/adps/kdsl-p1-compact-contract-schema.md
  schema: kdsl-p1@0.1-draft

Lint:
  spec/lint/kdsl-p1-p1l-lint.md

Validator implementation notes:
  tools/validator/kdsl-p1-contract-implementation-notes.md
```

## Ownership

```text
Core/Profile/R1/Bridge canonical meaning
> P1L canonical v2-draft contract schema
> P1 compact serialization profile
> P1/P1L lint
> validator/example/tool
```

## Required boundaries

```text
KDSL-DP direct execution prohibited
KDSL-DP→P1L/P1 normalization required
P1L/P1 valid != executable
P1L/P1 lint/round-trip pass != execution authority
profile completion != inference
unknown profile/alias/preset→blocked
BINDING.executable:false under v0.1 draft
RT:v result claim belongs to R1/R1C after target-environment evidence
NEXT remains proposal only
COMMIT remains non-authoritative unless actually executed
```

## Current implementation state

```text
P1L schema: adopted v2-draft
P1 compact schema: adopted v2-draft
lint: adopted v2-draft
examples: adopted explanatory corpus
parser/validator: Phase 7C first bounded slice integrated
round-trip corpus: 14 expectations / failed 0
shared parser core registration: not integrated / checker-local bootstrap only
runtime binding: not implemented
K1/PF1 canonical schema: absent
Packet→P1L/P1 normalization integration: not implemented
Packet executable promotion: prohibited
```

Validator targets:

```text
python tools/validator/kdsl_validate.py --target p1l <file>
python tools/validator/kdsl_validate.py --target p1 <file>
python tools/validator/kdsl_validate.py --target p1-contract <file>
python tools/validator/kdsl_p1_roundtrip.py <file>
```

```text
validator pass != semantic equivalence
validator pass != complete safety proof
validator pass != runtime binding
validator pass != execution authority
validator pass != RT:v
```

## Examples

```text
examples/adps/p1l-investigate.example.md
examples/adps/p1-profile-completed.example.md
examples/adps/p1-unknown-profile-blocked.example.md
examples/adps/p1-authority-missing-blocked.example.md
```

Examples are not specification sources.
