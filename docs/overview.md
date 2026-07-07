# KDSL / R1 Overview

status: overview-draft
project_status: docs/project-status.md

## 1. What this repository is

`kdsl-spec` は、KDSL と R1 を管理するための experimental preview specification repository。

```text
KDSL:=LLM直投入可能な安全gate保持型半構造化prompt記法
R1:=AI作業結果のEvidence/検収仕様
```

このrepositoryは、prompt圧縮だけではなく、Human-AI work interface / 作業契約 / 結果証跡 / 検収可能性を扱う。

現在の状態:

```text
public: yes
release: v1.1.0-rc1
release_class: experimental preview
public-ready: no
stable_release: none
```

## 2. Why KDSL exists

通常の長文promptでは、次の問題が起きやすい。

```text
禁止事項が埋もれる
承認gateが弱化する
未確認/未実行が確認済み扱いされる
Runtime確認とbuild/test passが混同される
NEXTが実行許可として誤解される
COMMIT候補がcommit許可として誤解される
```

KDSLは、これらを短くしながらも削らないための記法である。

## 3. Why R1 exists

AI coding toolの結果報告では、次の問題が起きやすい。

```text
実行していないcmdが実行済みのように書かれる
未実行verifyがpass扱いされる
build成功がRuntime確認済み扱いされる
推論と観測が混ざる
次候補提案が実行許可に見える
commit message候補がcommit許可に見える
```

R1は、これらを検収可能に分離するための結果仕様である。

## 4. Main components

```text
spec/core:
  KDSLの記法・保護語・mode/safety

spec/r1:
  KDSL_RESULT / RT / Evidence / Authority

spec/lint:
  KDSL/R1の保持・弱化・欠落検査

spec/bridge:
  KDSL / KDSL-DP / ADPS / P1/P1L / R1 境界

spec/manifest:
  正本参照関係

spec/glossary:
  用語定義

templates:
  dev-prompt実運用向け再利用部品

examples:
  before/after/R1例

tools/validator:
  experimental heuristic lint helpers / partial implementation

docs/project-status.md:
  repository現在状態の運用上の状態正本
```

## 5. Safety principles

```text
意味保持 > safety gate保持 > 判断分岐保持 > 誤実装防止 > 文字数削減
```

重要:

```text
KDSL-DP直接実行禁止
P1/P1L正規化必須
RT:v=対象環境runtime確認済のみ
build/diff/lint/test pass != RT:v
NEXT:=提案, 実行許可扱禁止
COMMIT:=実行済commitまたは推奨message, 自動commit許可扱禁止
```

## 6. Current maturity

```text
state: public experimental preview
release: v1.1.0-rc1
public: yes
public_ready: no
tag: v1.1.0-rc1
Release Assets: none
validator implementation: partial heuristic lint helpers
license: pending
```

現時点では、仕様・テンプレート・例・validator helperが揃った experimental preview 段階。
validator helperは、承認・実機確認・release readiness・意味等価性の証明を代替しない。

## 7. Recommended use now

```text
KDSL/R1の設計検討
MidFD等のAI coding prompt運用改善
external review / experimental previewとしての確認
template分離の検証
R1結果報告の検収観点確認
```

非推奨:

```text
stable release扱い
外部標準としての大々的告知
validator passを承認/RT:v代替にすること
Release Assets作成
既存tag移動
```
