# Ruleset Enforcement Test

status: temporary-verification
review_date: 2026-07-12
target_branch: main
required_check: KDSL Validation

```text
purpose:=verify required-check enforcement
merge: prohibited
close_without_merge: required
```

This temporary file exists only on the verification branch. The pull request must be closed without merge after confirming that merge is blocked while the required check is pending and becomes available only after the check succeeds.

```text
workflow success != semantic equivalence
workflow success != complete safety proof
workflow success != RT:v
workflow success != release readiness
```
