# Phase 6D-4 — Packet Normalization Installer Removal

status: completed / integrated
review_date: 2026-07-14
repository: tk999jp/kdsl-spec
tracking_issue: 55
implementation_pull_request: 92
implementation_source_head: 6c0a27f5374e9374a0b698f2501ff7060218e69f
implementation_squash_commit: 1e488c6fedb792cd1a40a003b68c374af93b7dae
workflow_run_id: 29290086908
workflow_run_number: 355
workflow_conclusion: success
validator_authority: non-authoritative

## 1. Goal

Remove the Packet Normalization direct installer from `kdsl_parser_adapter` after the active checker and round-trip consumer migrated to `NormalizationCompatibilityView`.

```text
remove install_normalization only
retain Packet installer
retain adapter file
retain local parity helpers
```

## 2. Integrated changes

Modified:

```text
tools/validator/kdsl_packet_normalization.py
tools/validator/kdsl_parser_adapter_inventory.py
tools/validator/run_parser_adapter_inventory_samples.py
tools/validator/run_all_samples.py
```

Added:

```text
tools/validator/run_normalization_installer_removal_samples.py
```

## 3. Checker diff boundary

`kdsl_packet_normalization.py` changed only:

```text
remove: from kdsl_parser_adapter import install_normalization
remove: install_normalization(globals())
update: compatibility comment
```

Diff statistics:

```text
+2 / -4
```

No semantic checker block, registry rule, authority rule, output rule, or normalization boundary was changed.

## 4. Current Normalization path

```text
active checker
→ NormalizationCompatibilityView
→ legacy/AST v2 parity guard
→ existing semantic validation

round-trip consumer
→ NormalizationCompatibilityView
→ unchanged parse_normalization dictionary

property consumer
→ indirect parse_normalization API
```

Local legacy helper functions remain for parity comparison and bounded compatibility evidence. They are no longer installed through `kdsl_parser_adapter`.

## 5. Dedicated removal corpus

Four cases verify:

```text
Normalization direct adapter import absent
local parity helpers retained
valid Normalization checker path passes
Packet property path passes
```

## 6. Verification

```text
workflow run: 29290086908 / #355
KDSL Validation: success
Packet Semantic Property: success
Normalization installer-removal: 4 / failed 0
Normalization consumer contract: 10 / failed 0
Normalization consumer migration: 3 / failed 0
adapter inventory: 4 / failed 0
consumer matrix: 5 / failed 0
unified runners: 25
unified expectations: 379 / failed 0
```

## 7. Direct installer state

```text
kdsl_packet.py -> install_packet
kdsl_packet_normalization.py -> none
kdsl_safety_gate.py -> none
```

The Packet family is now the only direct user of `kdsl_parser_adapter` installer functions.

## 8. Critical boundaries retained

```text
STATUS: non-executable
TARGET.executable: false
ROUND_TRIP.semantic_equivalence: not_proven
AUTHORITY.execution_authority: none
OUTPUT.executable: false
Packet executable: no
Packet state: not_normalized
```

## 9. Retirement impact

Satisfied for Normalization family:

```text
consumer contract/mutation evidence
round-trip consumer migration
checker independence
installer removal trial
checker/property/full-suite verification
```

Still blocking global adapter retirement:

```text
Packet direct installer remains
Packet helper consumers remain
Safety Gate helper-consumer decision remains
parity-only legacy helper strategy remains
post-adapter-file-removal proof absent
```

## 10. Trust boundary

```text
installer removal pass != semantic equivalence
installer removal pass != complete safety proof
installer removal pass != adapter file retirement proof
installer removal pass != U approval
installer removal pass != RT:v
installer removal pass != execution authority
CI pass != release readiness
```

No tag, release, stable/public-ready state, executable target, or Release Asset was created.

## 11. Next safe step

Phase 6D-5 candidate:

```text
Packet helper-consumer contract inventory
consumer-specific mutation/property corpus
Packet consumer migration before install_packet removal
```

## 12. Closeout decision

```text
Phase 6D-4 Normalization installer removal: integrated
Normalization direct installer: removed
Packet direct installer: retained
adapter file retirement: blocked
Issue #55: remain open
semantic equivalence: not_proven
complete safety proof: not_proven
RT:v: not granted
execution authority: none
public_ready: no
stable_release: none
Release Assets: none
```
