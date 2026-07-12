# KDSL Safety Gate Bounded Semantics v0.1 Draft

status: v2-draft adopted
canonical: v2-draft subordinate
model: kdsl-safety-language@0.1-draft
source_registry: spec/registry/kdsl-safety-gate-registry.md
composition: spec/registry/kdsl-safety-gate-composition.md
executable: no

## 1. Purpose

This v2-draft subordinate specification defines a bounded semantic intermediate representation for protected Safety Gate wording and a graph model for multi-generation inheritance.

```text
bounded semantic match != full natural-language understanding
semantic lint pass != semantic equivalence proof
inheritance graph pass != complete safety proof
scope relation pass != execution authority
```

Priority:

```text
canonical protected meaning > bounded semantic model > validator implementation > examples
```

## 2. Semantic atoms

Candidate atom shape:

```text
operator: prohibit|require|allow|claim|other
text: exact source statement
condition: detected condition or none
exception: detected exception or none
weakened: true|false
```

The model recognizes only declared protected concepts. Unknown language remains outside proof scope.

## 3. Protected concepts

```text
SG-DESIGN:
  design-approval-boundary

SG-SCOPE:
  scope-boundary

SG-EVIDENCE:
  evidence-separation

SG-RUNTIME:
  runtime-claim-marker
  runtime-non-substitution

SG-AUTHORITY:
  operation-authority-boundary

SG-ROLLBACK:
  rollback-preflight

SG-PUBLIC:
  public-history-protection

SG-DATA:
  data-recovery-boundary

SG-KDSL-DP:
  kdsl-dp-direct-execution-prohibition
  p1-normalization-required

SG-STOP:
  stop-condition-boundary
```

Each concept defines:

```text
strong wording alternatives
weakening/negation patterns
required concept groups
```

## 4. Bounded negation and exception handling

Representative weakening markers:

```text
禁止しない
必須ではない
不要
省略可
なくてもよい
not prohibited
not required
without approval
may proceed without
```

Conditions and exceptions may be recorded as atoms, but only declared concept patterns are used for pass/fail decisions.

```text
condition detected != condition proven complete
exception detected != exception authorized
unknown exception→manual review
```

## 5. Scope IR

Scope normalization produces:

```text
wildcard: true|false
items: normalized exact item set
```

Known relations:

```text
equal
narrowed
widened
overlap
disjoint
unknown
```

Rules:

```text
satisfied + equal→preserve
satisfied + narrowed→preserve candidate / evidence remains scope-limited
satisfied + widened|overlap|disjoint→explicit re-evaluation required
satisfied + unknown→warning/manual review
hold|blocked inheritance→scope relation does not remove gate
```

## 6. Multi-generation graph

Graph manifest:

```json
{
  "nodes": [
    {"id": "phase0", "file": "phase0.md"},
    {"id": "phase1", "file": "phase1.md"}
  ],
  "edges": [["phase0", "phase1"]]
}
```

Requirements:

```text
node id unique
edge endpoint exists
graph acyclic
all node files contain known SAFETY_GATES registry
parent hold/blocked preserved in descendants
unsafe transition requires explicit resolution/satisfaction evidence
multi-parent state conflict uses blocked > hold > satisfied
parent na is re-evaluated per child
```

## 7. Deep scope transition

For `satisfied→satisfied`:

```text
widened/overlap/disjoint without re-evaluation→fail in graph validator
widened/overlap/disjoint with explicit evidence→pass/info
narrowed→pass/info
unknown→warning
```

The legacy pairwise checker retains warning compatibility; the graph checker is the Phase 2 enforcement surface.

## 8. Aggregate state

```text
any blocked→blocked
no blocked + any hold→hold
all applicable satisfied→satisfied
all na→na
```

```text
aggregate satisfied != execution permission
aggregate satisfied != authority
aggregate satisfied != RT:v
```

## 9. Validator interfaces

```text
tools/validator/kdsl_safety_semantics.py <file>
tools/validator/kdsl_safety_gate_graph.py <graph.json>
python tools/validator/kdsl_validate.py --target safety-semantics <file>
```

Result boundaries:

```text
FULL_SEMANTIC_EQUIVALENCE: not_proven
FULL_SAFETY_PROOF: not_proven
EXECUTION_AUTHORITY: none
```

## 10. Invalid conditions

```text
protected concept weakened by declared pattern
required bounded concept missing
inheritance graph cycle
unknown graph node
parent hold/blocked missing from child
blocked/hold unsafe downgrade
multi-parent stronger gate ignored
satisfied scope widening without re-evaluation
parent na copied without independent reason
```

## 11. Non-goals

```text
full Japanese/English natural-language parser
complete semantic equivalence proof
LLM judgment as proof
Safety Gate automatic satisfaction
authority grant
RT:v decision
Packet execution
stable/public-ready promotion
```

## 12. Promotion gate

Before broader semantic/proof promotion:

```text
existing 147 regression expectations pass
bounded semantics/property suite pass
multi-generation graph property suite pass
registry/composition/lint ownership alignment completed
known limitation disclosure maintained
full semantic/proof promotion requires separate review/U approval
```
