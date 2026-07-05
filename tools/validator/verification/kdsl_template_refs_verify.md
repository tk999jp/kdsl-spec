# KDSL Template Reference Checker Verification

status: verified-local-copy
phase: validator-template-reference-check
script: tools/validator/kdsl_template_refs.py
samples:
  - tools/validator/samples/sample_template_ref_ok.md
  - tools/validator/samples/sample_template_ref_missing_gate.md

## Scope

```text
verified: known template path detection
verified: template safety gate detection
verified: missing gate returns fail
not_verified: full template expansion
not_verified: natural language semantic completeness
not_verified: runtime behavior
```

## Result: sample_template_ref_ok.md

Observed summary:

```text
STATUS: pass
ERRORS: none
WARNINGS: none
INFO: template references + template safety gates
exit code: 0
```

## Result: sample_template_ref_missing_gate.md

Observed summary:

```text
STATUS: fail
ERRORS: template reference exists but required template safety gates are missing
WARNINGS: none
INFO: template references
exit code: 2
```

## Safety note

```text
checker pass != template content fully expanded
checker pass != U approval
checker pass != implementation validity
```
