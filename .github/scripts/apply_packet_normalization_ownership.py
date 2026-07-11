from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected exactly one match, got {count}: {old!r}')
    p.write_text(text.replace(old, new), encoding='utf-8')


def replace_count(path: str, old: str, new: str, expected: int) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != expected:
        raise SystemExit(f'{path}: expected {expected} matches, got {count}: {old!r}')
    p.write_text(text.replace(old, new), encoding='utf-8')


# Contract and lint adoption headers.
replace_once(
    'spec/packet/kdsl-packet-normalization-contract.md',
    '# KDSL Packet Normalization Contract v0.1 Draft Candidate',
    '# KDSL Packet Normalization Contract v0.1 Draft',
)
replace_once(
    'spec/packet/kdsl-packet-normalization-contract.md',
    'status: design-candidate\ncanonical: no',
    'status: v2-draft adopted\ncanonical: v2-draft',
)
replace_once(
    'spec/packet/kdsl-packet-normalization-contract.md',
    'This candidate defines the evidence contract',
    'This v2-draft contract defines the evidence contract',
)
replace_once(
    'spec/packet/kdsl-packet-normalization-contract.md',
    'status: design-candidate\nNORMALIZATION_DRAFT:=non-executable evidence artifact',
    'status: v2-draft adopted\nNORMALIZATION_DRAFT:=non-executable evidence artifact',
)
replace_once(
    'spec/packet/kdsl-packet-normalization-contract.md',
    '> normalization contract candidate\n> normalization lint candidate',
    '> normalization contract/lint v2-draft mapping\n> examples/tools',
)
replace_once(
    'spec/packet/kdsl-packet-normalization-contract.md',
    'normalization candidate×canonical source→canonical source優先',
    'normalization contract×canonical source→canonical source優先',
)
replace_once(
    'spec/packet/kdsl-packet-normalization-contract.md',
    '## 5. Candidate record shape',
    '## 5. Record shape',
)
replace_once(
    'spec/packet/kdsl-packet-normalization-contract.md',
    'The example shape is illustrative. Candidate lint/tool implementation is a separate phase.',
    'This record shape is adopted for v2-draft authoring evidence. Validator/mapper implementation remains a separate phase.',
)
replace_once(
    'spec/packet/kdsl-packet-normalization-contract.md',
    'Allowed candidate kinds:',
    'Allowed target kinds:',
)
replace_once(
    'spec/packet/kdsl-packet-normalization-contract.md',
    'semantic_equivalence:not_proven固定 in v0.1 candidate',
    'semantic_equivalence:not_proven固定 in v0.1 draft',
)
replace_once(
    'spec/packet/kdsl-packet-normalization-contract.md',
    'Before adopted/tooling/executable promotion:',
    'Before validator/tooling/executable promotion:',
)

replace_once(
    'spec/lint/kdsl-packet-normalization-lint.md',
    '# KDSL Packet Normalization Lint v0.1 Draft Candidate',
    '# KDSL Packet Normalization Lint v0.1 Draft',
)
replace_once(
    'spec/lint/kdsl-packet-normalization-lint.md',
    'status: design-candidate\ncanonical: no',
    'status: v2-draft adopted\ncanonical: v2-draft',
)
replace_once(
    'spec/lint/kdsl-packet-normalization-lint.md',
    'This candidate defines structural and safety checks',
    'This v2-draft lint specification defines structural and safety checks',
)

# Packet index and design review status.
replace_once(
    'spec/packet/README.md',
    '## Normalization contract candidate',
    '## Adopted normalization contract',
)
replace_once(
    'spec/packet/README.md',
    'status: design-candidate\nexecutable: no\nvalidator/tool: not implemented',
    'status: v2-draft adopted\nexecutable: no\nvalidator/mapper: not implemented',
)
replace_once(
    'spec/packet/README.md',
    'The presence of a design candidate does not adopt it or authorize tooling, execution, stable promotion, tag/release operations, or Release Assets changes.',
    'The adopted v2-draft contract does not authorize tooling, normalization completion, execution, stable promotion, tag/release operations, or Release Assets changes.',
)

replace_once(
    'docs/reviews/kdsl-packet-normalization-design.md',
    'status: design-candidate\nreview_date: 2026-07-11\nbranch: agent/kdsl-packet-normalization-design\ntarget: main',
    'status: design-candidate integrated\nreview_date: 2026-07-11\nbranch: agent/kdsl-packet-normalization-design\ntarget: main\npull_request: 17\nsource_head: b11eac3b55853b240e850af5bc2f43bf5c7048b2\nsquash_commit: e27f130f64f0f0e9c3c6ac005adffc9476860f6f\nworkflow_run_id: 29149505919\nworkflow_run_number: 127\nworkflow_conclusion: success\nsample_total: 69\nsample_failed: 0',
)
replace_once(
    'docs/reviews/kdsl-packet-normalization-design.md',
    'status: design-candidate / non-executable',
    'status: v2-draft adopted candidate basis / non-executable',
)
replace_once(
    'docs/reviews/kdsl-packet-normalization-design.md',
    'P1: design candidate integration\nP2: manifest/Bridge/glossary ownership adoption review\nP3: normalization validator + structural mapper first slice',
    'P1: design candidate integration completed by PR #17\nP2: manifest/Bridge/glossary ownership adoption via PR #19\nP3: normalization validator + structural mapper first slice',
)
replace_once(
    'docs/reviews/kdsl-packet-normalization-design.md',
    'existing Validator CI regression: total 69 / failed 0',
    'Validator CI run #127: total 69 / failed 0',
)

# Manifest file map.
replace_once(
    'spec/manifest.md',
    '| `spec/packet/kdsl-packet-schema.md` | Packet authoring schema draft | PACKET_DRAFT fields / normalization / authority boundary | v2 draft adopted / non-executable |\n| `spec/r1/r1-result-spec.md` | R1 | KDSL_RESULT / RT / Evidence / Authority | Yes |',
    '| `spec/packet/kdsl-packet-schema.md` | Packet authoring schema draft | PACKET_DRAFT fields / normalization / authority boundary | v2 draft adopted / non-executable |\n| `spec/packet/kdsl-packet-normalization-contract.md` | Packet normalization draft | mapping/loss/round-trip evidence / non-executable preview | v2 draft adopted / non-executable |\n| `spec/r1/r1-result-spec.md` | R1 | KDSL_RESULT / RT / Evidence / Authority | Yes |',
)
replace_once(
    'spec/manifest.md',
    '| `spec/lint/kdsl-packet-lint.md` | Lint draft | Packet envelope/registry/gate/authority/normalization lint | v2 draft adopted / validator not implemented |\n| `spec/bridge/kdsl-adps-bridge.md` | Bridge | KDSL/KDSL-DP/ADPS/P1/P1L/R1境界 | Yes |',
    '| `spec/lint/kdsl-packet-lint.md` | Lint draft | Packet envelope/registry/gate/authority/normalization lint | v2 draft adopted / validator first slice integrated |\n| `spec/lint/kdsl-packet-normalization-lint.md` | Lint draft | normalization source/target/map/loss/round-trip/authority lint | v2 draft adopted / validator not implemented |\n| `spec/bridge/kdsl-adps-bridge.md` | Bridge | KDSL/KDSL-DP/ADPS/P1/P1L/R1境界 | Yes |',
)

replace_once(
    'spec/manifest.md',
    '### KDSL-CP\n',
    '''### Packet normalization contract

```text
v2-draft adopted contract:
  spec/packet/kdsl-packet-normalization-contract.md

schema/version:
  kdsl-packet-normalization@0.1-draft

lint:
  spec/lint/kdsl-packet-normalization-lint.md
```

Ownership rules:

```text
Core/Profile/R1/Bridge meaning > Packet schema > normalization contract/lint > Example/Tool
NORMALIZATION_DRAFT:=non-executable mapping/loss/round-trip evidence
KDSL_PROMPT_PREVIEW != KDSL_PROMPT
P1/P1L schema unresolved→TARGET blocked / preview禁止
semantic_equivalence:not_proven固定
AUTHORITY.execution_authority:none固定
normalization validator/mapper未実装→normalized扱禁止
```

### KDSL-CP
''',
)
replace_once(
    'spec/manifest.md',
    'schema/BASE/TASK/FLOW/lint:=v2-draft adopted\n  executable:=no\n  PKT:v1使用禁止\n  validator/normalization round-trip/stable dependency未充足→実行禁止',
    'schema/BASE/TASK/FLOW/lint:=v2-draft adopted\n  Packet validator:=first heuristic slice integrated\n  normalization contract/lint:=v2-draft adopted\n  normalization validator/mapper/round-trip proof:=not implemented\n  executable:=no\n  PKT:v1使用禁止\n  normalization/stable dependency未充足→実行禁止',
)
replace_once(
    'spec/manifest.md',
    'Packet authority/normalization非実行境界弱化→breaking/prohibited\nexample追加→patch候補',
    'Packet authority/normalization非実行境界弱化→breaking/prohibited\nnormalization schema/map/loss/round-trip意味変更→breaking候補\nP1/P1L unresolved→resolved変更→target schema adoption必須\nexample追加→patch候補',
)
replace_once(
    'spec/manifest.md',
    'Packet validator実装/期待結果\nnormalization round-trip証拠',
    'Packet validator実装/期待結果\nnormalization contract/lint ownership整合\nnormalization validator/mapper/round-trip証拠',
)
replace_once(
    'spec/manifest.md',
    'Packet lint:=v2-draft adopted / validator not implemented\nKDSL-Packet:=draft-non-executable / normalization required',
    'Packet lint:=v2-draft adopted / validator first slice integrated\nkdsl-packet-normalization@0.1-draft:=v2-draft adopted / non-executable\nnormalization lint:=v2-draft adopted / validator not implemented\nnormalization mapper/round-trip proof:=not implemented\nKDSL-Packet:=draft-non-executable / normalization required',
)

# Bridge alignment.
replace_once(
    'spec/bridge/kdsl-cp-packet-bridge.md',
    '# KDSL-CP / KDSL-Packet Bridge v0.5-draft',
    '# KDSL-CP / KDSL-Packet Bridge v0.6-draft',
)
replace_once(
    'spec/bridge/kdsl-cp-packet-bridge.md',
    'scope: CompactPrompt lift / Full KDSL boundary / Safety Gate Registry / R1C / Packet non-executable boundary',
    'scope: CompactPrompt lift / Full KDSL boundary / Safety Gate Registry / R1C / Packet normalization / non-executable boundary',
)
replace_once(
    'spec/bridge/kdsl-cp-packet-bridge.md',
    'This bridge defines when KDSL-CP must be lifted to Full KDSL, how the v2-draft Safety Gate Registry and R1C may be referenced, and why adopted KDSL-Packet authoring remains non-executable.',
    'This bridge defines when KDSL-CP must be lifted to Full KDSL, how Safety Gate/R1C/Packet normalization references are bounded, and why Packet authoring and normalization previews remain non-executable.',
)
replace_once(
    'spec/bridge/kdsl-cp-packet-bridge.md',
    'kdsl-r1c@0.1-draft:=canonical R1のv2-draft compact serialization profile\nKDSL-Packet:=v2-draft adopted authoring envelope / non-executable',
    'kdsl-r1c@0.1-draft:=canonical R1のv2-draft compact serialization profile\nkdsl-packet-normalization@0.1-draft:=Packet mapping/loss/round-trip evidence contract\nKDSL-Packet:=v2-draft adopted authoring envelope / non-executable',
)
replace_once(
    'spec/bridge/kdsl-cp-packet-bridge.md',
    'lint: spec/lint/kdsl-packet-lint.md\nvalidator: not implemented',
    'lint: spec/lint/kdsl-packet-lint.md\nvalidator: first heuristic slice integrated\nnormalization contract: spec/packet/kdsl-packet-normalization-contract.md\nnormalization lint: spec/lint/kdsl-packet-normalization-lint.md',
)
replace_once(
    'spec/bridge/kdsl-cp-packet-bridge.md',
    'Packet validator/sample matrix\nnormalization transformer and round-trip proof\nSafety Gate completeness/inheritance proof',
    'normalization validator/mapper and round-trip proof\nSafety Gate completeness/inheritance proof',
)
replace_once(
    'spec/bridge/kdsl-cp-packet-bridge.md',
    '## 8. Packet-Summary',
    '''## 8. Packet normalization alignment

Current v2-draft contract:

```text
schema: kdsl-packet-normalization@0.1-draft
source: spec/packet/kdsl-packet-normalization-contract.md
lint: spec/lint/kdsl-packet-normalization-lint.md
validator/mapper: not implemented
```

Required boundary:

```text
NORMALIZATION_DRAFT:=non-executable evidence artifact
STATUS:non-executable固定
TARGET.executable:false固定
AUTHORITY.execution_authority:none固定
semantic_equivalence:not_proven固定
KDSL_PROMPT_PREVIEW != KDSL_PROMPT
```

Target resolution:

```text
design-only→resolved review preview
full-kdsl-dev-prompt→resolved KDSL_PROMPT_PREVIEW
P1/P1L→blocked until canonical target field schema exists
unknown target schema推測禁止
```

Promotion boundary:

```text
contract/lint adoption != normalization completion
structural_pass != semantic equivalence/safety proof/authority
normalization validator/mapper未実装→Packet normalized扱禁止
executable target generation→separate specification/review/U承認必須
```

## 9. Packet-Summary''',
)
replace_once('spec/bridge/kdsl-cp-packet-bridge.md', '## 9. Summary restrictions', '## 10. Summary restrictions')
replace_once('spec/bridge/kdsl-cp-packet-bridge.md', '## 10. Boundary examples', '## 11. Boundary examples')
replace_once('spec/bridge/kdsl-cp-packet-bridge.md', '### 10.1 KDSL-CP is enough', '### 11.1 KDSL-CP is enough')
replace_once('spec/bridge/kdsl-cp-packet-bridge.md', '### 10.2 CP-Lift required', '### 11.2 CP-Lift required')
replace_once('spec/bridge/kdsl-cp-packet-bridge.md', '### 10.3 Packet design draft only', '### 11.3 Packet design draft only')
replace_once('spec/bridge/kdsl-cp-packet-bridge.md', '## 11. Non-goals', '## 12. Non-goals')
replace_once(
    'spec/bridge/kdsl-cp-packet-bridge.md',
    '未定義Packet直接実行\n```',
    '未定義Packet直接実行\nNORMALIZATION_DRAFT/KDSL_PROMPT_PREVIEW直接実行\nP1/P1L schema推測\n```',
)

# Glossary current Packet status and normalization terms.
replace_once(
    'spec/glossary-v2-draft.md',
    'validator: not implemented\nnormalization required: yes',
    'validator: first heuristic slice integrated\nnormalization required: yes\nnormalization contract: v2-draft adopted',
)
replace_once(
    'spec/glossary-v2-draft.md',
    '### Packet NORMALIZE\n',
    '''### NORMALIZATION_DRAFT

```text
NORMALIZATION_DRAFT:=Packet source→target mapping/loss/round-trip evidence artifact
schema: kdsl-packet-normalization@0.1-draft
```

Current status:

```text
v2-draft adopted
non-executable
validator/mapper: not implemented
```

Required boundary:

```text
STATUS:non-executable
TARGET.executable:false
semantic_equivalence:not_proven
AUTHORITY.execution_authority:none
```

### KDSL_PROMPT_PREVIEW

```text
KDSL_PROMPT_PREVIEW:=Full KDSL target mappingを確認する非実行preview marker
KDSL_PROMPT_PREVIEW != KDSL_PROMPT
```

It must not be passed directly to an AI coding tool as an implementation contract.

### Structural round-trip

```text
structural round-trip:=Packet required fields/order/exact stringsをtarget projectionから再構成して比較する検査
```

```text
structural_pass != semantic equivalence
structural_pass != safety proof
structural_pass != authority/normalization completion
```

### Normalization loss

```text
render_only:=表示差のみ候補
critical:=scope/safety/authority/order/exact string等の損失
```

Critical loss or blocked unresolved items prohibit target preview/execution.

### Packet NORMALIZE
''',
)

# README status/navigation/current boundary/next phase.
replace_once(
    'README.md',
    'Packet validator: first heuristic slice integrated\nvalidator sample suite: 69 expectations / failed 0',
    'Packet validator: first heuristic slice integrated\nPacket normalization contract: kdsl-packet-normalization@0.1-draft / v2-draft adopted / non-executable\nPacket normalization validator/mapper: not implemented\nvalidator sample suite: 69 expectations / failed 0',
)
replace_once(
    'README.md',
    'Packet:\n  spec/packet/kdsl-packet-schema.md',
    'Packet:\n  spec/packet/kdsl-packet-schema.md\n  spec/packet/kdsl-packet-normalization-contract.md',
)
replace_once(
    'README.md',
    '  spec/lint/kdsl-packet-lint.md',
    '  spec/lint/kdsl-packet-lint.md\n  spec/lint/kdsl-packet-normalization-lint.md',
)
replace_once(
    'README.md',
    'lint: spec/lint/kdsl-packet-lint.md\nstatus: non-executable',
    'lint: spec/lint/kdsl-packet-lint.md\nnormalization: kdsl-packet-normalization@0.1-draft\nnormalization lint: spec/lint/kdsl-packet-normalization-lint.md\nstatus: non-executable',
)
replace_once(
    'README.md',
    'Packet full YAML/semantic parser\nPacket normalization transformer/round-trip proof',
    'Packet full YAML/semantic parser\nPacket normalization validator/mapper/round-trip proof',
)
replace_once(
    'README.md',
    'P0:\n  PR #16 CI確認 / squash merge / Packet validator closeout\n\nP1:\n  Packet normalization round-trip tooling/tests',
    'P0:\n  PR #19 CI確認 / squash merge / normalization ownership closeout\n\nP1:\n  normalization validator/structural mapper first slice\n\nP2:\n  normalization round-trip/property tests',
)
replace_once(
    'README.md',
    'P2:\n  Safety Gate protected wording/inheritance validator拡張\n\nP3:\n  R1C round-trip/property-based validator検討\n\nP4:',
    'P3:\n  Safety Gate protected wording/inheritance validator拡張\n\nP4:\n  R1C round-trip/property-based validator検討\n\nP5:',
)

# Changelog design/adoption evidence and boundary.
replace_once(
    'CHANGELOG.md',
    '### Added\n\n#### Packet validator first slice',
    '''### Added

#### Packet normalization v2-draft ownership alignment

- Adopted `kdsl-packet-normalization@0.1-draft` as a non-executable mapping/loss/round-trip evidence contract.
- Adopted normalization lint requirements while keeping validator/mapper unimplemented.
- Kept `KDSL_PROMPT_PREVIEW` distinct from executable `KDSL_PROMPT:`.
- Kept P1/P1L targets blocked while canonical target field schemas are absent.
- Kept `semantic_equivalence:not_proven` and `execution_authority:none` mandatory.

#### Packet normalization contract design candidate

- Added normalization contract/lint candidates and exact source fixtures.
- Added Full KDSL preview, P1 blocked, and critical-loss blocked examples.
- PR #17 squash: `e27f130f64f0f0e9c3c6ac005adffc9476860f6f`.
- Validator CI run #127: existing 69 expectations / failed 0.
- Design integration did not generate executable targets or normalize Packet state.

#### Packet validator first slice''',
)
replace_once(
    'CHANGELOG.md',
    'Packet sample suite:=69 expectations / failed 0\nnormalization transformer/round-trip proof:=not implemented',
    'Packet sample suite:=69 expectations / failed 0\nnormalization contract/lint:=v2-draft adopted / non-executable\nnormalization validator/mapper/round-trip proof:=not implemented',
)

# Project status PR records and current state.
replace_once(
    'docs/project-status.md',
    '## 3. Current architecture direction',
    '''### PR #17 — Packet normalization contract design candidate

```yaml
pull_request: 17
merge_status: merged
merge_method: squash
source_branch: agent/kdsl-packet-normalization-design
source_head: b11eac3b55853b240e850af5bc2f43bf5c7048b2
squash_commit: e27f130f64f0f0e9c3c6ac005adffc9476860f6f
schema_id: kdsl-packet-normalization@0.1-draft
status: design_candidate_integrated
executable: no
workflow_run_id: 29149505919
workflow_run_number: 127
workflow_conclusion: success
sample_total: 69
sample_failed: 0
stable_effect: none
```

### PR #18 — Packet normalization ownership work branch

```yaml
pull_request: 18
merge_status: work_branch_pending_close
source_branch: agent/kdsl-packet-normalization-ownership-work
superseded_by: 19
execution_effect: none
stable_effect: none
```

### PR #19 — Packet normalization v2-draft ownership alignment

```yaml
pull_request: 19
merge_status: pending
source_branch: agent/kdsl-packet-normalization-ownership
schema_id: kdsl-packet-normalization@0.1-draft
target_status: v2_draft_adopted_non_executable
validator_mapper: not_implemented
execution_effect: none
stable_effect: none
```

## 3. Current architecture direction''',
)
replace_once(
    'docs/project-status.md',
    'Packet validator first slice:=main統合済み / 69 expectations verified\nKDSL-Packet:=non-executable / normalization required',
    'Packet validator first slice:=main統合済み / 69 expectations verified\nPacket normalization contract/lint:=v2-draft adopted / non-executable\nPacket normalization validator/mapper:=未実装\nKDSL-Packet:=non-executable / normalization required',
)
replace_once(
    'docs/project-status.md',
    '  validator: first_slice_integrated\n  normalize_required: true',
    '  validator: first_slice_integrated\n  normalization_schema: kdsl-packet-normalization@0.1-draft\n  normalization_status: v2_draft_adopted_non_executable\n  normalization_lint: adopted\n  normalization_validator_mapper: not_implemented\n  semantic_equivalence: not_proven\n  normalize_required: true',
)
replace_once(
    'docs/project-status.md',
    'Packet full YAML/semantic parser\nPacket Safety Gate state/evidence deep lint\nPacket normalization transformer/round-trip proof',
    'Packet full YAML/semantic parser\nPacket Safety Gate state/evidence deep lint\nNormalization validator/mapper未実装\nNormalization round-trip/property proofなし',
)
replace_once(
    'docs/project-status.md',
    '### Packet design candidate regression\n',
    '''### Packet normalization design regression

```yaml
pull_request: 17
source_head: b11eac3b55853b240e850af5bc2f43bf5c7048b2
squash_commit: e27f130f64f0f0e9c3c6ac005adffc9476860f6f
workflow_run_id: 29149505919
run_number: 127
conclusion: success
sample_total: 69
failed: 0
meaning: existing validator regression evidence; not normalization lint/mapper proof
```

### Packet design candidate regression
''',
)
replace_once(
    'docs/project-status.md',
    'Packet full YAML/semantic parserなし\nPacket normalization transformer/round-trip proofなし',
    'Packet full YAML/semantic parserなし\nNormalization validator/mapper未実装\nNormalization round-trip/property proofなし',
)
replace_once(
    'docs/project-status.md',
    '  Packet v2-draft adopted non-executable authoring schema\n  experimental heuristic validator helpers',
    '  Packet v2-draft adopted non-executable authoring schema\n  Packet normalization v2-draft non-executable evidence contract\n  experimental heuristic validator helpers',
)
replace_once(
    'docs/project-status.md',
    'P0: PR #16 CI確認 / squash merge / Packet validator closeout\nP1: Packet normalization round-trip tooling/tests\nP2: Safety Gate protected wording/inheritance validator拡張\nP3: R1C round-trip/property-based validator検討\nP4: public-facing v2 overview / CI required check検討',
    'P0: PR #19 CI確認 / squash merge / normalization ownership closeout\nP1: normalization validator/structural mapper first slice\nP2: normalization round-trip/property tests\nP3: Safety Gate protected wording/inheritance validator拡張\nP4: R1C round-trip/property-based validator検討\nP5: public-facing v2 overview / CI required check検討',
)

# Ownership review record.
Path('docs/reviews/kdsl-packet-normalization-ownership.md').write_text(
    '''# KDSL Packet Normalization Ownership Integration

status: merge-pending
review_date: 2026-07-11
work_pull_request: 18
pull_request: 19
target: main

## Adopted ownership

```text
Core/Profile/R1/Bridge canonical meaning
> Packet authoring schema/registries/lint
> normalization contract/lint v2-draft mapping
> examples/tools
```

```text
kdsl-packet-normalization@0.1-draft:=v2-draft adopted
NORMALIZATION_DRAFT:=non-executable evidence artifact
normalization validator/mapper:=not implemented
canonical/stable/executable:=no
```

## Target boundary

```text
design-only/full-kdsl-dev-prompt preview:=structurally resolvable
KDSL_PROMPT_PREVIEW != KDSL_PROMPT
P1/P1L:=blocked until canonical target schema exists
unknown target schema推測禁止
```

## Required safety boundary

```text
STATUS:non-executable
TARGET.executable:false
semantic_equivalence:not_proven
AUTHORITY.execution_authority:none
critical loss/unresolved→blocked
normalization validator/mapper未実装→normalized扱禁止
```

## Evidence

```text
PR #17 design source: b11eac3b55853b240e850af5bc2f43bf5c7048b2
PR #17 squash: e27f130f64f0f0e9c3c6ac005adffc9476860f6f
Validator CI run #127: success / 69 expectations / failed 0
normalization source digests fixed
P1/P1L blocked examples reviewed
```

## Non-actions

```text
KDSL_PROMPT executable生成なし
P1/P1L生成なし
Packet normalized化なし
semantic equivalence claimなし
authority付与なし
tag/release/Release Assets操作なし
stable/public-ready化なし
source branch削除なし
```
''',
    encoding='utf-8',
)

Path('.github/scripts/apply_packet_normalization_ownership.py').unlink()
