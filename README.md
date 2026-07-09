# kdsl-spec

KDSL / R1 specification repository.

このリポジトリは、KDSL（安全gate保持型prompt記法）と R1 Result Specification（AI作業結果の証跡・検収仕様）を管理するための正本候補です。

## 重要な現在状態

```text
status: v1.1.0-rc1 experimental preview published
repository_visibility: public
release: v1.1.0-rc1
release_type: prerelease / experimental preview
public: yes
public_ready: no
stable_release: none
Release Assets: none
license: pending
validator: experimental heuristic lint helpers / partial implementation
validator_authority: non_authoritative
```

現在の状態は「公開済み experimental preview」であり、「正式public-ready release」ではありません。
状態正本は次を参照してください。

```text
docs/project-status.md
```

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
Project status:
  docs/project-status.md

Overview:
  docs/overview.md

Public-facing draft:
  docs/public-facing-readme-draft.md

v2 draft direction:
  docs/design/kdsl-v2-direction.md

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

CompactPrompt / KDSL-CP v2 draft:
  spec/profiles/kdsl-profile-compact-prompt.md
  spec/profiles/kdsl-compact-kanji-aliases.md

CP / Packet bridge v2 draft:
  spec/bridge/kdsl-cp-packet-bridge.md

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

CompactPrompt examples:
  examples/compact-prompt/README.md
  examples/compact-prompt/blog_meta.kdsl-cp.md
  examples/compact-prompt/blog_meta.kdsl-cp-kanji.md
  examples/compact-prompt/novel_review.kdsl-cp-kanji.md
  examples/compact-prompt/prompt_improver.kdsl-cp.md
  examples/compact-prompt/cp_lift_example.md

Public examples:
  examples/public/README.md
  examples/public/kdsl_prompt_safe_fix.example.md
  examples/public/kdsl_prompt_template_inheritance.example.md
  examples/public/r1_result_valid.example.md
  examples/public/r1_result_authority_guard.example.md
  examples/public/kdsl_dp_boundary_warning.example.md

Validator helpers:
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
  tools/validator/run_samples.py
  tools/validator/kdsl_validate_usage.md

Validator samples / verification:
  tools/validator/samples/*
  tools/validator/verification/*

Review / checklist:
  docs/reviews/*

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
  profiles/     dev-prompt / converter / compact-prompt など用途別profile
  r1/           R1 Result Specification / KDSL_RESULT
  lint/         KDSL/R1 lint checklist
  bridge/       KDSL / KDSL-DP / ADPS / R1 / CP-Packet 境界

templates/      再利用prompt template置き場
experimental/   Actor Model / Protocol Stack / HMI / Python Validator等の実験案
examples/       変換例・運用例
tools/          validator等の設計/実装候補置き場
docs/           project status / overview / review / release planning / design 等の運用文書
```

## 仕様レベル

```text
Core: 壊してはいけない正本
Manifest: 正本参照関係
Glossary: 用語定義
Profile: 用途別の運用仕様
R1: AI作業結果の証跡・検収仕様
Lint: 意味欠落・safety gate欠落検査
Bridge: KDSL-DP / ADPS / R1 / CP-Packet 境界
Templates: 実運用向け再利用部品
Experimental: 検証中の概念・拡張案
Examples: 正本ではない理解補助
Tools: 任意補助。validator passは承認/RT:v/要件妥当性の代替ではない
Reviews: tag/release前の判断記録
Release planning: tag/release判断の準備文書。実行許可ではない
Public readiness: 公開可否判断メモ。公開実行ではない
Project status: repositoryの現在状態を示す運用上の状態正本
Design docs: 仕様再編やv2 draft方針の判断記録。Core正本ではない
```

## Validator helpers

現時点のvalidatorは、experimental heuristic lint helpersです。

```text
checks:
  required block presence
  RT:v basis wording in evidence-related fields
  NEXT/COMMIT authority shape
  template reference gates
  template expansion evidence markers

not checks:
  semantic equivalence proof
  full template expansion proof
  runtime execution
  U approval
  release readiness
```

サンプル期待値確認:

```text
python tools/validator/run_samples.py
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
- Project status は現在状態の同期元として扱う
- KDSL-DP は P1/P1L へ正規化するまで実行指示扱いしない
- KDSL_RESULT の NEXT は提案であり、次タスク実行許可ではない
- KDSL_RESULT の COMMIT は実行結果または推奨messageであり、自動commit許可ではない
- unknown profile / alias / preset / template は推測しない
- v0.1.0-draft tag は履歴として維持し、main の仕様整理とは分離する
- v2-draft documents are design/proposal additions and do not by themselves replace Core/R1/Lint canonical rules

## v2 draft candidates

```text
Status:
  draft / not stable / not public-ready

Initial scope:
  KDSL-CP: CompactPrompt for general LLM / Project files / single prompts
  KDSL-CP漢: dense-ja aliases for compact Japanese prompts
  CP-Lift: boundary rule from KDSL-CP to KDSL-Packet / Full KDSL

Files:
  docs/design/kdsl-v2-direction.md
  spec/profiles/kdsl-profile-compact-prompt.md
  spec/profiles/kdsl-compact-kanji-aliases.md
  spec/bridge/kdsl-cp-packet-bridge.md
  examples/compact-prompt/*

Non-goals:
  Core正本の即置換
  R1C/SG/Packet registryの同時導入
  stable v2 release
  tag/release/Release Assets操作
```

## 次候補

```text
Phase: rc1 correction / experimental preview hardening
A. README / overview / public-readiness / manifest / validator README の状態同期
B. validator helperの過大表現を補正
C. sample expectation runnerでサンプル期待値を確認
D. LICENSE判断
E. 問題がなければv1.1.0 stable化を別途U承認後に検討
Release Assets追加なし
大々的告知なし

Phase: v2 CompactPrompt draft follow-up
A. R1C compact schema検討
B. Safety Gate registry / bitmask検討
C. Packet registry検討
```