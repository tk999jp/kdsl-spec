# kdsl-spec

KDSL / R1 specification repository.

このリポジトリは、KDSL（安全gate保持型prompt記法）と R1 Result Specification（AI作業結果の証跡・検収仕様）を管理するための正本候補です。

## 目的

KDSL/R1を、単なるプロンプト圧縮記法ではなく、Human-AI work interface / 作業契約・結果証跡仕様として整理します。

主な目的:

- AI coding tool向けpromptの意味保持と安全gate保持
- D禁止 / rollback / 未確認 / 未実行 / 承認gate / 実機確認分離の保持
- KDSL_PROMPT / KDSL_RESULT の入出力契約整理
- R1による結果報告の検収可能化
- lint / template / profile / experimental案の分離管理

## 構成

```text
spec/
  core/       KDSLの正本・core記法・mode定義
  profiles/   dev-prompt / converter など用途別profile
  r1/         R1 Result Specification / KDSL_RESULT
  lint/       KDSL/R1 lint checklist
  bridge/     KDSL / KDSL-DP / ADPS / R1境界

templates/    再利用prompt template置き場
experimental/ Actor Model / Protocol Stack / HMI / Python Validator等の実験案
examples/     変換例・運用例
```

## 仕様レベル

```text
Core: 壊してはいけない正本
Profile: 用途別の運用仕様
R1: AI作業結果の証跡・検収仕様
Lint: 意味欠落・safety gate欠落検査
Experimental: 検証中の概念・拡張案
```

## 現在の状態

```text
status: initial specification import
visibility: private
stability: draft
```

## 運用方針

- Core / R1 / Lint は慎重に変更する
- Experimental は正本扱いしない
- KDSL-DP は P1/P1L へ正規化するまで実行指示扱いしない
- KDSL_RESULT の NEXT は提案であり、次タスク実行許可ではない
- KDSL_RESULT の COMMIT は実行結果または推奨messageであり、自動commit許可ではない
