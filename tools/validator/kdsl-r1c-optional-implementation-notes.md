# R1C Deep Optional-Block Validation / Round-Trip

status: integrated / verified
model: kdsl-r1c-optional-blocks@0.1-draft
parent_schema: kdsl-r1c@0.1-draft
validator_authority: non-authoritative

## Implemented tools

```text
tools/validator/kdsl_r1c_optional.py
tools/validator/kdsl_r1c_roundtrip.py
tools/validator/run_r1c_optional_samples.py
```

## EVIDENCE

```text
exact observed/inferred/not_observed/unverified keys
array<string> and duplicate checks
cross-class overlap checks
VERIFY.pass contradiction checks
RT:v basis contradiction checks
```

## AUTHORITY

```text
exact read/edit/stage/commit/push/release rails
known authority values only
FILES/CMD/COMMIT cross-field conflict checks
separate permission_basis handling for COMMIT.actual
```

## SAFETY_GATES

```text
known kdsl-sg@0.1-draft registry
known ID/state/record fields
required field checks
satisfied evidence/authority checks
registry/entry/field-order projection and reconstruction
valid records no longer blocked by round-trip helper
```

## ANNUNCIATOR

```text
JSON object
canonical key allowlist
structural preservation only
full value-semantic consistency proofなし
```

## Verification target

```text
existing unified total: 181 / failed 0
Phase 3 optional-block suite: 34 / failed 0
verified unified total: 215 / failed 0
pull_request: 45
workflow_run: 29185669224 / #207 / success
```

## Boundaries

```text
structural_pass != Full R1 semantic equivalence
optional lint pass != safety proof
optional lint pass != RT:v
AUTHORITY record != authority grant
COMMIT.proposed != commit permission
Packet executable effect:none
stable/public-ready effect:none
```
