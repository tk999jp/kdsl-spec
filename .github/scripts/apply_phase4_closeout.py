from pathlib import Path

ROOT = Path('.')


def replace_once(path: str, old: str, new: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: anchor count {count} for {old[:80]!r}')
    target.write_text(text.replace(old, new, 1), encoding='utf-8')


phase4_changelog = '''#### Phase 4 Packet / Normalization semantic-property proof

- Added `kdsl-packet-property@0.1-draft` subordinate property contract.
- Added an explicit strict Packet semantic surface and `packet-semantic` wrapper target.
- Added a non-executable strict normalization mapper preserving selected exact strings, Safety Gate records, flow/order, result schema, and authority rails.
- Added source Packet × Normalization property comparison with section-scoped VERIFY/result-schema reconstruction checks.
- Added 42 positive/negative/property expectations and a focused read-only CI job.
- Expanded unified `KDSL Validation` from 215 to 257 expectations.

Verification:

```text
pull_request: 48
source_head: ea982099bd5b99862191e0792e15cd501c4cc4f4
squash_commit: 47b15f9af3496dc36e14673cf0a681e3c333b098
workflow_run_id: 29191890776
run_number: 224
phase4_total: 42
unified_total: 257
failed: 0
```

Boundaries:

```text
SEMANTIC_EQUIVALENCE:not_proven
FULL_SAFETY_PROOF:not_proven
NORMALIZATION_COMPLETION:not_proven
EXECUTION_AUTHORITY:none
```

'''
replace_once('CHANGELOG.md', '### Added\n\n#### Phase 3 R1C deep optional-block round-trip', '### Added\n\n' + phase4_changelog + '#### Phase 3 R1C deep optional-block round-trip')

replace_once(
    'README.md',
    'Packet normalization structural round-trip: first-slice integrated / selected structural properties only\nCommon parser/AST: Phase 1 integrated / source-spanned first slice\nmajor parser adapters: R1C / Packet / Packet Normalization / Safety Gate\nKDSL Validation unified suite: 215 expectations / failed 0',
    'Packet normalization structural round-trip: first-slice integrated / selected structural properties only\nPacket semantic/property contract: kdsl-packet-property@0.1-draft / Phase 4 strict first slice integrated / non-executable\nCommon parser/AST: Phase 1 integrated / source-spanned first slice\nmajor parser adapters: R1C / Packet / Packet Normalization / Safety Gate\nKDSL Validation unified suite: 257 expectations / failed 0',
)
replace_once(
    'README.md',
    'Packet:\n  spec/packet/kdsl-packet-schema.md\n  spec/packet/kdsl-packet-normalization-contract.md',
    'Packet:\n  spec/packet/kdsl-packet-schema.md\n  spec/packet/kdsl-packet-normalization-contract.md\n  spec/packet/kdsl-packet-semantic-property-contract.md',
)
replace_once(
    'README.md',
    '  tools/validator/kdsl_packet_roundtrip.py\n  tools/validator/kdsl_parser.py',
    '  tools/validator/kdsl_packet_roundtrip.py\n  tools/validator/kdsl_packet_semantic.py\n  tools/validator/kdsl_packet_normalize_semantic.py\n  tools/validator/kdsl_packet_property.py\n  tools/validator/kdsl_parser.py',
)
replace_once(
    'README.md',
    'normalization: kdsl-packet-normalization@0.1-draft\nnormalization lint: spec/lint/kdsl-packet-normalization-lint.md\nstatus: non-executable',
    'normalization: kdsl-packet-normalization@0.1-draft\nnormalization lint: spec/lint/kdsl-packet-normalization-lint.md\nsemantic/property contract: kdsl-packet-property@0.1-draft\nsemantic/property spec: spec/packet/kdsl-packet-semantic-property-contract.md\nstatus: non-executable',
)
replace_once(
    'README.md',
    'Packet validator/sample matrix\nnormalization transformer/round-trip proof\nSafety Gate completeness/inheritance proof\nstable/canonical execution dependency\nexplicit executable promotion review/U承認',
    'full Packet/Normalization semantic equivalence proof\ncomplete Safety Gate completeness/inheritance proof across arbitrary documents\ncanonical P1/P1L target schema\nstable/canonical execution dependency\nexplicit executable transformer specification/review/U承認',
)
replace_once(
    'README.md',
    'python tools/validator/kdsl_validate.py --target packet <file>\npython tools/validator/kdsl_validate.py --target normalization <file>\npython tools/validator/kdsl_packet_normalize.py <packet-file>\npython tools/validator/kdsl_packet_roundtrip.py <packet-file> [normalization-file]',
    'python tools/validator/kdsl_validate.py --target packet <file>\npython tools/validator/kdsl_validate.py --target packet-semantic <file>\npython tools/validator/kdsl_validate.py --target normalization <file>\npython tools/validator/kdsl_packet_normalize.py <packet-file>\npython tools/validator/kdsl_packet_roundtrip.py <packet-file> [normalization-file]\npython tools/validator/kdsl_packet_normalize_semantic.py <packet-file>\npython tools/validator/kdsl_packet_property.py <packet-file> [normalization-file]',
)
replace_once(
    'README.md',
    '  run_safety_semantics_examples.py: 2\n  run_r1c_optional_samples.py: 34',
    '  run_safety_semantics_examples.py: 2\n  run_r1c_optional_samples.py: 34\n  run_packet_semantic_property_samples.py: 42',
)
replace_once(
    'README.md',
    'pull_request: 45\nsource_head: 1fcd09cf13aaeb3aa54ed0194d443c962bbbd4b7\nsquash_commit: 24f08a4397f22555e73469099014b6ba502760c3\nworkflow/check: KDSL Validation\nworkflow_run: #207 / success\nunified expectations: 215',
    'pull_request: 48\nsource_head: ea982099bd5b99862191e0792e15cd501c4cc4f4\nsquash_commit: 47b15f9af3496dc36e14673cf0a681e3c333b098\nworkflow/check: KDSL Validation + Packet Semantic Property\nworkflow_run: #224 / success\nunified expectations: 257',
)
replace_once(
    'README.md',
    'examples/packet/packet-design.example.md\n```',
    'examples/packet/packet-design.example.md\nexamples/packet/packet-semantic-property.example.md\n```',
)
replace_once(
    'README.md',
    'Packet validator first slice:=main integrated / 69 expectations verified\nPacket full semantic parserなし\nPacket normalization validator/mapper first slice:=main integrated / 93 expectations verified\nPacket normalization structural round-trip first slice:=main integrated / 108 expectations verified\nPacket normalization semantic/property proofなし\nPacket Safety Gate completeness/inheritance proofなし',
    'Packet validator first slice:=main integrated / 69 expectations verified\nPacket strict bounded semantic/property first slice:=Phase 4 integrated / 42 expectations / 257 unified verified\nPacket full YAML/natural-language semantic equivalence proofなし\nPacket normalization validator/mapper first slice:=main integrated / 93 expectations verified\nPacket normalization structural round-trip first slice:=main integrated / 108 expectations verified\nPacket selected semantic/property comparison:=Phase 4 integrated\nPacket complete Safety Gate completeness/inheritance proofなし',
)
replace_once(
    'README.md',
    'P1:\n  Phase 4 Packet / Normalization semantic-property proof\n\nP3:\n  Phase 5 public-facing v2 hardening / release-readiness review',
    'P1:\n  Phase 5 public-facing v2 hardening / release-readiness review',
)

pr48_record = '''### PR #48 — Phase 4 Packet / Normalization semantic-property proof

```yaml
pull_request: 48
merge_status: merged
merge_method: squash
source_branch: agent/kdsl-phase4-packet-semantic-property
source_head: ea982099bd5b99862191e0792e15cd501c4cc4f4
squash_commit: 47b15f9af3496dc36e14673cf0a681e3c333b098
model: kdsl-packet-property@0.1-draft
workflow: KDSL Validation
workflow_run_id: 29191890776
workflow_run_number: 224
workflow_conclusion: success
previous_unified_total: 215
phase4_property_total: 42
unified_total: 257
failed: 0
semantic_equivalence: not_proven
full_safety_proof: not_proven
normalization_completion: not_proven
execution_authority: none
stable_effect: none
```

'''
replace_once('docs/project-status.md', '### PR #45 — Phase 3 R1C deep optional-block round-trip', pr48_record + '### PR #45 — Phase 3 R1C deep optional-block round-trip')
replace_once(
    'docs/project-status.md',
    'Packet normalization structural round-trip first slice:=main統合済み / 108 expectations verified\nKDSL-Packet:=non-executable / normalization required',
    'Packet normalization structural round-trip first slice:=main統合済み / 108 expectations verified\nPacket/Normalization semantic-property Phase 4:=main統合済み / 42 property expectations / 257 unified verified\nKDSL-Packet:=non-executable / normalization required',
)
replace_once('docs/project-status.md', '  optional_safety_gates_round_trip: blocked', '  optional_safety_gates_round_trip: structural_pass_first_slice_phase3')
replace_once(
    'docs/project-status.md',
    '  normalization_validator_mapper: first_slice_integrated_non_executable\n  semantic_equivalence: not_proven',
    '  normalization_validator_mapper: first_slice_integrated_non_executable\n  semantic_property_model: kdsl-packet-property@0.1-draft\n  semantic_property_validator: phase4_strict_first_slice_integrated\n  property_pass_scope: selected_properties_only\n  semantic_equivalence: not_proven',
)
replace_once(
    'docs/project-status.md',
    '    - packet\n    - normalization',
    '    - packet\n    - packet-semantic\n    - normalization',
)
replace_once(
    'docs/project-status.md',
    '    - Packet registry/ID/gate/flow/authority/normalization lint\n    - Packet out-of-scope separation\n    - Normalization envelope/source/target/map/loss/authority/output lint\n    - Non-executable structural mapper',
    '    - Packet registry/ID/gate/flow/authority/normalization lint\n    - Packet strict OBS/Safety Gate/FLOW/authority bounded semantic lint\n    - Packet out-of-scope separation\n    - Normalization envelope/source/target/map/loss/authority/output lint\n    - Non-executable structural mapper\n    - strict source-to-preview exact/protected/order/authority/result property comparison',
)
replace_once(
    'docs/project-status.md',
    '      - python tools/validator/run_safety_semantics_examples.py\n      - python tools/validator/run_r1c_optional_samples.py\n    expected_unified_total: 215',
    '      - python tools/validator/run_safety_semantics_examples.py\n      - python tools/validator/run_r1c_optional_samples.py\n      - python tools/validator/run_packet_semantic_property_samples.py\n    expected_unified_total: 257',
)
replace_once(
    'docs/project-status.md',
    '      pull_request: 45\n      run_id: 29185669224\n      run_number: 207\n      conclusion: success\n      unified_total: 215',
    '      pull_request: 48\n      run_id: 29191890776\n      run_number: 224\n      conclusion: success\n      unified_total: 257',
)
replace_once(
    'docs/project-status.md',
    'Packet full YAML/semantic parser\nPacket Safety Gate state/evidence deep lint\nNormalization semantic/property proofなし\nPacket Safety Gate completeness/inheritance proof\nPacket OUT/R1C integration lint',
    'Packet strict bounded semantic/property first slice integrated; full YAML/natural-language semantic equivalence proof未実装\nPacket Safety Gate state/evidence/authority strict first slice integrated; arbitrary cross-document completeness/inheritance proof未実装\nNormalization selected property comparison integrated; full normalization semantic proof/normalization completion proofなし\nPacket OUT result-schema section property integrated; full R1/R1C semantic integration proofなし',
)
phase4_evidence = '''### Phase 4 Packet / Normalization semantic-property proof

```yaml
pull_request: 48
source_head: ea982099bd5b99862191e0792e15cd501c4cc4f4
squash_commit: 47b15f9af3496dc36e14673cf0a681e3c333b098
model: kdsl-packet-property@0.1-draft
workflow: KDSL Validation
workflow_run_id: 29191890776
run_number: 224
conclusion: success
previous_unified_total: 215
phase4_property_total: 42
unified_total: 257
failed: 0
semantic_equivalence: not_proven
full_safety_proof: not_proven
normalization_completion: not_proven
execution_authority: none
meaning: selected bounded source/preview properties only; not full semantic/safety/normalization/authority proof
```

'''
replace_once('docs/project-status.md', '### Phase 2 Safety Semantics / multi-generation inheritance', phase4_evidence + '### Phase 2 Safety Semantics / multi-generation inheritance')
validation_evidence = '''### Packet / Normalization semantic-property Phase 4

```yaml
pull_request: 48
source_branch: agent/kdsl-phase4-packet-semantic-property
source_head: ea982099bd5b99862191e0792e15cd501c4cc4f4
squash_commit: 47b15f9af3496dc36e14673cf0a681e3c333b098
workflow_run_id: 29191890776
run_number: 224
conclusion: success
phase4_property_total: 42
phase4_property_failed: 0
unified_runners: 8
unified_total: 257
unified_failed: 0
full_kdsl_selected_properties: property_pass
p1_p1l: blocked
meaning: selected source/preview property evidence; not semantic-equivalence/safety/normalization-completion/execution proof
```

'''
replace_once('docs/project-status.md', '### Packet normalization structural round-trip first slice', validation_evidence + '### Packet normalization structural round-trip first slice')
replace_once(
    'docs/project-status.md',
    'tools/validator/verification/kdsl_common_parser_verify.md\ndocs/reviews/kdsl-phase2-safety-semantics.md',
    'tools/validator/verification/kdsl_common_parser_verify.md\ndocs/reviews/kdsl-phase4-packet-normalization-property.md\ntools/validator/kdsl-packet-semantic-property-implementation-notes.md\ndocs/reviews/kdsl-phase2-safety-semantics.md',
)
replace_once(
    'docs/project-status.md',
    'R1C full semantic equivalence proofなし / optional SAFETY_GATES round-trip blocked\nPacket full YAML/semantic parserなし\nNormalization semantic/property proofなし\nPacket Safety Gate completeness/inheritance proofなし',
    'R1C full semantic equivalence proofなし / optional SAFETY_GATES structural round-trip Phase 3 first slice統合済み\nPacket strict bounded semantic/property Phase 4 first slice統合済み\nPacket full YAML/natural-language semantic equivalence proofなし\nNormalization full semantic/property/normalization-completion proofなし\nPacket arbitrary cross-document Safety Gate completeness/inheritance proofなし',
)
replace_once(
    'docs/project-status.md',
    'P0: required KDSL Validation check activation / issue #39\nP1: Phase 4 Packet / Normalization semantic-property proof\nP2: Phase 5 public-facing v2 hardening / release-readiness review',
    'P0: required KDSL Validation check activation / issue #39\nP1: Phase 5 public-facing v2 hardening / release-readiness review',
)

replace_once(
    'spec/manifest.md',
    'v2_branch_direction: CompactPrompt / Lexicon / CP-Lift / Safety Gate Registry / Safety Semantics / R1C architecture',
    'v2_branch_direction: CompactPrompt / Lexicon / CP-Lift / Safety Gate Registry / Safety Semantics / R1C / Packet semantic-property architecture',
)
replace_once(
    'spec/manifest.md',
    '| `spec/packet/kdsl-packet-normalization-contract.md` | Packet normalization draft | mapping/loss/round-trip evidence / non-executable preview | v2 draft adopted / non-executable |',
    '| `spec/packet/kdsl-packet-normalization-contract.md` | Packet normalization draft | mapping/loss/round-trip evidence / non-executable preview | v2 draft adopted / non-executable |\n| `spec/packet/kdsl-packet-semantic-property-contract.md` | Packet property subordinate draft | strict source semantics / selected source-preview property comparison | v2 draft adopted subordinate / non-executable |',
)
replace_once(
    'spec/manifest.md',
    '| `spec/lint/kdsl-packet-lint.md` | Lint draft | Packet envelope/registry/gate/authority/normalization lint | v2 draft adopted / validator first slice integrated |\n| `spec/lint/kdsl-packet-normalization-lint.md` | Lint draft | normalization source/target/map/loss/round-trip/authority lint | v2 draft adopted / validator not implemented |',
    '| `spec/lint/kdsl-packet-lint.md` | Lint draft | Packet envelope/registry/gate/authority/normalization lint | v2 draft adopted / Phase 4 strict first slice integrated |\n| `spec/lint/kdsl-packet-normalization-lint.md` | Lint draft | normalization source/target/map/loss/round-trip/authority lint | v2 draft adopted / Phase 4 selected property first slice integrated |',
)
replace_once(
    'spec/manifest.md',
    'lint:\n  spec/lint/kdsl-packet-lint.md\n```',
    'lint:\n  spec/lint/kdsl-packet-lint.md\n\nstrict semantic/property subordinate:\n  spec/packet/kdsl-packet-semantic-property-contract.md\n  model: kdsl-packet-property@0.1-draft\n```',
)
replace_once(
    'spec/manifest.md',
    'normalization artifact未生成/未検証→実行禁止\nunknown schema/registry/ID/opcode推測禁止',
    'normalization artifact未生成/未検証→実行禁止\nproperty_pass != semantic equivalence/safety proof/normalization completion/execution authority\nunknown schema/registry/ID/opcode推測禁止',
)
replace_once(
    'spec/manifest.md',
    'lint:\n  spec/lint/kdsl-packet-normalization-lint.md\n```',
    'lint:\n  spec/lint/kdsl-packet-normalization-lint.md\n\nstrict property contract:\n  spec/packet/kdsl-packet-semantic-property-contract.md\n```',
)
replace_once(
    'spec/manifest.md',
    'normalization validator/mapper未実装→normalized扱禁止',
    'normalization validator/mapper/property first slices integrated→なお normalized扱禁止',
)

replace_once(
    'spec/packet/kdsl-packet-schema.md',
    'normalization未完了→実行指示扱禁止\n```',
    'normalization未完了→実行指示扱禁止\nstrict property model: kdsl-packet-property@0.1-draft\nproperty_pass != semantic equivalence/safety proof/normalization completion/execution authority\n```',
)
phase4_schema_section = '''## 11.1 Phase 4 strict semantic/property surface

```text
contract: spec/packet/kdsl-packet-semantic-property-contract.md
model: kdsl-packet-property@0.1-draft
validator target: packet-semantic
strict mapper: non-executable preview only
property result: property_pass|blocked|fail
```

Selected checks:

```text
OBS classification
SG id/state/scope/reason/evidence/authority
bounded protected wording
FLOW×authority/blocked-state consistency
exact/protected/order preservation
section-scoped VERIFY/result-schema preservation
P1/P1L unresolved blocking
```

Boundary:

```text
property_pass != semantic equivalence
property_pass != complete safety proof
property_pass != normalization completion
property_pass != execution authority
```

'''
replace_once('spec/packet/kdsl-packet-schema.md', '## 12. Promotion gate', phase4_schema_section + '## 12. Promotion gate')
replace_once(
    'spec/packet/kdsl-packet-schema.md',
    'Packet lint implementation\nvalidator sample suite\nnormalization round-trip tests\nSafety Gate completeness tests\nAuthority non-substitution tests\nR1C output integration tests',
    'Packet/Normalization first-slice tooling review\nfull semantic-equivalence/safety-completeness review\ncanonical P1/P1L target schema before related generation\nexecutable transformer specification and independent authority review\nR1/R1C full semantic output integration review',
)

replace_once(
    'spec/packet/kdsl-packet-normalization-contract.md',
    '> normalization contract/lint v2-draft mapping\n> examples/tools\n> examples/tools',
    '> normalization contract/lint v2-draft mapping\n> semantic/property subordinate contract\n> examples/tools',
)
phase4_normalization_section = '''## 14.1 Phase 4 strict semantic/property comparison

```text
contract: spec/packet/kdsl-packet-semantic-property-contract.md
model: kdsl-packet-property@0.1-draft
strict mapper: tools/validator/kdsl_packet_normalize_semantic.py
property checker: tools/validator/kdsl_packet_property.py
```

Selected properties:

```text
source digest
all 17 MAP fields/mode policy
exact strings/protected wording/ordered fields
SG state/scope/reason/evidence/authority
FLOW/STOP/VERIFY section order
six authority rails
OUT result schema in report-format section
LOSS/UNRESOLVED consistency
```

```text
property_pass != semantic equivalence
property_pass != safety proof
property_pass != normalization completion
property_pass != execution authority
P1/P1L unresolved→blocked / preview禁止
```

'''
replace_once('spec/packet/kdsl-packet-normalization-contract.md', '## 15. Validity conditions', phase4_normalization_section + '## 15. Validity conditions')
replace_once(
    'spec/packet/kdsl-packet-normalization-contract.md',
    'normalization lint implementation\npositive/negative sample matrix\nFull KDSL structural mapper tests\nPacket reconstruction/round-trip tests\nexact-string/protected-wording property tests\nAuthority non-substitution tests',
    'first-slice lint/mapper/property review\nfull semantic-equivalence/safety-completeness review\nadditional target-profile property matrices\ncanonical P1/P1L target schema before related mapping\nexecutable transformer specification and independent authority review',
)

replace_once('spec/lint/kdsl-packet-lint.md', 'validator: not implemented', 'validator: Phase 4 strict first slice integrated')
replace_once(
    'spec/lint/kdsl-packet-lint.md',
    'Packet validator: not implemented\nsample runner coverage: not implemented\nPacket lint pass claim: prohibited until implementation/execution evidence',
    'Packet validator: first slice integrated\nPacket strict semantic validator: Phase 4 first slice integrated\nPacket semantic/property runner: 42 expectations / failed 0\nunified KDSL Validation: 257 expectations / failed 0\nPacket lint pass claim outside executed evidence: prohibited',
)
replace_once(
    'spec/lint/kdsl-packet-lint.md',
    'Packet parser/lint implementation\npositive/negative sample matrix\nnormalization round-trip tests\nSafety Gate inheritance/composition tests\nAuthority non-substitution tests\nR1C integration tests',
    'full YAML/natural-language semantic parser review\narbitrary cross-document Safety Gate completeness/inheritance review\nfull normalization semantic-equivalence review\ncanonical P1/P1L schema and executable transformer review\nR1/R1C full semantic integration review',
)

replace_once('spec/lint/kdsl-packet-normalization-lint.md', 'validator: first-slice integrated', 'validator: Phase 4 selected property first slice integrated')
replace_once(
    'spec/lint/kdsl-packet-normalization-lint.md',
    'normalization validator: first-slice integrated\nnormalization mapper: first-slice integrated / non-executable preview only\nround-trip property tests: first-slice integrated / selected structural properties only\nlint pass claim: prohibited until implementation/execution evidence',
    'normalization validator: first-slice integrated\nnormalization mapper: first-slice integrated / non-executable preview only\nstructural round-trip tests: first-slice integrated / selected structural properties only\nstrict semantic/property comparison: Phase 4 integrated / 42 expectations / failed 0\nunified KDSL Validation: 257 expectations / failed 0\nlint/property pass claim outside executed evidence: prohibited',
)
replace_once(
    'spec/lint/kdsl-packet-normalization-lint.md',
    'positive/negative normalization sample matrix\nsource digest tests\nFull KDSL mapping tests\nreconstruction/round-trip tests\nexact-string/protected-wording property tests\nAuthority non-substitution tests',
    'additional target-profile property matrices\nfull semantic-equivalence/safety-completeness review\ncanonical P1/P1L target schema before related mapping\nexecutable transformer specification and independent authority review',
)

replace_once('spec/packet/kdsl-packet-semantic-property-contract.md', 'status: implementation-candidate', 'status: v2-draft adopted subordinate')
replace_once(
    'spec/packet/kdsl-packet-semantic-property-contract.md',
    'contract: implementation-candidate\nvalidator: Phase 4 candidate\nproperty suite target: 42 expectations\nunified target: 257 expectations',
    'contract: v2-draft adopted subordinate\nvalidator: Phase 4 strict first slice integrated\nproperty suite: 42 expectations / failed 0\nunified suite: 257 expectations / failed 0\nimplementation PR: 48 / squash 47b15f9af3496dc36e14673cf0a681e3c333b098\nworkflow run: 29191890776 / #224 / success',
)

replace_once(
    'docs/reviews/kdsl-phase4-packet-normalization-property.md',
    'status: implementation-candidate\nreview_date: 2026-07-12\nbranch: agent/kdsl-phase4-packet-semantic-property\ntarget: main',
    'status: completed / merged\nreview_date: 2026-07-12\nbranch: agent/kdsl-phase4-packet-semantic-property\ntarget: main\npull_request: 48\nsource_head: ea982099bd5b99862191e0792e15cd501c4cc4f4\nsquash_commit: 47b15f9af3496dc36e14673cf0a681e3c333b098\nworkflow_run: 29191890776 / #224 / success\nunified_total: 257 / failed 0',
)
replace_once(
    'docs/reviews/kdsl-phase4-packet-normalization-property.md',
    'expected unified total: 257 / failed 0',
    'verified unified total: 257 / failed 0',
)

replace_once('tools/validator/kdsl-packet-semantic-property-implementation-notes.md', 'status: implementation-candidate', 'status: completed / main integrated')
replace_once(
    'tools/validator/kdsl-packet-semantic-property-implementation-notes.md',
    '## Candidate verification matrix\n\n```text\nexisting unified expectations: 215\nPhase 4 Packet semantic/property expectations: 42\ncandidate unified expectations: 257\n```',
    '## Verification matrix\n\n```text\nimplementation PR: 48\nsource head: ea982099bd5b99862191e0792e15cd501c4cc4f4\nsquash commit: 47b15f9af3496dc36e14673cf0a681e3c333b098\nworkflow run: 29191890776 / #224 / success\nexisting unified expectations: 215 / failed 0\nPhase 4 Packet semantic/property expectations: 42 / failed 0\nunified expectations: 257 / failed 0\n```',
)

replace_once(
    'tools/validator/README.md',
    'spec/packet/kdsl-packet-normalization-contract.md\nspec/r1/r1-result-spec.md',
    'spec/packet/kdsl-packet-normalization-contract.md\nspec/packet/kdsl-packet-semantic-property-contract.md\nspec/r1/r1-result-spec.md',
)
packet_tools = '''kdsl_packet_semantic.py:
  OBS explicit classification
  Safety Gate state/evidence/authority strict checks
  bounded protected-language checks
  FLOW×authority/blocked-state consistency
  VERIFY requirement/evidence separation

kdsl_packet_normalize_semantic.py:
  strict Packet semantic prerequisite
  non-executable preview generation
  full SG record / exact / protected / order / authority preservation evidence
  P1/P1L unresolved blocking

kdsl_packet_property.py:
  source digest and all-17-field MAP comparison
  exact/protected/order/property comparison
  section-scoped VERIFY/result-schema checks
  authority non-widening / LOSS/UNRESOLVED consistency

'''
replace_once('tools/validator/README.md', 'kdsl_packet_normalization.py:\n', packet_tools + 'kdsl_packet_normalization.py:\n')
replace_once(
    'tools/validator/README.md',
    'target wrapper: r1 / prompt / compact / safety-gate / safety-semantics / r1c / packet / normalization / all',
    'target wrapper: r1 / prompt / compact / safety-gate / safety-semantics / r1c / packet / packet-semantic / normalization / all',
)
replace_once(
    'tools/validator/README.md',
    'run_all_samples.py:\n  unified core/Safety Gate/R1C round-trip/parser/Safety Semantics runner',
    'run_all_samples.py:\n  unified core/Safety Gate/R1C/Packet semantic-property runner',
)
phase4_validator_record = '''Packet / Normalization semantic-property Phase 4 integrated:
  previous unified: 215 / failed: 0
  strict semantic/property suite: 42 / failed: 0
  unified total: 257 / failed: 0
  pull_request: 48
  workflow_run: 224 / success
  model: kdsl-packet-property@0.1-draft

'''
replace_once('tools/validator/README.md', 'Common parser / unified validation Phase 1 integrated:', phase4_validator_record + 'Common parser / unified validation Phase 1 integrated:')
replace_once(
    'tools/validator/README.md',
    'examples/packet/packet-design.example.md\nexamples/packet/normalization-full-kdsl.example.md',
    'examples/packet/packet-design.example.md\nexamples/packet/packet-semantic-property.example.md\nexamples/packet/normalization-full-kdsl.example.md',
)
replace_once(
    'tools/validator/README.md',
    'tools/validator/kdsl-r1c-optional-implementation-notes.md\n```',
    'tools/validator/kdsl-r1c-optional-implementation-notes.md\ndocs/reviews/kdsl-phase4-packet-normalization-property.md\ntools/validator/kdsl-packet-semantic-property-implementation-notes.md\n```',
)
replace_once(
    'tools/validator/README.md',
    'Packet envelope/registry/gate/flow/authority/normalization境界検出\nNormalization mapping/loss/authority/output境界検出',
    'Packet envelope/registry/gate/flow/authority/normalization境界検出\nPacket strict OBS/Safety Gate/FLOW/authority bounded semantic検出\nNormalization mapping/loss/authority/output境界検出\nsource Packet×preview selected property比較',
)
replace_once(
    'tools/validator/README.md',
    'Packet execution/normalization readinessを判定しない',
    'Packet semantic/property passをfull semantic-equivalence/safety/normalization-completion proofとして扱わない\nPacket execution/normalization readinessを判定しない',
)
