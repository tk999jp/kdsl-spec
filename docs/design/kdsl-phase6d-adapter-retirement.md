# Phase 6D — Parser Adapter Retirement Gates

status: design-draft / non-normative implementation plan
repository: tk999jp/kdsl-spec
tracking_issue: 55
review_date: 2026-07-13

## 1. Purpose

Define an evidence-based path for deciding whether `tools/validator/kdsl_parser_adapter.py` and its installed helper exports can be migrated, explicitly retained, or removed after Phase 6C active-checker migration.

```text
active checker migration complete != adapter retirement proof
no direct checker dependency != no helper-consumer dependency
CI pass before removal != CI pass after removal
```

## 2. Current state entering Phase 6D

Phase 6C established:

```text
Full R1 / R1C / CompactPrompt / Safety Gate / Packet / Packet Normalization
active checker structural inputs→AST v2 CompatibilityViews
legacy/AST v2 parity guards→active
```

Remaining compatibility surface includes:

```text
direct adapter installer imports
checker-module helper re-exports
semantic/property/round-trip helper consumers
inheritance/graph/optional helper consumers
standalone parity comparison helpers
```

These surfaces must not be treated as equivalent.

## 3. Dependency classes

### A. Active checker structural input

```text
status: migrated in Phase 6C
source: AST v2 CompatibilityView
legacy path: parity comparison only
```

### B. Direct adapter installer

A module imports one of:

```text
install_packet
install_normalization
install_safety_gate
install_r1c
```

Current direct installers are compatibility exports, not proof that the active checker still consumes Phase 1 structure.

### C. Legacy structural helper consumer

A module imports structural helper symbols re-exported by:

```text
kdsl_packet
kdsl_packet_normalization
kdsl_safety_gate
```

Examples include scope, top-level, nested scalar, record, list, and multiline extraction helpers.

### D. Semantic API consumer

A module imports constants or semantic functions from those checker modules without importing structural helpers.

```text
semantic dependency != adapter dependency
```

### E. Parity-only legacy helper

Legacy helper functions retained solely so AST v2 parity code can compare the former contract.

```text
parity-only retention may remain until retirement proof is complete
```

## 4. Retirement gates

### G1 — Active checker independence

```text
all active checker structural inputs use AST v2 CompatibilityViews
legacy parity guard executes before semantic validation
```

Current state: satisfied.

### G2 — Direct installer inventory

```text
all direct imports from kdsl_parser_adapter are enumerated
unknown direct importer→CI failure
install_r1c recurrence→CI failure
```

Current state: pending implementation in Phase 6D-1.

### G3 — Helper-consumer inventory

```text
all legacy structural helper importers are enumerated by file/module/symbol
consumer classified as migrate|replace|retain-with-reason
unknown consumer drift→CI failure or explicit review
```

Current state: pending.

### G4 — Mutation/property/repository corpus

Each helper family requires cases that detect:

```text
scope drift
field-order drift
duplicate handling drift
nested structure drift
fence behavior drift
protected wording/raw text drift
authority or non-executable boundary drift
```

Current state: partial; active checker corpora exist, consumer-specific proof is incomplete.

### G5 — Replacement API or explicit retention

For each helper consumer:

```text
migrate to CompatibilityView API
or
replace with dedicated non-adapter compatibility helper
or
retain with documented reason and bounded contract
```

Silent deletion is prohibited.

### G6 — Removal candidate proof

Only after G1–G5:

```text
remove installer for one helper family
run full unified suite and dedicated consumer corpus
verify no import/runtime failure
record diff and workflow evidence
```

One family passing does not authorize removal of another family.

### G7 — Adapter file retirement

`kdsl_parser_adapter.py` may be removed only when:

```text
no direct installer imports remain
no consumer requires installed names
parity comparison has an explicit replacement or retirement decision
full suite succeeds after removal
repository status documents the result
```

## 5. Current decision

```text
adapter_retirement: blocked
reason:
  helper-consumer inventory incomplete
  replacement/retention decisions incomplete
  post-removal corpus absent
```

This is a safe progression state, not a failure of Phase 6C.

## 6. Phase 6D-1 deliverable

Add a non-authoritative inventory tool that:

```text
uses Python AST import analysis
lists direct adapter importers and installer symbols
lists structural helper consumers by source module and symbol
fails on unknown direct adapter importers
fails on install_r1c recurrence
reports retirement blocked while compatibility dependencies remain
```

The tool must not:

```text
rewrite imports
remove adapter calls
infer semantic equivalence
claim adapter retirement readiness
claim RT:v or execution authority
```

## 7. Proposed migration order

```text
1. inventory and freeze dependency graph
2. Packet helper consumers
3. Normalization helper consumers
4. Safety Gate inheritance/graph/optional consumers
5. parity-only helper strategy
6. mutation/property/repository corpus
7. per-family installer removal trials
8. adapter file retirement decision
```

The order may change only with explicit evidence and review.

## 8. Safety and authority boundaries

```text
validator/inventory pass != semantic equivalence
inventory pass != adapter retirement proof
CI pass != RT:v
NEXT:=proposal, not execution authority
COMMIT:=actual/proposed record, not auto-commit authority
Packet executable:no
Packet state:not_normalized
Normalization semantic_equivalence:not_proven
Normalization execution_authority:none
stable/public-ready/tag/release/Release Assets操作なし
```

## 9. Stop conditions

Stop and require review when:

```text
unknown direct adapter importer appears
helper symbol use cannot be classified
consumer exit/output changes
protected wording/raw text changes
RT/NEXT/COMMIT meaning changes
Packet/Normalization/Safety/CP-Lift boundary weakens
removal requires unknown defaults or schema inference
```

## 10. Completion criteria

Phase 6D is not complete until:

```text
inventory committed
consumer classifications recorded
mutation/property corpus expanded
per-family decisions recorded
adapter retirement or explicit retention decision recorded
post-decision full CI evidence recorded
```
