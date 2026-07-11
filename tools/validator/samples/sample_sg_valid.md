KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: lock-critical

SAFETY_GATES:
  registry: kdsl-sg@0.1-draft
  entries:
    - id: SG-SCOPE
      state: satisfied
      scope: repository preflight
      reason: exact target and non-target confirmed
      evidence: git status and diff inspected
      authority: not_required
    - id: SG-EVIDENCE
      state: satisfied
      scope: reported observations
      reason: executed evidence separated from inference
      evidence: command output recorded
      authority: not_required
    - id: SG-AUTHORITY
      state: satisfied
      scope: edit target files only
      reason: prompt grants edit authority
      evidence: authority block inspected
      authority: target_only
    - id: SG-STOP
      state: satisfied
      scope: preflight stop conditions
      reason: no mismatch observed
      evidence: preflight passed
      authority: not_required

Guard:
- 未確認→確認済扱禁止
