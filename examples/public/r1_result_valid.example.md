# R1 Result Valid Example

status: non-normative-example
example_type: KDSL_RESULT
core_spec: no
execution_authority: none

```text
KDSL_RESULT:
STATUS: success
PHASE: public documentation example
S: Updated a documentation-only example in the approved scope.
FILES:
  - examples/public/r1_result_valid.example.md
WHY: Demonstrate R1 required fields without claiming unexecuted commands or Runtime evidence.
CMD: []
VERIFY:
  - executed: document structure review / result=pass
RT: na / documentation-only
RISK:
  - example is not Core specification
  - document review does not prove semantic equivalence
NEXT: proposed: request human wording review / authority=proposal_only
COMMIT: actual:none / proposed:"Docs: align public R1 example" / permission_basis:none
```

## Notes

```text
CMD:[]:=実行commandなし
RT:na:=documentation-only
validator pass != U approval
validator pass != RT:v
NEXT is proposal-only
COMMIT.proposed is not commit approval
example availability != execution authority
```
