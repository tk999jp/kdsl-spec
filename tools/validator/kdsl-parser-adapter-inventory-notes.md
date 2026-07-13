# Parser Adapter Dependency Inventory Notes

status: phase6d-inventory-integrated / unified-ci-verified / retirement-blocked
inventory_tool: tools/validator/kdsl_parser_adapter_inventory.py
inventory_runner: tools/validator/run_parser_adapter_inventory_samples.py
corrective_pull_request: 87
corrective_squash_commit: 724d31dfb1adbbba7488db4cb444c65047492d5d
workflow: 29288377720 / 345 / success
tracking_issue: 55
validator_authority: non-authoritative

## Purpose

Inventory remaining direct adapter installers and legacy structural-helper consumers after all active checker structural inputs migrated to AST v2 CompatibilityViews.

```text
inventory != removal
inventory pass != adapter retirement proof
```

## Direct adapter import policy

Allowed direct installer imports are bounded to the current repository state:

```text
kdsl_packet.py: install_packet
kdsl_packet_normalization.py: install_normalization
```

Safety Gate direct installer status:

```text
kdsl_safety_gate.py: no direct kdsl_parser_adapter installer
```

Failures:

```text
unknown direct kdsl_parser_adapter importer
unexpected installer symbol in an allowed file
missing expected installer in repository mode
install_r1c recurrence
```

## Legacy helper families

```text
kdsl_packet:
  extract_packet_scope
  parse_top_level
  blocks_from_entries
  parse_nested_scalars
  parse_list_field
  parse_sequence_items

kdsl_packet_normalization:
  extract_scope
  parse_top_level
  blocks_from_entries
  parse_nested_scalars
  parse_list_records
  parse_nested_lists
  extract_multiline

kdsl_safety_gate:
  extract_gate_block
  parse_registry
  aggregate_state
  authority_is_unverified
  is_blank
```

Safety Gate remains in this list because structural-helper consumers are inventoried independently from direct adapter installers.

Imports from helper modules are split into:

```text
legacy structural helper consumer
nonstructural module consumer
```

The inventory does not infer whether a nonstructural import is semantically safe to relocate.

## Output

```text
PARSER_ADAPTER_INVENTORY_RESULT:
STATUS:
MODE:
DIRECT_ADAPTER_IMPORTERS:
LEGACY_STRUCTURAL_HELPER_CONSUMERS:
NONSTRUCTURAL_MODULE_CONSUMERS:
ERRORS:
RETIREMENT:
BOUNDARY:
```

## Verification

```text
inventory corpus: 4 / failed 0
consumer matrix corpus: 5 / failed 0
unified runners: 22
unified expectations: 362 / failed 0
workflow run: 29288377720 / #345
KDSL Validation: success
Packet Semantic Property: success
```

`run #345` is the first workflow that includes both Phase 6D dedicated runners in `run_all_samples.py`.

## Current retirement state

```text
state: blocked
reason: direct adapter installers or legacy structural helper consumers remain
```

Even a future `candidate` inventory state is not sufficient by itself. Post-change consumer corpus and full CI are still required.

## Corpus

```text
repository known-dependency pass
unauthorized direct import fail
install_r1c recurrence fail
legacy helper consumer classification pass
```

## Boundaries

```text
inventory pass != semantic equivalence
inventory pass != complete safety proof
inventory pass != U approval
inventory pass != RT:v
inventory pass != execution authority
inventory pass != adapter retirement proof
inventory pass != release readiness
```

## Next work

```text
consumer-specific mutation/property cases
migrate|replace|retain-with-reason execution per helper family
per-family installer removal trials
adapter file retirement decision last
```
