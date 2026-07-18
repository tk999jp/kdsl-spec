# KDSL K1 / PF1 Lint v0.1 Draft

status: v2-draft adopted
applies_to:
  - kdsl-k1@0.1-draft
  - kdsl-pf1@0.1-draft

## 1. Result classes

```text
pass:=required structural and boundary checks satisfied
warning:=non-critical review item
blocked:=canonical use prohibited
```

```text
lint pass != runtime binding
lint pass != authority grant
lint pass != executable
lint pass != RT:v
lint pass != semantic equivalence|safety proof
```

## 2. Shared identity checks

- [ ] Correct envelope, schema ID, status, and field order.
- [ ] `id/revision/canonicalization/digest/source_ref` are explicit.
- [ ] Canonicalization ID is `kdsl-runtime-control-c14n@0.1-draft`.
- [ ] Digest shape is `sha256:<64 lowercase hex>`.
- [ ] Digest recomputation substitutes only `IDENTITY.digest` with `sha256:SELF`.
- [ ] Stored `IDENTITY.digest` is not `sha256:SELF`.
- [ ] Unknown or duplicate fields are absent.
- [ ] Repo/path/URL/command/API/file/branch/tag/package/class/method/property strings remain exact.
- [ ] No implicit default or similar-name inference is used.

Blocked:

```text
identity mismatch
unsupported canonicalization
invalid/circular self-digest computation
unknown/duplicate field
implicit meaning
critical exact-string change
```

## 3. K1 checks

- [ ] K1 contains cross-project runtime-control semantics only.
- [ ] Project-specific commands, paths, aliases, presets, and routes are absent.
- [ ] All required state names remain distinct.
- [ ] `executable_under_current_contract:false` is present.
- [ ] All eight P1L authority rails are declared.
- [ ] Authority and capability are evaluated separately.
- [ ] `capability_is_permission:false` is present.
- [ ] Stop continuation is not authority.
- [ ] Verify requirement is not Verify result.
- [ ] `build_test_ci_is_rt_v:false` is present.
- [ ] NEXT and COMMIT authority boundaries are preserved.
- [ ] Binding evidence is external/content-addressed and `executable:false`.
- [ ] Binding evidence references `kdsl-binding-evidence@0.1-draft`; record lint remains separate.

Blocked:

```text
K1 valid treated as executable|authority
capability participates as permission
BINDING.executable:true
RT:v claimed from build/test/CI
project-specific implicit semantics in K1
```

## 4. PF1 identity and K1 reference

- [ ] PF1 identity is exact.
- [ ] `KERNEL_REF.id/revision/digest` is exact.
- [ ] Project/repository identity is explicit.
- [ ] Contract/task applicability is explicit.
- [ ] Exclusions do not conflict with included task kinds.

Blocked:

```text
K1 reference mismatch
project mismatch
applicability conflict
unknown task/profile identity
```

## 5. Defaults / presets / aliases

- [ ] Defaults are limited to Guard/Verify/Stop/Output/pre-execution Runtime/result schema.
- [ ] No authority rail is silently completed to allow.
- [ ] Every preset has exact ID/category/expansion/order.
- [ ] Nested preset references are known and acyclic.
- [ ] Every alias has exact category and expansion.
- [ ] Alias category is not substituted.
- [ ] Protected wording is not replaced or one-character shortened.
- [ ] Expansion provenance can be recorded.

Blocked:

```text
unknown/cyclic preset
unknown/similar alias
category mismatch
authority default allow
protected wording weakened
```

## 6. Restrictions and authority ceilings

- [ ] Every rail has explicit `mode/scope/cardinality`.
- [ ] Mode is one of `allow_max|propose_only_max|forbid|approval_required|not_applicable_only`.
- [ ] Scope is `any|target_only`.
- [ ] Cardinality is `any|once`.
- [ ] PF1 ceiling is described as a maximum, not a grant.
- [ ] P1L `forbid/not_requested/propose_only` is never widened.
- [ ] K1 absolute forbid always wins.
- [ ] `target_only` requires exact non-empty target.
- [ ] `once` requires exact operation instance.
- [ ] `approval_required` follows K1 Section 8 acceptance requirements.
- [ ] Capability is absent from the authority intersection table.
- [ ] Composite effective constraints are preserved without scalar loss.

Required cases:

```text
P1L allow × PF1 forbid → forbid
P1L forbid × PF1 allow_max → forbid
P1L propose_only × PF1 allow_max → propose_only
P1L not_requested × PF1 allow_max → not_requested
P1L allow_once × missing operation instance → blocked
approval_required × unsatisfied approval evidence → blocked
```

## 7. Approval evidence

- [ ] Approval reference contains exact id/revision/digest/source/issuer/time/operation/scope.
- [ ] Approval operation and scope exactly match the evaluated rail.
- [ ] Expiry and revocation are checked.
- [ ] K1 Section 8 structural and source-verification requirements are satisfied.
- [ ] Conversation memory is not used as approval evidence.
- [ ] Approval evidence is not described as executable authorization by itself.

Blocked:

```text
remembered approval
scope/operation mismatch
expired/revoked approval
missing digest/source
K1 Section 8 acceptance unsatisfied
```

## 8. Capability requirements and observations

- [ ] Requirement and observation are separate records.
- [ ] Requirement declares exact capability/scope/max age/invalidation.
- [ ] Observation state is classified.
- [ ] Only current `observed` evidence satisfies a requirement.
- [ ] Scope and environment digest match.
- [ ] `valid_until` and max age are satisfied.
- [ ] No invalidation condition is active.
- [ ] Capability is not treated as operation permission or RT:v.

Blocked or insufficient:

```text
missing observation
inferred|unverified|stale observation
scope/environment mismatch
expired evidence
credential rotated
repository state invalidated
```

## 9. Routing

- [ ] Route kind, target ID, revision, applicability, and digest/immutable reference are exact.
- [ ] Route resolution is not authority.
- [ ] Route availability is not unrelated capability evidence.
- [ ] Route procedure cannot weaken K1/PF1/P1L.
- [ ] Unknown route has explicit blocked/no-route disposition.

## 10. PF1 not_applicable

- [ ] K1 explicitly permits no-profile binding for the task kind.
- [ ] P1L profile identity is explicitly none/not_applicable.
- [ ] No project default/preset/alias/restriction/capability dependency exists.
- [ ] All P1L authority rails remain explicit.

Any implicit PF1 dependency→blocked.

## 11. Boundary checks

- [ ] KDSL-DP direct execution remains prohibited.
- [ ] KDSL-DP→P1L/P1 normalization remains required.
- [ ] P1L/P1 valid/lint/round-trip pass != executable|authority.
- [ ] K1/PF1 valid/lint pass != executable|authority.
- [ ] Binding valid != authority sufficient.
- [ ] Authority sufficient != capability sufficient.
- [ ] `BINDING.executable:false` remains fixed.
- [ ] Packet remains non-executable/not_normalized.
- [ ] `P1L_PREVIEW != P1L:` and `P1_PREVIEW != P1|` remain preserved.
- [ ] NEXT remains proposal only.
- [ ] COMMIT remains actual/proposed record, not commit authority.
- [ ] No stable/public-ready/tag/release/Release Assets operation is implied.

## 12. Validator limitation

```text
K1/PF1 parser/validator/exact compatibility:=Phase 9C bounded first slice
binding-evidence parser/validator:=not implemented
validator pass != binding-evidence conformance|runtime binding|authority proof
```
