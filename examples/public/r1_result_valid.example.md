# R1 Result Valid Example

status: draft-example
example_type: KDSL_RESULT
core_spec: no

```text
KDSL_RESULT:
STATUS: success
PHASE: public example validation
S: Completed a documentation-only draft example update.
FILES:
  - examples/public/example.md
WHY: Demonstrate R1 required fields and safe reporting boundaries.
CMD:
  - python tools/validator/r1_required_blocks.py examples/public/r1_result_valid.example.md
VERIFY:
  - required block structure present
RT: not_v / runtime未確認
RISK:
  - example is not Core specification
NEXT: proposed: review public-facing examples
COMMIT: actual:none / proposed:Docs: add public-facing examples
```

## Notes

```text
validator pass != U approval
validator pass != RT:v
NEXT is proposal-only
COMMIT is not automatic commit approval
```
