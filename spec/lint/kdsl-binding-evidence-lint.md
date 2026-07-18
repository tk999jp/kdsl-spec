# KDSL Binding Evidence Lint v0.1 Draft

status: v2-draft candidate
applies_to: kdsl-binding-evidence@0.1-draft

## Required checks

### Envelope / identity

```text
[ ] marker/SCHEMA/STATUS exact
[ ] required top-level order exact
[ ] unknown/duplicate/missing field absent
[ ] no implicit default
[ ] IDENTITY id/revision/canonicalization/digest/source_ref exact
[ ] self-digest substitution and lowercase SHA-256 valid
```

### Subject / runtime control

```text
[ ] contract schema/id/digest exact
[ ] K1 id/revision/digest/source_ref exact
[ ] PF1 exact or explicit not_applicable
[ ] compatibility state separate from binding state
[ ] project/repository/task scope consistent
```

### P1L compact reference

```text
[ ] compact JSON key order schema,id,revision,digest
[ ] no insignificant whitespace or unknown key
[ ] record id/revision/digest exact match
[ ] resolved reference paired with P1L bound|blocked as specified
[ ] unresolved used only with P1L unbound|blocked
```

### Completion / restrictions

```text
[ ] explicit/profile_completed/blocked state valid
[ ] every completed field has exact expansion provenance
[ ] unknown/cyclic/ambiguous/category mismatch blocked
[ ] completed values remain visible in P1L
[ ] applied restrictions retain exact PF1 provenance
[ ] restriction conflict blocks binding
[ ] protected wording not weakened
```

### Authority

```text
[ ] all eight rails present
[ ] requested/K1/PF1/effective facets separate
[ ] effective value/scope/cardinality retained
[ ] P1L and K1 prohibitions not widened
[ ] PF1 ceiling does not create permission
[ ] allow_once has exact operation instance
[ ] target_only has exact targets
[ ] approval requirement references exact evidence or reports missing
[ ] capability absent from authority calculation
[ ] summary state does not erase rail records
```

### Approval evidence

```text
[ ] operation/scope/time/revocation exact
[ ] id/revision/digest/source/issuer exact
[ ] content_state separate from trust_state
[ ] trust policy reference exact or explicit none
[ ] digest agreement not treated as issuer authenticity
[ ] unverified source leaves requirement unsatisfied
```

### Capability evidence

```text
[ ] requirement separate from observation
[ ] capability/scope/max age/state exact
[ ] observation identity/time/environment/evidence exact
[ ] invalidation and current_state consistent
[ ] stale/inferred/unverified/not_available not sufficient
[ ] capability state separate from authority state
[ ] capability evidence not treated as RT:v
```

### Stop / preconditions / binding

```text
[ ] Stop and precondition source evidence exact
[ ] Stop clear not treated as authority
[ ] unknown critical Stop/precondition blocks binding
[ ] every dimension state preserved independently
[ ] bound limited to exact record attachment and complete evaluation
[ ] bound may coexist with insufficiency/staleness/active/unsatisfied
[ ] executable:false
[ ] semantic_equivalence:not_proven
[ ] execution_authority:none
[ ] aggregate pass/ready/authorized field absent
```

### Provenance / final interpretation

```text
[ ] every dimension-affecting source listed
[ ] exact strings preserved
[ ] provenance presence not treated as source trust
[ ] lint pass != authority grant|semantic equivalence|safety proof|RT:v|release readiness
```
