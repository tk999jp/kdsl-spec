# Combined Validator Target Usage

status: draft
script: tools/validator/kdsl_validate.py

## Purpose

Run validator checks by target type so unrelated checker families do not run unless explicitly requested.

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
    all checkers above
```

## Default

```text
python tools/validator/kdsl_validate.py <file>
```

This uses `--target all` for backward compatibility.

Because each checker is heuristic and target-specific, prefer an explicit target for normal use.

## Examples

```text
python tools/validator/kdsl_validate.py --target r1 tools/validator/samples/sample_rt_v_valid.md
python tools/validator/kdsl_validate.py --target prompt tools/validator/samples/sample_template_expansion_ok.md
python tools/validator/kdsl_validate.py --target compact examples/compact-prompt/blog_meta.kdsl-cp.md
python tools/validator/kdsl_validate.py --target compact examples/compact-prompt/blog_meta.kdsl-cp-kanji.md
```

## Compact target behavior

```text
CompactPrompt未検出:
  pass + info

required block欠落:
  fail

mixed standard/kanji key:
  warn

restricted one-character alias:
  fail

representative CP-Lift trigger:
  fail

PKT:v1 / incomplete PACKET_DRAFT:
  fail
```

## Boundaries

```text
validator pass != RT:v
validator pass != U approval
validator pass != implementation validity
validator pass != semantic equivalence
--target prompt does not validate CompactPrompt required blocks
--target compact does not validate Template expansion or KDSL_RESULT fields
--target r1 does not validate KDSL_PROMPT or CompactPrompt fields
--target all may report unrelated target failures on mixed-purpose files
```
