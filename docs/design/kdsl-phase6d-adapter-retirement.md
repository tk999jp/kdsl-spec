# Phase 6D — Parser Adapter Retirement Gates

status: design-draft / evidence-tracked / non-normative implementation plan
repository: tk999jp/kdsl-spec
tracking_issue: 55
last_reviewed: 2026-07-14
latest_corrective: PR #87 / 724d31dfb1adbbba7488db4cb444c65047492d5d

## 1. Purpose

Define an evidence-based path for deciding whether `tools/validator/kdsl_parser_adapter.py` and installed helper exports can be migrated, explicitly retained, or removed after Phase 6C active-checker migration.

```text
active checker migration complete != adapter retirement proof
no direct checker dependency != no helper-consumer dependency
CI pass before removal != CI pass after removal
```

## 2. Current state

Phase 6C established:

```text
Full R1 / R1C / CompactPrompt / Safety Gate / Packet / Packet Normalization
active checker structural inputs→AST v2 CompatibilityViews
legacy/AST v2 parity guards→active
```

Phase 6D established:

```text
direct-installer inventory→integrated
helper-consumer decision matrix→integrated
inventory/matrix unified runner integration→verified by run #345
```

Verified direct adapter installers:

```text
kdsl_packet.py -> install_packet
kdsl_packet_normalization.py -> install_normalization
```

Safety Gate status:

```text
kdsl_safety_gate.py direct installer: absent
Safety Gate helper-consumer inventory: retained
```

## 3. Dependency classes

### A. Active checker structural input

```text
status: migrated
source: AST v2 CompatibilityView
legacy path: parity comparison only
```

### B. Direct adapter installer

Potential installer symbols:

```text
install_packet
install_normalization
install_safety_gate
install_r1c
```

Current direct imports are only `install_packet` and `install_normalization`. Unknown direct importers fail. `install_r1c` recurrence fails.

### C. Legacy structural helper consumer

A module imports structural helper symbols re-exported by:

```text
kdsl_packet
kdsl_packet_normalization
kdsl_safety_gate
```

### D. Semantic API consumer

A module imports constants or semantic functions without using the bounded structural-helper set.

```text
semantic dependency != adapter dependency
```

### E. Parity-only legacy helper

Legacy helper functions retained solely to compare the former extraction contract.

## 4. Decision vocabulary

```text
retain-temporarily
migrate-or-replace
retain-parity-only
retain-semantic-api
```

Blocking decisions:

```text
retain-temporarily
migrate-or-replace
```

## 5. Retirement gates

### G1 — Active checker independence

```text
all active checker structural inputs use AST v2 CompatibilityViews
parity guard executes before semantic validation
state: satisfied
```

### G2 — Direct installer inventory

```text
all direct imports are enumerated
unknown importer→failure
install_r1c recurrence→failure
state: integrated and unified-CI-verified
```

### G3 — Helper-consumer decision matrix

```text
all discovered consumers receive one allowed decision
unclassified dependency→failure
state: integrated and unified-CI-verified
```

### G4 — Consumer-specific mutation/property/repository corpus

Required detection classes:

```text
scope drift
field-order drift
duplicate handling drift
nested structure drift
fence behavior drift
protected wording/raw text drift
authority or non-executable boundary drift
```

```text
state: incomplete
```

### G5 — Replacement API or explicit retention evidence

Each blocking consumer must:

```text
migrate to CompatibilityView/direct API
or
move to a dedicated compatibility module
or
be retained with bounded reason and evidence
```

```text
state: incomplete
```

### G6 — Per-family removal candidate proof

Only after G1–G5 for one helper family:

```text
remove its installer or installed-name dependency
run dedicated consumer corpus
run full unified suite
verify no import/runtime failure
record workflow evidence
```

```text
state: absent
```

### G7 — Adapter file retirement

`kdsl_parser_adapter.py` may be removed only when:

```text
no direct installer imports remain
no consumer requires installed names
parity-only legacy strategy is explicitly decided
full suite succeeds after removal
repository status records the result
```

```text
state: blocked
```

## 6. Verified validation state

```text
corrective PR: #87
source head: 20cce60e459bbb379599d69e5a1e1b1bae66f202
squash commit: 724d31dfb1adbbba7488db4cb444c65047492d5d
workflow run: 29288377720 / #345
KDSL Validation: success
Packet Semantic Property: success
adapter inventory: 4 / failed 0
consumer matrix: 5 / failed 0
unified runners: 22
unified expectations: 362 / failed 0
```

## 7. Current decision

```text
adapter_retirement: blocked
adapter_removal: not performed
```

Reasons:

```text
direct installers remain
migrate-or-replace consumers remain
consumer-specific mutation/property proof incomplete
post-removal proof absent
```

## 8. Proposed migration order

```text
1. Packet Normalization round-trip/property consumer contract corpus
2. Packet Normalization consumer migration
3. Packet helper consumers
4. Safety Gate inheritance/graph/optional helper decisions
5. parity-only helper strategy
6. per-family installer removal trials
7. adapter file retirement decision
```

## 9. Safety and authority boundaries

```text
inventory/matrix pass != consumer migration
inventory/matrix pass != semantic equivalence
inventory/matrix pass != complete safety proof
inventory/matrix pass != adapter retirement proof
CI pass != RT:v
NEXT:=proposal, not execution authority
COMMIT:=actual/proposed record, not auto-commit authority
Packet executable:no
Packet state:not_normalized
Normalization semantic_equivalence:not_proven
Normalization execution_authority:none
stable/public-ready/tag/release/Release Assets操作なし
```

## 10. Stop conditions

Stop and require review when:

```text
unknown direct adapter importer appears
helper symbol use cannot be classified
consumer exit/output changes unexpectedly
protected wording/raw text changes
RT/NEXT/COMMIT meaning changes
Packet/Normalization/Safety/CP-Lift boundary weakens
removal requires unknown defaults or schema inference
```

## 11. Completion criteria

Phase 6D is not complete until:

```text
consumer-specific corpus expanded
per-family decisions recorded
blocking consumers cleared or explicitly retained with evidence
post-decision full CI recorded
adapter retirement or explicit retention decision recorded
```
