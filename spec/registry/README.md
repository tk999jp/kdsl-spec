# KDSL Registry

Purpose: hold declared registries used by KDSL profiles, bridges, result schemas, and future envelopes.

status: v2-draft adopted workspace

## Current v2-draft adopted registries

```text
kdsl-sg@0.1-draft
  spec/registry/kdsl-safety-gate-registry.md
  spec/registry/kdsl-safety-gate-composition.md
```

## Current v2-draft adopted Packet registries

```text
kdsl-packet-base@0.1-draft
  spec/registry/kdsl-packet-base-registry.md

kdsl-packet-task@0.1-draft
  spec/registry/kdsl-packet-task-registry.md

kdsl-packet-flow@0.1-draft
  spec/registry/kdsl-packet-flow-registry.md
```

Packet registry status:

```text
adopted: v2-draft
canonical: v2-draft only
stable/public-ready: no
Packet executable effect: none
validator: not implemented
```

Manifest ownership:

```text
spec/manifest.md
```

## Boundary

```text
Registry ID != permission
Registry state != execution authority
Registry reference != protected wording removal permission
BASE/TASK/FLOW ID != normalization completion
FLOW opcode != command
unknown registry/ID推測禁止
specialized gate != broader gate解除
```

The registry layer does not replace Core, Profile, R1, Lint, or Bridge specifications.

Current status:

```text
kdsl-sg@0.1-draft:=v2-draft adopted
Safety Gate validator:=first heuristic slice integrated
kdsl-r1c@0.1-draft:=v2-draft serialization profile adopted
Packet BASE/TASK/FLOW registries:=v2-draft adopted / non-executable
KDSL-Packet:=draft-non-executable
PKT:v1使用禁止
```

Adoption in `spec/manifest.md` authorizes v2-draft reference use only. Registry adoption does not authorize stable promotion, normalization completion, execution authority, Packet execution, tag/release operations, or Release Assets changes.
