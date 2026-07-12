# KDSL Glossary v1.1-v2-sync

目的: kdsl-spec内で使う主要用語を定義し、表記揺れと誤解を減らす。

status: draft-main-v2-sync
source_alignment: spec/core v1.1-v2-sync / manifest v2-draft-sync / bridge v0.2 / R1 v0.1-draft

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

### P1 / P1L

```text
P1/P1L:=KDSL-DPから正規化された実行契約候補
```

制約:

```text
P1/P1L valid != executable
P1/P1L正規化必須
```

### K1 / PF1

```text
K1/PF1:=Runtime Control系の実行制御層
```

現status:

```text
詳細仕様は本repoでは未整備
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
Authority:=read/edit/stage/commit/push/release等の許可状態
```

### AUTHORITY

```text
AUTHORITY:=R1/KDSL_PROMPT内で権限状態を明示するblock
```

推奨key:

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
```

## Actor terms

### U

```text
U:=ユーザー
```

### OrchestratorLLM

```text
OrchestratorLLM:=統括LLM。意図整理/KDSL生成/R1検収/安全gate管理を行う
```

### AI tool

```text
AI tool:=Codex等のAI coding tool。KDSL_PROMPT範囲内で調査/編集/検証/報告する
```

### SkillAgentTool

```text
SkillAgentTool:=AIのSkill / Agent / Tool / Template等の能力提供層
```
