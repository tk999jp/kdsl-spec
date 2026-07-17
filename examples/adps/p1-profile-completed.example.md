# P1 Profile-Completed Example

This example shows canonical `kdsl-p1@0.1-draft` serialization after an exact external profile supplied declared defaults. The profile itself is not defined by this repository.

Verified profile evidence assumed by the example:

```text
id: example.safe.v1
revision: 2026-07-17
digest: sha256:1111111111111111111111111111111111111111111111111111111111111111
completed fields: GUARD.constraints / VERIFY.requirements / RUNTIME.disposition / OUTPUT.report_requirements
```

```text
P1|SCHEMA=kdsl-p1@0.1-draft|STATUS=contract-candidate|M={"contract_rev":"0.1","contract_id":"example-profile-001","parent_id":"none"}|SRC={"kind":"kdsl-dp","digest":"sha256:2222222222222222222222222222222222222222222222222222222222222222","references":[]}|PF={"id":"example.safe.v1","revision":"2026-07-17","digest":"sha256:1111111111111111111111111111111111111111111111111111111111111111","completion":"profile_completed","completed_fields":["GUARD.constraints","VERIFY.requirements","RUNTIME.disposition","OUTPUT.report_requirements"]}|T={"kind":"fix","declared":"fix"}|S={"source":[],"read":["src/Feature.cs"],"target":["src/Feature.cs"],"non_target":["public API","data schema"]}|C={"background":["Correct one bounded defect"],"observed":[],"inferred":[],"unverified":["Runtime behavior remains unverified"]}|G={"expected":["Preserve existing behavior outside the target"],"questions":[]}|P={"strategy":["Apply a minimal correction"],"steps":["Inspect the target","Apply the bounded change","Run declared verification"]}|GD={"constraints":["narrow scope","no opportunistic refactor","KDSL-DP direct execution prohibited"],"safety_gates":[],"protected_wording":["未確認を確認済扱い禁止","build/diff/lint/test/CI pass != RT:v"]}|X=["The change exceeds SCOPE.target","A public API or data schema change becomes necessary"]|V={"requirements":["build","diff check"],"unavailable_policy":"report_not_run"}|RT={"disposition":"user_required","required_evidence":["Target-environment operation and observation"]}|O={"result_schema":"kdsl-r1c@0.1-draft","report_requirements":["Report unverified runtime separately","NEXT remains proposal only"]}|A={"read":"target_only","edit":"target_only","stage":"forbid","commit":"propose_only","push":"forbid","release":"forbid","public_repo":"forbid","destructive_ops":"forbid"}|N={"state":"profile_completed","unresolved":[],"loss":[],"round_trip":"not_tested","semantic_equivalence":"not_proven"}|BD={"runtime_control":"unresolved","state":"unbound","executable":false}
```

Important:

```text
profile completion values are expanded in the P1 fields
profile reference != permission
P1 valid != executable
RUNTIME:user_required != RT:v
```
