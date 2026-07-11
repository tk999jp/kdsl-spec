# KDSL-CP / KDSL-Packet Bridge v0.6-draft

status: v2-draft
scope: CompactPrompt lift / Full KDSL boundary / Safety Gate Registry / R1C / Packet normalization / non-executable boundary

## 1. Purpose

This bridge defines when KDSL-CP must be lifted to Full KDSL, how Safety Gate/R1C/Packet normalization references are bounded, and why Packet authoring and normalization previews remain non-executable.

```text
KDSL-CP:=一般LLM / Project files / 単体prompt向け軽量profile
Full KDSL dev-prompt:=現行のAI coding tool向け実行可能契約
kdsl-sg@0.1-draft:=既存safety意味を参照するv2-draft Registry
kdsl-r1c@0.1-draft:=canonical R1のv2-draft compact serialization profile
kdsl-packet-normalization@0.1-draft:=Packet mapping/loss/round-trip evidence contract
KDSL-Packet:=v2-draft adopted authoring envelope / non-executable
```

KDSL-CP must not become a shortcut for unsafe implementation instructions.

## 2. CP-Lift triggers

```text
実装/改修/削除を含む
repo/path/branch/commit操作を含む
file/API/command変更を含む
rollback/revertを含む
未push破棄を含む
RT:v/実機確認を含む
public履歴/tag/Release Assetsを含む
data migrationを含む
正本変更を含む
AI coding toolへ渡す場合
```

If any trigger is present:

```text
KDSL-CP単体実装指示禁止
現行: Full KDSL profile:dev-promptへ昇格
将来: Packet validator/normalization/execution promotion条件全充足後のみ実行可能性を再審査
必要safety gate明示必須
```

## 3. Current executable lift target

Current executable lift target:

```text
KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min|dense|lock
safety: lock-critical|lock-all
...
```

Rules:

```text
KDSL_PROMPT先頭固定
KDSL_PROMPT前自然文禁止
D禁止時KDSL_PROMPT出力禁止
KDSL_RESULT報告要求保持
```

## 4. Mapping: CP to Full KDSL / Packet authoring

```text
KDSL-CP Role    → task role / responsibility
KDSL-CP Goal    → goal / target
KDSL-CP Input   → source / read / observed
KDSL-CP Output  → required output
KDSL-CP Rules   → flow / verify / task rules
KDSL-CP Guard   → safety gate / stop conditions / SG references
KDSL-CP Style   → response style / human render
KDSL-CP Check   → verify / lint / result requirements
```

Mapping does not grant edit/commit/push/release authority.

## 5. Safety Gate Registry alignment

Current v2-draft registry:

```text
registry: kdsl-sg@0.1-draft
source: spec/registry/kdsl-safety-gate-registry.md
composition: spec/registry/kdsl-safety-gate-composition.md
lint: spec/lint/kdsl-safety-gate-registry-lint.md
```

Candidate IDs adopted in the v2-draft manifest:

```text
SG-DESIGN
SG-SCOPE
SG-EVIDENCE
SG-RUNTIME
SG-AUTHORITY
SG-ROLLBACK
SG-PUBLIC
SG-DATA
SG-KDSL-DP
SG-STOP
```

State model:

```text
hold|satisfied|blocked|na
```

Usage boundary:

```text
SG ID:=補助参照
SG ID != permission
state:satisfied != unrelated authority
unknown registry/SG ID推測禁止
blocked/hold gate削除禁止
specialized gate != broader gate解除
current Full KDSL:=SG ID + complete protected wording
SG IDのみで禁止/未確認/承認/RT:v条件を置換禁止
```

Typed non-substitution:

```text
U承認 != runtime evidence
runtime evidence != commit/push/release authority
CI/validator pass != semantic equivalence
CI/validator pass != U承認
NEXT != execution authority
COMMIT.proposed != commit authority
```

## 6. R1C alignment

Current v2-draft serialization profile:

```text
schema: kdsl-r1c@0.1-draft
source: spec/r1/r1c-compact-result-schema.md
canonical parent: spec/r1/r1-result-spec.md
lint: spec/lint/kdsl-r1c-lint.md
validator: tools/validator/kdsl_r1c.py
```

Ownership boundary:

```text
canonical R1 > R1C serialization profile
R1C != 独立canonical結果仕様
R1C envelope:=KDSL_RESULT
canonical 11 required field名保持
short field alias禁止
implicit default禁止
round-trip不成立→Full R1 fallback
RT:v/NEXT/COMMIT意味変更禁止
R1C validator pass != semantic equivalence/canonical R1適合証明
```

Packet effect:

```text
R1C v2-draft採用 != Packet executable
R1C validator実装 != Packet executable
OUT/R1C mappingはPacket authoring fieldであり実行許可ではない
```

## 7. KDSL-Packet adopted non-executable boundary

Current v2-draft components:

```text
schema: kdsl-packet@0.1-draft
source: spec/packet/kdsl-packet-schema.md
BASE registry: kdsl-packet-base@0.1-draft
TASK registry: kdsl-packet-task@0.1-draft
FLOW registry: kdsl-packet-flow@0.1-draft
lint: spec/lint/kdsl-packet-lint.md
validator: first heuristic slice integrated
normalization contract: spec/packet/kdsl-packet-normalization-contract.md
normalization lint: spec/lint/kdsl-packet-normalization-lint.md
```

Adoption boundary:

```text
Packet schema/registry/lint:=v2-draft adopted
KDSL-Packet:=non-executable authoring/transport envelope
STATUS:non-executable固定
NORMALIZE.required:true固定
NORMALIZE.state:not_normalized固定
BASE/TASK/FLOW ID/opcode != authority
normalization artifact未生成/未検証→実行禁止
```

Unresolved execution dependencies:

```text
normalization validator/mapper and round-trip proof
Safety Gate completeness/inheritance proof
stable/canonical execution dependency
explicit executable promotion review/U承認
```

Therefore:

```text
KDSL-Packet未正規化→実行指示扱禁止
Packet valid-looking/lint-looking != executable
PKT:v1使用禁止
unknown BASE/TASK/FLOW/SG/R1C推測禁止
validator未実装→Packet lint pass扱禁止
```

Required design notation:

```text
PACKET_DRAFT:
SCHEMA: kdsl-packet@0.1-draft
STATUS: non-executable
...
NORMALIZE:
  required: true
  state: not_normalized
```

This notation remains design/authoring input only and must not be passed directly to an AI coding tool as an implementation contract.

## 8. Packet normalization alignment

Current v2-draft contract:

```text
schema: kdsl-packet-normalization@0.1-draft
source: spec/packet/kdsl-packet-normalization-contract.md
lint: spec/lint/kdsl-packet-normalization-lint.md
validator/mapper: not implemented
```

Required boundary:

```text
NORMALIZATION_DRAFT:=non-executable evidence artifact
STATUS:non-executable固定
TARGET.executable:false固定
AUTHORITY.execution_authority:none固定
semantic_equivalence:not_proven固定
KDSL_PROMPT_PREVIEW != KDSL_PROMPT
```

Target resolution:

```text
design-only→resolved review preview
full-kdsl-dev-prompt→resolved KDSL_PROMPT_PREVIEW
P1/P1L→blocked until canonical target field schema exists
unknown target schema推測禁止
```

Promotion boundary:

```text
contract/lint adoption != normalization completion
structural_pass != semantic equivalence/safety proof/authority
normalization validator/mapper未実装→Packet normalized扱禁止
executable target generation→separate specification/review/U承認必須
```

## 9. Packet-Summary

Packet-Summary may summarize an adopted non-executable Packet authoring record to KDSL-CP for human-facing or Project file use.

```text
BASE/TASK/SG/FLOW → Guard/Rulesへ要約
SRC/READ/OBS/GOAL/NON → Input/Goal/Guardへ要約
OUT/R1C → Output/Checkへ要約
```

Packet-Summary is a view, not the original execution contract.

## 10. Summary restrictions

```text
D禁止削除禁止
RT:v条件削除禁止
NEXT/COMMIT権限分離削除禁止
rollback/revert条件削除禁止
public履歴/公開済tag/Release Assets保護削除禁止
repo安全条件の過剰要約禁止
hold/blocked Safety Gate削除禁止
SG ID-only compression禁止
```

## 11. Boundary examples

### 11.1 KDSL-CP is enough

```text
KDSL-CP漢:
役: 小説編集者/批評者
目: novel input→多角review+改善提案
材: novel_text
出: 総評/魅力/弱点/改善案
守: 入力外設定追加禁止, 不明→断定禁止
確: 本文根拠あり, 抽象論のみ禁止
```

Reason:

```text
repo操作なし
実装なし
runtime/R1不要
```

### 11.2 CP-Lift required

```text
KDSL-CP:
Goal: QuickAccessDialogのTab順を修正
Input: repo path / target file / observed UI bug
```

Reason:

```text
実装/改修を含む
file/pathを含む
AI coding toolへ渡す
→ Full KDSL profile:dev-promptへ昇格
```

Full KDSL safety reference example:

```text
SAFETY_GATES:
  registry: kdsl-sg@0.1-draft
  entries:
    - id: SG-SCOPE
      state: hold
      scope: target Phase
      reason: preflight確認待ち
    - id: SG-AUTHORITY
      state: hold
      scope: edit/commit/push
      reason: operation別authority確認待ち

Guard:
- 原因未確→広域修正禁止
- 未帰属差分へ上乗せ禁止
- authority未確認→実行禁止
```

### 11.3 Packet design draft only

```text
PACKET_DRAFT:
SCHEMA: kdsl-packet@0.1-draft
STATUS: non-executable
fields: BASE/TASK/SRC/READ/TGT/OBS/GOAL/NON/SG/STOP/FLOW/VERIFY/OUT/AUTHORITY/NORMALIZE
```

```text
AI coding tool直接投入禁止
canonical Packet schema/registry完成後に再評価
```

## 12. Non-goals

```text
KDSL-DP/P1/P1L境界変更
R1/KDSL_RESULT意味変更
RT:v条件緩和
KDSL-CPをAI coding tool実装契約として扱うこと
SG IDによる保護語置換
Registryによる実行権限付与
未定義Packet直接実行
NORMALIZATION_DRAFT/KDSL_PROMPT_PREVIEW直接実行
P1/P1L schema推測
```
