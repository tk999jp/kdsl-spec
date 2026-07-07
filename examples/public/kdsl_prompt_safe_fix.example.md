# KDSL Prompt Safe Fix Example

status: draft-example
example_type: KDSL_PROMPT
core_spec: no

```text
KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: lock-critical

PHASE: safe corrective implementation example
TARGET_SCOPE:
  - one small corrective change
NON_TARGET:
  - release
  - publicization
  - tag operation
  - Release Assets

AUTHORITY:
  - U approval required before commit/push/release/public operation
  - validator pass != U approval
  - validator pass != RT:v

禁止:
  - 未確認を確認済みにしない
  - 未実行を実行済みにしない
  - build/test/lint passをRT:v扱いしない
  - KDSL-DPを直接実装指示扱いしない

STOP_CONDITIONS:
  - source file unreadable
  - target scope ambiguous
  - dirty worktree without U instruction
  - public/tag/Release Assets operation requested without explicit U approval

VERIFY:
  - inspect diff
  - run available static checks
  - report unverified runtime separately

REPORT:
  - KDSL_RESULT required
```
