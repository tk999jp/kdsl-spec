# Binding Evidence Validator — Phase 9E Slice A

status: bounded-first-slice
tracking: #144

## Scope

```text
BINDING_EVIDENCE shared AST recognition
required envelope and field order
mapping/key order and enum checks
canonical JSON and self-digest validation
compact P1L runtime_control reference parsing
exact id/revision/digest matching
eight authority rails required
focused negative corpus and unified runner
```

## Entry points

```text
python tools/validator/kdsl_binding_evidence.py <evidence-file>
python tools/validator/kdsl_binding_evidence.py <evidence-file> '<compact-reference>'
python tools/validator/kdsl_validate.py --target binding-evidence <evidence-file>
python tools/validator/run_binding_evidence_samples.py
```

## Fixed boundaries

```text
BINDING.executable:false
semantic_equivalence:not_proven
execution_authority:none
validator pass != semantic equivalence|complete safety proof|RT:v
```

Approval trust, capability freshness, decision rules, and record generation remain Slice B/C work.
