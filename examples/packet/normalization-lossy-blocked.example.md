# Packet Normalization Critical-Loss Blocked Example

status: design-candidate example
canonical: no
executable: no

```yaml
NORMALIZATION_DRAFT:
SCHEMA: kdsl-packet-normalization@0.1-draft
STATUS: non-executable
SOURCE:
  schema: kdsl-packet@0.1-draft
  digest: "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
  packet_status: non-executable
  normalize_state: not_normalized
TARGET:
  kind: full-kdsl-dev-prompt
  schema: "format:KDSL/profile:dev-prompt"
  resolution: blocked
  executable: false
MAP:
  entries:
    - source: GOAL
      target: 目的
      mode: exact
      evidence: "retained"
    - source: SG
      target: safety gates
      mode: blocked
      evidence: "critical protected wording unavailable"
PRESERVE:
  exact_strings:
    - "src/Example.cs"
  protected_wording: []
  ordered_fields: []
UNRESOLVED:
  - source: SG
    reason: "only SG IDs remain; complete hold/reason wording missing"
    impact: blocked
LOSS:
  - class: critical
    source: SG
    detail: "protected wording and hold reasons lost"
  - class: critical
    source: AUTHORITY
    detail: "operation-specific rails unavailable"
ROUND_TRIP:
  state: loss_detected
  structural_equivalence: failed
  semantic_equivalence: not_proven
AUTHORITY:
  source_rails_preserved: false
  execution_authority: none
OUTPUT:
  marker: none
  executable: false
  preview: ""
```

Boundary:

```text
SG ID-only compression禁止
critical loss→TARGET blocked
source authority rails missing→execution禁止
Full KDSL preview生成禁止
```
