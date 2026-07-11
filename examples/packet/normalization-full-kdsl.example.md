# Packet Normalization Full KDSL Preview Example

status: design-candidate example
canonical: no
executable: no
source: examples/packet/normalization-source.example.md

```yaml
NORMALIZATION_DRAFT:
SCHEMA: kdsl-packet-normalization@0.1-draft
STATUS: non-executable
SOURCE:
  schema: kdsl-packet@0.1-draft
  digest: "sha256:b464944da1a3e080b08166e0b0eaa13327c4daa8974c3c56f6a22428dd81daed"
  packet_status: non-executable
  normalize_state: not_normalized
TARGET:
  kind: full-kdsl-dev-prompt
  schema: "format:KDSL/profile:dev-prompt"
  resolution: resolved
  executable: false
MAP:
  entries:
    - source: SCHEMA
      target: normalization provenance
      mode: exact
      evidence: "kdsl-packet@0.1-draft retained in SOURCE"
    - source: STATUS
      target: normalization provenance
      mode: exact
      evidence: "non-executable retained in SOURCE/STATUS"
    - source: BASE
      target: header/profile basis
      mode: structured
      evidence: "BASE-KDSL-DEV -> profile:dev-prompt"
    - source: TASK
      target: Phase/task metadata
      mode: structured
      evidence: "TASK-CHANGE retained"
    - source: SRC
      target: 前提/正本
      mode: exact
      evidence: "repository string retained"
    - source: READ
      target: 前提/読取対象
      mode: exact
      evidence: "ordered list retained"
    - source: TGT
      target: 対象Slice/変更対象
      mode: exact
      evidence: "ordered list retained"
    - source: OBS
      target: 前提/観測
      mode: exact
      evidence: "observation retained without cause inference"
    - source: GOAL
      target: 目的
      mode: exact
      evidence: "scalar retained"
    - source: NON
      target: 非対象/禁止
      mode: exact
      evidence: "prohibitions retained"
    - source: SG
      target: safety gates/禁止
      mode: expanded
      evidence: "IDs plus complete hold/reason wording retained"
    - source: STOP
      target: 停止条件
      mode: exact
      evidence: "ordered list retained"
    - source: FLOW
      target: 作業手順
      mode: expanded
      evidence: "opcode order and detail retained"
    - source: VERIFY
      target: 検証
      mode: exact
      evidence: "requirements retained as not-yet-executed"
    - source: OUT
      target: 報告形式
      mode: structured
      evidence: "kdsl-r1c@0.1-draft request retained"
    - source: AUTHORITY
      target: authority/禁止
      mode: exact
      evidence: "all six rails retained"
    - source: NORMALIZE
      target: normalization provenance
      mode: exact
      evidence: "required/target/not_normalized retained; not converted to permission"
PRESERVE:
  exact_strings:
    - "repository: tk999jp/example"
    - "src/Example.cs"
    - "git diff --check"
    - "kdsl-r1c@0.1-draft"
  protected_wording:
    - "Broad refactor prohibited"
    - "Commit/push/release not authorized"
    - "Root cause remains unconfirmed"
    - "authority not established"
  ordered_fields:
    - "FLOW-READ>FLOW-ANALYZE>FLOW-GATE>FLOW-CHANGE>FLOW-VERIFY>FLOW-REPORT"
    - "STOP: Unexpected diff outside TGT > Root cause remains unconfirmed"
UNRESOLVED: []
LOSS: []
ROUND_TRIP:
  state: not_tested
  structural_equivalence: not_proven
  semantic_equivalence: not_proven
AUTHORITY:
  source_rails_preserved: true
  execution_authority: none
OUTPUT:
  marker: KDSL_PROMPT_PREVIEW
  executable: false
  preview: |
    KDSL_PROMPT_PREVIEW:
    format: KDSL
    profile: dev-prompt
    mode: min
    safety: lock-critical
    Phase: TASK-CHANGE / Example duplicate entry correction
    目的: Confirm the cause and apply the smallest safe correction
    前提:
    - repository: tk999jp/example
    - READ: src/Example.cs
    - OBS: Duplicate entry observed after refresh
    - Root cause is not confirmed; 未確認を確認済扱い禁止
    対象Slice:
    - src/Example.cs
    非対象/禁止:
    - Broad refactor prohibited
    - Commit/push/release not authorized
    - TGT外変更禁止
    Safety Gates:
    - SG-SCOPE hold / preflight pending
    - SG-EVIDENCE hold / cause not confirmed
    - SG-AUTHORITY hold / authority not established
    - SG-STOP satisfied / stop condition declared
    停止条件:
    - Unexpected diff outside TGT
    - Root cause remains unconfirmed
    作業手順:
    - FLOW-READ: Inspect exact READ references
    - FLOW-ANALYZE: Separate observation from inference
    - FLOW-GATE: Evaluate required Safety Gates
    - FLOW-CHANGE: Change exact TGT only after approved normalization and authority
    - FLOW-VERIFY: Run git diff --check and relevant tests
    - FLOW-REPORT: Return KDSL_RESULT using requested schema
    検証:
    - git diff --check
    - relevant tests
    - 未実行verifyをpass扱禁止
    報告形式:
    - KDSL_RESULT / kdsl-r1c@0.1-draft
    Authority:
    - read: target_only
    - edit: not_requested
    - stage: not_requested
    - commit: propose_only
    - push: forbid
    - release: forbid
```

Boundary:

```text
KDSL_PROMPT_PREVIEW != KDSL_PROMPT
STATUS remains non-executable
ROUND_TRIP:not_tested
semantic_equivalence:not_proven
execution_authority:none
```
