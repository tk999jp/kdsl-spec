# KDSL P1 Compact Contract Schema v0.1 Draft

status: v2-draft adopted
canonical: subordinate compact serialization
schema_id: kdsl-p1@0.1-draft
canonical_projection: kdsl-p1l@0.1-draft
executable: no

## 1. Purpose

P1 is the compact, reversible serialization profile of canonical P1L.

```text
P1:=P1L compact serialization
P1 != independent canonical contract
P1 != direct execution instruction
P1 valid != executable
P1 parse/round-trip pass != authority
```

Ownership:

```text
P1L canonical projection > P1 serialization > P1/P1L lint > validator/example
```

When P1 cannot reconstruct P1L without invention, P1 is blocked and P1L must be used.

## 2. Canonical opening and order

Canonical one-line opening:

```text
P1|SCHEMA=kdsl-p1@0.1-draft|STATUS=contract-candidate|...
```

Required segment order:

```text
SCHEMA
STATUS
M
SRC
PF
T
S
C
G
P
GD
X
V
RT
O
A
N
BD
```

All segments are required. No implicit defaults exist in the P1 schema.

## 3. Field map

```text
M   → META
SRC → SOURCE
PF  → PROFILE
T   → TASK
S   → SCOPE
C   → CONTEXT
G   → GOAL
P   → PLAN
GD  → GUARD
X   → STOP
V   → VERIFY
RT  → RUNTIME
O   → OUTPUT
A   → AUTHORITY
N   → NORMALIZATION
BD  → BINDING
```

Each value is the complete canonical JSON projection of the corresponding P1L field.

P1 does not permit field-level omission merely because an object member is empty. Required P1L objects and arrays must still be serialized.

## 4. Serialization grammar

Conceptual grammar:

```text
p1          := "P1" segment-schema segment-status segment-m ... segment-bd
segment     := "|" key "=" json-value
key         := declared fixed key only
json-value  := RFC 8259 JSON value in compact form
```

Rules:

```text
UTF-8 required
JSON object key order follows canonical P1L field/subfield order
insignificant JSON whitespace prohibited in canonical rendering
unknown/repeated/out-of-order key→blocked
missing segment→blocked
trailing undeclared segment→blocked
```

The parser must identify JSON string/object/array boundaries. It must not split a `|` occurring inside a JSON string.

## 5. Exact-string preservation

Repo/path/file/branch/tag/commit/URL/command/package/class/method/property/API and Windows path values remain JSON strings with exact Unicode content.

```text
JSON escaping is representation-only
parse(render(value)) must reproduce the exact Unicode string
path separator normalization prohibited
case normalization prohibited
URL decoding/encoding normalization prohibited
command token rewriting prohibited
```

## 6. Canonical example shape

```text
P1|SCHEMA=kdsl-p1@0.1-draft|STATUS=contract-candidate|M={"contract_rev":"0.1","contract_id":"task-001","parent_id":"none"}|SRC={"kind":"manual","digest":"sha256:<hex>","references":[]}|PF={"id":"none","revision":"none","digest":"none","completion":"explicit","completed_fields":[]}|T={"kind":"investigate","declared":"investigate"}|S={"source":[],"read":["spec/bridge/kdsl-adps-bridge.md"],"target":[],"non_target":["implementation"]}|C={"background":[],"observed":[],"inferred":[],"unverified":[]}|G={"expected":[],"questions":["What is the current contract boundary?"]}|P={"strategy":["read-only review"],"steps":["inspect canonical sources"]}|GD={"constraints":["KDSL-DP direct execution prohibited"],"safety_gates":[],"protected_wording":["未確認を確認済扱い禁止"]}|X=[]|V={"requirements":["compare canonical sources"],"unavailable_policy":"report_not_run"}|RT={"disposition":"not_applicable","required_evidence":[]}|O={"result_schema":"kdsl-r1c@0.1-draft","report_requirements":[]}|A={"read":"target_only","edit":"forbid","stage":"forbid","commit":"propose_only","push":"forbid","release":"forbid","public_repo":"forbid","destructive_ops":"forbid"}|N={"state":"explicit","unresolved":[],"loss":[],"round_trip":"not_tested","semantic_equivalence":"not_proven"}|BD={"runtime_control":"unresolved","state":"unbound","executable":false}
```

This is a contract candidate, not an executable command.

## 7. PROFILE completion

P1 serializes the expanded P1L projection, not hidden profile shorthand.

```text
PF.completion:profile_completed→completed values must already appear in relevant canonical fields
PF.completed_fields lists supplied paths
exact profile id/revision/digest required
unknown profile/alias/preset→blocked
```

A profile reference is evidence for completion; it is not permission or runtime binding.

## 8. AUTHORITY and BINDING

`A` must contain all eight P1L authority rails. Missing rails are not defaulted.

```text
read/edit/stage/commit/push/release/public_repo/destructive_ops
```

`BD.executable` is fixed to `false` in this schema.

```text
P1 valid != executable
A.read allow != A.edit allow
A.commit allow != A.push allow
NEXT/COMMIT result fields != authority
```

## 9. RUNTIME

`RT` is a pre-execution requirement object and accepts only P1L contract dispositions:

```text
pending
user_required
not_applicable
```

Result claims are prohibited:

```text
v
fail
blk
verified
success
```

Legacy `RT:p/u/na` may be interpreted only by an explicit compatibility adapter and must expand to the canonical object.

## 10. Round-trip

Canonical check:

```text
P1L canonical projection
→ render P1
→ parse P1
→ reconstruct P1L projection
→ compare all required fields/subfields/order/exact strings
```

Allowed states:

```text
not_tested
structural_pass
loss_detected
blocked
```

`structural_pass` does not prove semantic equivalence, complete safety, runtime binding, or authority.

## 11. Legacy operational compatibility

Existing project-local forms such as:

```text
P1|M:contract_rev=0.1,...|T:F|S:...|...
```

are classified as `legacy-operational-p1`, not `kdsl-p1@0.1-draft`.

They may be converted only when an explicit compatibility profile defines every used field/alias/preset and supplies:

```text
exact profile revision/digest
expanded scope/context/guard/stop/verify/output
all eight authority rails
normalization evidence
binding remains non-executable
```

```text
loss=P may map to profile_completed only under explicit compatibility evidence
loss=L meaning unknown→blocked
AP/H meaning unknown→blocked
legacy absence of Authority rails→blocked unless exact permission contract supplies them
```

Legacy forms must not self-declare `SCHEMA=kdsl-p1@0.1-draft` without canonical reconstruction.

## 12. Fallback

Use P1L instead of P1 when:

```text
compact rendering cannot preserve exact strings
profile completion evidence is incomplete
unknown alias/preset exists
critical field would be omitted
round-trip detects loss
human review requires expanded evidence
```

## 13. Invalid conditions

```text
unknown/missing/repeated/out-of-order segment
invalid or non-canonical JSON
implicit default
hidden profile-completed value
missing Authority rail
BD.executable:true
RT result claim
protected wording or exact string loss
legacy colon syntax presented as kdsl-p1@0.1-draft
P1 passed directly as execution authority
```

Any invalid condition blocks P1 use.

## 14. Non-goals

```text
runtime binding
executable transformer
legacy alias invention
complete semantic equivalence proof
complete safety proof
Packet executable promotion
stable/public-ready/tag/release/Release Assets operation
```
