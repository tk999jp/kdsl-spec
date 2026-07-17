# P1 Unknown-Profile Blocked Example

This is intentionally invalid/blocked.

```text
P1|SCHEMA=kdsl-p1@0.1-draft|STATUS=contract-candidate|M={"contract_rev":"0.1","contract_id":"blocked-profile-001","parent_id":"none"}|SRC={"kind":"kdsl-dp","digest":"sha256:3333333333333333333333333333333333333333333333333333333333333333","references":[]}|PF={"id":"Similar.Safe.Profile","revision":"unknown","digest":"none","completion":"profile_completed","completed_fields":["GUARD","VERIFY","AUTHORITY"]}|T={"kind":"fix","declared":"F"}|S={"source":[],"read":[],"target":["src/Feature.cs"],"non_target":[]}|C={"background":[],"observed":[],"inferred":[],"unverified":[]}|G={"expected":["Apply a fix"],"questions":[]}|P={"strategy":[],"steps":[]}|GD={"constraints":["safe"],"safety_gates":[],"protected_wording":[]}|X=[]|V={"requirements":["b+diff"],"unavailable_policy":"report_not_run"}|RT={"disposition":"user_required","required_evidence":[]}|O={"result_schema":"kdsl-r1c@0.1-draft","report_requirements":[]}|A={"read":"target_only","edit":"target_only","stage":"not_requested","commit":"propose_only","push":"forbid","release":"forbid","public_repo":"forbid","destructive_ops":"forbid"}|N={"state":"profile_completed","unresolved":[],"loss":[],"round_trip":"not_tested","semantic_equivalence":"not_proven"}|BD={"runtime_control":"unresolved","state":"unbound","executable":false}
```

Blocked reasons:

```text
profile revision/digest unavailable
profile selected by similarity
T:F/G:safe/V:b+diff meanings not proven by an exact profile
protected wording absent
profile-completed critical values cannot be verified
```

Required handling:

```text
NORMALIZATION.state:blocked
unknown profile/alias/preset inference prohibited
no execution preview or authority promotion
```
