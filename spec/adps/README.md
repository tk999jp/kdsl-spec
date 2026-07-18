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

K1/PF1 runtime control:
  spec/runtime/README.md
  spec/runtime/kdsl-k1-runtime-kernel-schema.md
  spec/runtime/kdsl-pf1-project-profile-schema.md
  spec/runtime/kdsl-runtime-control-canonicalization.md
  spec/runtime/kdsl-binding-evidence-schema.md
  spec/lint/kdsl-k1-pf1-lint.md
  spec/lint/kdsl-binding-evidence-lint.md

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
> K1 runtime-control semantics
> PF1 exact project definitions
> K1/PF1 lint
> binding-evidence schema/lint
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
K1/PF1 valid|lint pass != executable|authority grant
capability != permission
Stop continuation/routing != authority
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
shared parser core P1L registration: Phase 8 first-class integrated
checker-local P1L bootstrap: removed
shared P1L compatibility corpus: 10 expectations / failed 0
Packet→P1L/P1 normalization: Phase 7D target-specific first slice integrated
Packet P1 normalization corpus: 17 expectations / failed 0
Packet preview markers: P1L_PREVIEW / P1_PREVIEW
Packet normalized-state promotion: not implemented
runtime binding: not implemented
K1 schema: kdsl-k1@0.1-draft adopted / non-executable
PF1 schema: kdsl-pf1@0.1-draft adopted / non-executable
runtime-control canonicalization: kdsl-runtime-control-c14n@0.1-draft adopted
K1/PF1 lint/examples: adopted explanatory/manual corpus
K1/PF1 parser/validator/exact compatibility: Phase 9C bounded first slice
binding-evidence schema/lint/example: kdsl-binding-evidence@0.1-draft adopted
binding-evidence evaluator/generator: not implemented
Packet executable promotion: prohibited
```

Validator targets:

```text
python tools/validator/kdsl_validate.py --target p1l <file>
python tools/validator/kdsl_validate.py --target p1 <file>
python tools/validator/kdsl_validate.py --target p1-contract <file>
python tools/validator/kdsl_p1_roundtrip.py <file>
python tools/validator/run_p1_shared_ast_samples.py
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
examples/runtime/binding-evidence-non-executable.example.md
```

Examples are not specification sources.
