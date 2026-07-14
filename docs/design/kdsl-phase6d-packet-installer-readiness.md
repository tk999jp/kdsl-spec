# Phase 6D-7A — Packet Installer Removal Readiness

status: design-draft / additive evidence slice
repository: tk999jp/kdsl-spec
tracking_issue: 55
review_date: 2026-07-14

## 1. Purpose

Prove that no top-level validator runtime module imports legacy structural helpers from `kdsl_packet` before attempting removal of `install_packet`.

```text
consumer migration complete != installer removal proof
inventory first
removal trial second
adapter file retirement last
```

## 2. Scope

Scan top-level Python modules under:

```text
tools/validator/*.py
```

Fixtures and documentation are excluded from the repository-runtime snapshot.

## 3. Required classifications

Direct adapter installer:

```text
kdsl_packet.py -> install_packet
```

Required legacy structural consumer result:

```text
module: kdsl_packet
runtime structural consumers: none
```

Allowed nonstructural imports from `kdsl_packet` include constants and helper APIs that are not installed by `kdsl_parser_adapter`, such as:

```text
AUTHORITY_RAILS
KNOWN_SG_IDS
SG_REGISTRY
SCHEMA_ID
load_text
unquote
```

Nonstructural dependency does not block `install_packet` removal, but it also does not declare those names a canonical public API.

## 4. Readiness properties

The corpus must prove:

```text
exact direct installer boundary
no legacy structural helper consumer from kdsl_packet
nonstructural consumers remain separately classified
retirement remains blocked only because install_packet is still present
```

Unknown direct adapter importers and `install_r1c` recurrence remain failures under the existing inventory tool.

## 5. Migration boundary

Phase 6D-7A must not:

```text
remove install_packet
change kdsl_packet.py
rewrite consumer imports
remove kdsl_parser_adapter.py
change Packet semantic/property behavior
claim adapter retirement readiness
```

## 6. Verification target

```text
new Packet installer readiness cases: 4
previous unified runners: 29
previous unified expectations: 407
expected unified runners: 30
expected unified expectations: 411
```

## 7. Removal authorization rule

A successful readiness corpus authorizes only a bounded `install_packet` removal trial.

It does not authorize:

```text
kdsl_parser_adapter.py deletion
parity helper deletion
semantic API relocation
Safety Gate helper-family changes
stable/public-ready/tag/release/Release Assets operations
```

## 8. Critical boundaries

```text
Packet STATUS: non-executable
NORMALIZE.required: true
NORMALIZE.state: not_normalized
Packet executable: no
execution_authority: none
PKT:v1 prohibited
```

## 9. Trust boundary

```text
readiness pass != installer removal success
readiness pass != semantic equivalence
readiness pass != complete safety proof
readiness pass != adapter retirement proof
readiness pass != U approval
readiness pass != RT:v
readiness pass != execution authority
CI pass != release readiness
```
