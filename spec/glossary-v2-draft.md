# KDSL v2 Draft Glossary

status: v2-draft
canonical: no
source_alignment: spec/manifest.md / spec/adps/* / spec/packet/* / spec/bridge/*

This file supplements `spec/glossary.md`. It does not replace canonical Core/R1/Bridge meanings.

## 1. Architecture axes

```text
profile:=用途別運用仕様
mode:=圧縮強度
safety:=安全保持強度
lexicon:=宣言済み語彙/alias集合
envelope:=prompt/resultを包む契約形式
```

```text
profile: compact-prompt|dev-prompt|converter|lint
mode: readable|min|dense|lock
safety: normal|lock-critical|lock-all
lexicon: standard|kanji-v1
envelope: plain|packet-draft|result
```

```text
lexicon != mode
lexicon != profile
unknown profile/mode/safety/lexicon/envelope推測禁止
```

## 2. CompactPrompt terms

### KDSL-CP

```text
KDSL-CP:=profile:compact-prompt
```

一般LLM/Project files/単体prompt向け。実装・repo・runtime・public操作を含む場合はCP-Lift必須。

### KDSL-CP漢

```text
KDSL-CP漢:=profile:compact-prompt + mode:dense + lexicon:kanji-v1
```

新しいmodeではない。

### kanji-v1

```text
kanji-v1:=KDSL-CP向け構造漢字alias lexicon
keys: 役/目/材/出/則/守/調/確
```

構造KEY位置のみ。Core保護語の一字短縮・上書は禁止。

### CP-Lift

```text
CP-Lift:=KDSL-CP適用外の実装/repo/runtime/public操作をprofile:dev-promptへ昇格する境界処理
```

## 3. Safety Gate terms

### Registry / SG

```text
Registry:=既存正本意味を参照するID/state/composition集合
SG:=Safety Gate Registry entry/reference
registry: kdsl-sg@0.1-draft
```

```text
Registry != authority
SG ID != permission
SG ID-only compression禁止
unknown SG ID/state→blocked
hold/blocked gate削除禁止
```

### SG state

```text
hold:=前提/evidence/承認未充足
satisfied:=必要根拠とauthorityがexact scope内で充足
blocked:=違反/衝突/停止条件発火
na:=非該当を理由付きで確認
```

```text
state:satisfied != unrelated authority
single gate satisfied != composite safety satisfied
validator/property pass != complete safety proof
```

## 4. ADPS contract terms

### KDSL-DP

```text
KDSL-DP:=ADPS向けAuthoring形式。実行指示ではない
```

```text
KDSL-DP直接実行禁止
KDSL-DPをAI coding toolへ直接実装指示として渡すこと禁止
KDSL-DP→P1L/P1正規化必須
```

### P1L

```text
P1L:=lossless structured normalized contract candidate
schema: kdsl-p1l@0.1-draft
```

```text
STATUS: contract-candidate
executable: no
BINDING.state: unbound
BINDING.executable: false
P1L valid/lint/round-trip pass != authority
```

### P1

```text
P1:=canonical P1Lのreversible compact serialization
schema: kdsl-p1@0.1-draft
```

```text
P1 != independent canonical contract
P1|SCHEMA=kdsl-p1@0.1-draft|STATUS=contract-candidate|...
P1→P1L再構成不能→blocked / P1L fallback
```

### P1 authority rails

```text
read/edit/stage/commit/push/release/public_repo/destructive_ops
```

```text
missing/implicit rail→blocked
read allow != edit allow
commit allow != push allow
push allow != release allow
not_requested != allow
propose_only != operation authority
PLAN/FLOW != authority
```

### Profile completion

```text
profile completion:=exact profile id/revision/digestとfield-specific default evidenceによる機械的補完
```

```text
profile completion != inference
completed valueはcanonical projectionへ展開必須
similar-name/memory/convention completion禁止
unknown alias/preset/profile→blocked
```

### P1L/P1 normalization state

```text
explicit|profile_completed|lossy|blocked
```

```text
critical unresolved/loss→blocked
lossy→runtime binding禁止
semantic_equivalence:not_proven固定
structural_pass != semantic equivalence|safety proof|authority
```

### BINDING

```text
BINDING:=contract validityとruntime execution readinessを分離するblock
state: unbound|bound|blocked
```

`kdsl-p1l@0.1-draft` / `kdsl-p1@0.1-draft`では`executable:false`固定。

### Legacy operational P1

```text
legacy operational P1:=project-local `P1|M:...|T:F|...` forms
```

```text
legacy form != kdsl-p1@0.1-draft conformance
loss=P→exact compatibility evidence時のみprofile_completed候補
loss=L意味推測禁止
AP/H意味推測禁止
Authority rails不在→canonical promotion blocked
```

## 5. Packet terms

### KDSL-Packet / PACKET_DRAFT

```text
KDSL-Packet:=non-executable authoring/transport envelope
schema: kdsl-packet@0.1-draft
marker: PACKET_DRAFT
```

```text
STATUS: non-executable
NORMALIZE.required: true
NORMALIZE.state: not_normalized
AI coding tool直接投入禁止
PKT:v1使用禁止
```

### BASE / TASK / FLOW

```text
BASE:=normalization baseline classification
TASK:=task/risk classification
FLOW:=ordered semantic work-state labels
```

ID/opcodeはauthority・command・success claimではない。

### NORMALIZATION_DRAFT

```text
NORMALIZATION_DRAFT:=Packet source→target mapping/loss/round-trip evidence artifact
schema: kdsl-packet-normalization@0.1-draft
```

```text
STATUS: non-executable
TARGET.executable:false
ROUND_TRIP.semantic_equivalence:not_proven
AUTHORITY.execution_authority:none
Packet source remains not_normalized
```

### Packet→P1L/P1 normalization

```text
contract: kdsl-packet-p1-normalization@0.1-draft
applicable BASE: BASE-ADPS-P1
NORMALIZE.target: P1L|P1
```

Phase 7D target-specific first sliceで統合済み。

```text
TARGET.resolution: resolved
TARGET.executable: false
P1L/P1 model/property first slice pass required
Packet normalized-state promotion: not implemented
```

Authority mapping:

```text
read/edit/stage/commit/push/release:=source exact copy
public_repo:=forbid
destructive_ops:=forbid
```

追加2 railは明示的な非拡張safety floorであり、hidden defaultやpermission grantではない。

### P1L_PREVIEW

```text
P1L_PREVIEW:=canonical P1L projectionをJSONで保持する非実行preview marker
```

```text
P1L_PREVIEW != P1L:
canonical top-level P1L marker露出禁止
```

### P1_PREVIEW

```text
P1_PREVIEW:=canonical P1 serializationをJSON stringで保持する非実行preview marker
```

```text
P1_PREVIEW != P1|
canonical top-level P1 marker露出禁止
```

### Structural round-trip

```text
structural round-trip:=required fields/order/exact strings/authority railsを再構成比較する検査
```

```text
structural_pass != semantic equivalence
structural_pass != complete safety proof
structural_pass != runtime binding
structural_pass != authority
structural_pass != Packet normalized
```

## 6. Result terms

### R1 / R1C

```text
R1:=execution evidence/result-reporting specification
R1C:=canonical R1/KDSL_RESULTのcompact serialization profile
schema: kdsl-r1c@0.1-draft
```

```text
R1C != independent canonical result spec
required fields省略禁止
round-trip不成立→Full R1 fallback
```

### RT

```text
p=runtime確認未完了
u=U実機確認待ち
v=対象環境runtime確認済
na=runtime対象なし
fail=runtime確認失敗
blk=runtime確認不能
```

P1L/P1 pre-execution disposition:

```text
pending↔p
user_required↔u
not_applicable↔na
```

`v/fail/blk`はR1/R1Cの実行結果。P1L/P1/previewで自己申告禁止。

### NEXT / COMMIT

```text
NEXT:=次候補の提案。次task実行許可ではない
COMMIT:=実行済commitまたは推奨message。commit authorityではない
```

## 7. Tool / trust terms

### Validator / Property checker

```text
Validator/Property checker:=形式/整合性/欠落/round-trip/propertyを検査する補助器
```

```text
validator/property未実行→pass扱禁止
pass != semantic equivalence
pass != complete safety proof
pass != runtime binding
pass != execution authority
pass != Packet normalized
pass != RT:v
pass != U承認
pass != release readiness
```

## 8. Release strategy

```text
v1.1.0-rc1:=experimental historical baseline
v1.1.0 stable:=hold
v2-draft:=優先設計線
```

この状態はtag/release/Release Assets操作を許可しない。
