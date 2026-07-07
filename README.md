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
Overview:
  docs/overview.md

Public-facing draft:
  docs/public-facing-readme-draft.md

KDSL全体仕様:
  spec/core/kdsl-spec.md

operator / 保護語 / 変換禁止:
  spec/core/kdsl-core.md

mode / safety / high-risk:
  spec/core/kdsl-modes.md

manifest / glossary:
  spec/manifest.md
  spec/glossary.md

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

Public examples:
  examples/public/README.md
  examples/public/kdsl_prompt_safe_fix.example.md
  examples/public/kdsl_prompt_template_inheritance.example.md
  examples/public/r1_result_valid.example.md
  examples/public/r1_result_authority_guard.example.md
  examples/public/kdsl_dp_boundary_warning.example.md

Validator:
  tools/validator/README.md
  tools/validator/r1-validator-design.md
  tools/validator/kdsl-template-lint-design.md
  tools/validator/mvp-design.md
  tools/validator/r1-mvp-implementation-notes.md
  tools/validator/r1_required_blocks.py
  tools/validator/r1_rt_basis.py
  tools/validator/r1_authority_guard.py
  tools/validator/kdsl_template_refs.py
  tools/validator/kdsl_template_expansion.py
  tools/validator/kdsl_validate.py
  tools/validator/kdsl_validate_usage.md

Validator samples / verification:
  tools/validator/samples/sample_r1_ok.md
  tools/validator/samples/sample_r1_missing_block.md
  tools/validator/samples/sample_rt_v_valid.md
  tools/validator/samples/sample_rt_v_invalid_basis.md
  tools/validator/samples/sample_rt_v_no_basis.md
  tools/validator/samples/sample_authority_ok.md
  tools/validator/samples/sample_authority_warn.md
  tools/validator/samples/sample_authority_fail.md
  tools/validator/samples/sample_template_ref_ok.md
  tools/validator/samples/sample_template_ref_missing_gate.md
  tools/validator/samples/sample_template_expansion_ok.md
  tools/validator/samples/sample_template_expansion_warn.md
  tools/validator/samples/sample_template_expansion_fail.md
  tools/validator/verification/r1_required_blocks_verify.md
  tools/validator/verification/r1_rt_basis_verify.md
  tools/validator/verification/r1_authority_guard_verify.md
  tools/validator/verification/kdsl_template_refs_verify.md
  tools/validator/verification/kdsl_template_expansion_verify.md
  tools/validator/verification/kdsl_validate_target_modes_verify.md

Review / checklist:
  docs/reviews/v0.1.0-draft-review.md
  docs/reviews/v0.1.0-draft-checklist.md
  docs/reviews/v1.1-sync-review.md
  docs/reviews/v1.1-release-readiness-checklist.md
  docs/reviews/v1.1-authority-guard-design.md
  docs/reviews/v1.1-full-template-expansion-checker-design.md
  docs/reviews/v1.1-public-facing-readme-examples-design.md
  docs/reviews/v1.1-release-candidate-checklist-review.md

Release / public planning:
  docs/release/v0.1.0-draft-tag-plan.md
  docs/release/v1.1-release-notes-draft.md
  docs/public-readiness.md
```

## 構成

```text
spec/
  manifest.md  正本参照関係
  glossary.md  用語集
  core/         KDSLの正本・core記法・mode定義
  profiles/     dev-prompt / converter など用途別profile
  r1/           R1 Result Specification / KDSL_RESULT
  lint/         KDSL/R1 lint checklist
  bridge/       KDSL / KDSL-DP / ADPS / R1境界

templates/      再利用prompt template置き場
experimental/   Actor Model / Protocol Stack / HMI / Python Validator等の実験案
examples/       変換例・運用例
tools/          validator等の設計/実装候補置き場
docs/           overview / review / release planning 等の運用文書
```

## 仕様レベル

```text
Core: 壊してはいけない正本
Manifest: 正本参照関係
Glossary: 用語定義
Profile: 用途別の運用仕様
R1: AI作業結果の証跡・検収仕様
Lint: 意味欠落・safety gate欠落検査
Bridge: KDSL-DP / ADPS / R1境界
Templates: 実運用向け再利用部品
Experimental: 検証中の概念・拡張案
Examples: 正本ではない理解補助
Tools: 任意補助。validator passは承認/RT:vの代替ではない
Reviews: tag/release前の判断記録
Release planning: tag/release判断の準備文書。実行許可ではない
Public readiness: 公開可否判断メモ。公開実行ではない
```

## 現在の状態

```text
status: main synced after v0.1.0-draft
current_main_spec: v1.1-ADPS-aware sync
base_tag: v0.1.0-draft
base_tag_type: annotated
base_tag_object: 797c88ad176dde5286187984de945040ec5eb945
base_tag_target: 89f508c4c8d5ea49a315e60cd3157b089942afee
visibility: private
stability: draft
release: none
public: not_yet
validator: required-block / RT-basis / authority-guard / template-reference / template-expansion slices implemented
validator_wrapper: target modes r1 / prompt / all
public_facing_docs: draft files created / U review pending
release_candidate_review: drafted / local validation and U explicit approval pending
readiness: not_ready
```

## 運用方針

- Core / R1 / Lint は慎重に変更する
- Manifest は正本参照関係を示す
- Glossary は用語定義を示す
- Experimental は正本扱いしない
- Examples は正本扱いしない
- Tools は補助であり、validator pass を承認/RT:v/要件妥当性の代替にしない
- Templates は未読時に意味が消えるため、参照だけで読了扱いしない
- Release planning は実行許可ではない
- Public readiness は公開判断のメモであり、公開許可ではない
- KDSL-DP は P1/P1L へ正規化するまで実行指示扱いしない
- KDSL_RESULT の NEXT は提案であり、次タスク実行許可ではない
- KDSL_RESULT の COMMIT は実行結果または推奨messageであり、自動commit許可ではない
- unknown profile / alias / preset / template は推測しない
- v0.1.0-draft tag は履歴として維持し、main の仕様整理とは分離する

## 次候補

```text
Phase 30: U local validation confirmation
A. U runs local validation commands
B. U reviews release candidate checklist
C. optional release/tag/public planning only after explicit U approval
release作成なし
public化なし
tag移動なし
```
