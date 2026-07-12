# KDSL-DP Boundary Warning Example

status: non-normative-example
example_type: boundary-warning
core_spec: no
execution_authority: none

## Unsafe interpretation to avoid

```text
KDSL-DP document -> directly pass to Codex/AI coding tool as implementation prompt
```

This is forbidden.

## Required boundary

```text
KDSL-DP:=ADPS authoring format
KDSL-DP direct execution:=forbidden
P1/P1L normalization:=required
P1/P1L valid != executable
unknown profile/alias/preset:=推測禁止
```

## Safe handling pattern

```text
1. Read KDSL-DP as authoring material only.
2. Normalize KDSL-DP into the canonical P1/P1L target contract.
3. Preserve safety gates, scope, evidence, stop conditions, and authority boundaries.
4. Apply Runtime binding/control only after the normalized contract is valid and required authority is established.
5. Execute within the bound contract and return R1/KDSL_RESULT evidence.
```

KDSL_PROMPT is a separate Full KDSL/dev-prompt envelope. It must not be presented as the automatic normalized output of KDSL-DP.

## Boundary notes

```text
KDSL-DP直接実行禁止
KDSL-DP→P1/P1L正規化必須
KDSL-DP valid != executable
P1/P1L valid != executable
KDSL_PROMPT != automatic KDSL-DP normalization output
validator pass != execution authority
validator pass != U approval
validator pass != RT:v
```
