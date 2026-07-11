# KDSL Packet Normalization Validator / Mapper First Slice

status: integration-candidate
schema: kdsl-packet-normalization@0.1-draft
checker: tools/validator/kdsl_packet_normalization.py
mapper: tools/validator/kdsl_packet_normalize.py
validator_authority: non-authoritative

## Checker scope

```text
NORMALIZATION_DRAFT detection/out-of-scope separation
required field presence/order
SOURCE digest/status/not_normalized
TARGET kind/schema/resolution/executable
MAP accounting/mode/evidence
PRESERVE classes
UNRESOLVED/LOSS consistency
ROUND_TRIP state/semantic boundary
AUTHORITY.execution_authority:none
OUTPUT marker/executable/preview boundary
P1/P1L blocked target enforcement
KDSL_PROMPT/P1/P1L/PKT:v1 marker rejection
```

## Mapper scope

```text
source Packet validated first
BASE-KDSL-DEV→KDSL_PROMPT_PREVIEW
BASE-DESIGN-ONLY→DESIGN_PREVIEW
BASE-ADPS-P1→blocked/no preview
source SHA-256 recorded
ROUND_TRIP:not_tested|blocked
semantic_equivalence:not_proven
execution_authority:none
```

## Boundaries

```text
line-based heuristic parser
first NORMALIZATION_DRAFT/PACKET_DRAFT block only
full YAML parserなし
semantic equivalence proofなし
round-trip proofなし
Safety Gate completeness proofなし
mapper output != executable target
KDSL_PROMPT:生成なし
P1/P1L生成なし
Packet state normalized化なし
```
