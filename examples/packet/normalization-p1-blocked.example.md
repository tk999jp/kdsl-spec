# Packet Normalization P1 Blocked Example

status: design-candidate example
canonical: no
executable: no
source: examples/packet/normalization-p1-source.example.md

```yaml
NORMALIZATION_DRAFT:
SCHEMA: kdsl-packet-normalization@0.1-draft
STATUS: non-executable
SOURCE:
  schema: kdsl-packet@0.1-draft
  digest: "sha256:b37951d0a8c30afef865a64f0e29566136b6c2dace51810c9ef328a6615df9f1"
  packet_status: non-executable
  normalize_state: not_normalized
TARGET:
  kind: P1
  schema: unresolved
  resolution: blocked
  executable: false
MAP:
  entries:
    - source: BASE
      target: P1 normalization route
      mode: blocked
      evidence: "BASE-ADPS-P1 selected but canonical P1 schema absent"
    - source: AUTHORITY
      target: normalization evidence only
      mode: exact
      evidence: "all source rails retained; no target authority granted"
PRESERVE:
  exact_strings:
    - "spec/bridge/kdsl-adps-bridge.md"
    - "kdsl-r1c@0.1-draft"
  protected_wording:
    - "KDSL-DP direct execution prohibited"
    - "Unknown P1/P1L schema inference prohibited"
    - "KDSL-DP→P1/P1L正規化必須"
  ordered_fields:
    - "FLOW-READ>FLOW-ANALYZE>FLOW-GATE>FLOW-DECIDE>FLOW-REPORT"
UNRESOLVED:
  - source: "P1 target field schema"
    reason: "canonical P1/P1L schema not present in repository"
    impact: blocked
LOSS: []
ROUND_TRIP:
  state: blocked
  structural_equivalence: not_proven
  semantic_equivalence: not_proven
AUTHORITY:
  source_rails_preserved: true
  execution_authority: none
OUTPUT:
  marker: none
  executable: false
  preview: ""
```

Boundary:

```text
P1/P1L target schema未定義→推測禁止
OUTPUT preview禁止
KDSL-DP直接実行禁止
source authority保持 != execution authority
normalization未完了→実行禁止
```
