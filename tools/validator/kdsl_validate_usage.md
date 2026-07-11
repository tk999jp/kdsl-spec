# Combined Validator Target Usage

status: draft
script: tools/validator/kdsl_validate.py

## Purpose

Run validator checks by target type so unrelated checks do not run against the wrong document class unless explicitly requested.

## Targets

```text
--target r1
  runs:
    r1_required_blocks.py
    r1_rt_basis.py
    r1_authority_guard.py

--target prompt
  runs:
    kdsl_template_refs.py
    kdsl_template_expansion.py

--target compact
  runs:
    kdsl_compact_prompt.py

--target all
  runs:
    r1_required_blocks.py
    r1_rt_basis.py
    r1_authority_guard.py
    kdsl_template_refs.py
    kdsl_template_expansion.py
    kdsl_compact_prompt.py
```

## Default

```text
python tools/validator/kdsl_validate.py <file>
```

This uses `--target all` for backward compatibility.

## Examples

```text
python tools/validator/kdsl_validate.py --target r1 tools/validator/samples/sample_rt_v_valid.md
python tools/validator/kdsl_validate.py --target prompt tools/validator/samples/sample_template_expansion_ok.md
python tools/validator/kdsl_validate.py --target compact examples/compact-prompt/blog_meta.kdsl-cp.md
python tools/validator/kdsl_validate.py --target all tools/validator/samples/sample_rt_v_valid.md
```

## CompactPrompt verification

Windows PowerShell 5.1 repository verification completed on 2026-07-11.

```text
python tools/validator/run_samples.py
→ total: 23 / failed: 0

CompactPrompt examples:
→ 4/4 pass
```

Evidence:

```text
tools/validator/verification/kdsl_compact_prompt_verify.md
```

## Exit codes

```text
0: pass
1: warn
2: fail / invalid invocation
```

The wrapper returns the highest exit code produced by the selected checker set.

## Boundaries

```text
validator pass != RT:v
validator pass != U approval
validator pass != implementation validity
validator pass != semantic equivalence
validator pass != release readiness
--target prompt does not validate KDSL_RESULT fields
--target r1 does not validate CompactPrompt structure
--target compact does not validate R1 or template expansion
--target all may report errors for intentionally single-target documents
```
