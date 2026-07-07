# KDSL-DP Boundary Warning Example

status: draft-example
example_type: boundary-warning
core_spec: no

## Unsafe interpretation to avoid

```text
KDSL-DP document -> directly pass to Codex as implementation prompt
```

This is forbidden.

## Required boundary

```text
KDSL-DP := ADPS authoring format
KDSL-DP direct execution: forbidden
P1/P1L normalization: required before execution
unknown profile / alias / preset: no inference
```

## Safe handling pattern

```text
1. Read KDSL-DP as authoring material only.
2. Normalize into P1/P1L.
3. Preserve safety gates and authority boundaries.
4. Create KDSL_PROMPT only after normalization.
5. Keep U approval gates for commit/release/public/tag/Release Assets operations.
```

## Boundary notes

```text
KDSL-DP直接実行禁止
P1/P1L正規化必須
validator pass != U approval
validator pass != RT:v
```
