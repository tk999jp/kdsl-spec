format: KDSL
profile: dev-prompt
mode: min
safety: lock-critical
lexicon: standard
envelope: plain

KDSL_PROMPT:
GOAL: "Inspect one repository"
INPUT:
  repo: tk999jp/kdsl-spec
  branch: main
GUARD: "KDSL-DP直接実行禁止"
CHECK:
  - parser
  - lint
