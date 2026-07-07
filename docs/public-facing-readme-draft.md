# KDSL / R1 Specification Draft

status: draft
release: none
public: not_yet
repository_visibility: private

## Project status

This repository is a draft specification workspace for KDSL and R1.

```text
stability: draft
release: none
public: not_yet
tag_move: none
Release Assets: none
```

This document is a public-facing README draft. It does not approve repository publicization, release creation, tag creation, tag movement, Release Assets operations, or public announcement.

## What is KDSL?

KDSL is a compact, safety-gate-preserving prompt notation for LLM and AI coding workflows.

Its goal is not only compression. Its priority is preserving meaning, safety gates, decision branches, and verification boundaries while reducing prompt size where possible.

```text
meaning preservation > safety gate preservation > decision branch preservation > implementation-error prevention > size reduction
```

## What is R1 / KDSL_RESULT?

R1 is a result-reporting contract for AI-assisted work.

A KDSL_RESULT report records status, phase, summary, files, reasons, commands, verification, runtime state, risks, next proposals, and commit state.

```text
KDSL_RESULT:
STATUS:
PHASE:
S:
FILES:
WHY:
CMD:
VERIFY:
RT:
RISK:
NEXT:
COMMIT:
```

## When to use this repository

Use this repository when designing or reviewing:

```text
KDSL prompts
AI coding tool prompts
KDSL_RESULT / R1 reports
prompt compression rules
safety-gate-preserving templates
validator checks for KDSL/R1 drafts
```

## Safety principles

KDSL must preserve high-risk operational gates.

Examples of protected boundaries:

```text
D禁止
未確認 / 未実行 handling
承認 / 承認待
rollback / revert
実機確認分離
public履歴 / 公開済tag / Release Assets protection
KDSL-DP直接実行禁止
P1/P1L正規化必須
RT:v conditions
NEXT proposal-only
COMMIT not automatic commit approval
```

## KDSL-DP boundary

KDSL and KDSL-DP are separate.

```text
KDSL := prompt notation that may be directly used with LLMs when safety gates are preserved
KDSL-DP := ADPS authoring format, not an execution instruction
```

KDSL-DP must not be passed directly to Codex or another AI coding tool as implementation instructions. It must be normalized into P1/P1L before execution.

Unknown profile, alias, preset, or template names must not be inferred from memory or similar names.

## Validator overview

Validator tools are optional aids. They do not replace human approval, runtime verification, semantic equivalence review, release judgment, or publicization judgment.

Current validator slices include:

```text
r1_required_blocks.py
r1_rt_basis.py
r1_authority_guard.py
kdsl_template_refs.py
kdsl_template_expansion.py
kdsl_validate.py
```

## Quick validation commands

```text
python tools/validator/r1_required_blocks.py tools/validator/samples/sample_r1_ok.md
python tools/validator/r1_rt_basis.py tools/validator/samples/sample_rt_v_valid.md
python tools/validator/r1_authority_guard.py tools/validator/samples/sample_authority_ok.md
python tools/validator/kdsl_template_refs.py tools/validator/samples/sample_template_ref_ok.md
python tools/validator/kdsl_template_expansion.py tools/validator/samples/sample_template_expansion_ok.md
python tools/validator/kdsl_validate.py --target r1 tools/validator/samples/sample_authority_ok.md
python tools/validator/kdsl_validate.py --target prompt tools/validator/samples/sample_template_expansion_ok.md
```

## Examples

Public-facing examples are planned under:

```text
examples/public/
```

Examples are not Core specification. They are understanding aids and must preserve safety boundaries.

## Specification map

```text
spec/core/      Core KDSL specification, core notation, modes
spec/profiles/  Usage-specific profiles
spec/r1/        R1 result-reporting contract
spec/lint/      Lint checklist
spec/bridge/    KDSL / KDSL-DP / ADPS bridge
templates/      Reusable prompt templates
examples/       Non-normative examples
tools/          Validator designs and slices
docs/           Overview, review, release planning, public readiness
```

## Non-goals

```text
No release approval
No publicization approval
No tag creation or tag movement approval
No Release Assets operation approval
No runtime verification by validator
No U approval delegation to validator
No full semantic equivalence proof by validator
```

## Release / publicization status

```text
release: none
public: not_yet
GitHub Release: none
Release Assets: none
```

A future public release candidate requires explicit U review and approval.
