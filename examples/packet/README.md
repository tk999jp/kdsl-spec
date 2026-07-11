# KDSL Packet Examples

status: v2-draft examples
canonical: no
executable: no

These examples illustrate the adopted Packet authoring schema and the normalization-contract design candidate.

```text
examples != specification
valid-looking example != executable contract
normalization preview != executable prompt
```

## Packet authoring

```text
packet-design.example.md
normalization-source.example.md
normalization-p1-source.example.md
```

Required Packet boundary:

```text
PACKET_DRAFT
STATUS:non-executable
NORMALIZE.required:true
NORMALIZE.state:not_normalized
PKT:v1使用禁止
```

## Normalization design

```text
normalization-full-kdsl.example.md
normalization-p1-blocked.example.md
normalization-lossy-blocked.example.md
```

Required normalization boundary:

```text
NORMALIZATION_DRAFT
STATUS:non-executable
TARGET.executable:false
semantic_equivalence:not_proven
AUTHORITY.execution_authority:none
```

Source identities:

```text
normalization-source.example.md
  sha256:b464944da1a3e080b08166e0b0eaa13327c4daa8974c3c56f6a22428dd81daed

normalization-p1-source.example.md
  sha256:b37951d0a8c30afef865a64f0e29566136b6c2dace51810c9ef328a6615df9f1
```

The Full KDSL example uses `KDSL_PROMPT_PREVIEW`, not `KDSL_PROMPT:`. P1/P1L examples remain blocked because a canonical target field schema is not present in this repository.

Before any real implementation work, Packet authoring must pass through a separately specified and verified normalization process. This example set does not implement that transformer or grant execution authority.
