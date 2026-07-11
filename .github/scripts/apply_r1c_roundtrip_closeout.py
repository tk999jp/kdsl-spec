from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected exactly one match, got {count}: {old!r}')
    p.write_text(text.replace(old, new), encoding='utf-8')


# R1C schema ownership/current implementation status.
replace_once(
    'spec/r1/r1c-compact-result-schema.md',
    '# R1C Compact Result Schema v0.1 Draft Candidate',
    '# R1C Compact Result Schema v0.1 Draft',
)
replace_once(
    'spec/r1/r1c-compact-result-schema.md',
    'status: review-candidate\ncanonical: no',
    'status: v2-draft adopted\ncanonical: v2-draft subordinate',
)
replace_once(
    'spec/r1/r1c-compact-result-schema.md',
    'candidate serialization:\n  spec/r1/r1c-compact-result-schema.md',
    'v2-draft serialization:\n  spec/r1/r1c-compact-result-schema.md',
)
replace_once(
    'spec/r1/r1c-compact-result-schema.md',
    'canonical R1 > R1C candidate',
    'canonical R1 > R1C v2-draft serialization profile',
)
replace_once(
    'spec/r1/r1c-compact-result-schema.md',
    '''schema: kdsl-r1c@0.1-draft
status: review-candidate
canonical: no
validator: not implemented
main integration: no
stable/public-ready effect: none''',
    '''schema: kdsl-r1c@0.1-draft
status: v2-draft adopted
canonical: v2-draft subordinate to spec/r1/r1-result-spec.md
validator: first heuristic slice integrated
structural_round_trip: first slice integrated
optional_safety_gates_round_trip: blocked
semantic_equivalence: not_proven
main integration: yes
stable/public-ready effect: none''',
)

# R1C lint ownership and implemented boundary.
replace_once(
    'spec/lint/kdsl-r1c-lint.md',
    '# KDSL R1C Lint v0.1 Draft Candidate',
    '# KDSL R1C Lint v0.1 Draft',
)
replace_once(
    'spec/lint/kdsl-r1c-lint.md',
    'status: review-candidate\ncanonical: no',
    'status: v2-draft adopted / first slices integrated\ncanonical: v2-draft subordinate',
)
replace_once(
    'spec/lint/kdsl-r1c-lint.md',
    'source_candidate: spec/r1/r1c-compact-result-schema.md',
    'source: spec/r1/r1c-compact-result-schema.md',
)
replace_once(
    'spec/lint/kdsl-r1c-lint.md',
    '''## 19. Validator status

```text
R1C lint specification: review-candidate
R1C validator implementation: not implemented
validator未実装→pass扱禁止
existing CI pass != R1C lint pass
```

## 20. Required adoption checks

Before v2-draft adoption:

```text
U design approval
manifest/bridge/glossary/status alignment
success/blocked/needs_user examples
R1C validator first slice
sample runner integration
Full R1 fallback verification
Packet non-executable boundary confirmation
```''',
    '''## 19. Validator status

```text
R1C lint specification: v2-draft adopted
R1C validator: first heuristic slice integrated
R1C structural round-trip helper: first slice integrated
R1C round-trip property suite: 14 expectations / failed 0
optional SAFETY_GATES round-trip: blocked
```

Boundary:

```text
structural_pass != Full R1 semantic equivalence
structural_pass != safety proof
structural_pass != RT:v
structural_pass != execution authority
structural_pass != release readiness
```

## 20. Remaining adoption/expansion checks

```text
multi-line optional JSON support
optional SAFETY_GATES dedicated expansion
full semantic equivalence proof
broader property/mutation coverage
canonical R1 remains authoritative
Packet non-executable boundary confirmation
```''',
)

# Validator README implementation/evidence/commands.
replace_once(
    'tools/validator/README.md',
    '''kdsl_r1c.py:
  KDSL_RESULT + kdsl-r1c@0.1-draft detection
  Full R1 fallback/out-of-scope separation
  canonical required field presence/order
  short alias rejection
  JSON-compatible structured field lint
  VERIFY class separation
  RT state/basis heuristic lint
  NEXT proposal_only lint
  COMMIT actual/proposed/permission basis lint

kdsl_packet.py:''',
    '''kdsl_r1c.py:
  KDSL_RESULT + kdsl-r1c@0.1-draft detection
  Full R1 fallback/out-of-scope separation
  canonical required field presence/order
  short alias rejection
  JSON-compatible structured field lint
  VERIFY class separation
  RT state/basis heuristic lint
  NEXT proposal_only lint
  COMMIT actual/proposed/permission basis lint

kdsl_r1c_roundtrip.py:
  canonical Full R1 structural projection/reconstruction
  scalar/array/class/order preservation
  optional EVIDENCE/AUTHORITY/ANNUNCIATOR preservation
  optional SAFETY_GATES safe block
  no semantic-equivalence/authority claim

kdsl_packet.py:''',
)
replace_once(
    'tools/validator/README.md',
    '''Safety Gate protected-wording/inheritance first slice integrated:
  existing suite: 108 / failed: 0
  extension suite: 14 / failed: 0
  pull_request: 31
  workflow_run: 173 / success
```''',
    '''Safety Gate protected-wording/inheritance first slice integrated:
  existing suite: 108 / failed: 0
  extension suite: 14 / failed: 0
  pull_request: 31
  workflow_run: 173 / success

R1C structural round-trip first slice integrated:
  existing suite: 108 / failed: 0
  Safety Gate suite: 14 / failed: 0
  R1C round-trip suite: 14 / failed: 0
  pull_request: 34
  workflow_run: 179 / success
```''',
)
replace_once(
    'tools/validator/README.md',
    '''  kdsl_r1c.py
  kdsl-r1c-implementation-notes.md
  kdsl_packet.py''',
    '''  kdsl_r1c.py
  kdsl_r1c_roundtrip.py
  run_r1c_roundtrip_samples.py
  kdsl-r1c-implementation-notes.md
  kdsl-r1c-roundtrip-implementation-notes.md
  kdsl_packet.py''',
)
replace_once(
    'tools/validator/README.md',
    '''python tools/validator/run_samples.py
python tools/validator/run_safety_gate_samples.py''',
    '''python tools/validator/run_samples.py
python tools/validator/run_safety_gate_samples.py
python tools/validator/run_r1c_roundtrip_samples.py''',
)

# Operational status and evidence.
replace_once(
    'docs/project-status.md',
    '''### PR #10 — Packet registry and schema design candidate''',
    '''### PR #34 — R1C structural round-trip first slice

```yaml
pull_request: 34
merge_status: merged
merge_method: squash
source_branch: agent/kdsl-r1c-roundtrip
source_head: 844a9f68306ffbb8ddfb539e3aba7a38d9cc6185
squash_commit: ccc4c976274a42c45dd8109680d08ddd56341e82
closeout_pull_request: 36
workflow_run_id: 29154476912
workflow_run_number: 179
job_id: 86549240768
workflow_conclusion: success
existing_sample_total: 108
existing_sample_failed: 0
safety_gate_extension_total: 14
safety_gate_extension_failed: 0
round_trip_sample_total: 14
round_trip_sample_failed: 0
status_model: structural_pass|blocked|fail
semantic_equivalence: not_proven
execution_authority: none
stable_effect: none
```

### PR #10 — Packet registry and schema design candidate''',
)
replace_once(
    'docs/project-status.md',
    '''R1C design-candidate validator first slice:=main統合済み
R1C ownership:=v2-draft adopted serialization profile''',
    '''R1C design-candidate validator first slice:=main統合済み
R1C structural round-trip first slice:=main統合済み / 14 expectations verified
R1C ownership:=v2-draft adopted serialization profile''',
)
replace_once(
    'docs/project-status.md',
    '''  validator: first heuristic slice integrated
  manifest_bridge_glossary_alignment: integrated by PR #8''',
    '''  validator: first heuristic slice integrated
  structural_round_trip: first_slice_integrated
  optional_safety_gates_round_trip: blocked
  semantic_equivalence: not_proven
  manifest_bridge_glossary_alignment: integrated by PR #8''',
)
replace_once(
    'docs/project-status.md',
    '''    - R1C RT/NEXT/COMMIT boundary lint
    - Full R1 fallback/out-of-scope separation''',
    '''    - R1C RT/NEXT/COMMIT boundary lint
    - R1C structural projection/reconstruction property lint
    - Full R1 fallback/out-of-scope separation''',
)
replace_once(
    'docs/project-status.md',
    '''    extension_command: python tools/validator/run_safety_gate_samples.py
    expected_sample_total: 108
    expected_safety_gate_extension_total: 14
    latest_pr_validation:
      pull_request: 31
      run_id: 29153870878
      run_number: 173
      conclusion: success
      sample_total: 108
      sample_failed: 0
      safety_gate_extension_total: 14
      safety_gate_extension_failed: 0''',
    '''    extension_command: python tools/validator/run_safety_gate_samples.py
    r1c_round_trip_command: python tools/validator/run_r1c_roundtrip_samples.py
    expected_sample_total: 108
    expected_safety_gate_extension_total: 14
    expected_r1c_round_trip_total: 14
    latest_pr_validation:
      pull_request: 34
      run_id: 29154476912
      run_number: 179
      conclusion: success
      sample_total: 108
      sample_failed: 0
      safety_gate_extension_total: 14
      safety_gate_extension_failed: 0
      r1c_round_trip_total: 14
      r1c_round_trip_failed: 0''',
)
replace_once(
    'docs/project-status.md',
    '''R1C multi-line JSON parsing
R1C round-trip semantic proof
R1C optional EVIDENCE/AUTHORITY deep lint''',
    '''R1C multi-line JSON parsing
R1C full semantic equivalence proof
R1C optional SAFETY_GATES dedicated round-trip
R1C optional EVIDENCE/AUTHORITY deep lint''',
)
replace_once(
    'docs/project-status.md',
    '''### Packet normalization structural round-trip first slice''',
    '''### R1C structural round-trip first slice

```yaml
pull_request: 34
source_branch: agent/kdsl-r1c-roundtrip
source_head: 844a9f68306ffbb8ddfb539e3aba7a38d9cc6185
squash_commit: ccc4c976274a42c45dd8109680d08ddd56341e82
workflow_run_id: 29154476912
run_number: 179
job_id: 86549240768
conclusion: success
existing_sample_total: 108
existing_failed: 0
safety_gate_extension_total: 14
safety_gate_extension_failed: 0
round_trip_sample_total: 14
round_trip_failed: 0
optional_safety_gates: blocked
meaning: selected structural properties only; not Full R1 semantic/safety/authority proof
```

### Packet normalization structural round-trip first slice''',
)
replace_once(
    'docs/project-status.md',
    '''docs/reviews/kdsl-r1c-validator-first-slice.md
```''',
    '''docs/reviews/kdsl-r1c-validator-first-slice.md
docs/reviews/kdsl-r1c-roundtrip-first-slice.md
```''',
)
replace_once(
    'docs/project-status.md',
    'R1C round-trip semantic proofなし',
    'R1C full semantic equivalence proofなし / optional SAFETY_GATES round-trip blocked',
)
replace_once(
    'docs/project-status.md',
    '''P0: R1C round-trip/property-based validator検討
P1: public-facing v2 overview / CI required check検討
P2: Safety Gate multi-generation inheritance/property tests検討''',
    '''P0: public-facing v2 overview / CI required check検討
P1: Safety Gate multi-generation inheritance/property tests検討
P2: R1C optional SAFETY_GATES dedicated round-trip検討''',
)

# Completed review record.
Path('docs/reviews/kdsl-r1c-roundtrip-first-slice.md').write_text(
    '''# R1C Structural Round-Trip First Slice

status: completed / merged
review_date: 2026-07-11
pull_request: 34
source_branch: agent/kdsl-r1c-roundtrip
source_head: 844a9f68306ffbb8ddfb539e3aba7a38d9cc6185
squash_commit: ccc4c976274a42c45dd8109680d08ddd56341e82
closeout_pull_request: 36

## Scope

```text
tools/validator/kdsl_r1c_roundtrip.py
tools/validator/run_r1c_roundtrip_samples.py
required field order/scalar/array/class preservation
RT/NEXT/COMMIT boundary preservation
optional EVIDENCE/AUTHORITY/ANNUNCIATOR preservation
representative property mutations
```

## Status model

```text
structural_pass:=selected structure reconstructs exactly
blocked:=optional SAFETY_GATES requires dedicated safe expansion
fail:=source lint failure or structural mismatch
```

## Verification

```text
workflow: Validator CI
workflow_run_id: 29154476912
run_number: 179
job_id: 86549240768
conclusion: success
existing suite: 108 / failed 0
Safety Gate suite: 14 / failed 0
R1C round-trip suite: 14 / failed 0
```

## Safety boundary

```text
R1C_STRUCTURAL_ROUND_TRIP_RESULT != KDSL_RESULT
EXECUTABLE:no
SEMANTIC_EQUIVALENCE:not_proven
EXECUTION_AUTHORITY:none
structural_pass != canonical Full R1 semantic proof
structural_pass != safety proof/RT:v/U approval/release readiness
```

## Non-actions

```text
canonical R1 replacementなし
Packet executable化なし
tag/release/Release Assets操作なし
stable/public-ready化なし
source branch削除なし
```
''',
    encoding='utf-8',
)

Path('.github/scripts/apply_r1c_roundtrip_closeout.py').unlink()
