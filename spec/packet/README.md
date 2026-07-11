# KDSL Packet Specifications

status: v2-draft workspace
canonical: manifest-owned

## Adopted Packet authoring schema

```text
schema: kdsl-packet@0.1-draft
source: spec/packet/kdsl-packet-schema.md
status: v2-draft adopted
executable: no
```

## Normalization contract candidate

```text
schema: kdsl-packet-normalization@0.1-draft
source: spec/packet/kdsl-packet-normalization-contract.md
status: design-candidate
executable: no
validator/tool: not implemented
```

## Boundary

```text
PACKET_DRAFT != execution contract
NORMALIZATION_DRAFT != execution contract
KDSL_PROMPT_PREVIEW != KDSL_PROMPT
P1/P1L mapping unresolved→blocked
Registry/opcode != authority
semantic_equivalence:not_proven
PKT:v1使用禁止
```

Ownership and promotion decisions are controlled by `spec/manifest.md`. The presence of a design candidate does not adopt it or authorize tooling, execution, stable promotion, tag/release operations, or Release Assets changes.
