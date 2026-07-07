# R1 Result Authority Guard Example

status: draft-example
example_type: KDSL_RESULT
core_spec: no

```text
KDSL_RESULT:
STATUS: success
PHASE: authority guard public example
S: Demonstrated proposal-only NEXT and separated COMMIT fields.
FILES:
  - examples/public/r1_result_authority_guard.example.md
WHY: Show safe authority wording for R1 reports.
CMD:
  - python tools/validator/r1_authority_guard.py examples/public/r1_result_authority_guard.example.md
VERIFY:
  - NEXT uses proposal-only wording
  - COMMIT separates actual/proposed state
RT: not_v / runtime未確認
RISK:
  - example is not Core specification
NEXT: proposed: review authority guard wording
COMMIT: actual:none / proposed:none
```

## Boundary

```text
NEXT validation != next-task approval
COMMIT validation != commit approval
validator pass != U approval
validator pass != RT:v
```
