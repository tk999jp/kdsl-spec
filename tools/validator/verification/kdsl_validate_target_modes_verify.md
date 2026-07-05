# Combined Validator Target Mode Verification

status: verified-local-copy
phase: validator-wrapper-target-mode-separation
script: tools/validator/kdsl_validate.py

## Scope

```text
verified: --target r1 runs R1 checkers only
verified: --target prompt runs template reference checker only
verified: default mode remains all
not_verified: release workflow
not_verified: GitHub Actions
```

## Expected local commands

```text
python tools/validator/kdsl_validate.py --target r1 tools/validator/samples/sample_rt_v_valid.md => exit 0
python tools/validator/kdsl_validate.py --target prompt tools/validator/samples/sample_template_ref_ok.md => exit 0
python tools/validator/kdsl_validate.py --target prompt tools/validator/samples/sample_template_ref_missing_gate.md => exit 2
python tools/validator/kdsl_validate.py tools/validator/samples/sample_template_ref_ok.md => exit 2
```

## Notes

```text
default all-mode intentionally runs all checkers
prompt target prevents R1-only checker false failure for KDSL_PROMPT samples
r1 target prevents template-only checker noise for KDSL_RESULT samples
```

## Safety note

```text
wrapper pass != RT:v
wrapper pass != U approval
wrapper pass != implementation validity
```
