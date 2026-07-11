# Safety Gate Validator Expected Results

status: first-slice expectations
validator: `tools/validator/kdsl_safety_gate.py`

| Sample | Expected exit | Expected classification |
|---|---:|---|
| `sample_sg_valid.md` | 0 | pass |
| `examples/safety-gates/dev-prompt-safety-gates.example.md` | 0 | pass: repository example |
| `sample_sg_unknown_registry.md` | 2 | fail: unknown registry |
| `sample_sg_unknown_id_state.md` | 2 | fail: unknown ID/state |
| `sample_sg_missing_field.md` | 2 | fail: required field missing |
| `sample_sg_satisfied_missing_basis.md` | 2 | fail: satisfied evidence/authority missing |
| `sample_sg_na_missing_reason.md` | 2 | fail: na reason missing |
| `sample_sg_baseline_missing.md` | 2 | fail: dev-prompt baseline missing |
| `sample_sg_composition_missing.md` | 2 | fail: rollback composition missing |

Wrapper expectations:

| Command target | Sample | Expected exit |
|---|---|---:|
| `--target safety-gate` | `sample_sg_valid.md` | 0 |
| `--target safety-gate` | `sample_sg_composition_missing.md` | 2 |

Sample runner total after this slice:

```text
SUMMARY:
  total: 34
  failed: 0
```

Boundary:

```text
expected exit一致 != semantic equivalence
expected exit一致 != safety proof
expected exit一致 != U承認
expected exit一致 != RT:v
```
