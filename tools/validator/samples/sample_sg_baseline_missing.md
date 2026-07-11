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
      scope: repository
      reason: preflight is pending
