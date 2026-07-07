# Experimental Validator Helpers

目的: KDSL / R1 / Template をPython等で機械検査するための experimental heuristic lint helper 置き場。

status: experimental-heuristic-helpers
implementation: partial
project_status: ../../docs/project-status.md
source_specs:

```text
spec/core/kdsl-spec.md
spec/lint/kdsl-lint-checklist.md
spec/r1/r1-result-spec.md
spec/bridge/kdsl-adps-bridge.md
templates/README.md
```

## 位置づけ

```text
Validator helpers:=形式/整合性/欠落/権限衝突を検査する補助器
Validator helpers != 承認者
Validator helpers != Runtime確認者
Validator helpers != 要件判断者
Validator helpers != D禁止解除者
Validator helpers != release readiness判定者
Validator helpers != semantic equivalence proof
```

## 現在の実装範囲

```text
r1_required_blocks.py:
  KDSL_RESULT required block presence lint

r1_rt_basis.py:
  RT:v basis wording heuristic lint
  RT/VERIFY/S field scoped
  文書全体の説明語だけではRT:v根拠扱いしない

r1_authority_guard.py:
  NEXT/COMMIT authority-shape heuristic lint
  同一行key-valueと簡易複数行blockを対象

kdsl_template_refs.py:
  known template reference and safety gate lint

kdsl_template_expansion.py:
  template expansion evidence lint
  実際のtemplate全文展開照合ではない

kdsl_validate.py:
  target wrapper: r1 / prompt / all

run_samples.py:
  sample expectation runner
```

## 目的

```text
KDSL_PROMPTの必須要素欠落検出
Template参照の未読/未定義検出
R1/KDSL_RESULTの必須block欠落検出
RT:v根拠語のfield-scoped検出
NEXT/COMMIT権限混同のshape検出
EVIDENCEの観測/推論/未観測/未確認分離検査設計
AUTHORITYのcommit/push/release衝突検査設計
```

## 非目的

```text
AIの判断を代行しない
ユーザー承認を代行しない
実機Runtime確認を代行しない
仕様変更の可否を判断しない
D禁止を解除しない
曖昧ログの意味を断定しない
template全文展開を証明しない
自然言語の意味等価性を証明しない
release readinessを判定しない
```

## 想定構成

```text
tools/validator/
  README.md
  r1-validator-design.md
  kdsl-template-lint-design.md
  r1_required_blocks.py
  r1_rt_basis.py
  r1_authority_guard.py
  kdsl_template_refs.py
  kdsl_template_expansion.py
  kdsl_validate.py
  run_samples.py
```

## 設計方針

```text
軽量lint helperとして扱う
検査項目を仕様として固定しすぎない
R1 validatorを優先
Template lintは未読/未定義/権限衝突を優先
KDSL parserは過剰に厳密化しない
Markdown + code block + key-value風blockの軽量検査から始める
validator passの過信を避ける
```

## 検査レベル

```text
ERROR: safety gate破損/権限事故/RT:v誤認/必須block欠落
WARN: 曖昧/弱化/推奨block欠落
INFO: 任意改善/表記揺れ
```

## Sample expectation runner

```text
python tools/validator/run_samples.py
```

このrunnerは、サンプルファイルと期待exit codeのズレを検出するための補助です。
runner passも、承認/RT:v/release readinessを意味しません。

## Known limitations

```text
文字列/軽量構造lint中心
full parserなし
full natural-language semantic parserなし
full template expansion proofなし
GitHub Actions未構成
runtime実行なし
source authenticity判断なし
approval delegationなし
```

## Safety first

```text
validator未実行→pass扱禁止
validator pass != RT:v
validator pass != U承認
validator pass != 実装妥当性保証
validator pass != semantic equivalence
validator pass != release readiness
validator failure時→該当箇所を修正またはU確認
```
