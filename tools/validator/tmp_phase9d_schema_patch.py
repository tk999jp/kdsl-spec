from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected one match, found {count}')
    p.write_text(text.replace(old, new, 1), encoding='utf-8')


# Runtime index
replace_once(
    'spec/runtime/README.md',
    '''Canonicalization:
  spec/runtime/kdsl-runtime-control-canonicalization.md
  id: kdsl-runtime-control-c14n@0.1-draft

Lint:
  spec/lint/kdsl-k1-pf1-lint.md''',
    '''Canonicalization:
  spec/runtime/kdsl-runtime-control-canonicalization.md
  id: kdsl-runtime-control-c14n@0.1-draft

Binding evidence:
  spec/runtime/kdsl-binding-evidence-schema.md
  schema: kdsl-binding-evidence@0.1-draft

Lint:
  spec/lint/kdsl-k1-pf1-lint.md
  spec/lint/kdsl-binding-evidence-lint.md''',
)
replace_once(
    'spec/runtime/README.md',
    '''> lint
> bounded resolver/parser/validator
> route/skill/tool implementation''',
    '''> lint
> bounded resolver/parser/validator
> binding-evidence schema
> future binding evaluator
> route/skill/tool implementation''',
)
replace_once(
    'spec/runtime/README.md',
    'Phase 9D binding-evidence schema: not implemented',
    'Phase 9D binding-evidence schema/lint/example: adopted v2-draft',
)
replace_once(
    'spec/runtime/README.md',
    '''examples/runtime/k1-pf1-non-executable.example.md
examples/runtime/k1-canonical.example.md''',
    '''examples/runtime/k1-pf1-non-executable.example.md
examples/runtime/k1-canonical.example.md
examples/runtime/binding-evidence-non-executable.example.md''',
)

# Canonicalization
replace_once(
    'spec/runtime/kdsl-runtime-control-canonicalization.md',
    '''applies_to:
  - kdsl-k1@0.1-draft
  - kdsl-pf1@0.1-draft''',
    '''applies_to:
  - kdsl-k1@0.1-draft
  - kdsl-pf1@0.1-draft
  - kdsl-binding-evidence@0.1-draft''',
)
replace_once(
    'spec/runtime/kdsl-runtime-control-canonicalization.md',
    'Define deterministic semantic projection and content identity for K1/PF1 definitions.',
    'Define deterministic semantic projection and content identity for K1/PF1 definitions and binding-evidence records.',
)
replace_once(
    'spec/runtime/kdsl-runtime-control-canonicalization.md',
    '→ parse one canonical K1 or PF1 envelope',
    '→ parse one canonical K1, PF1, or BINDING_EVIDENCE envelope',
)
replace_once(
    'spec/runtime/kdsl-runtime-control-canonicalization.md',
    'Every canonical K1/PF1 instance declares:',
    'Every canonical K1/PF1 instance and binding-evidence record declares:',
)

# K1 alignment
replace_once(
    'spec/runtime/kdsl-k1-runtime-kernel-schema.md',
    '  evidence_schema: deferred_phase9d',
    '  evidence_schema: kdsl-binding-evidence@0.1-draft',
)
replace_once(
    'spec/runtime/kdsl-k1-runtime-kernel-schema.md',
    'The record schema and resolver implementation remain Phase 9D/9C work. No executable-looking canonical envelope is introduced in Phase 9B.',
    'The record schema is `kdsl-binding-evidence@0.1-draft`. Evaluator and record-generation implementations remain separate future work.',
)
replace_once(
    'spec/runtime/kdsl-k1-runtime-kernel-schema.md',
    '''runtime-binding resolver implementation
binding-evidence field schema
BINDING.executable:true''',
    '''runtime-binding evaluator implementation
binding-evidence record generation
BINDING.executable:true''',
)

# P1L reference alignment
replace_once(
    'spec/adps/kdsl-p1l-contract-schema.md',
    '  runtime_control: "<K1/PF1 reference or unresolved>"',
    '  runtime_control: "<compact kdsl-binding-evidence reference or unresolved>"',
)
replace_once(
    'spec/adps/kdsl-p1l-contract-schema.md',
    '''## 13. BINDING

Schema adoption does not define runtime control.''',
    '''## 13. BINDING

`kdsl-binding-evidence@0.1-draft` defines the external evidence-record fields. P1L stores only this compact JSON scalar reference:

```text
{"schema":"kdsl-binding-evidence@0.1-draft","id":"<exact id>","revision":"<exact revision>","digest":"sha256:<64 lowercase hex>"}
```

The fixed key order is `schema,id,revision,digest` with no insignificant whitespace. A resolved reference must match the exact external record. This reference form does not define a runtime evaluator.''',
)

# K1/PF1 lint alignment
replace_once(
    'spec/lint/kdsl-k1-pf1-lint.md',
    '- [ ] Binding-evidence schema remains deferred, not invented.',
    '- [ ] Binding evidence references `kdsl-binding-evidence@0.1-draft`; record lint remains separate.',
)
replace_once(
    'spec/lint/kdsl-k1-pf1-lint.md',
    '''## 12. Validator limitation

Until Phase 9C:

```text
no canonical K1/PF1 resolver/parser/validator implementation
manual lint evidence only
existing validator pass != K1/PF1 conformance proof
```''',
    '''## 12. Validator limitation

```text
K1/PF1 parser/validator/exact compatibility:=Phase 9C bounded first slice
binding-evidence parser/validator:=not implemented
validator pass != binding-evidence conformance|runtime binding|authority proof
```''',
)

# Bridge
replace_once(
    'spec/bridge/kdsl-adps-bridge.md',
    '''K1/PF1 resolver/parser/validator:=not implemented
binding-evidence field schema:=not implemented
runtime binding:=not implemented''',
    '''K1/PF1 parser/validator/exact compatibility:=Phase 9C bounded first slice
binding-evidence field schema:=kdsl-binding-evidence@0.1-draft
runtime evaluator/binding:=not implemented''',
)
replace_once(
    'spec/bridge/kdsl-adps-bridge.md',
    '''runtime binding/resolver implementation
binding-evidence field schema
BINDING.executable:true''',
    '''runtime evaluator/resolver implementation
binding-evidence record generation
BINDING.executable:true''',
)

# ADPS index
replace_once(
    'spec/adps/README.md',
    '''  spec/runtime/kdsl-runtime-control-canonicalization.md
  spec/lint/kdsl-k1-pf1-lint.md''',
    '''  spec/runtime/kdsl-runtime-control-canonicalization.md
  spec/runtime/kdsl-binding-evidence-schema.md
  spec/lint/kdsl-k1-pf1-lint.md
  spec/lint/kdsl-binding-evidence-lint.md''',
)
replace_once(
    'spec/adps/README.md',
    '''> K1/PF1 lint
> Packet target-specific mapping contract/property''',
    '''> K1/PF1 lint
> binding-evidence schema/lint
> Packet target-specific mapping contract/property''',
)
replace_once(
    'spec/adps/README.md',
    '''K1/PF1 resolver/parser/validator: not implemented
binding-evidence field schema: not implemented''',
    '''K1/PF1 parser/validator/exact compatibility: Phase 9C bounded first slice
binding-evidence schema/lint/example: kdsl-binding-evidence@0.1-draft adopted
binding-evidence evaluator/generator: not implemented''',
)
replace_once(
    'spec/adps/README.md',
    'examples/packet/packet-p1l-normalization.example.md',
    'examples/packet/packet-p1l-normalization.example.md\nexamples/runtime/binding-evidence-non-executable.example.md',
)

# Manifest
replace_once(
    'spec/manifest.md',
    '''  valid != executable|authority grant
  resolver/runtime bindingとは分離''',
    '''  valid != executable|authority grant
  binding evidence:=external content-addressed record
  evaluator/runtime bindingとは分離''',
)
replace_once(
    'spec/manifest.md',
    '''| `spec/runtime/kdsl-runtime-control-canonicalization.md` | Runtime Control identity | schema-ordered JSON projection / SHA-256 | v2 draft adopted |
| `spec/packet/kdsl-packet-schema.md`''',
    '''| `spec/runtime/kdsl-runtime-control-canonicalization.md` | Runtime Control identity | schema-ordered JSON projection / SHA-256 | v2 draft adopted |
| `spec/runtime/kdsl-binding-evidence-schema.md` | Runtime Control evidence | external content-addressed binding dimensions/provenance | v2 draft adopted / non-executable |
| `spec/packet/kdsl-packet-schema.md`''',
)
replace_once(
    'spec/manifest.md',
    '''| `spec/lint/kdsl-k1-pf1-lint.md` | Lint | K1/PF1 identity/completion/authority/capability/routing/boundary | v2 draft adopted |
| `spec/lint/kdsl-packet-lint.md`''',
    '''| `spec/lint/kdsl-k1-pf1-lint.md` | Lint | K1/PF1 identity/completion/authority/capability/routing/boundary | v2 draft adopted |
| `spec/lint/kdsl-binding-evidence-lint.md` | Lint | binding evidence identity/dimensions/provenance/boundary | v2 draft adopted |
| `spec/lint/kdsl-packet-lint.md`''',
)
replace_once(
    'spec/manifest.md',
    '''> PF1 project definitions
> bounded parser/validator
> route/skill/tool''',
    '''> PF1 project definitions
> binding-evidence schema
> bounded parser/validator
> future binding evaluator
> route/skill/tool''',
)
replace_once(
    'spec/manifest.md',
    '''parser/validator/exact compatibility:=Phase 9C bounded first slice integrated
runtime binding/binding-evidence schema:=not implemented''',
    '''parser/validator/exact compatibility:=Phase 9C bounded first slice integrated
binding-evidence schema:=kdsl-binding-evidence@0.1-draft adopted
runtime evaluator/binding:=not implemented''',
)
replace_once(
    'spec/manifest.md',
    'bounded parser/validator scope明記 / binding未実装明記',
    'bounded parser/validator scope明記 / binding-evidence schema明記 / evaluator未実装明記',
)
replace_once(
    'spec/manifest.md',
    'binding-evidence schema:=not implemented / external content-addressed representation selected',
    'kdsl-binding-evidence@0.1-draft:=adopted external content-addressed evidence record / non-executable',
)

# Glossary main
replace_once(
    'spec/glossary.md',
    'source_alignment: spec/core v1.1-v2-sync / manifest v2-draft-sync / bridge v0.3 / P1L-P1 v0.1-draft / R1 v0.1-draft',
    'source_alignment: spec/core v1.1-v2-sync / manifest v2-draft-sync / bridge v0.3 / P1L-P1 v0.1-draft / K1-PF1-binding v0.1-draft / R1 v0.1-draft',
)
replace_once(
    'spec/glossary.md',
    '''binding evidence:=external content-addressed record
BINDING.executable:false under P1L/P1 v0.1 draft
resolver/runtime binding/binding-evidence schema:=not implemented''',
    '''binding evidence:=external content-addressed record / schema kdsl-binding-evidence@0.1-draft
BINDING.executable:false under P1L/P1 v0.1 draft
K1/PF1 bounded validator:=integrated / binding evaluator:=not implemented''',
)
replace_once(
    'spec/glossary.md',
    '### R1\n',
    '''### Binding evidence

```text
binding evidence:=P1L contractとexact K1/PF1評価次元を結ぶexternal content-addressed record
schema: kdsl-binding-evidence@0.1-draft
```

```text
bound != executable|authority sufficient|capability sufficient|RT:v
approval content validity != source trust
capability != authority
all evaluation dimensions/provenance保持必須
```

### R1
''',
)

# Glossary v2
replace_once(
    'spec/glossary-v2-draft.md',
    '''### Runtime-control canonicalization
''',
    '''### Binding evidence

```text
binding evidence:=external content-addressed runtime-control evaluation record
schema: kdsl-binding-evidence@0.1-draft
P1L reference:=compact JSON schema/id/revision/digest
```

```text
bound != authority sufficient|capability sufficient|executable
approval content validity != source trust
all eight authority rails and all evaluation dimensions remain explicit
```

### Runtime-control canonicalization
''',
)

# Overview
replace_once(
    'docs/overview.md',
    '''canonicalization: kdsl-runtime-control-c14n@0.1-draft
status: adopted v2-draft / non-executable''',
    '''canonicalization: kdsl-runtime-control-c14n@0.1-draft
binding evidence: kdsl-binding-evidence@0.1-draft
status: adopted v2-draft / non-executable''',
)
replace_once(
    'docs/overview.md',
    '''binding evidence:=external content-addressed record
BINDING.executable:false
resolver/runtime binding/binding-evidence schema:=not implemented''',
    '''binding evidence:=external content-addressed record
binding-evidence schema/lint:=adopted v2-draft
BINDING.executable:false
binding evaluator/runtime binding:=not implemented''',
)

# Example: remove YAML anchors from explanatory record.
path = Path('examples/runtime/binding-evidence-non-executable.example.md')
text = path.read_text(encoding='utf-8')
start = text.index('    read: &read_rail')
end_marker = '    destructive_ops: *forbid_rail'
end = text.index(end_marker, start) + len(end_marker)

def rail(name: str, requested: str, mode: str, value: str, scope: str, card: str) -> str:
    return f'''    {name}:
      requested: {requested}
      k1_disposition: preserve
      pf1_mode: {mode}
      pf1_scope: any
      pf1_cardinality: any
      approval_requirement: not_required
      approval_evidence_id: none
      targets: []
      operation_instance: none
      effective_value: {value}
      effective_scope: {scope}
      effective_cardinality: {card}
      state: sufficient'''

blocks = [rail('read', 'allow', 'allow_max', 'allow', 'any', 'any')]
for name in ('edit', 'stage', 'commit', 'push', 'release', 'public_repo', 'destructive_ops'):
    blocks.append(rail(name, 'forbid', 'forbid', 'forbid', 'none', 'none'))
path.write_text(text[:start] + '\n'.join(blocks) + text[end:], encoding='utf-8')

# Review record
Path('docs/reviews/kdsl-phase9d-binding-evidence-schema.md').write_text('''# Phase 9D — Binding Evidence Schema Review

status: schema-candidate
review_date: 2026-07-18
repository: tk999jp/kdsl-spec
tracking_issue: 132
base_main: 8c0c8e7dc6bd93234971c2e4f6e720cbdf83bc05

## Goal

Adopt the external content-addressed evidence-record fields referenced by `P1L.BINDING.runtime_control`.

## Candidate

```text
schema: kdsl-binding-evidence@0.1-draft
canonicalization: kdsl-runtime-control-c14n@0.1-draft
P1L reference: compact JSON schema/id/revision/digest
```

## Decisions

```text
record identity independent from P1L identity
record digest precedes P1L reference creation
evaluation dimensions remain separate
all eight authority rails remain explicit
approval content validity != source trust
capability != authority
bound records exact attachment; executable:false remains fixed
aggregate pass/ready/authorized field absent
```

## Deferred

```text
binding evaluator and record generator
approval authentication
capability observation acquisition
route/tool integration
release-state changes
```

Repository validation and closeout alignment are required before adoption. Lint and CI success remain heuristic evidence only.
''', encoding='utf-8')
