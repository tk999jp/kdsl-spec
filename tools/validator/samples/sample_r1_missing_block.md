# Sample R1 Missing Block

This sample intentionally omits required fields for validator MVP testing.

```text
KDSL_RESULT:
STATUS: partial
PHASE: sample missing block phase
S: sample summary
FILES: changed:none
WHY: sample validation target
```

Expected validator result:

```text
VALIDATION_RESULT:
STATUS: fail
ERRORS:
  - missing required fields such as CMD / VERIFY / RT / RISK / NEXT / COMMIT
```
