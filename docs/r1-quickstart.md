# R1 / KDSL_RESULT Quickstart

status: v2-draft-public-guide
last_updated: 2026-07-12
canonical_spec: spec/r1/r1-result-spec.md

## 1. Purpose

R1は、AI支援作業の結果を人間が検収できる形へ分離する結果証跡仕様です。

```text
R1:=Evidence / 結果証跡 / 検収仕様
KDSL_RESULT:=R1系の人間/AI向け結果block
```

このQuickstartは利用導入用です。競合時は [`spec/r1/r1-result-spec.md`](../spec/r1/r1-result-spec.md) を正とします。

## 2. Minimal skeleton

```text
KDSL_RESULT:
STATUS:
PHASE:
S:
FILES:
WHY:
CMD:
VERIFY:
RT:
RISK:
NEXT:
COMMIT:
```

AI coding toolの最終回答では、必要時にこのblockを先頭へ置きます。補足自然文はKDSL_RESULTの後に置きます。

## 3. Field guide

| Field | Purpose |
|---|---|
| `STATUS` | 完了・一部完了・停止・失敗などの状態 |
| `PHASE` | 対象Phase/Slice |
| `S` | 実施結果の短い要約 |
| `FILES` | 変更ファイル。閲覧のみは必要時に分離 |
| `WHY` | 変更理由。観測と推論を混同しない |
| `CMD` | 実行したcommandのみ |
| `VERIFY` | 実行した検証と結果 |
| `RT` | 対象環境Runtime確認状態 |
| `RISK` | 未確認・未実行・残存risk |
| `NEXT` | 次候補の提案。実行許可ではない |
| `COMMIT` | 実行済commitまたは推奨message。commit許可ではない |

## 4. STATUS

Canonical values:

```text
success
partial
blocked
noop
failed
needs_user
```

Use:

```text
success:=指示範囲内で完了
partial:=一部完了/一部未完了
blocked:=停止条件/承認待/前提不一致
noop:=変更不要/対象なし
failed:=実行失敗
needs_user:=U確認/承認が必要
```

## 5. CMD and VERIFY

```text
未実行cmd→CMD記載禁止
推奨cmd/次候補cmd→CMD混入禁止
未実行verify→pass扱禁止
```

Recommended shape:

```text
CMD:
  executed:
    - <実際に実行したcommand>

VERIFY:
  executed:
    - check: <検証名>
      result: pass|failed
  not_run:
    - <未実行検証>
```

実行していないcommandを説明する場合は、`NEXT`または補足説明へ分離します。

## 6. RT

Runtime verification status:

```text
p=runtime確認未完了
u=U実機確認待ち
v=対象環境runtime確認済
na=runtime対象なし
fail=runtime確認失敗
blk=runtime確認不能
```

Critical boundary:

```text
RT:v=対象環境runtime確認済のみ
build pass != RT:v
diff pass != RT:v
lint pass != RT:v
test/CI pass != RT:v
```

RT:vの根拠候補:

```text
対象環境runtime確認
U実機観測
U共有runtime log
明示された実機確認結果
```

RT:vにできないもの:

```text
build成功
unit test成功
静的確認
推測
validator pass
```

Documentation-only workは、理由を明記して `RT: na` とできます。

## 7. Evidence separation

必要時は次の補助blockを追加します。

```text
EVIDENCE:
  OBSERVED:
  INFERRED:
  NOT_OBSERVED:
  UNVERIFIED:
```

```text
OBSERVED:=ログ/実行結果/差分/実機で観測された事実
INFERRED:=観測からの推論
NOT_OBSERVED:=確認対象だが観測されなかった内容
UNVERIFIED:=未確認で確認済扱い禁止の内容
```

Rules:

```text
inferred→observed扱禁止
not_observed→確認済扱禁止
unverified→RT:v根拠禁止
未確認要因→断定禁止
```

## 8. Authority separation

必要時は権限状態を明示します。

```text
AUTHORITY:
  read:
  edit:
  stage:
  commit:
  push:
  release:
```

Representative values:

```text
allow
forbid
target_only
allow_once
propose_only
not_requested
not_applicable
```

Critical boundary:

```text
NEXT != 次task実行許可
COMMIT.proposed != commit許可
report != approval
validator pass != authority
```

## 9. Documentation-only example

```text
KDSL_RESULT:
STATUS: success
PHASE: public documentation update
S: Updated public documentation in the approved scope.
FILES:
  - docs/example.md
WHY: Clarify the public usage guide without changing execution contracts.
CMD:
  executed: []
VERIFY:
  executed:
    - check: document structure review
      result: pass
RT: na / documentation-only
RISK:
  - semantic equivalence is not proven by documentation review
NEXT: proposed: request human review of the wording
COMMIT:
  actual: none
  proposed: "Docs: clarify public guide"
  permission_basis: none
```

This example does not authorize commit, push, release, or stable promotion.

## 10. Runtime-pending example

```text
KDSL_RESULT:
STATUS: partial
PHASE: UI correction
S: Implemented and built the target change; runtime confirmation remains pending.
FILES:
  - src/Example.cs
WHY: Apply the approved minimal correction.
CMD:
  executed:
    - dotnet build
VERIFY:
  executed:
    - check: build
      result: pass
  not_run:
    - target environment runtime verification
RT: u / U実機確認待ち
RISK:
  - runtime_unverified
NEXT: proposed: U confirms the target UI behavior
COMMIT:
  actual: none
  proposed: "Fix: correct target UI behavior"
  permission_basis: none
```

```text
build pass != RT:v
NEXT proposal != execution authority
COMMIT proposed != commit authority
```

## 11. Blocked example

```text
KDSL_RESULT:
STATUS: blocked
PHASE: storage migration
S: No change was made because the rollback and data-recovery conditions are unresolved.
FILES: []
WHY: Destructive-risk preconditions are incomplete.
CMD:
  executed: []
VERIFY:
  executed: []
RT: blk / prerequisite unresolved
RISK:
  - data recovery path unverified
  - rollback condition undefined
NEXT: proposed: define recovery evidence and obtain approval
COMMIT:
  actual: none
  proposed: none
  permission_basis: none
```

## 12. R1C boundary

R1Cはcanonical R1を置換しません。

```text
schema: kdsl-r1c@0.1-draft
status: v2-draft adopted serialization profile
canonical parent: spec/r1/r1-result-spec.md
independent canonical spec: no
```

```text
canonical R1 > R1C serialization profile
R1C validator pass != canonical R1適合証明
R1C adoption != Packet executable
```

## 13. Validation

Unified suite:

```text
python tools/validator/run_all_samples.py
```

R1 wrapper:

```text
python tools/validator/kdsl_validate.py --target r1 <file>
```

R1C wrapper:

```text
python tools/validator/kdsl_validate.py --target r1c <file>
```

Validator boundaries:

```text
validator pass != semantic equivalence
validator pass != complete safety proof
validator pass != U承認
validator pass != RT:v
validator pass != release readiness
```

## 14. Next reading

```text
spec/r1/r1-result-spec.md
spec/r1/r1c-compact-result-schema.md
spec/lint/kdsl-lint-checklist.md
spec/lint/kdsl-r1c-lint.md
examples/public/README.md
```
