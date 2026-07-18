# KDSL Glossary v1.1-v2-sync

目的: kdsl-spec内で使う主要用語を定義し、表記揺れと誤解を減らす。

status: draft-main-v2-sync
source_alignment: spec/core v1.1-v2-sync / manifest v2-draft-sync / bridge v0.3 / P1L-P1 v0.1-draft / K1-PF1-binding v0.1-draft / R1 v0.1-draft

## Core terms

### KDSL

```text
KDSL:=LLM直投入可能な安全gate保持型半構造化prompt記法
```

説明:

```text
日本語運用promptを、漢字語幹/記号/最小制御語で再構成する。
完全な形式言語ではなく、LLM向けの半構造化prompt記法。
```

### format / profile / mode / safety / lexicon / envelope

```text
format:=記法系の指定。KDSLでは `format: KDSL`
profile:=用途別運用仕様。compact-prompt/dev-prompt/converter/lint
mode:=圧縮強度。readable/min/dense/lock
safety:=安全保持強度。normal/lock-critical/lock-all
lexicon:=宣言済み語彙/alias集合。standard/kanji-v1
envelope:=prompt/resultを包む契約形式。plain/packet-draft/result
```

制約:

```text
safety > high-risk判定 > mode > profile > lexicon > envelope
mode:converter廃止。converterはprofileで扱う
lexicon != mode
lexicon != profile
packet-draft:=non-executable
unknown profile/mode/safety/lexicon/envelope推測禁止
```

legacy:

```text
rulebook:=v1.1 legacy profile name
rulebook新規使用禁止
rulebookを正式v2 profile扱い禁止
legacy rulebook入力→用途確認なしにcompact-prompt/lintへ自動補正禁止
```

### operator

```text
→:=条件/処理遷移
=>:=変換/書換
>:=優先
=:=略語定義/短い同値
:=:=扱/状態指定
×:=衝突/不可/禁止組合
/:=並列列挙
```

制約:

```text
> 行頭使用禁止
= を扱/状態指定に使用禁止
```

### KDSL-DP

```text
KDSL-DP:=ADPS向けAuthoring形式。実行指示ではない
```

禁止:

```text
KDSL-DP直接実行禁止
KDSL-DPをAI coding toolへ実装指示として渡すこと禁止
KDSL本体の直投入前提をKDSL-DPへ自動継承禁止
```

### P1L

```text
P1L:=KDSL-DP等から正規化されたlossless structured contract candidate
schema: kdsl-p1l@0.1-draft
```

正本:

```text
spec/adps/kdsl-p1l-contract-schema.md
```

制約:

```text
P1L valid != executable
P1L lint/round-trip pass != execution authority
PROFILE completion != inference
all AUTHORITY rails explicit
BINDING.executable:false
RUNTIME pre-execution disposition != R1 result RT
```

### P1

```text
P1:=canonical P1Lに従属するreversible compact serialization
schema: kdsl-p1@0.1-draft
```

正本:

```text
spec/adps/kdsl-p1-compact-contract-schema.md
```

制約:

```text
P1 != 独立canonical contract
P1 valid != executable
P1→P1L再構成不能→blocked/P1L fallback
unknown profile/alias/preset推測禁止
implicit default禁止
```

Legacy boundary:

```text
project-local `P1|M:...|T:F|...`:=legacy operational evidence
loss=P→exact compatibility evidence時のみprofile_completed候補
loss=L意味推測禁止
AP/H意味推測禁止
Authority rails不在→canonical promotion blocked
```

### P1L / P1 normalization

```text
KDSL-DP
→ normalize
P1L
→ optional compact serialization
P1
→ separate runtime binding/authority evaluation
```

```text
KDSL-DP→P1L/P1正規化必須
P1L/P1 schema/lint pass != runtime binding
P1L/P1 structural_pass != semantic equivalence/safety proof/authority
```

### P1L / P1 BINDING

```text
BINDING:=contract validityとruntime execution readinessを分離するblock
```

```text
state: unbound|bound|blocked
executable:false under kdsl-p1l@0.1-draft / kdsl-p1@0.1-draft
runtime control valid != authority sufficient
authority sufficient != executed
```

### K1 / PF1

```text
K1:=canonical runtime-control semantics + exact conforming project/repository instance
PF1:=project-scoped exact defaults/presets/restrictions/authority ceilings/capability requirements/routing definitions
schemas: kdsl-k1@0.1-draft / kdsl-pf1@0.1-draft
canonicalization: kdsl-runtime-control-c14n@0.1-draft
```

```text
K1/PF1 valid|lint pass != executable|authority grant
PF1 may narrow but never widen P1L authority
capability != permission
Stop continuation != authority
routing != authority
binding evidence:=external content-addressed record / schema kdsl-binding-evidence@0.1-draft
BINDING.executable:false under P1L/P1 v0.1 draft
K1/PF1 bounded validator:=integrated / binding evaluator:=not implemented
```

### Binding evidence

```text
binding evidence:=P1L contractとexact K1/PF1評価次元を結ぶexternal content-addressed record
schema: kdsl-binding-evidence@0.1-draft
```

```text
bound != executable|authority sufficient|capability sufficient|RT:v
approval content validity != source trust
capability != authority
all evaluation dimensions/provenance保持必須
```

### R1

```text
R1:=Evidence / 結果証跡 / AI作業結果の検収仕様
```

説明:

```text
AI coding toolの作業結果を、人間と統括LLMが検収できる形にするための仕様。
```

### KDSL_PROMPT

```text
KDSL_PROMPT:=AI coding tool向けKDSL作業契約block
```

制約:

```text
先頭固定
前置き自然文禁止
D禁止時は出力禁止
P1L/P1 validのみで生成許可扱い禁止
```

### KDSL_RESULT

```text
KDSL_RESULT:=R1系の人間/AI向け結果block
```

必須block:

```text
STATUS
PHASE
S
FILES
WHY
CMD
VERIFY
RT
RISK
NEXT
COMMIT
```

## Safety terms

### D禁止

```text
D禁止:=要件変/方針変/rollback/revert/再実装/未push破棄/正本変/UI契約変/妥協案/data schema/public API/保存形式変更を含む場合に実装指示を禁止するgate
```

### high-risk

```text
high-risk:=D禁止/rollback/revert/未確認/未実行/承認gate/実機確認分離/public履歴/公開済tag/Release Assets/data migration/正本変更/UI契約変更/破壊操作/KDSL-DP直接実行/RT:v/KDSL_RESULT NEXT/KDSL_RESULT COMMIT
```

### RT

```text
RT:=Runtime verification status
```

値:

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

```text
v/fail/blk:=R1/R1C result only
P1L/P1で実行前result claim禁止
```

### RT:v

```text
RT:v:=対象環境runtime確認済
```

有効根拠:

```text
対象環境runtime確認
U実機観測
U共有runtime log
明示された実機確認結果
```

無効根拠:

```text
build成功
diff確認
lint pass
unit test pass
静的確認
推測
validator pass
P1L/P1 structural validity
```

### 未確認

```text
未確認:=確認されていない状態
```

制約:

```text
未確認→確認済扱禁止
未確認→成功扱禁止
未確認→断定禁止
```

### 未実行

```text
未実行:=実行されていない状態
```

制約:

```text
未実行→実行済扱禁止
未実行cmd→CMD記載禁止
未実行verify→pass扱禁止
```

## Evidence terms

### Evidence

```text
Evidence:=観測/推論/未観測/未確認を分離した検収材料
```

### OBSERVED

```text
OBSERVED:=ログ/実機/実行結果/差分などにより観測された事実
```

### INFERRED

```text
INFERRED:=観測から推論したが直接観測ではない内容
```

P1L/P1 normalizationでINFERREDをOBSERVEDへ昇格禁止。

### NOT_OBSERVED

```text
NOT_OBSERVED:=確認対象だが観測されなかった内容
```

制約:

```text
NOT_OBSERVED→確認済扱禁止
```

### UNVERIFIED

```text
UNVERIFIED:=未確認であり、確認済み扱いしてはいけない内容
```

制約:

```text
UNVERIFIED→RT:v根拠禁止
```

## Authority terms

### Authority

```text
Authority:=read/edit/stage/commit/push/release/public_repo/destructive_opsの許可状態
```

### AUTHORITY

```text
AUTHORITY:=R1/KDSL_PROMPT/P1L/P1内で権限状態を明示するblock
```

P1L/P1 required keys:

```text
read
edit
stage
commit
push
release
public_repo
destructive_ops
```

推奨値:

```text
allow
forbid
target_only
allow_once
propose_only
not_requested
not_applicable
```

制約:

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

### NEXT

```text
NEXT:=次候補の提案
```

制約:

```text
NEXT != 次task実行許可
NEXT実行許可扱禁止
```

### COMMIT

```text
COMMIT:=実行済commitまたは推奨messageの報告欄
```

制約:

```text
COMMIT.proposed != commit許可
COMMIT自動commit許可扱禁止
```

## Repository / release terms

### public履歴

```text
public履歴:=公開済みrepo/history/tag/releaseに属する変更履歴
```

制約:

```text
public履歴改竄禁止
公開済tag移動禁止
Release Assets上書前提操作禁止
```

### Release Assets

```text
Release Assets:=GitHub Release等に添付された公開配布物
```

## Template / Tool terms

### Template

```text
Template:=共通契約/定型手順/報告形式を再利用するための部品
```

制約:

```text
Template != Core正本
Template != 実行許可
Template参照 != 読了
Template未読→使用禁止/停止
```

### Validator

```text
Validator:=形式/整合性/欠落/権限衝突を検査する補助器
```

制約:

```text
Validator != 承認者
Validator != Runtime確認者
Validator != 要件判断者
Validator != D禁止解除者
validator未実行→pass扱禁止
validator pass != RT:v
validator pass != U承認
validator pass != 実装妥当性保証
validator pass != P1L/P1 runtime binding/authority
```

## Actor terms

### U

```text
U:=ユーザー
```

### OrchestratorLLM

```text
OrchestratorLLM:=統括LLM。意図整理/KDSL生成/P1L-P1正規化/R1検収/safety gate管理を行う
```

### AI tool

```text
AI tool:=Codex等のAI coding tool。runtime binding/authorityを満たしたKDSL_PROMPT範囲内で調査/編集/検証/報告する
```

### SkillAgentTool

```text
SkillAgentTool:=AIのSkill / Agent / Tool / Template等の能力提供層
```
