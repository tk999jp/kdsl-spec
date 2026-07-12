from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected exactly one match, got {count}: {old!r}')
    p.write_text(text.replace(old, new), encoding='utf-8')


# Adopt the bounded semantics model as a v2-draft subordinate registry specification.
replace_once(
    'spec/registry/kdsl-safety-semantics.md',
    '# KDSL Safety Gate Bounded Semantics v0.1 Draft Candidate',
    '# KDSL Safety Gate Bounded Semantics v0.1 Draft',
)
replace_once(
    'spec/registry/kdsl-safety-semantics.md',
    'status: design-candidate\ncanonical: no',
    'status: v2-draft adopted\ncanonical: v2-draft subordinate',
)
replace_once(
    'spec/registry/kdsl-safety-semantics.md',
    'This candidate defines a bounded semantic intermediate representation',
    'This v2-draft subordinate specification defines a bounded semantic intermediate representation',
)
replace_once(
    'spec/registry/kdsl-safety-semantics.md',
    'Before v2-draft adoption:',
    'Before broader semantic/proof promotion:',
)
replace_once(
    'spec/registry/kdsl-safety-semantics.md',
    'registry/composition/lint ownership alignment\nknown limitation disclosure\nclean PR + squash merge + closeout',
    'registry/composition/lint ownership alignment completed\nknown limitation disclosure maintained\nfull semantic/proof promotion requires separate review/U approval',
)

# Manifest ownership/file map.
replace_once(
    'spec/manifest.md',
    '| `spec/registry/kdsl-safety-gate-composition.md` | Registry draft | additive multi-gate composition | v2 draft adopted |\n| `spec/registry/kdsl-packet-base-registry.md`',
    '| `spec/registry/kdsl-safety-gate-composition.md` | Registry draft | additive multi-gate composition | v2 draft adopted |\n| `spec/registry/kdsl-safety-semantics.md` | Registry semantic draft | bounded protected-language IR / deep scope / multi-generation inheritance | v2 draft adopted subordinate |\n| `spec/registry/kdsl-packet-base-registry.md`',
)
replace_once(
    'spec/manifest.md',
    'composition:\n  spec/registry/kdsl-safety-gate-composition.md\n\nlint:',
    'composition:\n  spec/registry/kdsl-safety-gate-composition.md\n\nbounded semantics:\n  spec/registry/kdsl-safety-semantics.md\n  model: kdsl-safety-language@0.1-draft\n\nlint:',
)
replace_once(
    'spec/manifest.md',
    'current Full KDSL:=SG ID + complete protected wording\n```',
    'current Full KDSL:=SG ID + complete protected wording\nbounded semantic match != full semantic equivalence\nmulti-generation graph pass != complete safety proof\nscope relation pass != execution authority\n```',
)
replace_once(
    'spec/manifest.md',
    'v2_branch_direction: CompactPrompt / Lexicon / CP-Lift / Safety Gate Registry / R1C architecture',
    'v2_branch_direction: CompactPrompt / Lexicon / CP-Lift / Safety Gate Registry / Safety Semantics / R1C architecture',
)

# Registry index.
replace_once(
    'spec/registry/README.md',
    'kdsl-sg@0.1-draft\n  spec/registry/kdsl-safety-gate-registry.md\n  spec/registry/kdsl-safety-gate-composition.md',
    'kdsl-sg@0.1-draft\n  spec/registry/kdsl-safety-gate-registry.md\n  spec/registry/kdsl-safety-gate-composition.md\n  spec/registry/kdsl-safety-semantics.md\n  bounded model: kdsl-safety-language@0.1-draft',
)
replace_once(
    'spec/registry/README.md',
    'Safety Gate validator:=first heuristic slice integrated\nkdsl-r1c@0.1-draft',
    'Safety Gate validator:=first heuristic slice integrated\nSafety Semantics/multi-generation graph:=Phase 2 integrated / bounded / non-authoritative\nkdsl-r1c@0.1-draft',
)
replace_once(
    'spec/registry/README.md',
    'specialized gate != broader gate解除\n```',
    'specialized gate != broader gate解除\nbounded semantic match != full semantic equivalence\ngraph validation != execution authority\n```',
)

# Registry and composition alignment.
replace_once(
    'spec/registry/kdsl-safety-gate-registry.md',
    '## 6. Registry entries',
    '''## 5.1 Bounded semantic and graph alignment

```text
model: kdsl-safety-language@0.1-draft
source: spec/registry/kdsl-safety-semantics.md
```

```text
protected concepts:=declared strong/weak wording groups
condition/exception detection:=bounded only
scope relations:=equal|narrowed|widened|overlap|disjoint|unknown
multi-generation inheritance:=acyclic node/edge graph
multi-parent state precedence:=blocked > hold > satisfied
```

```text
bounded semantic pass != full semantic equivalence
inheritance graph pass != complete safety proof
scope relation pass != execution authority
```

## 6. Registry entries''',
)
replace_once(
    'spec/registry/kdsl-safety-gate-composition.md',
    '## 8. Packet boundary',
    '''## 8. Bounded semantic / graph boundary

```text
model: kdsl-safety-language@0.1-draft
bounded concept match != complete natural-language understanding
multi-generation graph validates declared inheritance edges only
widened/overlap/disjoint satisfied scope→explicit re-evaluation required
aggregate satisfied != execution permission
```

## 9. Packet boundary''',
)

# Lint ownership and implemented scope.
replace_once(
    'spec/lint/kdsl-safety-gate-registry-lint.md',
    'status: v2-draft adopted / first-slice implemented',
    'status: v2-draft adopted / Phase 2 bounded-semantics first slice implemented',
)
replace_once(
    'spec/lint/kdsl-safety-gate-registry-lint.md',
    '''tools/validator/kdsl_safety_gate_inheritance.py
  parent hold/blocked preservation
  unsafe transition rejection
  parent na copied-reason warning
  satisfied scope-change warning
```''',
    '''tools/validator/kdsl_safety_gate_inheritance.py
  parent hold/blocked preservation
  unsafe transition rejection
  parent na copied-reason warning
  pairwise deep-scope relation warning compatibility

tools/validator/kdsl_safety_semantics.py
  declared protected-concept strong/weak pattern checks
  bounded condition/exception atom capture
  explicit semantic weakening detection

tools/validator/kdsl_safety_gate_graph.py
  multi-generation DAG/cycle/node validation
  multi-parent aggregate precedence
  hold/blocked descendant preservation
  strict deep-scope re-evaluation enforcement
```''',
)
replace_once(
    'spec/lint/kdsl-safety-gate-registry-lint.md',
    '''representative wording check != full semantic equivalence
pairwise parent/child check != complete inheritance graph proof
aggregate state report != execution permission''',
    '''bounded wording model != full semantic equivalence
multi-generation DAG check != arbitrary workflow graph proof
normalized exact-item scope relation != full scope semantics
aggregate state report != execution permission''',
)

# Implementation/review records.
replace_once(
    'tools/validator/kdsl-safety-semantics-implementation-notes.md',
    'status: implementation-candidate',
    'status: first-slice integrated',
)
replace_once(
    'tools/validator/kdsl-safety-semantics-implementation-notes.md',
    '## Boundaries\n',
    '''## Integration evidence

```text
pull_request: 42
source_head: f11fe00da04f25ae5fe7855535b9634e645a901e
squash_commit: 66191b6b97bab720ffd14d5732aa6f5bc0d92a44
workflow_run_id: 29180355132
run_number: 200
unified_total: 181
failed: 0
```

## Boundaries
''',
)
replace_once(
    'docs/reviews/kdsl-phase2-safety-semantics.md',
    'status: implementation-candidate / verified\nreview_date: 2026-07-12\nbranch: agent/kdsl-phase2-safety-semantics\ntarget: main\npull_request: 42',
    'status: completed / merged\nreview_date: 2026-07-12\nbranch: agent/kdsl-phase2-safety-semantics\ntarget: main\npull_request: 42\nsource_head: f11fe00da04f25ae5fe7855535b9634e645a901e\nsquash_commit: 66191b6b97bab720ffd14d5732aa6f5bc0d92a44\ncloseout_work_pull_request: 43\ncloseout_pull_request: 44',
)

# Root README status/navigation/examples/CI/limitations/next phase.
replace_once(
    'README.md',
    'Safety Gate validator: first heuristic slice integrated\nR1C:',
    'Safety Gate validator: first heuristic slice integrated\nSafety Semantics: kdsl-safety-language@0.1-draft / Phase 2 bounded first slice integrated\nSafety Gate multi-generation graph/deep-scope first slice: integrated\nR1C:',
)
replace_once(
    'README.md',
    'KDSL Validation unified suite: 147 expectations / failed 0',
    'KDSL Validation unified suite: 181 expectations / failed 0',
)
replace_once(
    'README.md',
    'spec/registry/kdsl-safety-gate-composition.md\n  spec/registry/kdsl-packet-base-registry.md',
    'spec/registry/kdsl-safety-gate-composition.md\n  spec/registry/kdsl-safety-semantics.md\n  spec/registry/kdsl-packet-base-registry.md',
)
replace_once(
    'README.md',
    'SG ID-only compression禁止\n```',
    'SG ID-only compression禁止\nbounded semantic match != full semantic equivalence\nmulti-generation graph pass != complete safety proof\n```',
)
replace_once(
    'README.md',
    'python tools/validator/kdsl_validate.py --target safety-gate <file>\npython tools/validator/kdsl_validate.py --target r1c <file>',
    'python tools/validator/kdsl_validate.py --target safety-gate <file>\npython tools/validator/kdsl_validate.py --target safety-semantics <file>\npython tools/validator/kdsl_safety_gate_graph.py <graph.json>\npython tools/validator/kdsl_validate.py --target r1c <file>',
)
replace_once(
    'README.md',
    'run_parser_samples.py: 11\n```',
    'run_parser_samples.py: 11\n  run_safety_semantics_samples.py: 32\n  run_safety_semantics_examples.py: 2\n```',
)
replace_once(
    'README.md',
    '''pull_request: 38
source_head: 9fe8912b39e5df1b31b85e3302dfda35351f25c0
squash_commit: 701c1c6901bdf471ce979513da6dd2f215fd3b58
workflow/check: KDSL Validation
workflow_run: #192 / success
unified expectations: 147
failed: 0''',
    '''pull_request: 42
source_head: f11fe00da04f25ae5fe7855535b9634e645a901e
squash_commit: 66191b6b97bab720ffd14d5732aa6f5bc0d92a44
workflow/check: KDSL Validation
workflow_run: #200 / success
unified expectations: 181
failed: 0''',
)
replace_once(
    'README.md',
    'examples/safety-gates/dev-prompt-safety-gates.example.md\nexamples/r1c/',
    'examples/safety-gates/dev-prompt-safety-gates.example.md\nexamples/safety-gates/bounded-semantics.example.md\nexamples/safety-gates/multigeneration/graph.json\nexamples/r1c/',
)
replace_once(
    'README.md',
    '''full natural-language semantic parserなし
full negation parserなし
protected wording semantic equivalence lintなし
Safety Gate pairwise inheritance/aggregate:=integrated; multi-generation/deep scope未実装''',
    '''bounded Safety Semantics first slice:=main integrated
full natural-language semantic parserなし
full negation/exception reasoningなし
protected wording full semantic equivalence proofなし
Safety Gate multi-generation DAG/deep-scope first slice:=integrated; arbitrary graph/full scope proof未実装''',
)
replace_once(
    'README.md',
    '''P1:
  Phase 2 Safety Semantics / multi-generation inheritance / bounded protected-language model

P2:
  Phase 3 R1C deep optional-block round-trip / Evidence / Authority

P3:
  Phase 4 Packet / Normalization semantic-property proof

P4:
  Phase 5 public-facing v2 hardening / release-readiness review''',
    '''P1:
  Phase 3 R1C deep optional-block round-trip / Evidence / Authority

P2:
  Phase 4 Packet / Normalization semantic-property proof

P3:
  Phase 5 public-facing v2 hardening / release-readiness review''',
)

# Validator README current scope and evidence.
replace_once(
    'tools/validator/README.md',
    'spec/registry/kdsl-safety-gate-composition.md\nspec/registry/kdsl-packet-base-registry.md',
    'spec/registry/kdsl-safety-gate-composition.md\nspec/registry/kdsl-safety-semantics.md\nspec/registry/kdsl-packet-base-registry.md',
)
replace_once(
    'tools/validator/README.md',
    '''kdsl_safety_gate_inheritance.py:
  parent hold/blocked gate preservation
  blocked/hold unsafe transition check
  parent na re-evaluation warning
  satisfied scope-change warning

kdsl_r1c.py:''',
    '''kdsl_safety_gate_inheritance.py:
  parent hold/blocked gate preservation
  blocked/hold unsafe transition check
  parent na re-evaluation warning
  pairwise deep-scope warning compatibility

kdsl_safety_semantics.py:
  bounded protected-concept strong/weak wording checks
  condition/exception atom capture
  explicit semantic weakening detection

kdsl_safety_gate_graph.py:
  multi-generation DAG/cycle/node validation
  multi-parent aggregate precedence
  strict deep-scope re-evaluation enforcement

kdsl_r1c.py:''',
)
replace_once(
    'tools/validator/README.md',
    'target wrapper: r1 / prompt / compact / safety-gate / r1c / packet / normalization / all',
    'target wrapper: r1 / prompt / compact / safety-gate / safety-semantics / r1c / packet / normalization / all',
)
replace_once(
    'tools/validator/README.md',
    'unified core/Safety Gate/R1C round-trip/parser runner',
    'unified core/Safety Gate/R1C round-trip/parser/Safety Semantics runner',
)
replace_once(
    'tools/validator/README.md',
    '''Common parser / unified validation Phase 1 integrated:
  core suite: 108 / failed: 0
  Safety Gate suite: 14 / failed: 0
  R1C round-trip suite: 14 / failed: 0
  parser/adapter suite: 11 / failed: 0
  unified total: 147 / failed: 0
  pull_request: 38
  workflow_run: 192 / success
  required-check activation: pending / issue #39''',
    '''Common parser / unified validation Phase 1 integrated:
  core suite: 108 / failed: 0
  Safety Gate suite: 14 / failed: 0
  R1C round-trip suite: 14 / failed: 0
  parser/adapter suite: 11 / failed: 0
  unified total: 147 / failed: 0
  pull_request: 38
  workflow_run: 192 / success

Safety Semantics / multi-generation inheritance Phase 2 integrated:
  existing Phase 1 suite: 147 / failed: 0
  bounded semantic/graph properties: 32 / failed: 0
  repository examples: 2 / failed: 0
  unified total: 181 / failed: 0
  pull_request: 42
  workflow_run: 200 / success
  required-check activation: pending / issue #39''',
)
replace_once(
    'tools/validator/README.md',
    'examples/safety-gates/dev-prompt-safety-gates.example.md\nexamples/r1c/',
    'examples/safety-gates/dev-prompt-safety-gates.example.md\nexamples/safety-gates/bounded-semantics.example.md\nexamples/safety-gates/multigeneration/graph.json\nexamples/r1c/',
)
replace_once(
    'tools/validator/README.md',
    'Safety Gate baseline/compositionの代表的欠落検出\nR1C schema',
    'Safety Gate baseline/compositionの代表的欠落検出\nSafety Gate bounded protected-language弱化検出\nSafety Gate multi-generation inheritance/deep-scope検出\nR1C schema',
)
replace_once(
    'tools/validator/README.md',
    'common parser first sliceをfull semantic parserとして扱わない\nfull YAML/KDSL semantic parserとして扱わない',
    'common parser first sliceをfull semantic parserとして扱わない\nbounded Safety Semanticsをfull semantic equivalence proofとして扱わない\nmulti-generation graph passをcomplete safety proofとして扱わない\nfull YAML/KDSL semantic parserとして扱わない',
)
replace_once(
    'tools/validator/README.md',
    'kdsl_safety_gate_inheritance.py\n  run_safety_gate_samples.py',
    'kdsl_safety_gate_inheritance.py\n  kdsl_safety_semantics.py\n  kdsl_safety_gate_graph.py\n  run_safety_gate_samples.py\n  run_safety_semantics_samples.py\n  run_safety_semantics_examples.py',
)

# Changelog.
replace_once(
    'CHANGELOG.md',
    '### Added\n\n#### Phase 1 common parser / unified validation foundation',
    '''### Added

#### Phase 2 Safety Semantics / multi-generation inheritance

- Added `kdsl-safety-language@0.1-draft` bounded protected-language semantics.
- Added declared strong/weak concept checks for Safety Gate protected wording.
- Added condition/exception atom capture without claiming full natural-language understanding.
- Added multi-generation DAG inheritance, cycle/node validation, and multi-parent state precedence.
- Added strict deep-scope re-evaluation checks for widened/overlap/disjoint satisfied scopes.
- Added 32 property cases and 2 repository-example cases.
- Expanded unified `KDSL Validation` from 147 to 181 expectations.

Verification:

```text
pull_request: 42
source_head: f11fe00da04f25ae5fe7855535b9634e645a901e
squash_commit: 66191b6b97bab720ffd14d5732aa6f5bc0d92a44
workflow_run_id: 29180355132
run_number: 200
unified_total: 181
failed: 0
```

Boundaries:

```text
FULL_SEMANTIC_EQUIVALENCE:not_proven
FULL_SAFETY_PROOF:not_proven
EXECUTION_AUTHORITY:none
```

#### Phase 1 common parser / unified validation foundation''',
)

# Project operational status.
replace_once(
    'docs/project-status.md',
    '### PR #38 — Phase 1 common parser / unified validation foundation',
    '''### PR #42 — Phase 2 Safety Semantics / multi-generation inheritance

```yaml
pull_request: 42
merge_status: merged
merge_method: squash
source_branch: agent/kdsl-phase2-safety-semantics
source_head: f11fe00da04f25ae5fe7855535b9634e645a901e
squash_commit: 66191b6b97bab720ffd14d5732aa6f5bc0d92a44
closeout_work_pull_request: 43
closeout_pull_request: 44
model: kdsl-safety-language@0.1-draft
workflow: KDSL Validation
workflow_run_id: 29180355132
workflow_run_number: 200
workflow_conclusion: success
phase1_existing_total: 147
phase2_property_total: 32
phase2_repository_examples: 2
unified_total: 181
failed: 0
full_semantic_equivalence: not_proven
full_safety_proof: not_proven
execution_authority: none
stable_effect: none
```

### PR #38 — Phase 1 common parser / unified validation foundation''',
)
replace_once(
    'docs/project-status.md',
    'Safety Gate protected wording/inheritance first slice:=main統合済み / 108+14 expectations verified\nR1C design candidate',
    'Safety Gate protected wording/inheritance first slice:=main統合済み / 108+14 expectations verified\nSafety Semantics/multi-generation graph Phase 2:=main統合済み / 181 unified expectations verified\nR1C design candidate',
)
replace_once(
    'docs/project-status.md',
    '    - safety-gate\n    - r1c',
    '    - safety-gate\n    - safety-semantics\n    - r1c',
)
replace_once(
    'docs/project-status.md',
    '    - Safety Gate pairwise parent-child inheritance lint\n    - R1C schema',
    '    - Safety Gate pairwise parent-child inheritance lint\n    - bounded protected-language semantic IR lint\n    - multi-generation DAG inheritance/multi-parent conflict lint\n    - deep scope equal/narrowed/widened/overlap/disjoint/unknown lint\n    - R1C schema',
)
replace_once(
    'docs/project-status.md',
    '      - python tools/validator/run_parser_samples.py\n    expected_unified_total: 147',
    '      - python tools/validator/run_parser_samples.py\n      - python tools/validator/run_safety_semantics_samples.py\n      - python tools/validator/run_safety_semantics_examples.py\n    expected_unified_total: 181',
)
replace_once(
    'docs/project-status.md',
    '''latest_pr_validation:
      pull_request: 38
      run_id: 29177082691
      run_number: 192
      conclusion: success
      unified_total: 147
      failed: 0''',
    '''latest_pr_validation:
      pull_request: 42
      run_id: 29180355132
      run_number: 200
      conclusion: success
      unified_total: 181
      failed: 0''',
)
replace_once(
    'docs/project-status.md',
    '''protected wording full semantic equivalence proof
Safety Gate multi-generation inheritance graph/deep scope semantics
full natural-language trigger context parser''',
    '''bounded protected-language model integrated; full semantic equivalence proof未実装
multi-generation DAG/deep-scope first slice integrated; arbitrary graph/full scope proof未実装
full natural-language trigger/negation/exception context parser未実装''',
)
replace_once(
    'docs/project-status.md',
    '### Phase 1 common parser / unified validation',
    '''### Phase 2 Safety Semantics / multi-generation inheritance

```yaml
pull_request: 42
source_head: f11fe00da04f25ae5fe7855535b9634e645a901e
squash_commit: 66191b6b97bab720ffd14d5732aa6f5bc0d92a44
model: kdsl-safety-language@0.1-draft
workflow: KDSL Validation
workflow_run_id: 29180355132
run_number: 200
conclusion: success
phase1_existing_total: 147
phase2_property_total: 32
phase2_repository_examples: 2
unified_total: 181
failed: 0
full_semantic_equivalence: not_proven
full_safety_proof: not_proven
execution_authority: none
meaning: bounded declared-concept and graph evidence only; not complete semantic/safety proof
```

### Phase 1 common parser / unified validation''',
)
replace_once(
    'docs/project-status.md',
    'tools/validator/verification/kdsl_common_parser_verify.md\ndocs/reviews/kdsl-packet-validator-first-slice.md',
    'tools/validator/verification/kdsl_common_parser_verify.md\ndocs/reviews/kdsl-phase2-safety-semantics.md\ntools/validator/kdsl-safety-semantics-implementation-notes.md\ndocs/reviews/kdsl-packet-validator-first-slice.md',
)
replace_once(
    'docs/project-status.md',
    '''full natural-language semantic parserなし
full negation parserなし
protected wording full semantic equivalence proofなし
Safety Gate multi-generation inheritance graph/deep scope lintなし''',
    '''bounded Safety Semantics first slice統合済み
full natural-language semantic parserなし
full negation/exception reasoningなし
protected wording full semantic equivalence proofなし
multi-generation DAG/deep-scope first slice統合済み / arbitrary graph/full scope proofなし''',
)
replace_once(
    'docs/project-status.md',
    '''P1: Phase 2 Safety Semantics / multi-generation inheritance / bounded protected-language model
P2: Phase 3 R1C deep optional-block round-trip / Evidence / Authority
P3: Phase 4 Packet / Normalization semantic-property proof
P4: Phase 5 public-facing v2 hardening / release-readiness review''',
    '''P1: Phase 3 R1C deep optional-block round-trip / Evidence / Authority
P2: Phase 4 Packet / Normalization semantic-property proof
P3: Phase 5 public-facing v2 hardening / release-readiness review''',
)

# Remove this carrier before the workflow commits the closeout tree.
Path('.github/scripts/apply_phase2_safety_semantics_closeout.py').unlink()
