# K1 / PF1 Runtime-Control Validator Implementation Notes

status: Phase 9C bounded first slice / adoption candidate
repository: tk999jp/kdsl-spec
tracking_issue: 132
pull_request: 137

## Implemented

```text
shared AST markers: K1 / PF1
K1 schema/order/type checks
PF1 schema/order/type checks
schema-ordered canonical projection
IDENTITY.digest self-substitution with sha256:SELF
UTF-8 compact JSON SHA-256 recomputation
PF1 KERNEL_REF exact id/revision/digest comparison
K1 project_scope and PF1 PROJECT compatibility
K1/PF1 contract_schemas compatibility
PF1 authority ceiling structure checks
PF1 capability requirement structure checks
PF1 route identity structure checks
non-executable compatibility report
```

Entry points:

```text
kdsl_validate.py --target k1
kdsl_validate.py --target pf1
kdsl_validate.py --target runtime-control
kdsl_runtime_control_compatibility.py
```

Output boundary:

```text
EXECUTABLE:false
SEMANTIC_EQUIVALENCE:not_proven
EXECUTION_AUTHORITY:none
```

## Canonical digest behavior

```text
complete schema-ordered model
→ replace only IDENTITY.digest with sha256:SELF
→ JSON compact serialization without key sorting
→ UTF-8
→ SHA-256
→ compare with stored digest
```

The parser preserves declared mapping order and array order. Unknown top-level fields, wrong order, duplicate fields/keys, invalid digest shape, or digest mismatch are errors.

## Exact compatibility behavior

Compatibility succeeds only when:

```text
K1 and PF1 individually validate
PF1.KERNEL_REF.id == K1.IDENTITY.id
PF1.KERNEL_REF.revision == K1.IDENTITY.revision
PF1.KERNEL_REF.digest == K1.IDENTITY.digest
PF1 PROJECT matches K1 project_scope
PF1 contract_schemas exactly match K1 contract_schemas
```

Compatibility success means only that the two non-executable definitions are structurally compatible.

```text
compatibility valid != P1L binding
compatibility valid != authority sufficient
compatibility valid != capability sufficient
compatibility valid != executable
compatibility valid != RT:v
```

## Intentionally not implemented

```text
P1L authority-rail intersection
PF1 ceiling application to a P1L request
approval evidence acceptance or trusted-source verification
capability observation freshness/evidence evaluation
preset/alias semantic expansion and cycle resolution
PF1 not_applicable binding decision
Stop evaluation against a requested operation
binding-evidence canonical field schema
binding record generation
runtime binding
execution authorization artifact
BINDING.executable:true
route/tool/skill invocation
command or credential use
Packet normalized-state promotion
```

## Corpus

`run_runtime_control_samples.py` covers canonical K1/PF1 parsing, shared AST recognition, digest mismatch, KERNEL_REF mismatch, unknown ceiling mode, capability/permission separation, duplicate envelope rejection, dedicated CLIs, public validator targets, and fixed non-executable output.

The PF1 corpus instance is generated from an ordered in-memory model and assigned a recomputed canonical digest. It is not a project PF1 instance or permission profile.

## Validator authority limitation

```text
validator pass != semantic equivalence
validator pass != complete safety proof
validator pass != approval
validator pass != execution authority
validator pass != runtime binding
validator pass != RT:v
validator pass != release readiness
```
