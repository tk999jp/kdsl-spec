# Changelog

## Unreleased

### Changed

- Synced Core KDSL specification files on `main` after `v0.1.0-draft`:
  - `spec/core/kdsl-spec.md` to `v1.1-ADPS-aware`
  - `spec/core/kdsl-core.md` to `v1.1`
  - `spec/core/kdsl-modes.md` to `v1.1`
- Synced profile and lint contracts:
  - `spec/profiles/kdsl-profile-dev-prompt.md` to `v1.1`
  - `spec/profiles/kdsl-converter-prompt.md` to `v1.1-ADPS-aware`
  - `spec/lint/kdsl-lint-checklist.md` to `v1.1`
- Synced ADPS bridge wording to `v0.2`:
  - `spec/bridge/kdsl-adps-bridge.md`
- Synced glossary and reusable templates with main v1.1 alignment:
  - `spec/glossary.md`
  - `templates/README.md`
  - `templates/base/kdsl_base_dev.md`
  - `templates/result/r1_result_spec.md`
  - `templates/tasks/task_docs_state_closeout.md`
  - `templates/tasks/task_corrective_impl.md`
  - `templates/tasks/task_investigation_only.md`
- Synced validator design status:
  - `tools/validator/README.md`
  - `tools/validator/r1-validator-design.md`
  - `tools/validator/kdsl-template-lint-design.md`
  - `tools/validator/mvp-design.md`
- Added validator MVP first implementation slice and samples:
  - `tools/validator/r1_required_blocks.py`
  - `tools/validator/r1_required_blocks_usage.md`
  - `tools/validator/r1-mvp-implementation-notes.md`
  - `tools/validator/samples/sample_r1_ok.md`
  - `tools/validator/samples/sample_r1_missing_block.md`
  - `tools/validator/samples/expected_results.md`
- Added validator first-slice verification record:
  - `tools/validator/verification/r1_required_blocks_verify.md`
- Added RT basis checker phase:
  - `tools/validator/r1_rt_basis.py`
  - `tools/validator/samples/sample_rt_v_valid.md`
  - `tools/validator/samples/sample_rt_v_invalid_basis.md`
  - `tools/validator/samples/sample_rt_v_no_basis.md`
  - `tools/validator/verification/r1_rt_basis_verify.md`
- Added authority guard design and implementation:
  - `docs/reviews/v1.1-authority-guard-design.md`
  - `tools/validator/r1_authority_guard.py`
  - `tools/validator/samples/sample_authority_ok.md`
  - `tools/validator/samples/sample_authority_warn.md`
  - `tools/validator/samples/sample_authority_fail.md`
  - `tools/validator/verification/r1_authority_guard_verify.md`
- Added template reference checker phase:
  - `tools/validator/kdsl_template_refs.py`
  - `tools/validator/samples/sample_template_ref_ok.md`
  - `tools/validator/samples/sample_template_ref_missing_gate.md`
  - `tools/validator/verification/kdsl_template_refs_verify.md`
- Added full template expansion checker design and implementation:
  - `docs/reviews/v1.1-full-template-expansion-checker-design.md`
  - `tools/validator/kdsl_template_expansion.py`
  - `tools/validator/samples/sample_template_expansion_ok.md`
  - `tools/validator/samples/sample_template_expansion_warn.md`
  - `tools/validator/samples/sample_template_expansion_fail.md`
  - `tools/validator/verification/kdsl_template_expansion_verify.md`
- Added combined validator wrapper and target-mode separation:
  - `tools/validator/kdsl_validate.py`
  - `tools/validator/kdsl_validate_usage.md`
  - `tools/validator/verification/kdsl_validate_target_modes_verify.md`
- Added public-facing README / examples-public design and drafts:
  - `docs/reviews/v1.1-public-facing-readme-examples-design.md`
  - `docs/public-facing-readme-draft.md`
  - `examples/public/README.md`
  - `examples/public/kdsl_prompt_safe_fix.example.md`
  - `examples/public/kdsl_prompt_template_inheritance.example.md`
  - `examples/public/r1_result_valid.example.md`
  - `examples/public/r1_result_authority_guard.example.md`
  - `examples/public/kdsl_dp_boundary_warning.example.md`
  - `docs/release/v1.1-release-notes-draft.md`
- Added release candidate checklist review draft:
  - `docs/reviews/v1.1-release-candidate-checklist-review.md`
- Added v1.1 readiness documents:
  - `docs/reviews/v1.1-sync-review.md`
  - `docs/reviews/v1.1-release-readiness-checklist.md`
- Published v1.1.0-rc1 prerelease:
  - tag: `v1.1.0-rc1`
  - GitHub Release: `v1.1.0-rc1`
  - release type: prerelease
  - repository visibility: public
  - Release Assets: none
- Updated README navigation and current status for validator slices, wrapper target modes, public-facing draft files, and v1.1.0-rc1 prerelease status.

### Notes

- Development continues after `v0.1.0-draft`.
- Existing `v0.1.0-draft` tag is unchanged.
- GitHub Release `v1.1.0-rc1` has been created as a prerelease.
- Repository visibility is public.
- Release Assets are not attached.
- Validator implementation has required-block, RT-basis, authority-guard, template-reference, and template-expansion slices.
- Public-facing README / examples-public / release notes are draft-oriented rc1 materials.
- Combined validator wrapper supports target modes `r1`, `prompt`, and `all`.
- Required-block verification is recorded for OK and missing-block samples.
- RT-basis verification is recorded for valid, invalid-basis, and no-basis samples.
- Authority-guard verification is recorded for OK, warn, and fail samples.
- Template-reference verification is recorded for OK and missing-gate samples.
- Template-expansion verification is recorded for OK, warn, and fail samples.
- Validator does not perform runtime verification, user approval, semantic equivalence, release, or publicization decisions.
- v1.1.0-rc1 is not a stable production release.

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

### Added

- Initial private repository structure for KDSL / R1 specification management.
- README defining repository purpose, navigation, structure, draft status, and next candidate phase.
- Overview and planning documents:
  - `docs/overview.md`
  - `docs/public-readiness.md`
- Manifest and glossary:
  - `spec/manifest.md`
  - `spec/glossary.md`
- Core specification drafts:
  - `spec/core/kdsl-spec.md`
  - `spec/core/kdsl-core.md`
  - `spec/core/kdsl-modes.md`
- Profile drafts:
  - `spec/profiles/kdsl-profile-dev-prompt.md`
  - `spec/profiles/kdsl-converter-prompt.md`
- R1 draft:
  - `spec/r1/r1-result-spec.md`
- Lint draft:
  - `spec/lint/kdsl-lint-checklist.md`
- Bridge draft:
  - `spec/bridge/kdsl-adps-bridge.md`
- Workspace READMEs:
  - `templates/README.md`
  - `experimental/README.md`
  - `examples/README.md`
- Experimental drafts:
  - `experimental/actor-model.md`
  - `experimental/protocol-stack.md`
- Template baseline drafts:
  - `templates/base/kdsl_base_dev.md`
  - `templates/result/r1_result_spec.md`
  - `templates/tasks/task_docs_state_closeout.md`
  - `templates/tasks/task_corrective_impl.md`
  - `templates/tasks/task_investigation_only.md`
- MidFD example drafts:
  - `examples/midfd/docs_state_closeout.before.md`
  - `examples/midfd/docs_state_closeout.after.md`
  - `examples/midfd/r1_result.example.md`
- Validator design drafts:
  - `tools/validator/README.md`
  - `tools/validator/r1-validator-design.md`
  - `tools/validator/kdsl-template-lint-design.md`
  - `tools/validator/mvp-design.md`
- Review documents:
  - `docs/reviews/v0.1.0-draft-review.md`
  - `docs/reviews/v0.1.0-draft-checklist.md`
- Release planning:
  - `docs/release/v0.1.0-draft-tag-plan.md`

### Consolidated

- `docs/overview.md` summarizes KDSL/R1 purpose, components, safety principles, and current maturity.
- `docs/public-readiness.md` records that public release is not recommended yet.
- `tools/validator/mvp-design.md` defines a limited R1-first MVP scope and explicitly excludes approval/RT:v substitution.
- `docs/release/v0.1.0-draft-tag-plan.md` separates work continuation from explicit tag creation approval.
- `spec/manifest.md` defines source-of-truth ownership and reference relationships.
- `spec/glossary.md` defines key terms such as KDSL, KDSL-DP, P1/P1L, R1, KDSL_PROMPT, KDSL_RESULT, RT:v, D禁止, Evidence, Authority, Template, and Validator.
- `docs/reviews/v0.1.0-draft-checklist.md` records tag readiness checks and keeps tag creation under U approval.
- Experimental concepts are explicitly not Core specification.
- Examples are explicitly not Core specification.
- Tools are optional aids; validator pass is not approval, RT:v, or requirement validity.
- Template references require actual reading; unreadable templates must not be assumed.
- R1 is separated as an evidence / result-verification specification.
- Base dev prompt, R1 result, docs/state closeout, corrective implementation, and investigation-only templates are available as draft reusable parts.
- MidFD docs/state closeout example demonstrates before/after compression and R1 verification format.
- Validator design separates R1 validation from KDSL template lint.

### Notes

- This repository is a draft specification workspace.
- No GitHub Release has been created for `v0.1.0-draft`.
- Experimental concepts such as Actor Model, Protocol Stack, Contract Matrix, Evidence Ledger, Authority Rail, KDSL-Param, HMI-lint, and Python Validator are not Core specification yet.
- Validator implementation has started with required-block, RT-basis, authority-guard, template-reference, and template-expansion slices.
