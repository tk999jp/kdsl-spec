# KDSL Public Examples

status: public-examples-draft
scope: public-facing examples
release: v1.1.0-rc1
release_class: experimental preview
public: yes
public_ready: no

## Purpose

This directory contains public-facing draft examples for KDSL and R1.

Examples are not Core specification. They are explanatory material only.

## Files

```text
kdsl_prompt_safe_fix.example.md
kdsl_prompt_template_inheritance.example.md
r1_result_valid.example.md
r1_result_authority_guard.example.md
kdsl_dp_boundary_warning.example.md
```

## Rules

```text
examples must not be treated as Core specification
examples must preserve D禁止 / 未確認 / 未実行 / 承認 / RT:v boundaries
examples must not imply KDSL-DP direct execution
examples must not imply validator pass equals U approval
examples must not imply validator pass equals RT:v
examples must not imply validator pass equals release readiness
examples must avoid project-private names unless intentionally anonymized
examples must avoid Release Assets or public history operations
```

## Validator helper note

```text
validator helpers are experimental heuristic lint aids
validator pass != U approval
validator pass != RT:v
validator pass != semantic equivalence
validator pass != release readiness
kdsl_template_expansion.py checks expansion evidence, not full template expansion proof
```

## Status

```text
release: v1.1.0-rc1
release_type: prerelease
release_class: experimental preview
public: yes
public_ready: no
GitHub Release: v1.1.0-rc1 prerelease
Release Assets: none
license: pending
```

Stable release, Release Assets, tag movement, and license selection require explicit U approval.
