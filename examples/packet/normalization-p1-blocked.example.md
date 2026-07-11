# Packet Normalization P1 Blocked Example

status: design-candidate example
canonical: no
executable: no

```yaml
NORMALIZATION_DRAFT:
SCHEMA: kdsl-packet-normalization@0.1-draft
STATUS: non-executable
SOURCE:
  schema: kdsl-packet@0.1-draft
  digest: "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
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
PRESERVE:
  exact_strings: []
  protected_wording:
    - "KDSL-DP直接実行禁止"
    - "KDSL-DP→P1/P1L正規化必須"
  ordered_fields: []
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
  source_rails_preserved: false
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
normalization未完了→実行禁止
```
