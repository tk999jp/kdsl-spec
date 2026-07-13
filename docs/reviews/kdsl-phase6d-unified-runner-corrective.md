# Phase 6D — Unified Runner Integration Corrective

status: completed / integrated
review_date: 2026-07-14
repository: tk999jp/kdsl-spec
tracking_issue: 55
corrective_pull_request: 87
corrective_source_head: 20cce60e459bbb379599d69e5a1e1b1bae66f202
corrective_squash_commit: 724d31dfb1adbbba7488db4cb444c65047492d5d
final_workflow_run_id: 29288377720
final_workflow_run_number: 345
final_workflow_conclusion: success
validator_authority: non-authoritative

## 1. Purpose

Correct two evidence defects discovered after Phase 6D-2 closeout:

```text
PR #83/#85 dedicated runners were not connected to run_all_samples.py
adapter inventory still expected a Safety Gate direct installer already removed in Phase 6C
```

## 2. Corrected implementation

Modified:

```text
tools/validator/run_all_samples.py
tools/validator/kdsl_parser_adapter_inventory.py
tools/validator/run_parser_adapter_inventory_samples.py
```

Final unified runner additions:

```text
parser-adapter-inventory
parser-adapter-consumer-matrix
```

Current direct adapter installers:

```text
kdsl_packet.py -> install_packet
kdsl_packet_normalization.py -> install_normalization
```

Not a current direct installer:

```text
kdsl_safety_gate.py -> install_safety_gate
```

Safety Gate helper symbols remain in the helper-consumer inventory because helper API consumers and direct adapter installers are separate dependency classes.

## 3. Verification progression

```text
run #341:
  both Phase 6D runners connected
  KDSL Validation: failure
  Packet Semantic Property: success
  cause: stale Safety Gate installer expectation

run #342:
  inventory runner isolated before correction
  KDSL Validation: failure
  Packet Semantic Property: success

run #344:
  current direct-installer boundary applied
  inventory runner connected
  KDSL Validation: success
  Packet Semantic Property: success

run #345:
  inventory and matrix runners connected
  KDSL Validation: success
  Packet Semantic Property: success
```

Final verified state:

```text
adapter inventory: 4 / failed 0
consumer matrix: 5 / failed 0
unified runners: 22
unified expectations: 362 / failed 0
```

## 4. Evidence correction

The following earlier statement was invalid before PR #87:

```text
22 runners / 362 expectations were verified by PR #83/#85 workflows
```

Correct statement:

```text
PR #83/#85 integrated tools and dedicated runners
PR #87 connected them to unified validation
run #345 is the first verified 22-runner / 362-expectation workflow
```

## 5. Retirement impact

```text
Safety Gate direct installer: already absent
Packet direct installer: remains
Normalization direct installer: remains
legacy structural helper consumers: remain
adapter_retirement: blocked
adapter_removal: not performed
```

The corrective narrows the known dependency graph. It does not establish adapter-retirement readiness.

## 6. Safety and authority boundaries

```text
corrective/validator/CI pass != consumer migration
corrective/validator/CI pass != semantic equivalence
corrective/validator/CI pass != complete safety proof
corrective/validator/CI pass != adapter retirement proof
corrective/validator/CI pass != U approval
corrective/validator/CI pass != RT:v
corrective/validator/CI pass != execution authority
CI pass != release readiness
```

Retained:

```text
Packet executable:no
Packet state:not_normalized
Normalization semantic_equivalence:not_proven
Normalization execution_authority:none
NEXT:=proposal, not execution authority
COMMIT:=actual/proposed record, not auto-commit authority
stable/public-ready/tag/release/Release Assets操作なし
```

## 7. Closeout decision

```text
Phase 6D unified-runner corrective: integrated
verified unified runners: 22
verified unified expectations: 362 / failed 0
adapter retirement: blocked
adapter removal: not performed
Issue #55: remain open
```
