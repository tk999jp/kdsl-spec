# Packet Semantic Property Example

status: v2-draft example
canonical: no
executable: no

```yaml
PACKET_DRAFT:
SCHEMA: kdsl-packet@0.1-draft
STATUS: non-executable
BASE:
  registry: kdsl-packet-base@0.1-draft
  id: BASE-KDSL-DEV
TASK:
  registry: kdsl-packet-task@0.1-draft
  id: TASK-CHANGE
SRC:
  - "repository: tk999jp/example"
  - "branch: main"
READ:
  - "src/Example.cs"
  - "tests/Example.Tests.cs"
TGT:
  - "src/Example.cs"
OBS:
  - "observed: duplicate entry appears after refresh"
  - "inferred: cache invalidation may be involved"
  - "unverified: root cause is not confirmed"
GOAL: "Confirm the cause and apply the smallest safe correction"
NON:
  - "TGT外変更禁止"
  - "Broad refactor prohibited"
  - "未確認を確認済扱い禁止"
  - "build/diff/lint/test/CI pass != RT:v"
  - "NEXT実行許可扱禁止"
  - "COMMIT自動commit許可扱禁止"
  - "KDSL-DP直接実行禁止"
  - "P1/P1L正規化必須"
  - "Commit/push/release not authorized"
SG:
  registry: kdsl-sg@0.1-draft
  entries:
    - id: SG-SCOPE
      state: hold
      scope: "src/Example.cs"
      reason: "exact target preflight pending"
      evidence: "TGT and READ declared"
      authority: "none"
    - id: SG-EVIDENCE
      state: hold
      scope: "root cause"
      reason: "cause remains unverified"
      evidence: "OBS separates observed/inferred/unverified"
      authority: "not_required"
    - id: SG-RUNTIME
      state: hold
      scope: "target Windows runtime"
      reason: "runtime未実行"
      evidence: "none"
      authority: "not_required"
    - id: SG-AUTHORITY
      state: hold
      scope: "edit/stage/commit/push/release"
      reason: "operation authority not established"
      evidence: "AUTHORITY rails recorded"
      authority: "not_established"
    - id: SG-KDSL-DP
      state: satisfied
      scope: "authoring-to-execution boundary"
      reason: "direct execution prohibited and normalization required"
      evidence: "KDSL-DP直接実行禁止 / P1/P1L正規化必須"
      authority: "not_required"
    - id: SG-STOP
      state: satisfied
      scope: "unexpected diff or unconfirmed cause"
      reason: "停止条件 declared"
      evidence: "STOP entries present"
      authority: "not_required"
STOP:
  - "Unexpected diff outside TGT"
  - "Root cause remains unconfirmed"
  - "Required authority remains unavailable"
FLOW:
  registry: kdsl-packet-flow@0.1-draft
  steps:
    - op: FLOW-READ
      detail: "Inspect exact READ references"
    - op: FLOW-ANALYZE
      detail: "Separate observation from inference"
    - op: FLOW-GATE
      detail: "Evaluate all declared Safety Gates and stop on blocked state"
    - op: FLOW-CHANGE
      detail: "Change exact TGT only after approved normalization and SG-AUTHORITY satisfaction"
    - op: FLOW-VERIFY
      detail: "Run git diff --check and relevant unit tests as requirements"
    - op: FLOW-REPORT
      detail: "Return KDSL_RESULT using kdsl-r1c@0.1-draft"
VERIFY:
  - "git diff --check"
  - "relevant unit tests"
  - "target runtime remains not_run"
OUT:
  result_schema: kdsl-r1c@0.1-draft
AUTHORITY:
  read: target_only
  edit: not_requested
  stage: not_requested
  commit: propose_only
  push: forbid
  release: forbid
NORMALIZE:
  required: true
  target: full-kdsl-dev-prompt
  state: not_normalized
```

Boundary:

```text
Packet semantic/property pass != semantic equivalence
Packet semantic/property pass != safety proof
Packet semantic/property pass != execution authority
KDSL-Packet直接実行禁止
```
