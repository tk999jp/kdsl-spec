# Dev Prompt Safety Gate State Example

status: v2-draft example
canonical: no
executable: no
source_candidate: spec/registry/kdsl-safety-gate-registry.md

## Example

```text
KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: lock-critical
Phase: Example safe corrective

SAFETY_GATES:
  registry: kdsl-sg@0.1-draft
  entries:
    - id: SG-SCOPE
      state: satisfied
      scope: target dialog / one corrective Slice
      reason: target/non-target and observed mismatch are separated
      evidence: inspected source/diff/runtime observation
      authority: target_only

    - id: SG-EVIDENCE
      state: satisfied
      scope: reported inspection and executed checks only
      reason: observed/inferred/unverified are separated
      evidence: command output/diff/log references
      authority: not_required

    - id: SG-RUNTIME
      state: hold
      scope: target Windows UI runtime
      reason: runtime verification has not been performed after the change
      evidence: none
      authority: U実機確認待ち

    - id: SG-AUTHORITY
      state: hold
      scope: commit/push/release
      reason: edit authority does not grant commit/push/release authority
      evidence: none
      authority: propose_only

    - id: SG-STOP
      state: satisfied
      scope: source/ref/preflight
      reason: required source and target ref are available and no preflight mismatch is observed
      evidence: source/ref/preflight records
      authority: not_required

Guard:
- 原因未確→広域修正禁止
- 未確認→確認済扱禁止
- 未実行→実行済扱禁止
- build/diff/lint/test/CI pass != RT:v
- Runtime未確認→RT:p|RT:u, 確認済扱禁止
- KDSL_RESULT NEXT:=提案, 実行許可扱禁止
- KDSL_RESULT COMMIT:=推奨messageまたは実行済commit, 自動commit許可扱禁止
```

## Why both IDs and full wording are present

```text
current Full KDSL:=critical wording remains explicit
SG ID:=review/index/reference aid
SG ID only→protected wording replacement禁止
```

## Invalid compression

```text
SAFETY_GATES:
- SG-RUNTIME: satisfied
- SG-AUTHORITY: satisfied
```

Invalid because:

```text
registry versionなし
scope/reason/evidence/authorityなし
runtime evidenceなし
operation別authority分離なし
protected wordingなし
```

## Packet boundary

This example is not a Packet.

```text
SG registry candidate != Packet schema
SG registry candidate != R1C schema
AI coding toolへこのexampleを直接実装契約として渡すこと禁止
```
