# P1L / P1 Contract Validator Implementation Notes

status: Phase 8 shared AST integration candidate
implementation_date: 2026-07-17
schema_sources:
  - spec/adps/kdsl-p1l-contract-schema.md
  - spec/adps/kdsl-p1-compact-contract-schema.md
lint_source:
  - spec/lint/kdsl-p1-p1l-lint.md

## Components

```text
kdsl_p1_contract.py
  bounded P1L/P1 parser, model validation, canonical P1 rendering

kdsl_parser_v2.py
  shared first-class P1L envelope registration

kdsl_p1_contract.py
  owns legacy colon-P1 rejection without parser-registration side effects

kdsl_p1l.py / kdsl_p1.py / kdsl_p1_auto.py
  CLI target wrappers

kdsl_p1_roundtrip.py
  P1L/P1→canonical P1→reconstructed P1L projection comparison

run_p1_contract_samples.py
  positive/blocked/mutation corpus
```

## Validator targets

```text
python tools/validator/kdsl_validate.py --target p1l <file>
python tools/validator/kdsl_validate.py --target p1 <file>
python tools/validator/kdsl_validate.py --target p1-contract <file>
python tools/validator/kdsl_p1_roundtrip.py <file>
```

## First-slice coverage

```text
P1L top-level and nested field order
P1 ordered JSON segment grammar
source/profile digest shape
profile-completed exact evidence
unknown profile/alias blocking
scope/context classification separation
pre-execution Runtime disposition
all eight Authority rails
Normalization/Binding boundaries
P1L→P1→P1L structural projection
JSON pipe-delimiter handling
Windows path exact-string preservation
legacy colon P1 non-promotion
mixed P1L/P1 source rejection
```

Corpus:

```text
14 expectations / failed 0
```

## Parser architecture

Phase 8 promotes P1L marker recognition into shared AST v2 after compatibility and consumer review.

```text
shared DocumentNodeV2
→ recognizes P1L in raw-envelope context
→ preserves active-document fence isolation
→ P1L schema-specific model validation remains in kdsl_p1_contract.py
```

P1 compact serialization remains a dedicated delimiter-aware scanner and is not promoted to an AST envelope.

P1 is a one-line ordered JSON serialization and is parsed by a dedicated delimiter-aware scanner. `|` inside JSON strings is not treated as a segment separator.

## Exit semantics

```text
0: first-slice structural pass
1: warnings only
2: fail/blocked for contract use
```

```text
exit 0 != executable
exit 0 != semantic equivalence
exit 0 != complete safety proof
exit 0 != runtime binding
exit 0 != execution authority
exit 0 != RT:v
```

## Deliberate limits

```text
no full natural-language protected-wording proof
no arbitrary profile registry resolution
no legacy loss=L/AP/H inference
no K1/PF1 validation
no runtime binding
no executable transformer
no Packet→P1L/P1 mapping
no semantic equivalence proof
```

Profile validation verifies declared id/revision/digest shape and completed-field evidence. It does not fetch or prove arbitrary external profile content in this first slice.

## Preserved authority boundary

Every canonical model requires:

```text
read/edit/stage/commit/push/release/public_repo/destructive_ops
```

The checker rejects missing/implicit rails and pre-execution runtime result claims. It always emits:

```text
EXECUTABLE: no
SEMANTIC_EQUIVALENCE: not_proven
EXECUTION_AUTHORITY: none
```

## Verification evidence

```text
implementation PR: 123
source head: 497bdd45942caa687c74890cdb2f94ecf36bb8a7
squash commit: b808325c957c9f403fed461dfdbb9e3ce5d547b1
workflow run: 29583167723 / #427
KDSL Validation: success
Packet Semantic Property: success
```

Initial run #426 failed inside the new P1 corpus. The legacy colon syntax boundary was corrected without changing existing Packet or parser behavior; run #427 succeeded.

## Phase 8 compatibility corpus

```text
shared P1L marker registration
canonical field-order projection
active-document fence isolation
duplicate envelope detection
legacy colon-P1 rejection ownership
P1 compact non-envelope boundary
bootstrap file/import inventory
known consumer migration
```
