# Changelog

Detailed decisions and verification evidence are retained in `docs/reviews/*`, `tools/validator/verification/*`, and Git history.

## Unreleased

### Added

#### Packet validator first slice

- Added `tools/validator/kdsl_packet.py`.
- Added Packet envelope/required-field/order checks.
- Added BASE/TASK/FLOW/SG registry and known ID checks.
- Added TASK minimum Safety Gate/FLOW matrix checks.
- Added AUTHORITY/NORMALIZE/OUT boundary checks.
- Added PKT:v1 and representative trigger checks.
- Added `--target packet` and Packet checking to `--target all`.
- Expanded the candidate sample suite from 49 to 69 expectations.
- Added actual `examples/packet/packet-design.example.md` coverage.
- Packet execution/normalization readiness remains explicitly out of scope.

#### Packet v2-draft ownership alignment

- Adopted `kdsl-packet@0.1-draft` as a v2-draft non-executable authoring schema.
- Adopted BASE / TASK / FLOW registries as v2-draft classification registries.
- Adopted Packet lint requirements while keeping the validator unimplemented.
- Required `STATUS:non-executable`, `NORMALIZE.required:true`, and `NORMALIZE.state:not_normalized`.
- Kept registry IDs/opcodes separate from authority, Safety Gate satisfaction, commands, and normalization completion.
- Kept `PKT:v1` prohibited and direct AI coding tool execution forbidden.

#### Packet registry and schema design candidate

- Added `kdsl-packet@0.1-draft`.
- Added `kdsl-packet-base@0.1-draft`, `kdsl-packet-task@0.1-draft`, and `kdsl-packet-flow@0.1-draft`.
- Added Packet lint candidate, design-only example, and design review record.
- PR #10 regression CI: run #78 / existing 49 expectations / failed 0.
- Design integration did not make Packet adopted, canonical, stable, or executable until the separate ownership review.

#### R1C v2-draft ownership alignment

- Adopted `kdsl-r1c@0.1-draft` as a v2-draft compact serialization profile subordinate to canonical R1.
- Kept `spec/r1/r1-result-spec.md` as the canonical R1 authority.
- Aligned manifest, CP-Packet Bridge, v2 glossary, README, and project status.
- Kept all canonical R1 field names and RT/NEXT/COMMIT meanings unchanged.
- Kept short aliases, required-field omission, and implicit defaults prohibited.
- Kept Full R1 fallback required when reversible expansion cannot be guaranteed.
- R1C adoption does not make KDSL-Packet executable.

#### R1C compact-result design candidate

- Added `kdsl-r1c@0.1-draft` as a design candidate for compact serialization of canonical R1 / `KDSL_RESULT`.
- Retained the `KDSL_RESULT:` envelope and all 11 canonical required field names.
- Added JSON-compatible inline structures for `FILES`, `CMD`, `VERIFY`, `RT`, `RISK`, `NEXT`, and `COMMIT`.
- Prohibited:
  - short field aliases
  - required-field omission
  - implicit defaults
  - `R1C:` as a replacement top-level envelope
- Required reversible expansion to Full R1 and Full R1 fallback when round-trip cannot be guaranteed.
- Added:
  - `spec/r1/r1c-compact-result-schema.md`
  - `spec/lint/kdsl-r1c-lint.md`
  - `examples/r1c/README.md`
  - success / blocked / needs-user examples
  - design, approval, round-trip, and integration records

Design integration:

```text
pull_request: 6
source_head: d2460fa656d017963c34e382dddf4faa0248b68e
squash_commit: 34d95a78aa1012662b3f2f68aac678686c95bdf0
workflow_run_id: 29143936842
run_number: 41
existing_sample_total: 34
failed: 0
```

Status:

```text
R1C design candidate: main integrated
R1C canonical/stable adoption: no
canonical R1 change: none
```

#### R1C validator first slice

- Added `tools/validator/kdsl_r1c.py`.
- Added exact detection for `KDSL_RESULT:` + `SCHEMA:kdsl-r1c@0.1-draft`.
- Added Full R1 fallback/out-of-scope handling when no R1C schema marker exists.
- Added required-field presence and order checks.
- Added short-alias rejection.
- Added JSON-compatible shape checks for:
  - `FILES`
  - `CMD`
  - `VERIFY`
  - `RT`
  - `RISK`
  - `NEXT`
  - `COMMIT`
- Added representative boundary checks:
  - `RT:v` requires runtime evidence wording
  - `RT:p|u` requires runtime-unverified risk
  - `NEXT.authority=proposal_only`
  - automatic commit authority prohibited
  - contradictory VERIFY classes prohibited
- Added `--target r1c` and included R1C checking in `--target all`.
- Expanded the sample runner from 34 to 49 expectations.
- Added the three repository R1C examples to CI coverage.

Verification:

```text
pull_request: 7
source_head: 7e79a4db2e8800f5ba73f6ea8318ebd2f3c5f0bc
squash_commit: 49957fe530d028738cea94d3b6ab1f473f8b176d
workflow_run_id: 29144196401
run_number: 50
sample_total: 49
failed: 0
```

Boundaries:

```text
line-based heuristic parser
inline JSON-compatible values only
full JSON/YAML/KDSL parserなし
semantic equivalence proofなし
validator pass != RT:v/U承認/execution authority/release readiness
validator pass != R1C canonical/stable promotion
R1C design/validator implementation != Packet executable
```

#### Safety Gate Registry validator first slice

- Added `tools/validator/kdsl_safety_gate.py`.
- Added explicit `SAFETY_GATES:` block detection.
- Added `kdsl-sg@0.1-draft` registry, known-ID, known-state, and required-field checks.
- Added `state:satisfied` evidence/authority checks and `state:blocked` evidence warning.
- Added dev-prompt baseline and representative additive-composition checks.
- Added `--target safety-gate` and Safety Gate checking to `--target all`.
- Added Safety Gate samples and the actual repository example to the sample runner.

Verification:

```text
pull_request: 5
source_head: bc49316ba83ef59a7c49f6ae24a29f581e2ea16c
squash_commit: 05773b4426481b783f2aeb55f1bcbcc50c17ee93
workflow_run_id: 29143048337
run_number: 33
sample_total: 34
failed: 0
```

#### Safety Gate Registry v0.1 draft

- Added and adopted `kdsl-sg@0.1-draft` as a v2-draft registry.
- Added states `hold|satisfied|blocked|na`.
- Added ten semantic Safety Gate IDs.
- Added additive multi-gate composition and typed non-substitution rules.
- Added Registry, composition, lint, example, and design/integration files.
- Aligned manifest, CP-Packet bridge, v2 glossary, README, and project status.
- Registry adoption does not make KDSL-Packet executable.

#### Validator CI baseline

- Added `.github/workflows/validator.yml`.
- Runs on pull requests to `main`, pushes to `main`, and manual dispatch.
- Uses `ubuntu-latest`, Python 3.11, `contents: read`, and a five-minute timeout.
- Runs `python tools/validator/run_samples.py`.

#### CompactPrompt validator first slice

- Added `tools/validator/kdsl_compact_prompt.py`.
- Added CompactPrompt profile/shorthand, value, required-block, alias, CP-Lift, and Packet-boundary checks.
- Added `--target compact`.
- Expanded the sample runner from 16 to 23 cases.
- Recorded Windows PowerShell 5.1 verification with `total 23 / failed 0` and four repository examples passing.

#### KDSL v2 draft architecture

- Corrected the architecture to orthogonal axes:
  - `profile`: compact-prompt / dev-prompt / converter / lint
  - `mode`: readable / min / dense / lock
  - `safety`: normal / lock-critical / lock-all
  - `lexicon`: standard / kanji-v1
  - `envelope`: plain / packet-draft / result
- Added `profile:compact-prompt` and `lexicon:kanji-v1`.
- Added CompactPrompt lint and CP-Lift boundary.
- Kept KDSL-Packet draft-non-executable and `PKT:v1` prohibited.
- Kept v1.1 stable promotion on hold.

### Current unreleased boundaries

```text
v1.1.0-rc1:=experimental historical baseline
v1.1.0 stable:=hold
public_ready: no
Release Assets: none
R1C:=kdsl-r1c@0.1-draft / v2-draft adopted serialization profile
R1C independent canonical/stable status:=no
R1C manifest/Bridge/glossary alignment:=integrated
KDSL-Packet:=kdsl-packet@0.1-draft / v2-draft adopted / non-executable
Packet BASE/TASK/FLOW registries:=v2-draft adopted
Packet lint:=v2-draft adopted / validator first slice integration pending
Packet sample suite:=69 expectations candidate
normalization transformer/round-trip proof:=not implemented
PKT:v1:=prohibited
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
- Added R1 required-block, RT:v basis, NEXT/COMMIT authority, template-reference, and template-expansion-evidence validators.
- Added combined validator wrapper target separation and sample expectation runner.
- Added public-facing draft material and release-readiness review documents.

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
