from pathlib import Path


def replace_once(path, old, new):
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected one match, found {count}')
    p.write_text(text.replace(old, new, 1), encoding='utf-8')

status = 'docs/project-status.md'
replace_once(status, 'phase: phase9c-k1-pf1-validator-complete', 'phase: phase9d-binding-evidence-schema-complete')
replace_once(status, 'verified_main_head: c2d6e8be0e8f54b73db6ba410ada1b93260c70cb', 'verified_main_head: b4fbec0d0be3bd2a06bf61afa4cac0e409c19571')
replace_once(status, 'K1/PF1 lint:=spec/lint/kdsl-k1-pf1-lint.md\nvalidator結果:=', 'K1/PF1 lint:=spec/lint/kdsl-k1-pf1-lint.md\nBinding evidence:=spec/runtime/kdsl-binding-evidence-schema.md\nBinding evidence lint:=spec/lint/kdsl-binding-evidence-lint.md\nvalidator結果:=')
replace_once(status, 'Phase 9C K1/PF1 parser/validator compatibility first slice: complete\n', 'Phase 9C K1/PF1 parser/validator compatibility first slice: complete\nPhase 9D binding-evidence schema/lint/example: complete\n')
replace_once(status, '## 6. Latest verified design / implementation\n\nPhase 9C validator proof:', '''## 6. Latest verified design / implementation

Phase 9D schema proof:

```text
PR: 142
source head: dc090a26593e920a550545957dce092e6fed1e7d
squash commit: b4fbec0d0be3bd2a06bf61afa4cac0e409c19571
workflow run: 29639314207 / #524
KDSL Validation: success
Packet Semantic Property: success
Packet P1 Normalization Property: success
scope: binding-evidence schema/lint/example/canonical alignment
binding-evidence parser/validator/evaluator: not implemented
```

Phase 9C validator proof:''')
replace_once(status, 'Phase 9C shared-parser registration was validated before storage; final parser diff added only K1/PF1 markers\n', 'Phase 9C shared-parser registration was validated before storage; final parser diff added only K1/PF1 markers\nPhase 9D self-audit separated bound state from authority/capability sufficiency and aligned candidate/adopted status before merge\n')
replace_once(status, '''K1/PF1 exact compatibility: id/revision/digest/project_scope/contract_schemas
BINDING.state: unbound''', '''K1/PF1 exact compatibility: id/revision/digest/project_scope/contract_schemas
Binding evidence schema: kdsl-binding-evidence@0.1-draft / adopted v2-draft
Binding evidence parser/validator/evaluator: not implemented
P1L runtime_control reference: compact JSON schema/id/revision/digest
BINDING.state: unbound''')
replace_once(status, 'K1/PF1 bounded non-executable validator/compatibility first slice\nexperimental heuristic validator helpers', 'K1/PF1 bounded non-executable validator/compatibility first slice\nBinding-evidence canonical schema/lint/non-executable example\nexperimental heuristic validator helpers')
replace_once(status, 'K1/PF1 runtime binding/execution authorization implementation', 'Binding-evidence parser/evaluator and runtime binding implementation')
replace_once(status, '''P0: Phase 9D binding-evidence field schema only under separate approval
P1: future P1L→K1/PF1 binding evaluator only under separate approval
Hold: runtime binding/executable promotion/stable/public-ready/tag/release/Release Assets''', '''P0: Phase 9E binding-evidence parser/validator first slice only under separate approval
P1: future P1L→K1/PF1 binding evaluator only under separate approval
Hold: runtime binding/executable promotion/stable/public-ready/tag/release/Release Assets''')

replace_once('docs/reviews/kdsl-phase9d-binding-evidence-schema.md', 'status: schema-adoption-candidate', 'status: adopted-v2-draft')
replace_once('docs/reviews/kdsl-phase9d-binding-evidence-schema.md', 'Repository validation and closeout alignment are required before adoption. Lint and CI success remain heuristic evidence only.', 'Adopted by PR #142 at `b4fbec0d0be3bd2a06bf61afa4cac0e409c19571`. Lint and CI success remain heuristic evidence only.')
replace_once('docs/reviews/kdsl-phase9d-validation-evidence.md', 'status: pre-merge-evidence', 'status: merged-evidence')
replace_once('docs/reviews/kdsl-phase9d-validation-evidence.md', 'Repository-required checks are rerun from the subsequent normal commit.', 'Repository-required checks were rerun from normal commit `dc090a26593e920a550545957dce092e6fed1e7d` and all required jobs succeeded in run #524. The schema PR was squash-merged as `b4fbec0d0be3bd2a06bf61afa4cac0e409c19571`.')
