# Combined Validator Target Usage

status: v2-draft
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

--target safety-gate
  runs:
    kdsl_safety_gate.py

--target all
  runs:
    r1_required_blocks.py
    r1_rt_basis.py
    r1_authority_guard.py
    kdsl_template_refs.py
    kdsl_template_expansion.py
    kdsl_compact_prompt.py
    kdsl_safety_gate.py
```

## Default

```text
python tools/validator/kdsl_validate.py <file>
```

This uses `--target all` for backward compatibility.

The Safety Gate checker returns pass/info when no `SAFETY_GATES:` block is detected, so it can participate in `--target all` without requiring every document to declare registry records.

## Examples

```text
python tools/validator/kdsl_validate.py --target r1 tools/validator/samples/sample_rt_v_valid.md
python tools/validator/kdsl_validate.py --target prompt tools/validator/samples/sample_template_expansion_ok.md
python tools/validator/kdsl_validate.py --target compact examples/compact-prompt/blog_meta.kdsl-cp.md
python tools/validator/kdsl_validate.py --target safety-gate examples/safety-gates/dev-prompt-safety-gates.example.md
python tools/validator/kdsl_validate.py --target all tools/validator/samples/sample_rt_v_valid.md
```

## Safety Gate first-slice scope

```text
known registry: kdsl-sg@0.1-draft
known IDs: adopted 10 Safety Gate IDs
known states: hold|satisfied|blocked|na
required fields: id/state/scope/reason
satisfied basis: evidence/authority
baseline: SG-SCOPE/SG-EVIDENCE/SG-AUTHORITY/SG-STOP
representative composition: rollback/data/public/runtime/KDSL-DP
```

Not covered:

```text
full YAML parsing
full natural-language trigger parsing
full negation parsing
protected wording semantic equivalence
parent-child inheritance across documents
execution authority judgment
```

## Sample verification

CompactPrompt Windows verification completed on 2026-07-11:

```text
python tools/validator/run_samples.py
→ total: 23 / failed: 0
```

After the Safety Gate validator first slice, the expected repository suite is:

```text
python tools/validator/run_samples.py
→ total: 33 / failed: 0
```

Evidence:

```text
tools/validator/verification/kdsl_compact_prompt_verify.md
tools/validator/verification/kdsl_safety_gate_verify.md
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
validator pass != safety proof
validator pass != release readiness
validator pass != execution authority
--target prompt does not validate KDSL_RESULT fields
--target r1 does not validate CompactPrompt or Safety Gate structure
--target compact does not validate R1/template expansion/Safety Gate records
--target safety-gate does not validate R1/CompactPrompt/template expansion
--target all may report errors for intentionally single-target documents
Safety Gate validator implementation != Packet/R1C readiness
```
