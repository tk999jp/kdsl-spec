# Packet→P1L/P1 Normalization Implementation Notes

status: Phase 7D first slice integrated
implementation_date: 2026-07-17
source_schema: kdsl-packet@0.1-draft
target_schemas:
  - kdsl-p1l@0.1-draft
  - kdsl-p1@0.1-draft
contract: spec/packet/kdsl-packet-p1-normalization-contract.md
lint: spec/lint/kdsl-packet-p1-normalization-lint.md

## Components

```text
kdsl_packet_normalize_p1.py
  BASE-ADPS-P1 dedicated mapper
  P1L/P1 preview generation

kdsl_packet_p1_property.py
  target-specific source/mapping/model/authority/preview property checker

run_packet_p1_normalization_samples.py
  positive and mutation corpus

validator workflow:
  Packet P1 Normalization Property job
```

## Mapping boundary

```text
BASE: BASE-ADPS-P1
NORMALIZE.target: P1L|P1
TARGET.resolution: resolved
TARGET.executable: false
```

Generic Packet normalization remains conservative. Resolution applies only through the dedicated target-specific contract, mapper, and property checker.

## Preview boundary

```text
P1L_PREVIEW != P1L:
P1_PREVIEW != P1|
OUTPUT.executable:false
AUTHORITY.execution_authority:none
semantic_equivalence:not_proven
```

P1L preview stores the canonical projection as JSON. P1 preview stores the P1 serialization as a JSON string so no executable-looking top-level P1 marker is emitted.

## Authority mapping

Source Packet rails copied exactly:

```text
read/edit/stage/commit/push/release
```

Additional P1L rails are explicit safety narrowing:

```text
public_repo: forbid
destructive_ops: forbid
```

This expansion is recorded in MAP evidence. It is not a hidden default or authority grant.

## Parser architecture

The property checker uses `NormalizationCompatibilityView` directly.

Initial Phase 7D attempt imported legacy structural helpers from `kdsl_packet_normalization.py`. Repository inventory correctly rejected the new legacy consumer. The checker was migrated to AST v2 CompatibilityView methods before integration.

```text
legacy structural helper consumer: none
shared parser adapter state: unchanged
```

## Corpus

```text
Packet→P1L/P1 corpus: 17 / failed 0
```

Covered:

```text
P1L and P1 mapper/property positive paths
supplied artifact verification
TARGET executable widening
canonical-looking preview marker exposure
source authority widening
public_repo/destructive_ops widening/removal
Binding executable widening
semantic equivalence claim
missing MAP field
Packet normalized self-claim
wrong BASE
```

## CI evidence

```text
implementation PR: 125
source head: df86e547b63a0499c74f412118ed34df93d836c6
squash commit: 222b8483ec12e09d5316a7124f3f611dbb5e507c
workflow run: 29585279349 / #433
KDSL Validation: success
Packet Semantic Property: success
Packet P1 Normalization Property: success
```

Corrective history:

```text
run #430: unified suite failed
run #431: dedicated Packet P1 corpus passed; unified suite still failed
cause: new property checker imported legacy normalization structural helpers
correction: use NormalizationCompatibilityView directly
run #433: all three jobs success
```

## Deliberate limits

```text
Packet source remains not_normalized
no runtime binding
no K1/PF1 schema
no executable transformer
no AI coding tool direct execution
no complete semantic equivalence proof
no complete safety proof
```

## Trust boundary

```text
property_pass != Packet normalized
property_pass != executable
property_pass != runtime binding
property_pass != execution authority
property_pass != RT:v
CI success != release readiness
```
