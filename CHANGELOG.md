# Changelog

Detailed implementation decisions and verification evidence are retained in `docs/reviews/*`, `tools/validator/verification/*`, and Git history.

## Unreleased

### Added

#### Safety Gate Registry validator first slice

- Added `tools/validator/kdsl_safety_gate.py`.
- Added explicit `SAFETY_GATES:` block detection.
- Added `kdsl-sg@0.1-draft` registry validation.
- Added known-ID validation for:
  - `SG-DESIGN`
  - `SG-SCOPE`
  - `SG-EVIDENCE`
  - `SG-RUNTIME`
  - `SG-AUTHORITY`
  - `SG-ROLLBACK`
  - `SG-PUBLIC`
  - `SG-DATA`
  - `SG-KDSL-DP`
  - `SG-STOP`
- Added known-state validation for `hold|satisfied|blocked|na`.
- Added required-field checks for `id/state/scope/reason`.
- Added `state:satisfied` evidence/authority checks.
- Added `state:blocked` evidence warning.
- Added dev-prompt baseline checks for:
  - `SG-SCOPE`
  - `SG-EVIDENCE`
  - `SG-AUTHORITY`
  - `SG-STOP`
- Added representative additive-composition checks for rollback, data, public, runtime, and KDSL-DP triggers.
- Added `--target safety-gate` to `tools/validator/kdsl_validate.py`.
- Added Safety Gate checking to `--target all`; documents without `SAFETY_GATES:` are treated as out-of-scope pass/info.
- Added Safety Gate samples, expected results, implementation notes, verification record, and design review.
- Added the actual repository example to the sample runner:
  - `examples/safety-gates/dev-prompt-safety-gates.example.md`

Verification:

```text
pull_request: 5
source_head: bc49316ba83ef59a7c49f6ae24a29f581e2ea16c
squash_commit: 05773b4426481b783f2aeb55f1bcbcc50c17ee93
workflow: Validator CI
workflow_run_id: 29143048337
run_number: 33
sample_total: 34
failed: 0
```

Boundaries:

```text
line-based heuristic parser
full YAML parserなし
full natural-language/negation parserなし
protected wording semantic equivalence proofなし
parent-child inheritance lintなし
validator pass != safety proof/RT:v/U承認/execution authority/release readiness
Safety Gate validator implementation != Packet/R1C readiness
```

#### Safety Gate Registry v0.1 draft

- Added and adopted `kdsl-sg@0.1-draft` as a v2-draft registry.
- Added states `hold|satisfied|blocked|na`.
- Added ten semantic Safety Gate IDs.
- Added additive multi-gate composition rules.
- Added typed non-substitution between approval, evidence, runtime, and authority.
- Added:
  - `spec/registry/README.md`
  - `spec/registry/kdsl-safety-gate-registry.md`
  - `spec/registry/kdsl-safety-gate-composition.md`
  - `spec/lint/kdsl-safety-gate-registry-lint.md`
  - `examples/safety-gates/dev-prompt-safety-gates.example.md`
  - design/integration review records
- Aligned manifest, CP-Packet bridge, v2 glossary, README, and project status.
- Registry adoption does not make KDSL-Packet executable.

#### Validator CI baseline

- Added `.github/workflows/validator.yml`.
- Runs on pull requests to `main`, pushes to `main`, and manual dispatch.
- Uses `ubuntu-latest`, Python 3.11, `contents: read`, and a 5-minute timeout.
- Runs:

```text
python tools/validator/run_samples.py
```

#### CompactPrompt validator first slice

- Added `tools/validator/kdsl_compact_prompt.py`.
- Added CompactPrompt profile/shorthand detection.
- Added mode/safety/lexicon checks.
- Added standard and kanji-v1 required-block checks.
- Added representative restricted-alias and CP-Lift checks.
- Added Packet draft-boundary checks.
- Added `--target compact`.
- Extended the sample runner from 16 to 23 cases.
- Recorded Windows PowerShell 5.1 verification with `total 23 / failed 0` and four repository examples passing.

#### KDSL v2 draft architecture

- Corrected the architecture to orthogonal axes:
  - `profile`: compact-prompt / dev-prompt / converter / lint
  - `mode`: readable / min / dense / lock
  - `safety`: normal / lock-critical / lock-all
  - `lexicon`: standard / kanji-v1
  - `envelope`: plain / packet-draft / result
- Added `profile:compact-prompt`.
- Added `lexicon:kanji-v1` with structural-key-only aliases.
- Added CompactPrompt lint and CP-Lift boundary.
- Kept KDSL-Packet draft-non-executable.
- Kept `PKT:v1` prohibited.
- Kept v1.1 stable promotion on hold.

### Current unreleased boundaries

```text
v1.1.0-rc1:=experimental historical baseline
v1.1.0 stable:=hold
public_ready: no
Release Assets: none
KDSL-Packet:=draft-non-executable
R1C schema:=undefined
Packet schema/BASE/TASK/FLOW registry/Packet lint:=undefined
```

## v1.1.0-rc1

### Release

```text
tag: v1.1.0-rc1
release: GitHub prerelease
release_class: experimental preview
repository_visibility: public
Release Assets: none
stable: no
public_ready: no
license: MIT
```

### Major changes

- Synchronized Core KDSL specification to v1.1/ADPS-aware wording.
- Synchronized dev-prompt, converter, lint, ADPS bridge, glossary, and templates.
- Defined KDSL-DP / P1 / P1L / R1 boundaries.
- Defined KDSL_PROMPT and KDSL_RESULT contracts.
- Added R1 required-block validator.
- Added RT:v basis validator.
- Added NEXT/COMMIT authority guard.
- Added template reference and template expansion-evidence validators.
- Added combined validator wrapper target separation.
- Added sample expectation runner.
- Added public-facing README/examples/release-note drafts.
- Added release-readiness and synchronization review documents.

### Safety boundaries

```text
KDSL-DP直接実行禁止
P1/P1L正規化必須
build/diff/lint/test pass != RT:v
NEXT:=提案, 実行許可扱禁止
COMMIT:=実行済commitまたは推奨message, 自動commit許可扱禁止
validator pass != U承認/RT:v/release readiness
public履歴/公開済tag/Release Assets保護
```

## v0.1.0-draft

### Tag

```text
tag: v0.1.0-draft
tag_type: annotated
tag_object: 797c88ad176dde5286187984de945040ec5eb945
tag_target: 89f508c4c8d5ea49a315e60cd3157b089942afee
release: none
public: not_yet
```

### Initial scope

- Created the initial KDSL / R1 specification workspace.
- Added Core, profile, R1, lint, bridge, template, example, validator-design, review, and release-planning directories.
- Added initial manifest and glossary.
- Added base dev-prompt and R1 templates.
- Added MidFD examples.
- Defined tools as non-authoritative aids.
- Defined examples, templates, and experimental concepts as non-canonical.
- Kept tag creation and public operations under explicit user approval.
