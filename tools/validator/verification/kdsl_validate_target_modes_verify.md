# Combined Validator Target Mode Verification

status: expectation-runner-aligned
phase: validator-wrapper-target-mode-separation
script: tools/validator/kdsl_validate.py
sample_runner: tools/validator/run_samples.py

## Scope

```text
verified_by_runner: --target r1 runs R1 checkers only
verified_by_runner: --target prompt runs prompt/template checkers only
verified_by_runner: default mode remains all
not_verified: release workflow
not_verified: GitHub Actions
```

## Expected local commands

```text
python tools/validator/kdsl_validate.py --target r1 tools/validator/samples/sample_rt_v_valid.md => exit 0
python tools/validator/kdsl_validate.py --target prompt tools/validator/samples/sample_template_expansion_ok.md => exit 0
python tools/validator/kdsl_validate.py --target prompt tools/validator/samples/sample_template_ref_ok.md => exit 2
python tools/validator/kdsl_validate.py --target prompt tools/validator/samples/sample_template_ref_missing_gate.md => exit 2
python tools/validator/kdsl_validate.py tools/validator/samples/sample_template_ref_ok.md => exit 2
```

## Runner command

```text
python tools/validator/run_samples.py
```

The runner is the preferred local expectation check for sample exit codes.

## Notes

```text
default all-mode intentionally runs all checkers
prompt target prevents R1-only checker false failure for KDSL_PROMPT samples
r1 target prevents template-only checker noise for KDSL_RESULT samples
sample_template_ref_ok is template-reference-only OK, not expansion-evidence OK
sample_template_expansion_ok is the expected prompt target pass sample
```

## Safety note

```text
wrapper pass != RT:v
wrapper pass != U approval
wrapper pass != implementation validity
wrapper pass != release readiness
```
