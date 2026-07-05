# Combined Validator Target Usage

status: draft
script: tools/validator/kdsl_validate.py

## Purpose

Run validator checks by target type so KDSL_RESULT checks do not run against KDSL_PROMPT-only samples unless explicitly requested.

## Targets

```text
--target r1
  runs: r1_required_blocks.py, r1_rt_basis.py

--target prompt
  runs: kdsl_template_refs.py

--target all
  runs: r1_required_blocks.py, r1_rt_basis.py, kdsl_template_refs.py
```

## Default

```text
python tools/validator/kdsl_validate.py <file>
```

This uses `--target all` for backward compatibility.

## Examples

```text
python tools/validator/kdsl_validate.py --target r1 tools/validator/samples/sample_rt_v_valid.md
python tools/validator/kdsl_validate.py --target prompt tools/validator/samples/sample_template_ref_ok.md
python tools/validator/kdsl_validate.py --target all tools/validator/samples/sample_rt_v_valid.md
```

## Boundaries

```text
validator pass != RT:v
validator pass != U approval
validator pass != implementation validity
--target prompt does not validate KDSL_RESULT fields
--target r1 does not validate template references
```
