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

--target r1c
  runs:
    kdsl_r1c.py

--target packet
  runs:
    kdsl_packet.py

--target all
  runs:
    r1_required_blocks.py
    r1_rt_basis.py
    r1_authority_guard.py
    kdsl_template_refs.py
    kdsl_template_expansion.py
    kdsl_compact_prompt.py
    kdsl_safety_gate.py
    kdsl_r1c.py
    kdsl_packet.py
```

## Default

```text
python tools/validator/kdsl_validate.py <file>
```

This uses `--target all` for backward compatibility.

Out-of-scope behavior:

```text
Safety Gate checker:
  SAFETY_GATES blockなし→pass/info

R1C checker:
  KDSL_RESULTなし→pass/info
  KDSL_RESULTあり + SCHEMAなし→Full R1 fallback / pass/info
  unknown SCHEMA→fail

Packet checker:
  PACKET_DRAFTなし→pass/info
  Packet SCHEMAのみ + PACKET_DRAFTなし→fail
  unknown SCHEMA/registry/ID/opcode→fail
```

These behaviors allow the checkers to participate in `--target all` without forcing every document into every profile.

## Examples

```text
python tools/validator/kdsl_validate.py --target r1 tools/validator/samples/sample_rt_v_valid.md
python tools/validator/kdsl_validate.py --target prompt tools/validator/samples/sample_template_expansion_ok.md
python tools/validator/kdsl_validate.py --target compact examples/compact-prompt/blog_meta.kdsl-cp.md
python tools/validator/kdsl_validate.py --target safety-gate examples/safety-gates/dev-prompt-safety-gates.example.md
python tools/validator/kdsl_validate.py --target r1c examples/r1c/r1c-success.example.md
python tools/validator/kdsl_validate.py --target packet examples/packet/packet-design.example.md
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

## R1C first-slice scope

```text
schema: kdsl-r1c@0.1-draft
envelope: KDSL_RESULT
canonical required field presence/order
short field alias rejection
JSON-compatible structured values
STATUS values
VERIFY pass/fail/not_run separation
RT state/basis
NEXT.authority=proposal_only
COMMIT actual/proposed/permission_basis
Full R1 fallback/out-of-scope
```

Not covered:

```text
full JSON/YAML/KDSL parser
multi-line JSON objects
semantic equivalence proof
execution evidence authenticity
runtime evidence authenticity
R1C canonical/stable promotion
Packet OUT/R1C integration
```

## Packet first-slice scope

```text
schema/envelope/status exact checks
required field presence/order
BASE/TASK/FLOW/SG known registry/ID checks
TASK minimum gate/flow matrix
FLOW-CHANGE ordering
AUTHORITY rails/values
NORMALIZE required/target/state
OUT.result_schema representative values
PKT:v1 and representative trigger checks
out-of-scope separation
```

Not covered:

```text
full YAML parser
full natural-language trigger parser
Safety Gate state/evidence deep lint
protected wording semantic equivalence
normalization transformer/round-trip proof
execution authority/readiness
```

## Sample verification

Historical checkpoints:

```text
CompactPrompt first slice:
  total: 23 / failed: 0

Safety Gate first slice:
  total: 34 / failed: 0

R1C first slice candidate:
  total: 49 / failed: 0

Packet first slice integrated:
  total: 69 / failed: 0
  pull_request: 14
  workflow_run: 116 / success
```

The current suite includes actual repository examples:

```text
examples/safety-gates/dev-prompt-safety-gates.example.md
examples/r1c/r1c-success.example.md
examples/r1c/r1c-blocked.example.md
examples/r1c/r1c-needs-user.example.md
examples/packet/packet-design.example.md
```

Evidence:

```text
tools/validator/verification/kdsl_compact_prompt_verify.md
tools/validator/verification/kdsl_safety_gate_verify.md
tools/validator/verification/kdsl_r1c_verify.md
tools/validator/verification/kdsl_packet_verify.md
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
--target r1 does not validate CompactPrompt/Safety Gate/R1C serialization
--target compact does not validate R1/template expansion/Safety Gate/R1C
--target safety-gate does not validate R1/CompactPrompt/template expansion/R1C
--target r1c does not validate Full R1 Evidence/Authority semantics beyond first-slice shape
--target packet does not prove Packet normalization/execution/authority semantics
--target all may report errors for intentionally single-target documents
Safety Gate validator implementation != Packet readiness
R1C validator implementation != R1C canonical/stable promotion
R1C validator implementation != Packet readiness
Packet validator implementation != Packet executable/normalized/readiness
```
