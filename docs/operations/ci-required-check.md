# Required CI Check Activation

status: activation-pending
repository: tk999jp/kdsl-spec
target_branch: main
required_check_name: KDSL Validation

## Purpose

Require the unified validator workflow before a pull request may merge into `main`.

## Prerequisite

The workflow must have completed at least once on a pull request with this exact check name:

```text
KDSL Validation
```

## GitHub UI procedure

```text
Repository Settings
→ Rules
→ Rulesets
→ New branch ruleset (or edit the existing main ruleset)
→ Target branches: main
→ Require status checks to pass
→ Add check: KDSL Validation
→ Require branches to be up to date before merging: recommended
→ Block force pushes: enable
→ Restrict deletions: enable
→ Save / activate ruleset
```

For repositories using classic branch protection:

```text
Settings
→ Branches
→ Add/Edit branch protection rule for main
→ Require status checks to pass before merging
→ Select KDSL Validation
→ Save changes
```

## Verification evidence

After activation, open or update a test pull request and verify:

```text
merge is blocked while KDSL Validation is pending/failing
merge becomes available after KDSL Validation succeeds
ruleset/branch-protection screenshot or API evidence is recorded
```

## Boundary

```text
workflow success != branch protection enabled
runbook presence != activation
required-check activation != semantic equivalence/safety proof/RT:v/release readiness
```
