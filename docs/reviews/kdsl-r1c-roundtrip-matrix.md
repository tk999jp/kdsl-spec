# R1C Round-Trip Matrix

status: design-candidate evidence
canonical: no
schema: kdsl-r1c@0.1-draft

Purpose: show that the selected R1C serialization can expand to canonical R1 without implicit defaults.

| Canonical R1 field | R1C representation | Empty representation | Expansion rule |
|---|---|---|---|
| `STATUS` | canonical scalar | prohibited | exact value |
| `PHASE` | scalar | prohibited | exact text |
| `S` | scalar | prohibited | exact summary meaning |
| `FILES` | JSON array of exact paths | `[]` | each item becomes changed-file entry |
| `WHY` | scalar | prohibited | exact reason meaning |
| `CMD` | JSON array of executed commands | `[]` | each item becomes executed command entry |
| `VERIFY` | object with `pass/fail/not_run` arrays | each class `[]` | classes remain separate |
| `RT` | object with `state/basis` | prohibited | state becomes canonical RT; basis remains evidence |
| `RISK` | JSON array | `[]` | each item becomes risk entry |
| `NEXT` | object with `proposal/authority` | `proposal:null` | proposal remains proposal; authority remains `proposal_only` |
| `COMMIT` | object with `actual/proposed/permission_basis` | `actual:null`, `proposed:null` | actual/proposed remain separated |

## Required invariants

```text
missing != none
[] != not checked unless the field semantics explicitly mean no entries
null != success
VERIFY.not_run != VERIFY.pass
RT.state=v requires runtime basis
NEXT.authority=proposal_only fixed
COMMIT.proposed != commit authority
```

## Example expansion: blocked

R1C source:

```text
CMD:["git status -sb -uall","git diff --check"]
VERIFY:{"pass":["branch/ref確認","git diff --check"],"fail":[],"not_run":["implementation","build","target runtime"]}
RT:{"state":"p","basis":"実装未実施かつtarget runtime未実行"}
RISK:["runtime_unverified","未確認差分の帰属不明","実装状態未確認"]
```

Canonical expansion meaning:

```text
CMD:
- git status -sb -uall
- git diff --check

VERIFY:
- executed/pass: branch/ref確認
- executed/pass: git diff --check
- not_run: implementation
- not_run: build
- not_run: target runtime

RT:p
RT basis: 実装未実施かつtarget runtime未実行

RISK:
- runtime_unverified
- 未確認差分の帰属不明
- 実装状態未確認
```

No field is inferred from omission.

## Failure examples

```text
CMD omitted
→ invalid; cannot distinguish none from missing

VERIFY:{"pass":["runtime"],"fail":[],"not_run":["runtime"]}
→ invalid; contradictory class

RT:{"state":"v","basis":"CI pass"}
→ invalid; CI pass != RT:v

NEXT:{"proposal":"continue","authority":"allow"}
→ invalid; NEXT is proposal_only

COMMIT:{"actual":null,"proposed":"Fix","permission_basis":"automatic"}
→ invalid; automatic commit permission prohibited
```

## Boundary

```text
round-trip matrix != parser implementation
round-trip matrix != semantic equivalence proof
round-trip matrix != Packet readiness
validator未実装→R1C pass扱禁止
```
