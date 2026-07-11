KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: lock-critical

SAFETY_GATES:
  registry: kdsl-sg@0.1-draft
  entries:
    - id: SG-SCOPE
      state: hold
      scope: repository rollback
      reason: rollback target is not isolated
    - id: SG-EVIDENCE
      state: hold
      scope: current diff
      reason: status and diff are not inspected
    - id: SG-AUTHORITY
      state: hold
      scope: rollback operation
      reason: rollback authority is pending
    - id: SG-STOP
      state: hold
      scope: rollback preflight
      reason: preflight is incomplete

Guard:
- rollback前にstatus/diff/退避確認必須
