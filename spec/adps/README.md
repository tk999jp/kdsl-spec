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

P1L/P1 lint:
  spec/lint/kdsl-p1-p1l-lint.md

Packet→P1L/P1 normalization:
  spec/packet/kdsl-packet-p1-normalization-contract.md
  spec/lint/kdsl-packet-p1-normalization-lint.md

Validator implementation notes:
  tools/validator/kdsl-p1-contract-implementation-notes.md
  tools/validator/kdsl-packet-p1-normalization-implementation-notes.md
```

## Ownership

```text
Core/Profile/R1/Bridge canonical meaning
> P1L canonical v2-draft contract schema
> P1 compact serialization profile
> P1/P1L lint
> Packet target-specific mapping contract/property
> validator/example/tool
```

## Required boundaries

```text
KDSL-DP direct execution prohibited
KDSL-DP→P1L/P1 normalization required
P1L/P1 valid != executable
P1L/P1 lint/round-trip/property pass != execution authority
profile completion != inference
unknown profile/alias/preset→blocked
BINDING.executable:false under v0.1 draft
RT:v result claim belongs to R1/R1C after target-environment evidence
NEXT remains proposal only
COMMIT remains non-authoritative unless actually executed
Packet remains non-executable/not_normalized
P1L_PREVIEW != P1L:
P1_PREVIEW != P1|
```

## Current implementation state

```text
P1L schema: adopted v2-draft
P1 compact schema: adopted v2-draft
lint: adopted v2-draft
examples: adopted explanatory corpus
parser/validator: Phase 7C first bounded slice integrated
P1L/P1 round-trip corpus: 14 expectations / failed 0
shared parser core registration: not integrated / checker-local bootstrap only
Packet→P1L/P1 normalization: Phase 7D target-specific first slice integrated
Packet P1 normalization corpus: 17 expectations / failed 0
Packet preview markers: P1L_PREVIEW / P1_PREVIEW
Packet normalized-state promotion: not implemented
runtime binding: not implemented
K1/PF1 canonical schema: absent
Packet executable promotion: prohibited
```

Validator targets:

```text
python tools/validator/kdsl_validate.py --target p1l <file>
python tools/validator/kdsl_validate.py --target p1 <file>
python tools/validator/kdsl_validate.py --target p1-contract <file>
python tools/validator/kdsl_p1_roundtrip.py <file>
python tools/validator/kdsl_validate.py --target packet-p1-normalization <packet-file>
python tools/validator/kdsl_packet_normalize_p1.py <packet-file>
python tools/validator/kdsl_packet_p1_property.py <packet-file> [normalization-file]
```

```text
validator/property pass != semantic equivalence
validator/property pass != complete safety proof
validator/property pass != runtime binding
validator/property pass != execution authority
validator/property pass != Packet normalized
validator/property pass != RT:v
```

## Examples

```text
examples/adps/p1l-investigate.example.md
examples/adps/p1-profile-completed.example.md
examples/adps/p1-unknown-profile-blocked.example.md
examples/adps/p1-authority-missing-blocked.example.md
examples/packet/packet-p1l-normalization.example.md
```

Examples are not specification sources.
