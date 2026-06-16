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

## Quick navigation

```text
KDSL全体仕様:
  spec/core/kdsl-spec.md

operator / 保護語 / 変換禁止:
  spec/core/kdsl-core.md

mode / safety / high-risk:
  spec/core/kdsl-modes.md

dev-prompt運用:
  spec/profiles/kdsl-profile-dev-prompt.md

converter運用:
  spec/profiles/kdsl-converter-prompt.md

R1 / KDSL_RESULT:
  spec/r1/r1-result-spec.md

lint:
  spec/lint/kdsl-lint-checklist.md

KDSL / KDSL-DP / ADPS bridge:
  spec/bridge/kdsl-adps-bridge.md

テンプレート:
  templates/README.md
  templates/base/kdsl_base_dev.md
  templates/result/r1_result_spec.md
  templates/tasks/task_docs_state_closeout.md
  templates/tasks/task_corrective_impl.md
  templates/tasks/task_investigation_only.md

実験案:
  experimental/README.md
  experimental/actor-model.md
  experimental/protocol-stack.md

例:
  examples/README.md
  examples/midfd/docs_state_closeout.before.md
  examples/midfd/docs_state_closeout.after.md
  examples/midfd/r1_result.example.md

Validator design:
  tools/validator/README.md
  tools/validator/r1-validator-design.md
  tools/validator/kdsl-template-lint-design.md

Review:
  docs/reviews/v0.1.0-draft-review.md
```

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
tools/        validator等の設計/将来実装置き場
docs/         review / release planning 等の運用文書
```

## 仕様レベル

```text
Core: 壊してはいけない正本
Profile: 用途別の運用仕様
R1: AI作業結果の証跡・検収仕様
Lint: 意味欠落・safety gate欠落検査
Bridge: KDSL-DP / ADPS / R1境界
Templates: 実運用向け再利用部品
Experimental: 検証中の概念・拡張案
Examples: 正本ではない理解補助
Tools: 任意補助。validator passは承認/RT:vの代替ではない
Reviews: tag/release前の判断記録
```

## 現在の状態

```text
status: v0.1.0-draft review completed
visibility: private
stability: draft
release: none
public: not_yet
tag: not_created
```

## 運用方針

- Core / R1 / Lint は慎重に変更する
- Experimental は正本扱いしない
- Examples は正本扱いしない
- Tools は補助であり、validator pass を承認/RT:v/要件妥当性の代替にしない
- Templates は未読時に意味が消えるため、参照だけで読了扱いしない
- KDSL-DP は P1/P1L へ正規化するまで実行指示扱いしない
- KDSL_RESULT の NEXT は提案であり、次タスク実行許可ではない
- KDSL_RESULT の COMMIT は実行結果または推奨messageであり、自動commit許可ではない
- unknown profile / alias / preset / template は推測しない

## 次候補

```text
Phase 7: Manifest and glossary
- spec/manifest.md
- spec/glossary.md
- docs/reviews/v0.1.0-draft-checklist.md
```
