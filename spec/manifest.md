# KDSL Spec Manifest v0.1-draft

目的: kdsl-spec内の各ファイルの責務・正本性・参照関係を定義し、重複規則の更新不一致を防ぐ。

status: draft

## 1. Spec layers

```text
Core: KDSL本体/記法/保護語/mode/safetyの正本
Profiles: 用途別運用仕様
R1: 結果証跡/検収仕様の正本
Lint: 保持/弱化/欠落検査の正本
Bridge: KDSL-DP/ADPS/P1/P1L/R1境界の正本
Templates: 実運用向け再利用部品。Core正本ではない
Experimental: 検証中案。正本ではない
Examples: 理解補助。正本ではない
Tools: 任意補助。承認/RT:v/要件妥当性の代替ではない
Docs/Reviews: 判断記録。仕様正本ではない
```

## 2. File responsibility map

| Path | Layer | Responsibility | Canonical? |
|---|---|---|---|
| `spec/core/kdsl-spec.md` | Core | KDSL全体定義 / 設計単位 / KDSL_PROMPT / KDSL_RESULT入口 | Yes |
| `spec/core/kdsl-core.md` | Core | operator / abbrev / 保護語 / 禁止文型 / 変換禁止 | Yes |
| `spec/core/kdsl-modes.md` | Core | mode / safety / high-risk判定 | Yes |
| `spec/profiles/kdsl-profile-dev-prompt.md` | Profile | dev-prompt用途の実運用規則 | Profile canonical |
| `spec/profiles/kdsl-converter-prompt.md` | Profile | KDSL Converterの出力契約 | Profile canonical |
| `spec/r1/r1-result-spec.md` | R1 | KDSL_RESULT / RT / EVIDENCE / AUTHORITY / 検収仕様 | Yes |
| `spec/lint/kdsl-lint-checklist.md` | Lint | KDSL/R1変換後lint/checklist | Yes |
| `spec/bridge/kdsl-adps-bridge.md` | Bridge | KDSL/KDSL-DP/ADPS/P1/P1L/R1境界 | Yes |
| `templates/*` | Templates | 再利用部品 | No |
| `experimental/*` | Experimental | 検証中案 | No |
| `examples/*` | Examples | 理解補助/運用例 | No |
| `tools/validator/*` | Tools | validator設計/将来実装 | No |
| `docs/reviews/*` | Review | 判断記録 | No |

## 3. Canonical rule ownership

### KDSL syntax / operator

正本:

```text
spec/core/kdsl-core.md
```

参照側:

```text
spec/core/kdsl-spec.md
spec/lint/kdsl-lint-checklist.md
```

### mode / safety / high-risk

正本:

```text
spec/core/kdsl-modes.md
```

参照側:

```text
spec/core/kdsl-spec.md
spec/profiles/kdsl-converter-prompt.md
spec/lint/kdsl-lint-checklist.md
```

### KDSL-DP / ADPS boundary

正本:

```text
spec/bridge/kdsl-adps-bridge.md
```

Core上の要約:

```text
spec/core/kdsl-spec.md
spec/core/kdsl-core.md
```

Lint上の検査:

```text
spec/lint/kdsl-lint-checklist.md
```

### KDSL_RESULT / R1

正本:

```text
spec/r1/r1-result-spec.md
```

参照側:

```text
spec/core/kdsl-spec.md
spec/profiles/kdsl-profile-dev-prompt.md
spec/lint/kdsl-lint-checklist.md
templates/result/r1_result_spec.md
tools/validator/r1-validator-design.md
```

### RT:v

正本:

```text
spec/r1/r1-result-spec.md
```

Core上の保護:

```text
spec/core/kdsl-spec.md
spec/core/kdsl-core.md
```

Profile/Template上の運用:

```text
spec/profiles/kdsl-profile-dev-prompt.md
templates/base/kdsl_base_dev.md
templates/result/r1_result_spec.md
```

Lint/Validator上の検査:

```text
spec/lint/kdsl-lint-checklist.md
tools/validator/r1-validator-design.md
tools/validator/kdsl-template-lint-design.md
```

### NEXT / COMMIT authority

正本:

```text
spec/r1/r1-result-spec.md
```

運用参照:

```text
spec/profiles/kdsl-profile-dev-prompt.md
templates/base/kdsl_base_dev.md
templates/result/r1_result_spec.md
```

検査参照:

```text
spec/lint/kdsl-lint-checklist.md
tools/validator/r1-validator-design.md
tools/validator/kdsl-template-lint-design.md
```

### D禁止

正本:

```text
spec/core/kdsl-core.md
```

運用拡張:

```text
spec/profiles/kdsl-profile-dev-prompt.md
templates/base/kdsl_base_dev.md
```

検査:

```text
spec/lint/kdsl-lint-checklist.md
tools/validator/kdsl-template-lint-design.md
```

## 4. Duplication policy

重複は以下の範囲で許容する。

```text
Core: 正本定義
Profile: 運用文脈で再掲可
R1: 結果検収文脈で再掲可
Lint: 検査項目として再掲可
Template: 実運用prompt部品として再掲可
Validator design: 機械検査項目として再掲可
```

ただし、正本と矛盾する再掲は禁止。

## 5. Update policy

```text
Coreのoperator/保護語変更→breaking候補
R1のRT:v/NEXT/COMMIT意味変更→breaking候補
BridgeのKDSL-DP/P1/P1L境界変更→breaking候補
Lint項目追加→compatible候補
Template追加→compatible候補
Example追加→patch候補
Experimental追加→patch候補
```

## 6. Promotion policy

ExperimentalからCore/R1/Lintへ昇格する場合:

```text
昇格元file
採用理由
不採用代替案
影響範囲
互換性: breaking/compatible/patch
必要lint
必要example
```

## 7. Tag readiness dependency

v0.1.0-draft tag前に必要:

```text
spec/manifest.md present
spec/glossary.md present
docs/reviews/v0.1.0-draft-checklist.md present
README status updated
CHANGELOG updated
tag/release判断はU承認
```
