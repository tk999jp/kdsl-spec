# KDSL / R1 Project Status

status: canonical-project-status
last_updated: 2026-07-10

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

```text
public: yes
public-ready: no
stable: no
```

現在の状態は「公開済み experimental preview」であり、正式public-ready/stable releaseではありません。

## 2. Current development workstream

```yaml
development_workstream:
  branch: feature/kdsl-v2-compact-prompt
  base: main
  status: v2_architecture_draft
  focus:
    - CompactPrompt profile
    - kanji-v1 lexicon
    - CompactPrompt lint
    - CP-Lift boundary
    - future Packet non-executable boundary
  merge_status: not_merged
  stable_effect: none
```

Direction:

```text
v1.1.0-rc1:=experimental historical baseline
v1.1.0 stable:=当面保留
v2-draft設計を優先
mainへのmerge:=別判断
stable/tag/release/Release Assets操作:=別途U明示承認必須
```

## 3. License state

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

## 4. Validator maturity

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

Constraints:

```text
validator pass != U承認
validator pass != RT:v
validator pass != 実装妥当性保証
validator pass != semantic equivalence
validator pass != release readiness
```

CompactPrompt lint status:

```text
spec/lint/kdsl-compact-prompt-lint.md:=v2 draft checklist
validator implementation:=未実装
lint document existence != automated validation
```

## 5. Safety status

保持対象:

```text
意味保持 > safety gate保持
KDSL-DP直接実行禁止
P1/P1L正規化必須
RT:v=対象環境runtime確認済のみ
build/diff/lint/test pass != RT:v
KDSL_RESULT NEXT:=提案, 実行許可扱禁止
KDSL_RESULT COMMIT:=実行済commitまたは推奨message, 自動commit許可扱禁止
public履歴/公開済tag/Release Assets保護
```

v2 additional boundaries:

```text
lexicon != mode/profile
unknown lexicon/alias推測禁止
構造aliasはKEY位置のみ
保護語の一字短縮禁止
KDSL-CP実装指示禁止
Packet registry未定義→KDSL-Packet直接実行禁止
PKT:v1使用禁止
```

## 6. Local validation evidence

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

v2 branch review:

```text
method: GitHub connector file review / branch compare
runtime: not applicable
validator runner: not executed against v2 additions
```

## 7. Known gaps before merge or stable

```text
KDSL-CP/kanji-v1はv2 draft
CompactPrompt validator未実装
Packet schema/BASE/TASK/FLOW/SG/R1C registry未定義
KDSL-Packetはdraft-non-executable
v2 public-facing overview未確定
GitHub Actions未構成
full parserなし
full template expansion照合なし
```

## 8. Recommended positioning

```text
Use as:
  experimental preview
  internal/public review candidate
  safety-gate-preserving prompt notation draft
  CompactPrompt architecture draft
  R1 evidence-reporting draft

Do not present as:
  stable standard
  production-ready validator suite
  proof system
  approval/runtime/release substitute
  executable Packet specification
```

## 9. Next safe steps

```text
P0: v2 branch architecture review / lint review
P1: merge可否判断
P2: R1C / Safety Gate registry / Packet registryを別Phaseで検討
P3: validatorへのCompactPrompt lint実装を別Phaseで検討
Hold: v1.1.0 stable / tag / release / Release Assets
```
