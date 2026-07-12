# KDSL Public Examples

status: non-normative-public-examples
release: v1.1.0-rc1
release_class: experimental preview
public_ready: no
canonical: no
execution_authority: none
license: MIT

## Purpose

This directory contains small external-facing examples for understanding KDSL and R1 behavior.

```text
examples/public/* != Core specification
examples/public/* != execution contract
examples/public/* != approval
examples/public/* != RT:v evidence
examples/public/* != commit/push/release authority
```

When an example conflicts with a specification file, the specification file wins.

```text
spec/manifest.md
spec/core/*
spec/profiles/*
spec/r1/*
spec/lint/*
spec/bridge/*
```

## Files

```text
kdsl_prompt_safe_fix.example.md
  safety-gate-preserving dev-prompt example

kdsl_prompt_template_inheritance.example.md
  template inheritance/evidence example

r1_result_valid.example.md
  documentation-only KDSL_RESULT structure

r1_result_authority_guard.example.md
  NEXT / COMMIT / Authority separation

kdsl_dp_boundary_warning.example.md
  KDSL-DP direct-execution prohibition
```

## Reading rules

```text
D禁止/承認/未確認/未実行/rollback/RT:v境界を保持
KDSL-DP直接実行禁止
P1/P1L正規化必須
KDSL-Packet:=non-executable
CMD:=illustrated executed commands only
VERIFY:=illustrated executed/not_run verification
RT:v:=target runtime evidence required
NEXT:=proposal only
COMMIT.proposed:=message candidate only
```

Do not copy an example mechanically into a real workflow without replacing its files, commands, verification evidence, Runtime state, risks, and authority basis.

## Validator boundary

```text
validator pass != semantic equivalence
validator pass != complete safety proof
validator pass != U approval
validator pass != RT:v
validator pass != release readiness
```

## Release boundary

```text
public example availability != public-ready approval
public example availability != stable release approval
existing tag movement prohibited
Release Assets operation prohibited
```

## Next reading

```text
docs/r1-quickstart.md
spec/r1/r1-result-spec.md
spec/lint/kdsl-lint-checklist.md
spec/bridge/kdsl-adps-bridge.md
```
