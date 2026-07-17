# KDSL Glossary v1.1-v2-sync

目的: `kdsl-spec` 内で使う主要用語を定義し、表記揺れと誤解を減らす。

status: draft-main-v2-sync
source_alignment: spec/core v1.1-v2-sync / manifest v2-draft-sync / bridge v0.3 / P1L-P1 / Packet P1 normalization / R1

## 1. Core terms

### KDSL

```text
KDSL:=LLM直投入可能な安全gate保持型半構造化prompt記法
```

完全な形式言語ではなく、LLM向けの半構造化prompt記法。

### format / profile / mode / safety / lexicon / envelope

```text
format:=記法系。KDSLでは `format: KDSL`
profile:=用途別運用仕様。compact-prompt|dev-prompt|converter|lint
mode:=圧縮強度。readable|min|dense|lock
safety:=安全保持強度。normal|lock-critical|lock-all
lexicon:=宣言済み語彙/alias集合。standard|kanji-v1
envelope:=prompt/resultを包む契約形式。plain|packet-draft|result
```

```text
safety > high-risk判定 > mode > profile > lexicon > envelope
lexicon != mode
lexicon != profile
unknown値推測禁止
```

### operator

```text
→:=条件/処理遷移
=>:=変換/書換
>:=優先
=:=略語定義/短い同値
:=:=扱/状態指定
×:=衝突/不可
/:=並列列挙
```

## 2. Authoring / contract terms

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
P1L:=KDSL-DP等から正規化されたlossless structured contract candidate
schema: kdsl-p1l@0.1-draft
```

```text
P1L valid != executable
P1L lint/round-trip pass != execution authority
BINDING.executable:false
```

### P1

```text
P1:=canonical P1Lに従属するreversible compact serialization
schema: kdsl-p1@0.1-draft
```

```text
P1 != independent canonical contract
P1 valid != executable
P1→P1L再構成不能→blocked / P1L fallback
```

### Profile completion

```text
Profile completion:=exact profile id/revision/digestとfield-specific default evidenceによる機械的補完
```

```text
completion != inference
completed valueはcanonical projectionへ展開必須
similar-name/memory/convention completion禁止
unknown profile/alias/preset→blocked
```

### P1L / P1 normalization state

```text
explicit|profile_completed|lossy|blocked
```

```text
critical unresolved/loss→blocked
lossy→runtime binding禁止
semantic_equivalence:not_proven固定
```

### BINDING

```text
BINDING:=contract validityとruntime execution readinessを分離するblock
state: unbound|bound|blocked
```

`kdsl-p1l@0.1-draft` / `kdsl-p1@0.1-draft`では`executable:false`固定。

### K1 / PF1

```text
K1/PF1:=Runtime Control系の実行制御層
```

現status:

```text
canonical詳細仕様は本repoでは未整備
P1L/P1 schema adoptionから推測・自動生成禁止
```

### Legacy operational P1

```text
Legacy operational P1:=project-local `P1|M:...|T:F|...` forms
```

```text
legacy form != kdsl-p1@0.1-draft conformance
loss=P→exact compatibility evidence時のみprofile_completed候補
loss=L意味推測禁止
AP/H意味推測禁止
missing Authority rails→canonical promotion blocked
```

## 3. Packet / normalization terms

### KDSL-Packet / PACKET_DRAFT

```text
KDSL-Packet:=non-executable authoring/transport schema
PACKET_DRAFT:=top-level marker
schema: kdsl-packet@0.1-draft
```

```text
STATUS: non-executable
NORMALIZE.required:true
NORMALIZE.state:not_normalized
AI coding tool直接投入禁止
PKT:v1使用禁止
```

### NORMALIZATION_DRAFT

```text
NORMALIZATION_DRAFT:=Packet source→target mapping/loss/round-trip evidence artifact
schema: kdsl-packet-normalization@0.1-draft
```

```text
STATUS: non-executable
TARGET.executable:false
semantic_equivalence:not_proven
AUTHORITY.execution_authority:none
Packet source remains not_normalized
```

### Packet→P1L/P1 normalization

```text
Packet→P1L/P1 normalization:=BASE-ADPS-P1 Packetをcanonical P1L/P1 projectionへ写像するtarget-specific non-executable normalization
schema: kdsl-packet-p1-normalization@0.1-draft
```

Phase 7D first sliceで統合済み。

```text
NORMALIZE.target: P1L|P1
TARGET.resolution: resolved
TARGET.executable:false
property pass != Packet normalized|runtime binding|authority
```

Authority mapping:

```text
read/edit/stage/commit/push/release:=source exact copy
public_repo:=forbid
destructive_ops:=forbid
```

追加2 railは明示的な非拡張safety floor。hidden default・permission grantではない。

### P1L_PREVIEW

```text
P1L_PREVIEW:=canonical P1L projectionをJSONで保持する非実行preview marker
```

```text
P1L_PREVIEW != P1L:
P1L_PREVIEWをcanonical top-level P1L contract扱い禁止
```

### P1_PREVIEW

```text
P1_PREVIEW:=canonical P1 serializationをJSON stringで保持する非実行preview marker
```

```text
P1_PREVIEW != P1|
P1_PREVIEWをcanonical top-level P1 contract扱い禁止
```

### Structural round-trip

```text
Structural round-trip:=required fields/order/exact strings/authority railsの再構成比較
```

```text
structural_pass != semantic equivalence
structural_pass != complete safety proof
structural_pass != runtime binding
structural_pass != execution authority
structural_pass != Packet normalized
```

## 4. Result / evidence terms

### R1

```text
R1:=Evidence / 実行結果証跡 / AI作業結果の検収仕様
```

### R1C

```text
R1C:=canonical R1/KDSL_RESULTのcompact serialization profile
schema: kdsl-r1c@0.1-draft
```

```text
R1C != independent canonical result spec
required fields省略禁止
round-trip不成立→Full R1 fallback
```

### KDSL_PROMPT

```text
KDSL_PROMPT:=AI coding tool向けKDSL作業契約block
```

```text
先頭固定
前置き自然文禁止
D禁止時出力禁止
P1L/P1/preview validのみで生成許可扱い禁止
```

### KDSL_RESULT

```text
KDSL_RESULT:=R1系の人間/AI向け結果block
```

Required:

```text
STATUS/PHASE/S/FILES/WHY/CMD/VERIFY/RT/RISK/NEXT/COMMIT
```

### Evidence classes

```text
OBSERVED:=ログ/実機/実行結果/差分により観測
INFERRED:=観測から推論したが直接観測ではない
NOT_OBSERVED:=確認対象だが観測されなかった
UNVERIFIED:=未確認
```

```text
INFERRED→OBSERVED昇格禁止
NOT_OBSERVED→確認済扱禁止
UNVERIFIED→RT:v根拠禁止
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

`v/fail/blk`はR1/R1C result only。P1L/P1/previewで実行前claim禁止。

### NEXT

```text
NEXT:=次候補の提案。次task実行許可ではない
```

### COMMIT

```text
COMMIT:=実行済commitまたは推奨message。commit authorityではない
```

## 5. Safety / authority terms

### D禁止

```text
D禁止:=要件/方針/rollback/revert/再実装/未push破棄/正本/UI契約/data schema/public API/保存形式/public履歴変更等を含む場合に実装指示を禁止するgate
```

### high-risk

```text
high-risk:=D禁止/rollback/revert/未確認/未実行/承認gate/実機確認分離/public履歴/tag/Release Assets/data migration/正本変更/破壊操作/KDSL-DP境界/RT:v/NEXT/COMMIT
```

### Authority / AUTHORITY

```text
Authority:=operation別の許可状態
AUTHORITY:=権限状態を明示するblock
```

P1L/P1 required rails:

```text
read/edit/stage/commit/push/release/public_repo/destructive_ops
```

Values:

```text
allow|forbid|target_only|allow_once|propose_only|not_requested|not_applicable
```

```text
missing/implicit rail→blocked
read allow != edit allow
edit allow != commit allow
commit allow != push allow
push allow != release allow
not_requested != allow
propose_only != operation authority
PLAN/FLOW != authority
```

### public履歴 / Release Assets

```text
public履歴:=公開済repo/history/tag/releaseの変更履歴
Release Assets:=GitHub Release等の公開配布物
```

```text
public履歴改竄禁止
公開済tag移動禁止
Release Assets上書前提操作禁止
```

## 6. Tool / actor terms

### Validator / Property checker

```text
Validator/Property checker:=形式/整合性/欠落/authority conflict/round-trip/propertyを検査する補助器
```

```text
未実行→pass扱禁止
pass != semantic equivalence
pass != complete safety proof
pass != runtime binding
pass != execution authority
pass != Packet normalized
pass != RT:v
pass != U承認
pass != release readiness
```

### U / OrchestratorLLM / AI tool

```text
U:=ユーザー
OrchestratorLLM:=意図整理/KDSL生成/P1L-P1正規化/R1検収/safety gate管理を行う統括LLM
AI tool:=runtime binding/authorityを満たしたKDSL_PROMPT範囲内で作業・報告するAI coding tool
```
