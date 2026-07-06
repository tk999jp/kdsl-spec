# KDSL Template Expansion Checker Verification

status: verified-local-copy
phase: validator-template-expansion
script: tools/validator/kdsl_template_expansion.py
samples:
  - tools/validator/samples/sample_template_expansion_ok.md
  - tools/validator/samples/sample_template_expansion_warn.md
  - tools/validator/samples/sample_template_expansion_fail.md

## Scope

```text
verified: known template path detection
verified: expansion/inheritance marker detection
verified: required section group pass
verified: partial required section group warn
verified: missing expansion/inheritance marker fail
not_verified: full semantic equivalence
not_verified: source file content comparison
not_verified: runtime behavior
not_verified: approval judgment
```

## Expected local commands

```text
python tools/validator/kdsl_template_expansion.py tools/validator/samples/sample_template_expansion_ok.md => exit 0
python tools/validator/kdsl_template_expansion.py tools/validator/samples/sample_template_expansion_warn.md => exit 1
python tools/validator/kdsl_template_expansion.py tools/validator/samples/sample_template_expansion_fail.md => exit 2
python tools/validator/kdsl_validate.py --target prompt tools/validator/samples/sample_template_expansion_ok.md => exit 0
```

## Safety note

```text
template expansion pass != semantic equivalence
template expansion pass != U approval
template expansion pass != implementation validity
template expansion pass != RT:v
template expansion pass != release readiness
```
