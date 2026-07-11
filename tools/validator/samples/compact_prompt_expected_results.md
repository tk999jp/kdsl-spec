# CompactPrompt Sample Expected Results

status: sample-expectation-draft
script: tools/validator/kdsl_compact_prompt.py

| Sample | Expected status | Expected exit |
|---|---|---:|
| `sample_cp_standard_ok.md` | pass | 0 |
| `sample_cp_kanji_ok.md` | pass | 0 |
| `sample_cp_missing_block.md` | fail | 2 |
| `sample_cp_restricted_alias.md` | fail | 2 |
| `sample_cp_lift_required.md` | fail | 2 |

## Main expectations

```text
sample_cp_standard_ok.md:
  standard required blocks保持
  Guard/Check保持

sample_cp_kanji_ok.md:
  mode:dense + lexicon:kanji-v1
  目/材/出/守/確保持
  free-text安全語は完全語

sample_cp_missing_block.md:
  Check欠落検出

sample_cp_restricted_alias.md:
  材外/不→/守違反をrestricted free-text aliasとして検出

sample_cp_lift_required.md:
  implementation/repository operationをCP-Lift必要として検出
```

These expectations are heuristic lint expectations, not semantic correctness or safety proof.
