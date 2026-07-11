# R1C Structural Round-Trip First Slice

status: implementation-candidate
schema: kdsl-r1c@0.1-draft
tool: tools/validator/kdsl_r1c_roundtrip.py
validator_authority: non-authoritative

## Implemented structural checks

```text
source R1C validation
KDSL_RESULT/SCHEMA provenance
canonical required field order
scalar exact preservation
FILES/CMD/RISK exact strings and order
VERIFY pass/fail/not_run class preservation
RT state/basis preservation
NEXT proposal/proposal_only preservation
COMMIT actual/proposed/permission_basis preservation
optional EVIDENCE/AUTHORITY/ANNUNCIATOR JSON preservation
```

## Status model

```text
structural_pass:
  selected structural properties reconstruct exactly

blocked:
  optional SAFETY_GATES requires a dedicated safe expansion path

fail:
  source lint failure or structural mismatch
```

## Fixed boundaries

```text
EXECUTABLE:no
SEMANTIC_EQUIVALENCE:not_proven
EXECUTION_AUTHORITY:none
structural_pass != canonical Full R1 semantic proof
structural_pass != safety proof
structural_pass != RT:v
structural_pass != execution authority
structural_pass != release readiness
```

## Intentional limitations

```text
first KDSL_RESULT block only
line-based R1C source parser
Full R1 projection is an internal structural model
natural-language S/WHY semantic equivalence not proven
optional SAFETY_GATES round-trip blocked
multi-line optional JSON not supported by source validator
property mutations are representative, not exhaustive
```
