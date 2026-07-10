# KDSL Spec Manifest v2-draft-sync

目的: kdsl-spec内の各fileの責務・正本性・参照関係を定義し、重複規則の更新不一致を防ぐ。

status: v2-draft-sync
project_status: docs/project-status.md
base_release: v1.1.0-rc1 experimental preview
license: MIT

## 0. Current alignment

```text
repository_visibility: public
release: v1.1.0-rc1
release_class: experimental preview
public_ready: no
stable_release: none
Release Assets: none
license: MIT
validator: partial heuristic lint helpers / non-authoritative
v2_branch_direction: CompactPrompt / Lexicon / CP-Lift architecture correction
```

Policy:

```text
v0.1.0-draft tagは履歴として維持
v1.1.0-rc1:=experimental historical baseline
v1.1.0 stable:=当面保留
v2-draft設計を優先
既存tag移動禁止
Release Assets操作禁止
stable/public-ready化→別途U明示承認必須
docs/project-status.md:=repository現在状態の運用上の状態正本
```

## 1. Architecture axes

```text
format:=記法系
profile:=用途別運用仕様
mode:=圧縮強度
safety:=安全保持強度
lexicon:=宣言済み語彙/alias集合
envelope:=prompt/resultを包む契約形式
```

Allowed draft alignment:

```text
format: KDSL
profile: compact-prompt|dev-prompt|converter|lint
mode: readable|min|dense|lock
safety: normal|lock-critical|lock-all
lexicon: standard|kanji-v1
envelope: plain|packet-draft|result
```

Rules:

```text
lexicon != mode
lexicon != profile
unknown profile/mode/safety/lexicon/envelope推測禁止
Core保護語をLexiconで上書禁止
```

## 2. Specification layers

```text
Core:
  KDSL本体/operator/保護語/変換禁止/mode/safetyの正本

Profiles:
  用途別運用仕様

Lexicons:
  profile内で使用する宣言済み語彙/alias集合
  Core保護語を上書きしない

R1:
  結果証跡/検収仕様の正本

Lint:
  意味/safety gate/構造の保持・弱化・欠落検査

Bridge:
  KDSL-DP/ADPS/P1/P1L/R1/CP-Lift/Packet境界

Templates:
  実運用向け再利用部品。正本ではない

Examples:
  理解補助。正本ではない

Tools:
  heuristic lint補助。承認/RT:v/要件妥当性/release readinessの代替ではない

Docs/Reviews/Design:
  判断記録。仕様正本ではない

Project Status:
  repository現在状態の運用上の状態正本。仕様正本ではない
```

## 3. File responsibility map

| Path | Layer | Responsibility | Canonical? |
|---|---|---|---|
| `docs/project-status.md` | Status | public/release/license/validator現在状態 | Operational status canonical |
| `docs/design/kdsl-v2-direction.md` | Design | v2 architecture / orthogonal axes / release strategy | No / v2 draft |
| `spec/core/kdsl-spec.md` | Core | KDSL全体定義 / KDSL_PROMPT / KDSL_RESULT入口 | Yes |
| `spec/core/kdsl-core.md` | Core | operator / abbrev / 保護語 / 変換禁止 | Yes |
| `spec/core/kdsl-modes.md` | Core | mode / safety / high-risk | Yes |
| `spec/profiles/kdsl-profile-dev-prompt.md` | Profile | AI coding dev-prompt運用 | Profile canonical |
| `spec/profiles/kdsl-converter-prompt.md` | Profile | KDSL Converter出力契約 | Profile canonical |
| `spec/profiles/kdsl-profile-compact-prompt.md` | Profile draft | 一般LLM / Project files向けKDSL-CP | v2 draft |
| `spec/lexicons/kdsl-lexicon-kanji-v1.md` | Lexicon draft | KDSL-CP構造漢字alias | v2 draft |
| `spec/r1/r1-result-spec.md` | R1 | KDSL_RESULT / RT / Evidence / Authority | Yes |
| `spec/lint/kdsl-lint-checklist.md` | Lint | Core/dev-prompt/R1 lint | Yes |
| `spec/lint/kdsl-compact-prompt-lint.md` | Lint draft | KDSL-CP / kanji-v1 / CP-Lift lint | v2 draft |
| `spec/bridge/kdsl-adps-bridge.md` | Bridge | KDSL/KDSL-DP/ADPS/P1/P1L/R1境界 | Yes |
| `spec/bridge/kdsl-cp-packet-bridge.md` | Bridge draft | CP-Lift / Full KDSL / future Packet境界 | v2 draft |
| `spec/glossary.md` | Glossary | v1.1 canonical terms | Yes |
| `spec/glossary-v2-draft.md` | Glossary draft | KDSL-CP/Lexicon/Packet draft terms | v2 draft |
| `templates/*` | Templates | 再利用部品 | No |
| `examples/*` | Examples | 理解補助/運用例 | No |
| `tools/validator/*` | Tools | experimental heuristic lint helpers | No |
| `docs/reviews/*` | Review | 判断記録 | No |

## 4. Canonical ownership

### Syntax / operator / protected words

```text
canonical:
  spec/core/kdsl-core.md

references:
  spec/core/kdsl-spec.md
  spec/lint/kdsl-lint-checklist.md
  spec/lexicons/kdsl-lexicon-kanji-v1.md
```

Lexicon rule:

```text
構造alias追加可
保護語弱化禁止
禁止→禁 短縮禁止
未確認/未実行/承認待/断定禁止の弱化禁止
```

### Mode / safety / high-risk

```text
canonical:
  spec/core/kdsl-modes.md

allowed mode:
  readable|min|dense|lock

forbidden as formal mode:
  dense-ja
  CP:dense-ja
```

Kanji selection:

```text
mode:dense + lexicon:kanji-v1
```

### KDSL-DP / ADPS boundary

```text
canonical:
  spec/bridge/kdsl-adps-bridge.md

required:
  KDSL-DP直接実行禁止
  P1/P1L正規化必須
```

### KDSL_RESULT / R1 / RT:v / NEXT / COMMIT

```text
canonical:
  spec/r1/r1-result-spec.md

required:
  build/diff/lint/test pass != RT:v
  RT:v=対象環境runtime確認済のみ
  NEXT:=提案, 実行許可扱禁止
  COMMIT:=実行済commitまたは推奨message, 自動commit許可扱禁止
```

### KDSL-CP

```text
draft profile:
  spec/profiles/kdsl-profile-compact-prompt.md

required blocks:
  Goal/Input/Output/Guard/Check

kanji-v1 required keys:
  目/材/出/守/確
```

### kanji-v1

```text
draft lexicon:
  spec/lexicons/kdsl-lexicon-kanji-v1.md

structural key aliases:
  役/目/材/出/則/守/調/確

restricted free-text aliases:
  禁/不/実/要
```

### CP-Lift / Packet

```text
draft bridge:
  spec/bridge/kdsl-cp-packet-bridge.md

current lift target:
  Full KDSL profile:dev-prompt

future Packet:
  draft-non-executable
  PKT:v1使用禁止
  registry未定義→実行禁止
```

## 5. Duplication policy

Allowed:

```text
Core:=正本定義
Profile:=用途文脈で再掲
Lexicon:=alias定義
R1:=結果検収文脈で再掲
Lint:=検査項目として再掲
Bridge:=境界規則として再掲
Template:=実運用部品として再掲
Examples:=理解補助として再掲
Design:=採用前提案として再掲
```

Restrictions:

```text
正本と矛盾する再掲禁止
repository現在状態はdocs/project-status.mdと矛盾禁止
example/template/designを正本扱禁止
```

## 6. Update policy

```text
Core operator/保護語変更→breaking候補
mode/safety意味変更→breaking候補
R1 RT:v/NEXT/COMMIT意味変更→breaking候補
KDSL-DP/P1/P1L境界変更→breaking候補
profile追加→compatible候補
lexicon追加→compatible候補
既存alias意味変更→breaking候補
lint追加→compatible候補
example追加→patch候補
validator heuristic改善→patch/compatible候補
validatorを承認者扱い→禁止
未定義Packet実行許可→禁止
```

## 7. Promotion policy

v2 draftから正本へ昇格する場合:

```text
採用理由
不採用代替案
影響範囲
互換性: breaking/compatible/patch
必要lint
必要example
Core/R1/Bridge整合
保護語弱化なし
KDSL-DP/P1/P1L境界破損なし
public履歴/公開済tag/Release Assets非操作
U明示承認
```

## 8. Stable/release dependency

Stable/public-ready化に必要:

```text
README/status/manifest/glossary同期
review/checklist更新
validator maturity/limitations明記
sample expectation runner確認
public-facing guide確定
R1 quickstart
stable tag/release policy
U明示承認
```

Current decision:

```text
v1.1.0 stable:=hold
v2-draft:=continue
Release Assets追加なし
既存tag移動なし
```
