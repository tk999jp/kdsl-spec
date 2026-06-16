# Changelog

## Unreleased

### Added

- Initial private repository structure for KDSL / R1 specification management.
- README defining repository purpose, navigation, structure, draft status, and next candidate phase.
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

### Consolidated

- Repository status clarified as `validator design imported`.
- Experimental concepts are explicitly not Core specification.
- Examples are explicitly not Core specification.
- Tools are optional aids; validator pass is not approval, RT:v, or requirement validity.
- Template references require actual reading; unreadable templates must not be assumed.
- R1 is separated as an evidence / result-verification specification.
- Base dev prompt, R1 result, docs/state closeout, corrective implementation, and investigation-only templates are now available as draft reusable parts.
- MidFD docs/state closeout example demonstrates before/after compression and R1 verification format.
- Validator design separates R1 validation from KDSL template lint.

### Notes

- This repository is currently a draft specification workspace.
- No tag/release has been created yet.
- Experimental concepts such as Actor Model, Protocol Stack, Contract Matrix, Evidence Ledger, Authority Rail, KDSL-Param, HMI-lint, and Python Validator are not Core specification yet.
- Validator implementation has not started.
