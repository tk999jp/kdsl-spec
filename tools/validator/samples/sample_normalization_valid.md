NORMALIZATION_DRAFT:
SCHEMA: kdsl-packet-normalization@0.1-draft
STATUS: non-executable
SOURCE:
  schema: kdsl-packet@0.1-draft
  digest: "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
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
      target: "provenance"
      mode: exact
      evidence: "retained"
    - source: STATUS
      target: "provenance"
      mode: exact
      evidence: "retained"
    - source: BASE
      target: "header"
      mode: structured
      evidence: "retained"
    - source: TASK
      target: "task"
      mode: structured
      evidence: "retained"
    - source: SRC
      target: "source"
      mode: exact
      evidence: "retained"
    - source: READ
      target: "read"
      mode: exact
      evidence: "retained"
    - source: TGT
      target: "target"
      mode: exact
      evidence: "retained"
    - source: OBS
      target: "observation"
      mode: exact
      evidence: "retained"
    - source: GOAL
      target: "goal"
      mode: exact
      evidence: "retained"
    - source: NON
      target: "non-goal"
      mode: exact
      evidence: "retained"
    - source: SG
      target: "safety"
      mode: expanded
      evidence: "retained"
    - source: STOP
      target: "stop"
      mode: exact
      evidence: "retained"
    - source: FLOW
      target: "flow"
      mode: expanded
      evidence: "retained"
    - source: VERIFY
      target: "verify"
      mode: exact
      evidence: "retained"
    - source: OUT
      target: "result"
      mode: structured
      evidence: "retained"
    - source: AUTHORITY
      target: "authority"
      mode: exact
      evidence: "retained"
    - source: NORMALIZE
      target: "normalization provenance"
      mode: exact
      evidence: "retained"
PRESERVE:
  exact_strings:
    - "src/Example.cs"
  protected_wording:
    - "KDSL_PROMPT_PREVIEW != KDSL_PROMPT"
  ordered_fields:
    - "FLOW-READ>FLOW-GATE>FLOW-REPORT"
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
    execution: prohibited
