from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def replace_once(path, old, new):
    target = ROOT / path
    text = target.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected exactly one match, found {count}: {old[:100]!r}')
    target.write_text(text.replace(old, new, 1), encoding='utf-8')


def prepend_after(path, anchor, addition):
    replace_once(path, anchor, anchor + addition)


# R1C schema ownership/status.
replace_once(
    'spec/r1/r1c-compact-result-schema.md',
    'v2-draft serialization:\n  spec/r1/r1c-compact-result-schema.md\n',
    'v2-draft serialization:\n  spec/r1/r1c-compact-result-schema.md\n\nPhase 3 subordinate optional-block contract:\n  spec/r1/r1c-optional-block-contract.md\n',
)
replace_once(
    'spec/r1/r1c-compact-result-schema.md',
    'Optional blocks retain their canonical names. No alias is defined in this candidate.\n',
    'Optional blocks retain their canonical names. No alias is defined in this candidate.\n\nPhase 3 deep optional validation and round-trip rules are defined in `spec/r1/r1c-optional-block-contract.md`.\n',
)
replace_once(
    'spec/r1/r1c-compact-result-schema.md',
    'validator: first heuristic slice integrated\nstructural_round_trip: first slice integrated\noptional_safety_gates_round_trip: blocked\nsemantic_equivalence: not_proven',
    'validator: first heuristic slice integrated\ndeep_optional_validator: Phase 3 first slice integrated\nstructural_round_trip: Phase 3 optional-block first slice integrated\noptional_evidence_authority_round_trip: structural_pass first slice\noptional_safety_gates_round_trip: structural_pass first slice\nannunciator_round_trip: structural-only first slice\nsemantic_equivalence: not_proven',
)

# R1C lint status and implementation evidence.
replace_once(
    'spec/lint/kdsl-r1c-lint.md',
    'status: v2-draft adopted / first slices integrated',
    'status: v2-draft adopted / Phase 3 deep optional-block first slice integrated',
)
replace_once(
    'spec/lint/kdsl-r1c-lint.md',
    '## 19. Validator status\n',
    '''## 18.1 Phase 3 deep optional-block enforcement\n\n```text\nEVIDENCE:\n  exact observed/inferred/not_observed/unverified keys\n  cross-class duplicate/conflict detection\n  VERIFY.pass / RT:v contradiction detection\n\nAUTHORITY:\n  exact read/edit/stage/commit/push/release rails\n  FILES/CMD/COMMIT cross-field authority conflict detection\n  AUTHORITY record != authority grant\n\nANNUNCIATOR:\n  canonical-key structural validation only\n  full value-semantic consistency proofなし\n\nSAFETY_GATES:\n  registry/ID/state/record deep lint\n  ordered structural projection/reconstruction\n  valid optional block→structural_pass first slice\n```\n\n## 19. Validator status\n''',
)
replace_once(
    'spec/lint/kdsl-r1c-lint.md',
    'R1C structural round-trip helper: first slice integrated\nR1C round-trip property suite: 14 expectations / failed 0\noptional SAFETY_GATES round-trip: blocked',
    'R1C structural round-trip helper: Phase 3 optional-block first slice integrated\nR1C base round-trip property suite: 14 expectations / failed 0\nR1C deep optional-block suite: 34 expectations / failed 0\noptional EVIDENCE/AUTHORITY/ANNUNCIATOR round-trip: structural_pass first slice\noptional SAFETY_GATES round-trip: structural_pass first slice',
)
replace_once(
    'spec/lint/kdsl-r1c-lint.md',
    'multi-line optional JSON support\noptional SAFETY_GATES dedicated expansion\nfull semantic equivalence proof\nbroader property/mutation coverage',
    'multi-line optional JSON support: common parser/Phase 3 integrated\noptional SAFETY_GATES dedicated expansion: Phase 3 integrated\nfull Evidence/Authority natural-language semantic equivalence proof\nANNUNCIATOR full value-semantic consistency proof\nbroader property/mutation coverage',
)

# Manifest ownership.
replace_once(
    'spec/manifest.md',
    '| `spec/r1/r1c-compact-result-schema.md` | R1 serialization draft | canonical R1のcompact serialization profile | v2 draft adopted / canonical R1 subordinate |\n',
    '| `spec/r1/r1c-compact-result-schema.md` | R1 serialization draft | canonical R1のcompact serialization profile | v2 draft adopted / canonical R1 subordinate |\n| `spec/r1/r1c-optional-block-contract.md` | R1C subordinate contract draft | EVIDENCE/AUTHORITY/ANNUNCIATOR/SAFETY_GATES deep optional-block rules | v2 draft adopted / R1C subordinate |\n',
)
replace_once(
    'spec/manifest.md',
    'lint:\n  spec/lint/kdsl-r1c-lint.md\n\nschema/version:',
    'lint:\n  spec/lint/kdsl-r1c-lint.md\n\noptional-block contract:\n  spec/r1/r1c-optional-block-contract.md\n\nschema/version:',
)
replace_once(
    'spec/manifest.md',
    'R1C validator pass != canonical R1適合証明\n',
    'R1C validator pass != canonical R1適合証明\nPhase 3 optional-block structural_pass != semantic equivalence/safety proof/authority\n',
)

# Root README status/navigation/verification.
replace_once(
    'README.md',
    'R1C validator: first heuristic slice integrated\nR1C independent canonical/stable status: no',
    'R1C validator: first heuristic slice integrated\nR1C deep optional-block validator/round-trip: Phase 3 first slice integrated\nR1C independent canonical/stable status: no',
)
replace_once(
    'README.md',
    'KDSL Validation unified suite: 181 expectations / failed 0',
    'KDSL Validation unified suite: 215 expectations / failed 0',
)
replace_once(
    'README.md',
    '  spec/r1/r1c-compact-result-schema.md\n',
    '  spec/r1/r1c-compact-result-schema.md\n  spec/r1/r1c-optional-block-contract.md\n',
)
replace_once(
    'README.md',
    'python tools/validator/kdsl_validate.py --target r1c <file>\n',
    'python tools/validator/kdsl_validate.py --target r1c <file>\npython tools/validator/kdsl_r1c_roundtrip.py <file>\n',
)
replace_once(
    'README.md',
    '  run_safety_semantics_examples.py: 2\n',
    '  run_safety_semantics_examples.py: 2\n  run_r1c_optional_samples.py: 34\n',
)
replace_once(
    'README.md',
    'pull_request: 42\nsource_head: f11fe00da04f25ae5fe7855535b9634e645a901e\nsquash_commit: 66191b6b97bab720ffd14d5732aa6f5bc0d92a44\nworkflow/check: KDSL Validation\nworkflow_run: #200 / success\nunified expectations: 181',
    'pull_request: 45\nsource_head: 1fcd09cf13aaeb3aa54ed0194d443c962bbbd4b7\nsquash_commit: 24f08a4397f22555e73469099014b6ba502760c3\nworkflow/check: KDSL Validation\nworkflow_run: #207 / success\nunified expectations: 215',
)
replace_once(
    'README.md',
    'R1C round-trip semantic proofなし\n',
    'R1C deep optional-block structural round-trip:=Phase 3 integrated\nR1C round-trip full semantic proofなし\n',
)
replace_once(
    'README.md',
    'P1:\n  Phase 3 R1C deep optional-block round-trip / Evidence / Authority\n\nP2:\n  Phase 4 Packet / Normalization semantic-property proof',
    'P1:\n  Phase 4 Packet / Normalization semantic-property proof',
)

# Changelog Phase 3 entry.
prepend_after(
    'CHANGELOG.md',
    '### Added\n',
    '''\n#### Phase 3 R1C deep optional-block round-trip\n\n- Added `kdsl-r1c-optional-blocks@0.1-draft` subordinate contract.\n- Added exact EVIDENCE classification and cross-class contradiction checks.\n- Added six-rail AUTHORITY checks against FILES/CMD/COMMIT evidence.\n- Added ANNUNCIATOR structural preservation and dedicated SAFETY_GATES projection/reconstruction.\n- Promoted valid optional SAFETY_GATES from blocked to structural pass.\n- Expanded unified `KDSL Validation` from 181 to 215 expectations.\n\nVerification:\n\n```text\npull_request: 45\nsource_head: 1fcd09cf13aaeb3aa54ed0194d443c962bbbd4b7\nsquash_commit: 24f08a4397f22555e73469099014b6ba502760c3\nworkflow_run_id: 29185669224\nrun_number: 207\nunified_total: 215\nfailed: 0\n```\n\nBoundaries:\n\n```text\nSEMANTIC_EQUIVALENCE:not_proven\nFULL_SAFETY_PROOF:not_proven\nEXECUTION_AUTHORITY:none\n```\n''',
)

# Project status.
replace_once(
    'docs/project-status.md',
    '### PR #42 — Phase 2 Safety Semantics / multi-generation inheritance\n',
    '''### PR #45 — Phase 3 R1C deep optional-block round-trip\n\n```yaml\npull_request: 45\nmerge_status: merged\nmerge_method: squash\nsource_branch: agent/kdsl-phase3-r1c-deep-optional\nsource_head: 1fcd09cf13aaeb3aa54ed0194d443c962bbbd4b7\nsquash_commit: 24f08a4397f22555e73469099014b6ba502760c3\ncloseout_pull_request: 46\nmodel: kdsl-r1c-optional-blocks@0.1-draft\nworkflow: KDSL Validation\nworkflow_run_id: 29185669224\nworkflow_run_number: 207\nworkflow_conclusion: success\nprevious_unified_total: 181\nphase3_optional_total: 34\nunified_total: 215\nfailed: 0\nsemantic_equivalence: not_proven\nfull_safety_proof: not_proven\nexecution_authority: none\nstable_effect: none\n```\n\n### PR #42 — Phase 2 Safety Semantics / multi-generation inheritance\n''',
)
replace_once(
    'docs/project-status.md',
    'R1C structural round-trip first slice:=main統合済み / 14 expectations verified\n',
    'R1C structural round-trip first slice:=main統合済み / 14 expectations verified\nR1C deep optional-block Phase 3:=main統合済み / 34 optional expectations / 215 unified verified\n',
)
replace_once(
    'docs/project-status.md',
    '    - safety-semantics\n    - r1c\n',
    '    - safety-semantics\n    - r1c\n',
)
replace_once(
    'docs/project-status.md',
    '    - R1C structural projection/reconstruction property lint\n',
    '    - R1C structural projection/reconstruction property lint\n    - R1C EVIDENCE/AUTHORITY/ANNUNCIATOR/SAFETY_GATES deep optional lint\n',
)
replace_once(
    'docs/project-status.md',
    '      - python tools/validator/run_safety_semantics_examples.py\n    expected_unified_total: 181',
    '      - python tools/validator/run_safety_semantics_examples.py\n      - python tools/validator/run_r1c_optional_samples.py\n    expected_unified_total: 215',
)
replace_once(
    'docs/project-status.md',
    '      pull_request: 42\n      run_id: 29180355132\n      run_number: 200\n      conclusion: success\n      unified_total: 181',
    '      pull_request: 45\n      run_id: 29185669224\n      run_number: 207\n      conclusion: success\n      unified_total: 215',
)
replace_once(
    'docs/project-status.md',
    'R1C full semantic equivalence proof\nR1C optional SAFETY_GATES dedicated round-trip\nR1C optional EVIDENCE/AUTHORITY deep lint',
    'R1C optional-block structural/deep lint first slice integrated\nR1C full semantic equivalence proof\nR1C ANNUNCIATOR full value-semantic consistency proof',
)
replace_once(
    'docs/project-status.md',
    'P1: Phase 3 R1C deep optional-block round-trip / Evidence / Authority\nP2: Phase 4 Packet / Normalization semantic-property proof\nP3: Phase 5 public-facing v2 hardening / release-readiness review',
    'P1: Phase 4 Packet / Normalization semantic-property proof\nP2: Phase 5 public-facing v2 hardening / release-readiness review',
)

# Validator README.
replace_once(
    'tools/validator/README.md',
    'spec/r1/r1c-compact-result-schema.md\n',
    'spec/r1/r1c-compact-result-schema.md\nspec/r1/r1c-optional-block-contract.md\n',
)
replace_once(
    'tools/validator/README.md',
    'kdsl_r1c_roundtrip.py:\n',
    '''kdsl_r1c_optional.py:\n  EVIDENCE exact classification/cross-field lint\n  AUTHORITY rail vs FILES/CMD/COMMIT lint\n  ANNUNCIATOR structural lint\n  SAFETY_GATES deep record lint\n\nkdsl_r1c_roundtrip.py:\n''',
)
replace_once(
    'tools/validator/README.md',
    '  optional SAFETY_GATES safe block\n',
    '  optional EVIDENCE/AUTHORITY/ANNUNCIATOR/SAFETY_GATES structural preservation\n',
)
replace_once(
    'tools/validator/README.md',
    'Common parser / unified validation Phase 1 integrated:\n',
    '''R1C deep optional-block Phase 3 integrated:\n  previous unified: 181 / failed: 0\n  optional-block suite: 34 / failed: 0\n  unified total: 215 / failed: 0\n  pull_request: 45\n  workflow_run: 207 / success\n\nCommon parser / unified validation Phase 1 integrated:\n''',
)
replace_once(
    'tools/validator/README.md',
    'tools/validator/verification/kdsl_common_parser_verify.md\n',
    'tools/validator/verification/kdsl_common_parser_verify.md\ndocs/reviews/kdsl-phase3-r1c-deep-optional.md\ntools/validator/kdsl-r1c-optional-implementation-notes.md\n',
)

# Review and implementation notes.
replace_once(
    'docs/reviews/kdsl-phase3-r1c-deep-optional.md',
    'status: implementation-candidate',
    'status: completed / merged',
)
prepend_after(
    'docs/reviews/kdsl-phase3-r1c-deep-optional.md',
    'target: main\n',
    'pull_request: 45\nsource_head: 1fcd09cf13aaeb3aa54ed0194d443c962bbbd4b7\nsquash_commit: 24f08a4397f22555e73469099014b6ba502760c3\ncloseout_pull_request: 46\nworkflow_run: 29185669224 / #207 / success\nunified_total: 215 / failed 0\n',
)
replace_once(
    'tools/validator/kdsl-r1c-optional-implementation-notes.md',
    'status: implementation-candidate',
    'status: integrated / verified',
)
replace_once(
    'tools/validator/kdsl-r1c-optional-implementation-notes.md',
    'expected unified total: 215 / failed 0',
    'verified unified total: 215 / failed 0\npull_request: 45\nworkflow_run: 29185669224 / #207 / success',
)

# Remove the carrier after successful application.
Path(__file__).unlink()
print('Phase 3 closeout alignment applied')
