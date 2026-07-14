# Phase 6D-7A — Packet Installer Removal Readiness

status: completed / integrated
review_date: 2026-07-14
repository: tk999jp/kdsl-spec
tracking_issue: 55
implementation_pull_request: 102
implementation_source_head: 4aa4a3e64eb1714c581794f6164eb6f9f34224fa
implementation_squash_commit: 4d667ea026e962b7e108a7b37d2f5aa180bb28c8
workflow_run_id: 29331728324
workflow_run_number: 375
workflow_conclusion: success

## 1. Goal

Prove that no top-level validator runtime module imports legacy structural helpers from `kdsl_packet` before attempting removal of `install_packet`.

```text
consumer migration: complete
runtime structural consumer inventory: complete
installer removal: not performed
```

## 2. Integrated files

```text
docs/design/kdsl-phase6d-packet-installer-readiness.md
tools/validator/run_packet_installer_readiness_samples.py
tools/validator/run_all_samples.py
```

Unchanged:

```text
tools/validator/kdsl_packet.py
tools/validator/kdsl_parser_adapter.py
consumer imports
spec/packet/*
spec/registry/*
```

## 3. Proven dependency state

Direct adapter installer:

```text
kdsl_packet.py -> install_packet
```

Runtime structural consumers from `kdsl_packet`:

```text
none
```

Nonstructural imports remain separately classified, including constants, `load_text`, and `unquote`.

Packet parity comparison uses legacy helpers from `kdsl_parser`, not installed exports from `kdsl_packet`.

## 4. Verification

```text
implementation PR: 102
source head: 4aa4a3e64eb1714c581794f6164eb6f9f34224fa
squash commit: 4d667ea026e962b7e108a7b37d2f5aa180bb28c8
workflow run: 29331728324 / #375
KDSL Validation: success
Packet Semantic Property: success
Packet installer readiness: 4 / failed 0
unified runners: 30
unified expectations: 411 / failed 0
```

Readiness cases:

```text
repository inventory has no errors
direct installer boundary is exact
legacy structural Packet consumers are absent
nonstructural consumers are separated and installer presence blocks retirement
```

## 5. Authorization boundary

The readiness result authorizes only a bounded Packet installer removal trial.

It does not authorize:

```text
kdsl_parser_adapter.py deletion
Safety Gate helper-family changes
parity helper deletion
semantic API relocation
stable/public-ready/tag/release/Release Assets operations
```

## 6. Packet and authority boundary

```text
Packet STATUS: non-executable
NORMALIZE.required: true
NORMALIZE.state: not_normalized
Packet executable: no
execution_authority: none
PKT:v1 prohibited
```

## 7. Trust boundary

```text
readiness pass != installer removal success
readiness pass != semantic equivalence
validator pass != complete safety proof
validator pass != U approval
validator pass != RT:v
validator pass != execution authority
validator pass != adapter retirement proof
CI pass != release readiness
```

## 8. Next safe step

Phase 6D-7B:

```text
remove only install_packet import/call from kdsl_packet.py
update direct-installer inventory to none
replace readiness runner with installer-removal runner
retain Packet base/semantic/normalize/property corpora
keep kdsl_parser_adapter.py and Safety Gate helper decisions unchanged
```

## 9. Closeout decision

```text
Phase 6D-7A Packet installer readiness: integrated
Packet installer removal trial: authorized as bounded next phase
install_packet: retained
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
