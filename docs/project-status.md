# KDSL / R1 Project Status

status: canonical-project-status
last_updated: 2026-07-07

この文書は、`kdsl-spec` repository の現在状態を示す運用上の状態正本です。
仕様正本は `spec/manifest.md` と `spec/core/*` / `spec/r1/*` / `spec/lint/*` / `spec/bridge/*` を参照します。

## 1. Current public state

```yaml
current_public_state:
  repository_visibility: public
  published_release: v1.1.0-rc1
  release_class: experimental_preview
  release_type: prerelease
  public_ready: no
  stable_release: none
  release_assets: none
  license: MIT
```

補足:

```text
public: yes
public-ready: no
license: MIT
```

この2つは分離して扱います。現在の状態は「公開済み experimental preview」であり、「正式public-ready release」ではありません。

## 2. License state

```yaml
license:
  type: MIT
  file: LICENSE
  approved_by_user: 2026-07-07
  scope:
    - specifications
    - documentation
    - examples
    - templates
    - validator helper code
```

## 3. Validator maturity

```yaml
validator:
  maturity: experimental_heuristic_helpers
  implementation: partial
  authority: non_authoritative
  scope:
    - required block presence lint
    - RT:v basis wording heuristic lint
    - NEXT/COMMIT authority-shape heuristic lint
    - template reference lint
    - template expansion evidence lint
  not_scope:
    - semantic equivalence proof
    - full template expansion proof
    - runtime verification
    - user approval
    - release readiness judgment
```

制約:

```text
validator pass != U承認
validator pass != RT:v
validator pass != 実装妥当性保証
validator pass != semantic equivalence
validator pass != release readiness
```

## 4. Safety status

保持対象:

```text
KDSL-DP直接実行禁止
P1/P1L正規化必須
RT:v=対象環境runtime確認済のみ
build/diff/lint/test pass != RT:v
KDSL_RESULT NEXT:=提案, 実行許可扱禁止
KDSL_RESULT COMMIT:=実行済commitまたは推奨message, 自動commit許可扱禁止
public履歴/公開済tag/Release Assets保護
```

## 5. Local validation evidence

```yaml
local_sample_validation:
  date: 2026-07-07
  command: python tools/validator/run_samples.py
  result: pass
  total: 16
  failed: 0
  repo_status_after: clean / main...origin/main
  meaning: sample expectation runner passed locally
  not_meaning:
    - validator proof
    - RT:v
    - U approval
    - release readiness
    - semantic equivalence
    - full template expansion proof
```

## 6. Known gaps before stable

```text
GitHub Actions未構成
validatorは文字列/軽量構造lint中心
full parserなし
full template expansion照合なし
外部向け導入導線はdraft
ADPS/KDSL-DP説明は初見向けには重い
```

## 7. Recommended positioning

```text
Use as:
  experimental preview
  internal/public review candidate
  safety-gate-preserving prompt notation draft
  R1 evidence-reporting draft

Do not present as:
  stable standard
  production-ready validator suite
  proof system
  approval/runtime/release substitute
```

## 8. Next safe steps

```text
P0: license表記をREADME / overview / public-readiness / manifest等へ同期
P1: validator名称と説明を heuristic lint helpers で維持
P2: GitHub Actionsでsample runner実行を検討
P3: stable v1.1.0 はU明示承認後のみ検討
```
