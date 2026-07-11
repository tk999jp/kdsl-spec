# KDSL Registry

Purpose: hold declared registries used by KDSL profiles, bridges, result schemas, and future envelopes.

status: v2-draft workspace

## Current registry candidates

```text
spec/registry/kdsl-safety-gate-registry.md
```

## Boundary

```text
Registry ID != permission
Registry state != execution authority
Registry reference != protected wording removal permission
unknown registry/ID推測禁止
```

The registry layer does not replace Core, Profile, R1, Lint, or Bridge specifications.

Until `spec/manifest.md` explicitly adopts a registry file, the file remains a review candidate and must not be treated as stable/public-ready specification.
