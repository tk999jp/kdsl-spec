# Runtime-Control Specification Index

status: v2-draft adopted index

## Canonical files

```text
K1 schema:
  spec/runtime/kdsl-k1-runtime-kernel-schema.md
  schema: kdsl-k1@0.1-draft

PF1 schema:
  spec/runtime/kdsl-pf1-project-profile-schema.md
  schema: kdsl-pf1@0.1-draft

Canonicalization:
  spec/runtime/kdsl-runtime-control-canonicalization.md
  id: kdsl-runtime-control-c14n@0.1-draft

Lint:
  spec/lint/kdsl-k1-pf1-lint.md
```

## Ownership

```text
Core/R1/Bridge canonical meaning
> P1L/P1 canonical contract meaning
> K1 runtime-control semantics
> PF1 project-scoped exact definitions
> future resolver/lint
> route/skill/tool implementation
> example/template/tool
```

## Required boundaries

```text
K1/PF1 valid != executable|authority grant
PF1 may narrow but never widen P1L authority
capability != permission
Stop continuation != authority
routing != authority
binding evidence:=external content-addressed record
binding evidence != executable instruction
BINDING.executable:false under P1L/P1 v0.1 draft
```

## Phase state

```text
Phase 9A design: complete
Phase 9B schema/lint/examples: adopted v2-draft
Phase 9C resolver/parser/validator: not implemented
Phase 9D binding-evidence schema: not implemented
runtime binding: not implemented
```

## Examples

```text
examples/runtime/k1-pf1-non-executable.example.md
```

Examples are explanatory and are not specification sources, digest proofs, approval evidence, capability evidence, or execution instructions.
