# KDSL Registry

Purpose: hold declared registries used by KDSL profiles, bridges, result schemas, and future envelopes.

status: v2-draft adopted workspace

## Current v2-draft registries

```text
kdsl-sg@0.1-draft
  spec/registry/kdsl-safety-gate-registry.md
  spec/registry/kdsl-safety-gate-composition.md
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
unknown registry/ID推測禁止
specialized gate != broader gate解除
```

The registry layer does not replace Core, Profile, R1, Lint, or Bridge specifications.

Current status:

```text
kdsl-sg@0.1-draft:=v2-draft adopted
stable/public-ready:=no
Safety Gate validator:=not implemented
KDSL-Packet:=draft-non-executable
```

Adoption in `spec/manifest.md` authorizes v2-draft reference use only. It does not authorize stable promotion, execution authority, Packet execution, tag/release operations, or Release Assets changes.
