# KDSL / R1 Overview

status: v2-draft-public-overview
last_updated: 2026-07-12
project_status: docs/project-status.md
manifest: spec/manifest.md

## 1. What this repository is

`kdsl-spec` is a public experimental-preview repository for KDSL and R1.

```text
KDSL:=LLM直投入可能な安全gate保持型半構造化prompt記法
R1:=AI支援作業のEvidence/結果証跡/検収仕様
```

KDSL/R1は、prompt圧縮だけではなく、Human-AI work interface、作業契約、結果証跡、検収可能性を扱います。

Current maturity:

```text
public: yes
release: v1.1.0-rc1
release_class: experimental preview
public_ready: no
stable_release: none
Release Assets: none
validator: partial / non-authoritative
license: MIT
```

## 2. Why KDSL exists

通常のpromptでは、編集・短縮・再利用の過程で安全境界が埋もれます。

```text
禁止事項が弱化する
承認gateが消える
未確認/未実行が確認済扱いされる
rollback/revert条件が落ちる
Runtime確認とbuild/test passが混同される
public履歴/tag/Release Assets保護が消える
NEXTが実行許可として誤解される
COMMIT候補がcommit許可として誤解される
```

KDSLの優先順位:

```text
意味保持 > safety gate保持 > 判断分岐保持 > 誤実装防止 > 文字数削減
```

KDSLは完全な形式言語ではなく、LLM向け半構造化notationです。短さより、条件・対象・禁止動作・権限境界の保持を優先します。

## 3. KDSL architecture

KDSL v2 draft uses orthogonal axes.

```text
format: KDSL
profile: compact-prompt|dev-prompt|converter|lint
mode: readable|min|dense|lock
safety: normal|lock-critical|lock-all
lexicon: standard|kanji-v1
envelope: plain|packet-draft|result
```

Responsibilities:

```text
format:=記法系
profile:=用途別運用仕様
mode:=圧縮強度
safety:=安全保持強度
lexicon:=宣言済み語彙/alias集合
envelope:=prompt/resultを包む契約形式
```

Rules:

```text
lexicon != mode
lexicon != profile
unknown profile/mode/safety/lexicon/envelope推測禁止
Core保護語をLexicon/Registryで上書禁止
```

Legacy boundary:

```text
rulebook:=v1.1 legacy profile name
rulebook新規使用禁止
用途確認なしにcompact-prompt/lintへ自動補正禁止
```

## 4. Profiles

### compact-prompt

General LLM prompts、Project files、単体instruction向けの軽量profileです。

```text
required: Goal / Input / Output / Guard / Check
optional: Role / Rules / Style
```

KDSL-CP漢:

```text
profile: compact-prompt
mode: dense
lexicon: kanji-v1
```

構造漢字aliasはKEY位置のみで使用し、禁止・未確認・未実行・承認待・断定禁止などの保護語は弱化しません。

### dev-prompt

AI coding tool向けの調査・実装・検証・報告契約profileです。repo、Runtime、public操作、data、authorityを扱います。

### converter

入力promptを対象profileへ変換します。正本参照は確認済みGitHub `main` を優先し、GitHub参照不能時のみProject files snapshotをfallback使用します。

### lint

KDSL/R1の保持・弱化・欠落・権限衝突を検査するprofileです。

## 5. CP-Lift

CompactPrompt対象に次が含まれる場合は `profile:dev-prompt` へLiftします。

```text
実装/改修/削除
repo/path/branch/commit操作
file/API/command変更
rollback/revert
RT:v/実機確認
public履歴/公開済tag/Release Assets
data migration
正本変更
AI coding toolへの投入
```

F/GなどCompactPrompt指定があっても、CP-Lift triggerを回避しません。

## 6. KDSL-DP / ADPS boundary

```text
KDSL:=安全gate保持型prompt記法
KDSL-DP:=ADPS向けAuthoring形式 / 実行指示ではない
P1/P1L:=実行契約候補
K1/PF1:=Runtime Control
R1/KDSL_RESULT:=Evidence/結果証跡
```

Required boundary:

```text
KDSL-DP直接実行禁止
KDSL-DPをAI coding toolへ実装指示として渡すこと禁止
KDSL-DP→P1/P1L正規化必須
P1/P1L valid != executable
```

## 7. Packet boundary

KDSL-Packetはv2-draft authoring schemaですが、実行仕様ではありません。

```text
schema: kdsl-packet@0.1-draft
status: adopted v2-draft / non-executable
normalization: required
packet_state: not_normalized
PKT:v1: prohibited
```

```text
Registry/lint/validator/property pass != execution authority
normalization preview != executable target
semantic/property pass != semantic equivalence proof
```

## 8. Why R1 exists

AI toolの報告では、実行事実・検証結果・推論・Runtime・権限が混同されやすくなります。

R1は次を分離します。

```text
実行したcommand / 未実行command
実行したverify / 未実行verify
observed / inferred / not_observed / unverified
build/test result / Runtime result
NEXT proposal / execution permission
COMMIT actual/proposed / commit authority
```

Canonical R1 fields:

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

Critical rules:

```text
未実行cmd→CMD記載禁止
未実行verify→pass扱禁止
build/diff/lint/test/CI pass != RT:v
RT:v:=対象環境runtime確認済のみ
NEXT:=提案, 実行許可扱禁止
COMMIT:=実行済commitまたは推奨message, 自動commit許可扱禁止
```

See [`r1-quickstart.md`](r1-quickstart.md) for a minimal workflow.

## 9. Specification layers

```text
spec/core:       KDSL記法・保護語・mode/safety
spec/profiles:   用途別profile
spec/lexicons:   宣言済み語彙/alias
spec/registry:   Safety Gate/Packet ID・state・composition
spec/r1:         KDSL_RESULT / Evidence / RT / Authority
spec/lint:       保持・弱化・欠落検査
spec/bridge:     KDSL-DP/ADPS/CP-Lift/Packet境界
spec/manifest:   正本参照関係
```

Non-canonical layers:

```text
templates:       再利用部品
examples:        理解補助
validator tools: heuristic lint helpers
docs/reviews:    設計・統合記録
```

## 10. Validator maturity

Current unified suite:

```text
command: python tools/validator/run_all_samples.py
expectations: 257
failed: 0
required repository check: pending / issue #39
```

Limitations:

```text
full YAML/KDSL semantic parserなし
full natural-language negation/exception reasoningなし
full semantic equivalence proofなし
complete safety proofなし
Packet normalization completion proofなし
```

Validator pass does not replace U approval, Runtime confirmation, semantic review, execution authority, or release judgment.

## 11. Recommended use

```text
KDSL/R1設計・レビュー
一般promptのsafety-preserving compression
AI coding promptのgate保持
KDSL_RESULTの検収
experimental validator/lint evaluation
```

Do not use as:

```text
stable external standard
production-ready proof system
approval/runtime/release substitute
executable Packet specification
```

## 12. Next reading

```text
README.md
spec/manifest.md
spec/core/kdsl-spec.md
spec/profiles/kdsl-converter-prompt.md
spec/r1/r1-result-spec.md
docs/r1-quickstart.md
examples/public/README.md
```
