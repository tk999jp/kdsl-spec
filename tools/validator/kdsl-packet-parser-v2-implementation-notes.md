# Packet Parser v2 Compatibility Notes

status: active-checker-and-runtime-consumers-migrated / direct-installer-removed
compatibility_view: tools/validator/kdsl_parser_v2_packet_compat.py
parity_checker: tools/validator/kdsl_parser_v2_packet_parity.py
parity_runner: tools/validator/run_parser_v2_packet_parity_samples.py
active_checker: tools/validator/kdsl_packet.py
checker_migration_runner: tools/validator/run_packet_migration_samples.py
normalize_consumer: tools/validator/kdsl_packet_normalize.py
semantic_consumer: tools/validator/kdsl_packet_semantic.py
normalize_migration_runner: tools/validator/run_packet_normalize_migration_samples.py
semantic_migration_runner: tools/validator/run_packet_semantic_migration_samples.py
installer_removal_runner: tools/validator/run_packet_installer_removal_samples.py
compatibility_pull_request: 71
checker_migration_pull_request: 73
normalize_migration_pull_request: 96
semantic_migration_pull_request: 100
installer_removal_pull_request: 104
installer_removal_squash_commit: 4701a5fce31dc6c5d11bd40bd6a0de5abbb343fe
latest_workflow: 29333878799 / 379 / success
tracking_issue: 55
validator_authority: non-authoritative

## Purpose

Provide source-spanned Packet extraction for the active checker and runtime consumers without changing Packet semantics, normalization state, authority, or executability.

```text
parser/consumer migration != semantic equivalence proof
installer removal != adapter file retirement proof
validator/CI pass != Packet execution authority
```

## Active checker path

```text
input
→ PacketCompatibilityView
→ compare_packet_legacy_v2
→ mismatch: fail before semantic validation
→ match: AST v2 scope/entries/duplicates/blocks
→ existing Packet validation
```

Consumed channels:

```text
view.scope_lines
view.entries
view.duplicates
view.values
view.legacy_blocks
view.nested_scalars
view.sequence_items
```

Output markers:

```text
Packet parser parity guard: pass
Packet structural extraction: AST v2 compatibility view
```

## Runtime consumer paths

Packet normalization mapper:

```text
kdsl_packet_normalize.collect_data
→ PacketCompatibilityView
→ existing returned dictionary
→ existing normalization emission/property paths
```

Packet semantic checker:

```text
kdsl_packet_semantic.parse_packet
→ PacketCompatibilityView
→ existing SG/FLOW record parsing
→ existing semantic/property decisions
```

Runtime consumers no longer import legacy structural helpers from `kdsl_packet`.

Retained nonstructural imports include constants, `load_text`, and `unquote`.

## Direct installer state

Removed from `kdsl_packet.py`:

```text
from kdsl_parser_adapter import install_packet
install_packet(globals())
```

Current direct adapter installer allowlist:

```text
empty
```

Any future direct `kdsl_parser_adapter` import is rejected by the inventory tool.

Local legacy helper functions remain in `kdsl_packet.py` only for parity evidence and must not be treated as the active checker or runtime-consumer path.

## Compatibility view path

```text
legacy-compatible PACKET_DRAFT scope selection
→ exact original scope retained
→ DocumentNodeV2 raw-envelope parse
→ PacketBlockNodeV2 records
→ legacy helper output reconstruction
→ legacy/AST v2 parity comparison
```

Compared legacy outputs:

```text
envelope presence
exact scope lines
top-level field order/value/relative line
duplicate top-level fields
raw block boundaries
nested scalar maps and duplicate order
SG.id list
FLOW.op list
sequence items
```

## Fenced example boundary

```text
AST v2 active-document→fenced Packet inactive
legacy parser→first PACKET_DRAFT marker selected
PacketCompatibilityView→same legacy-compatible scope selected
selected scope→raw-envelope parse
```

General parser fence behavior remains unchanged.

## Semantic rules retained

```text
SCHEMA/STATUS validity
required field/order rules
BASE/TASK registry and ID validity
TASK/FLOW composition
SG registry/ID/composition
trigger-required gates
AUTHORITY rails
OUT result schema
NORMALIZE required/target/state
GOAL placeholder handling
list warnings
OBS classification
FLOW/Authority consistency
VERIFY requirement-vs-evidence rules
PKT:v1 prohibition
Packet semantic/property rules
```

Critical Packet boundary:

```text
SCHEMA: kdsl-packet@0.1-draft
STATUS: non-executable
NORMALIZE.required: true
NORMALIZE.state: not_normalized
Packet executable: no
normalization_required: yes
normalization_completion: not_proven
execution_authority: none
```

No parser, consumer, inventory, or removal result grants edit, stage, commit, push, release, or execution permission.

## Verification

```text
Packet structural parity: 8 / failed 0
Packet checker migration: 6 / failed 0
Packet normalize contract: 10 / failed 0
Packet normalize migration: 4 / failed 0
Packet semantic contract: 10 / failed 0
Packet semantic migration: 4 / failed 0
Packet installer removal: 4 / failed 0
adapter inventory: 4 / failed 0
consumer matrix: 5 / failed 0
unified runners: 30
unified expectations: 411 / failed 0
workflow run: 29333878799 / #379
KDSL Validation: success
Packet Semantic Property: success
```

## Current boundary

```text
CompatibilityView: integrated
active base checker migration: integrated
runtime Packet consumer migrations: integrated
legacy parity guard: active
Packet direct installer: removed
direct adapter imports: none
kdsl_parser_adapter.py file: retained
Safety Gate helper-family decision: pending
parity-only helper strategy: pending
adapter file retirement: blocked
```

## Next step

```text
inventory Safety Gate inheritance/graph/optional helper consumers
add consumer-specific contract evidence
record migrate|replace|retain decisions
make adapter file retirement decision only after all helper families are resolved
```

## Trust boundary

```text
parity/contract/migration/removal pass != semantic equivalence
validator pass != complete safety proof
validator pass != U approval
validator pass != RT:v
validator pass != execution authority
validator pass != adapter file retirement proof
CI pass != release readiness
```
