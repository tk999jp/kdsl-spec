# R1C Candidate Examples

status: review-candidate examples
canonical: no
schema: kdsl-r1c@0.1-draft
source_candidate: ../../spec/r1/r1c-compact-result-schema.md

These examples demonstrate compact serialization of canonical R1 / `KDSL_RESULT`.

```text
R1C example != canonical R1 replacement
R1C example != execution authority
R1C example != Packet contract
```

Files:

```text
r1c-success.example.md
  success result with executed verification and RT:na

r1c-blocked.example.md
  blocked result with no executed command and explicit hold/risk

r1c-needs-user.example.md
  user confirmation required and RT:u
```

All examples retain:

```text
KDSL_RESULT先頭
SCHEMA
11 canonical required fields
RT basis
NEXT proposal_only
COMMIT actual/proposed/permission_basis
```

No field alias is defined in the v0.1 candidate.

Packet boundary:

```text
R1C example valid-looking != KDSL-Packet executable
PKT:v1使用禁止
```
