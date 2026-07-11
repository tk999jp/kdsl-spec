# R1C Validator Expected Results

status: first-slice expectations
validator: `tools/validator/kdsl_r1c.py`
schema: `kdsl-r1c@0.1-draft`

| Case | Input | Expected exit |
|---|---|---:|
| repository success example | `examples/r1c/r1c-success.example.md` | 0 |
| repository blocked example | `examples/r1c/r1c-blocked.example.md` | 0 |
| repository needs-user example | `examples/r1c/r1c-needs-user.example.md` | 0 |
| unknown schema | `sample_r1c_unknown_schema.md` | 2 |
| missing required field | `sample_r1c_missing_field.md` | 2 |
| short alias | `sample_r1c_alias.md` | 2 |
| invalid JSON value | `sample_r1c_invalid_json.md` | 2 |
| invalid RT:v basis | `sample_r1c_invalid_rt.md` | 2 |
| invalid NEXT authority | `sample_r1c_invalid_next.md` | 2 |
| invalid COMMIT authority | `sample_r1c_invalid_commit.md` | 2 |
| VERIFY contradiction | `sample_r1c_verify_contradiction.md` | 2 |
| field order mismatch | `sample_r1c_order_mismatch.md` | 2 |
| Full R1 fallback/out-of-scope | `sample_r1_ok.md` | 0 |
| wrapper valid | success example | 0 |
| wrapper invalid | invalid RT sample | 2 |

Repository runner after this slice:

```text
SUMMARY:
  total: 49
  failed: 0
```

Boundary:

```text
expected exit一致 != semantic equivalence
expected exit一致 != safety proof
expected exit一致 != RT:v
expected exit一致 != U承認
expected exit一致 != execution authority
expected exit一致 != Packet readiness
```
