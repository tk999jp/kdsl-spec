# R1C Validator First-Slice Implementation Notes

status: implementation-candidate
branch: agent/kdsl-r1c-validator
schema: kdsl-r1c@0.1-draft
source: tools/validator/kdsl_r1c.py

## Implemented scope

```text
KDSL_RESULT block detection
exact SCHEMA detection
Full R1 fallback/out-of-scope pass
required field presence/order
short alias rejection
STATUS values
JSON-compatible array/object parsing
FILES/CMD/RISK string arrays
VERIFY pass/fail/not_run classes
RT state/basis
NEXT proposal/proposal_only
COMMIT actual/proposed/permission_basis
representative PKT:v1 boundary
```

## Parsing model

```text
line-based top-level field parser
first KDSL_RESULT block only
structured values: one-line JSON-compatible values
optional blocks: limited object validation
```

The parser intentionally does not attempt a complete YAML, Markdown, or KDSL grammar.

## Full R1 fallback

```text
KDSL_RESULTあり + SCHEMAなし
→ Full R1 / R1C target out-of-scope
→ pass/info
```

This allows `kdsl_r1c.py` to participate in `--target all` without forcing every canonical R1 result into R1C.

Unknown `SCHEMA` does not fall back.

```text
unknown schema→fail
schema推測禁止
```

## RT checks

```text
state:=p|u|v|na|fail|blk
basis:=non-empty string
RT:v→runtime evidence marker必須
RT:p|u→runtime_unverified相当RISK必須
```

This is heuristic wording validation. It does not perform runtime verification.

## NEXT / COMMIT checks

```text
NEXT.authority:=proposal_only固定
COMMIT.actual/proposed分離
permission_basis必須
automatic commit authority表現→fail
```

The validator does not grant operation authority.

## VERIFY checks

```text
pass/fail/not_run全subkey必須
各value:=array<string>
同一項目のclass重複→fail
```

The first slice does not prove that a claimed command or verification was actually executed.

## Sample expansion

```text
previous total: 34
new total: 49
```

Coverage:

```text
3 repository examples
unknown schema
missing field
alias rejection
invalid JSON
invalid RT:v basis
invalid NEXT authority
invalid COMMIT authority
VERIFY contradiction
field order mismatch
Full R1 fallback
wrapper valid/invalid
```

## Known limitations

```text
full parserなし
multi-line JSON object parsingなし
full semantic equivalence proofなし
full command execution evidence proofなし
full RT evidence authenticity判断なし
optional EVIDENCE/AUTHORITY deep lint限定
parent/child result aggregationなし
Packet OUT/R1C integration lintなし
```

## Safety boundary

```text
validator pass != R1 canonical promotion
validator pass != semantic equivalence
validator pass != safety proof
validator pass != RT:v
validator pass != U承認
validator pass != execution authority
validator pass != release readiness
validator pass != Packet executable
```
