from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected exactly one match, got {count}: {old!r}')
    p.write_text(text.replace(old, new), encoding='utf-8')


# Specification lint status and implemented boundary.
replace_once(
    'spec/lint/kdsl-safety-gate-registry-lint.md',
    'status: v2-draft adopted / specification-only',
    'status: v2-draft adopted / first-slice implemented',
)
replace_once(
    'spec/lint/kdsl-safety-gate-registry-lint.md',
    'validator: not_implemented',
    'validator: first_slice_integrated',
)
replace_once(
    'spec/lint/kdsl-safety-gate-registry-lint.md',
    '''## 12. Validator boundary

```text
validator未実装→自動pass扱禁止
future validator pass != semantic equivalence
future validator pass != U承認
future validator pass != RT:v
future validator pass != release readiness
```''',
    '''## 12. Validator boundary

Implemented first slice:

```text
tools/validator/kdsl_safety_gate.py
  registry/ID/state/field/composition
  representative protected wording
  trigger-present na rejection
  aggregate state reporting

tools/validator/kdsl_safety_gate_inheritance.py
  parent hold/blocked preservation
  unsafe transition rejection
  parent na copied-reason warning
  satisfied scope-change warning
```

Remaining boundary:

```text
representative wording check != full semantic equivalence
pairwise parent/child check != complete inheritance graph proof
aggregate state report != execution permission
validator pass != semantic equivalence
validator pass != U承認
validator pass != RT:v
validator pass != execution authority
validator pass != release readiness
```''',
)

# Validator README scope, evidence, and commands.
replace_once(
    'tools/validator/README.md',
    '''kdsl_safety_gate.py:
  SAFETY_GATES block detection
  kdsl-sg@0.1-draft registry check
  known Safety Gate ID/state check
  id/state/scope/reason required field check
  satisfied evidence/authority check
  dev-prompt baseline gate check
  representative additive composition check

kdsl_r1c.py:''',
    '''kdsl_safety_gate.py:
  SAFETY_GATES block detection
  kdsl-sg@0.1-draft registry check
  known Safety Gate ID/state check
  id/state/scope/reason required field check
  satisfied evidence/authority check
  dev-prompt baseline gate check
  representative additive composition check
  representative protected wording check
  trigger-present state:na rejection
  aggregate state reporting

kdsl_safety_gate_inheritance.py:
  parent hold/blocked gate preservation
  blocked/hold unsafe transition check
  parent na re-evaluation warning
  satisfied scope-change warning

kdsl_r1c.py:''',
)
replace_once(
    'tools/validator/README.md',
    '''Packet normalization round-trip first slice integrated:
  total: 108 / failed: 0
  pull_request: 27
  workflow_run: 163 / success
```''',
    '''Packet normalization round-trip first slice integrated:
  total: 108 / failed: 0
  pull_request: 27
  workflow_run: 163 / success

Safety Gate protected-wording/inheritance first slice integrated:
  existing suite: 108 / failed: 0
  extension suite: 14 / failed: 0
  pull_request: 31
  workflow_run: 173 / success
```''',
)
replace_once(
    'tools/validator/README.md',
    '''  kdsl_safety_gate.py
  kdsl-safety-gate-implementation-notes.md
  kdsl_r1c.py''',
    '''  kdsl_safety_gate.py
  kdsl_safety_gate_inheritance.py
  run_safety_gate_samples.py
  kdsl-safety-gate-implementation-notes.md
  kdsl_r1c.py''',
)
replace_once(
    'tools/validator/README.md',
    '''representative composition:=rollback/data/public/runtime/KDSL-DP
```

Boundary:

```text
SAFETY_GATES blockなし→対象外pass/info
current Full KDSL protected wording検査→未実装
parent-child inheritance lint→未実装
aggregate state calculation→未実装
```''',
    '''representative composition:=rollback/data/public/runtime/KDSL-DP
representative protected wording:=baseline + design/runtime/authority/rollback/public/data/KDSL-DP/stop
trigger-present required gate state:na:=error
aggregate state:=blocked > hold > satisfied / na outside severity
parent-child inheritance:=pairwise first slice
```

Boundary:

```text
SAFETY_GATES blockなし→対象外pass/info
protected wording検査:=representative pattern heuristic
inheritance lint:=one parent/one child pair
multi-generation graph/full semantic scope analysis未実装
aggregate satisfied != execution authority
```''',
)
replace_once(
    'tools/validator/README.md',
    '''```text
python tools/validator/run_samples.py
```''',
    '''```text
python tools/validator/run_samples.py
python tools/validator/run_safety_gate_samples.py
```''',
)

# Operational status: integration record and current scope.
replace_once(
    'docs/project-status.md',
    '''### PR #6 — R1C compact-result design candidate''',
    '''### PR #31 — Safety Gate protected wording / inheritance first slice

```yaml
pull_request: 31
merge_status: merged
merge_method: squash
source_branch: agent/kdsl-safety-gate-inheritance
source_head: 34f2b80aec145821001b078cd2dfeb1ced1c64b5
squash_commit: a05e44395b70761e7e709531fcff4ba99f7bf11d
closeout_pull_request: 33
workflow_run_id: 29153870878
workflow_run_number: 173
job_id: 86547689872
workflow_conclusion: success
existing_sample_total: 108
existing_sample_failed: 0
extension_sample_total: 14
extension_sample_failed: 0
validator_authority: non_authoritative
execution_effect: none
stable_effect: none
```

### PR #6 — R1C compact-result design candidate''',
)
replace_once(
    'docs/project-status.md',
    '''Safety Gate validator first slice:=main統合済み
R1C design candidate:=main統合済み''',
    '''Safety Gate validator first slice:=main統合済み
Safety Gate protected wording/inheritance first slice:=main統合済み / 108+14 expectations verified
R1C design candidate:=main統合済み''',
)
replace_once(
    'docs/project-status.md',
    '''    - Safety Gate registry/ID/state/field/composition lint
    - R1C schema/field/order/JSON shape lint''',
    '''    - Safety Gate registry/ID/state/field/composition lint
    - Safety Gate representative protected wording/trigger-na/aggregate lint
    - Safety Gate pairwise parent-child inheritance lint
    - R1C schema/field/order/JSON shape lint''',
)
replace_once(
    'docs/project-status.md',
    '''    command: python tools/validator/run_samples.py
    expected_sample_total: 108
    latest_pr_validation:
      pull_request: 27
      run_id: 29151860435
      run_number: 163
      conclusion: success
      sample_total: 108
      sample_failed: 0''',
    '''    command: python tools/validator/run_samples.py
    extension_command: python tools/validator/run_safety_gate_samples.py
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
)
replace_once(
    'docs/project-status.md',
    '''protected wording semantic equivalence lint
Safety Gate parent-child inheritance lint
Safety Gate aggregate composite state calculation
full natural-language trigger context parser''',
    '''protected wording full semantic equivalence proof
Safety Gate multi-generation inheritance graph/deep scope semantics
full natural-language trigger context parser''',
)
replace_once(
    'docs/project-status.md',
    '''### R1C design regression''',
    '''### Safety Gate protected wording / inheritance first slice

```yaml
pull_request: 31
source_branch: agent/kdsl-safety-gate-inheritance
source_head: 34f2b80aec145821001b078cd2dfeb1ced1c64b5
squash_commit: a05e44395b70761e7e709531fcff4ba99f7bf11d
workflow_run_id: 29153870878
run_number: 173
job_id: 86547689872
conclusion: success
existing_sample_total: 108
existing_failed: 0
extension_sample_total: 14
extension_failed: 0
meaning: representative wording/pairwise inheritance evidence; not complete safety or authority proof
```

### R1C design regression''',
)
replace_once(
    'docs/project-status.md',
    '''tools/validator/verification/kdsl_safety_gate_verify.md
tools/validator/verification/kdsl_r1c_verify.md''',
    '''tools/validator/verification/kdsl_safety_gate_verify.md
docs/reviews/kdsl-safety-gate-protected-inheritance-first-slice.md
tools/validator/verification/kdsl_r1c_verify.md''',
)
replace_once(
    'docs/project-status.md',
    '''protected wording semantic equivalence lintなし
Safety Gate parent-child inheritance lintなし
Safety Gate aggregate state lintなし
R1C round-trip semantic proofなし''',
    '''protected wording full semantic equivalence proofなし
Safety Gate multi-generation inheritance graph/deep scope lintなし
R1C round-trip semantic proofなし''',
)
replace_once(
    'docs/project-status.md',
    '''P0: Safety Gate protected wording/inheritance validator拡張
P1: R1C round-trip/property-based validator検討
P2: public-facing v2 overview / CI required check検討''',
    '''P0: R1C round-trip/property-based validator検討
P1: public-facing v2 overview / CI required check検討
P2: Safety Gate multi-generation inheritance/property tests検討''',
)

# Completed review record.
Path('docs/reviews/kdsl-safety-gate-protected-inheritance-first-slice.md').write_text(
    '''# Safety Gate Protected Wording / Inheritance First Slice

status: completed / merged
review_date: 2026-07-11
pull_request: 31
source_branch: agent/kdsl-safety-gate-inheritance
source_head: 34f2b80aec145821001b078cd2dfeb1ced1c64b5
squash_commit: a05e44395b70761e7e709531fcff4ba99f7bf11d
closeout_pull_request: 33

## Scope

```text
tools/validator/kdsl_safety_gate.py
  representative protected wording
  trigger-present na rejection
  aggregate state reporting

tools/validator/kdsl_safety_gate_inheritance.py
  parent hold/blocked preservation
  unsafe transition rejection
  parent na copied-reason warning
  satisfied scope-change warning

tools/validator/run_safety_gate_samples.py
  14 extension expectations
```

## Verification

```text
workflow: Validator CI
workflow_run_id: 29153870878
run_number: 173
job_id: 86547689872
conclusion: success
existing suite: 108 / failed 0
extension suite: 14 / failed 0
```

## Safety boundary

```text
no gate auto-satisfaction
aggregate satisfied != execution permission
inheritance validation != authority grant
representative wording match != semantic equivalence
pairwise parent/child check != complete inheritance graph proof
validator pass != safety proof/RT:v/U approval/release readiness
```

## Non-actions

```text
Packet executable化なし
normalization completionなし
tag/release/Release Assets操作なし
stable/public-ready化なし
source branch削除なし
```
''',
    encoding='utf-8',
)

Path('.github/scripts/apply_safety_gate_inheritance_closeout.py').unlink()
