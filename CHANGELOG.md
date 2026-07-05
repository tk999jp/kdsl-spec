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
- Updated README status to clarify that `v0.1.0-draft` remains a recorded base tag while `main` now contains a v1.1-oriented spec sync.

### Notes

- Development continues after `v0.1.0-draft`.
- Existing tag/release/public status is unchanged.
- No GitHub Release has been created.
- Repository remains private.
- Validator implementation has not started.

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
- No GitHub Release has been created.
- Release/publicization are still not recommended.
- Experimental concepts such as Actor Model, Protocol Stack, Contract Matrix, Evidence Ledger, Authority Rail, KDSL-Param, HMI-lint, and Python Validator are not Core specification yet.
- Validator implementation has not started.
