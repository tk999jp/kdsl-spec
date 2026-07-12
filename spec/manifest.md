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
v2_branch_direction: CompactPrompt / Lexicon / CP-Lift / Safety Gate Registry / Safety Semantics / R1C architecture
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
unknown registry/ID推測禁止
Core保護語をLexicon/Registryで上書禁止
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

Registries:
  既存正本意味を参照するID/state/composition集合
  Registry ID != permission
  Registry reference != protected wording削除許可

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
| `spec/registry/README.md` | Registry index | Registry layer境界/一覧 | v2 draft |
| `spec/registry/kdsl-safety-gate-registry.md` | Registry draft | Safety Gate ID/state/inheritance | v2 draft adopted |
| `spec/registry/kdsl-safety-gate-composition.md` | Registry draft | additive multi-gate composition | v2 draft adopted |
| `spec/registry/kdsl-safety-semantics.md` | Registry semantic draft | bounded protected-language IR / deep scope / multi-generation inheritance | v2 draft adopted subordinate |
| `spec/registry/kdsl-packet-base-registry.md` | Registry draft | Packet normalization baseline IDs | v2 draft adopted / non-executable |
| `spec/registry/kdsl-packet-task-registry.md` | Registry draft | Packet task-class IDs / minimum gate sets | v2 draft adopted / non-executable |
| `spec/registry/kdsl-packet-flow-registry.md` | Registry draft | Packet semantic flow opcodes | v2 draft adopted / non-executable |
| `spec/packet/kdsl-packet-schema.md` | Packet authoring schema draft | PACKET_DRAFT fields / normalization / authority boundary | v2 draft adopted / non-executable |
| `spec/packet/kdsl-packet-normalization-contract.md` | Packet normalization draft | mapping/loss/round-trip evidence / non-executable preview | v2 draft adopted / non-executable |
| `spec/r1/r1-result-spec.md` | R1 | KDSL_RESULT / RT / Evidence / Authority | Yes |
| `spec/r1/r1c-compact-result-schema.md` | R1 serialization draft | canonical R1のcompact serialization profile | v2 draft adopted / canonical R1 subordinate |
| `spec/r1/r1c-optional-block-contract.md` | R1C subordinate contract draft | EVIDENCE/AUTHORITY/ANNUNCIATOR/SAFETY_GATES deep optional-block rules | v2 draft adopted / R1C subordinate |
| `spec/lint/kdsl-lint-checklist.md` | Lint | Core/dev-prompt/R1 lint | Yes |
| `spec/lint/kdsl-compact-prompt-lint.md` | Lint draft | KDSL-CP / kanji-v1 / CP-Lift lint | v2 draft |
| `spec/lint/kdsl-safety-gate-registry-lint.md` | Lint draft | SG ID/state/composition/protected wording lint | v2 draft |
| `spec/lint/kdsl-r1c-lint.md` | Lint draft | R1C field/order/RT/NEXT/COMMIT/round-trip boundary lint | v2 draft adopted |
| `spec/lint/kdsl-packet-lint.md` | Lint draft | Packet envelope/registry/gate/authority/normalization lint | v2 draft adopted / validator first slice integrated |
| `spec/lint/kdsl-packet-normalization-lint.md` | Lint draft | normalization source/target/map/loss/round-trip/authority lint | v2 draft adopted / validator not implemented |
| `spec/bridge/kdsl-adps-bridge.md` | Bridge | KDSL/KDSL-DP/ADPS/P1/P1L/R1境界 | Yes |
| `spec/bridge/kdsl-cp-packet-bridge.md` | Bridge draft | CP-Lift / Full KDSL / Safety Gate / R1C / future Packet境界 | v2 draft |
| `spec/glossary.md` | Glossary | v1.1 canonical terms | Yes |
| `spec/glossary-v2-draft.md` | Glossary draft | KDSL-CP/Lexicon/SG/R1C/Packet draft terms | v2 draft |
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
  spec/registry/kdsl-safety-gate-registry.md
```

Lexicon/Registry rule:

```text
構造alias追加可
Safety Gate参照ID追加可
保護語弱化禁止
禁止→禁 短縮禁止
未確認/未実行/承認待/断定禁止の弱化禁止
SG IDのみで保護語置換禁止
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

### Safety Gate Registry

```text
v2 draft registry:
  spec/registry/kdsl-safety-gate-registry.md

composition:
  spec/registry/kdsl-safety-gate-composition.md

bounded semantics:
  spec/registry/kdsl-safety-semantics.md
  model: kdsl-safety-language@0.1-draft

lint:
  spec/lint/kdsl-safety-gate-registry-lint.md

registry/version:
  kdsl-sg@0.1-draft

states:
  hold|satisfied|blocked|na
```

Ownership rules:

```text
Core/R1/Bridge safety meaning > Registry mapping > Profile usage > Example/Tool
Registry:=既存safety意味の参照ID/state/composition
Registry != 新しい実行権限
Registry state:satisfied != unrelated authority
unknown registry/SG ID推測禁止
hold/blocked gate削除禁止
specialized gate != broader gate解除
current Full KDSL:=SG ID + complete protected wording
bounded semantic match != full semantic equivalence
multi-generation graph pass != complete safety proof
scope relation pass != execution authority
```

Packet boundary:

```text
SG/R1C adoption alone != Packet execution readiness
Packet schema/registry/lint adoption != Packet executable
Packet validator/normalization proof未充足→実行禁止
KDSL-Packet:=non-executable / normalization required保持
PKT:v1使用禁止保持
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

### R1C compact serialization profile

```text
v2-draft adopted profile:
  spec/r1/r1c-compact-result-schema.md

lint:
  spec/lint/kdsl-r1c-lint.md

optional-block contract:
  spec/r1/r1c-optional-block-contract.md

schema/version:
  kdsl-r1c@0.1-draft
```

Ownership rules:

```text
canonical R1 > R1C serialization profile > R1C lint > validator/example
R1C:=canonical R1/KDSL_RESULTのcompact serialization profile
R1C != 独立canonical結果仕様
R1CでRT:v/NEXT/COMMIT意味変更禁止
11必須field省略禁止
short field alias禁止
implicit default禁止
round-trip不成立→Full R1 fallback必須
R1C validator pass != canonical R1適合証明
Phase 3 optional-block structural_pass != semantic equivalence/safety proof/authority
```

### KDSL-Packet authoring schema

```text
v2-draft adopted schema:
  spec/packet/kdsl-packet-schema.md

registries:
  kdsl-packet-base@0.1-draft
  kdsl-packet-task@0.1-draft
  kdsl-packet-flow@0.1-draft

lint:
  spec/lint/kdsl-packet-lint.md
```

Ownership rules:

```text
Core/Profile/R1/Bridge meaning > Packet schema/registry > Packet lint > Example/Tool
KDSL-Packet:=non-executable authoring/transport schema
Packet != Full KDSL/P1/P1L/KDSL_RESULT
BASE/TASK/FLOW ID != authority
STATUS:non-executable固定
NORMALIZE.required:true固定
NORMALIZE.state:not_normalized固定
normalization artifact未生成/未検証→実行禁止
unknown schema/registry/ID/opcode推測禁止
PKT:v1使用禁止
```

### Packet normalization contract

```text
v2-draft adopted contract:
  spec/packet/kdsl-packet-normalization-contract.md

schema/version:
  kdsl-packet-normalization@0.1-draft

lint:
  spec/lint/kdsl-packet-normalization-lint.md
```

Ownership rules:

```text
Core/Profile/R1/Bridge meaning > Packet schema > normalization contract/lint > Example/Tool
NORMALIZATION_DRAFT:=non-executable mapping/loss/round-trip evidence
KDSL_PROMPT_PREVIEW != KDSL_PROMPT
P1/P1L schema unresolved→TARGET blocked / preview禁止
semantic_equivalence:not_proven固定
AUTHORITY.execution_authority:none固定
normalization validator/mapper未実装→normalized扱禁止
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

current Packet:
  schema/BASE/TASK/FLOW/lint:=v2-draft adopted
  Packet validator:=first heuristic slice integrated
  normalization contract/lint:=v2-draft adopted
  normalization validator/mapper/round-trip proof:=not implemented
  executable:=no
  PKT:v1使用禁止
  normalization/stable dependency未充足→実行禁止
```

## 5. Duplication policy

Allowed:

```text
Core:=正本定義
Profile:=用途文脈で再掲
Lexicon:=alias定義
Registry:=既存正本意味の参照ID/state/compositionとして再掲
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
RegistryでCore/R1/Bridge意味変更禁止
Registry IDで保護語置換禁止
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
registry追加→compatible draft候補
adopted registry ID意味変更→breaking候補または新ID必須
registry state意味変更→breaking候補
lint追加→compatible候補
R1C serialization profile追加→compatible v2-draft候補
R1C RT:v/NEXT/COMMIT意味変更→breaking候補
R1C required field削除/alias置換/default追加→breaking候補
Packet schema/registry追加→compatible v2-draft候補
Packet adopted ID/opcode意味変更→breaking候補または新ID必須
Packet authority/normalization非実行境界弱化→breaking/prohibited
normalization schema/map/loss/round-trip意味変更→breaking候補
P1/P1L unresolved→resolved変更→target schema adoption必須
example追加→patch候補
validator heuristic改善→patch/compatible候補
validatorを承認者扱い→禁止
Registryを権限付与者扱い→禁止
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

Registry promotion additional checks:

```text
ID意味固定
state遷移整合
composition不足なし
unknown ID handling
protected wording併記
Packet非実行境界保持
validator未実装→pass扱禁止
```

## 8. Stable/release dependency

Stable/public-ready化に必要:

```text
README/status/manifest/glossary同期
review/checklist更新
validator maturity/limitations明記
sample expectation runner確認
Packet validator実装/期待結果
normalization contract/lint ownership整合
normalization validator/mapper/round-trip証拠
public-facing guide確定
R1 quickstart
stable tag/release policy
U明示承認
```

Current decision:

```text
v1.1.0 stable:=hold
v2-draft:=continue
kdsl-sg@0.1-draft:=v2-draft registry adopted
Safety Gate validator:=first heuristic slice integrated
kdsl-r1c@0.1-draft:=v2-draft serialization profile adopted
R1C validator:=first heuristic slice integrated
canonical R1 replacement:=none
kdsl-packet@0.1-draft:=v2-draft authoring schema adopted
Packet BASE/TASK/FLOW registries:=v2-draft adopted
Packet lint:=v2-draft adopted / validator first slice integrated
kdsl-packet-normalization@0.1-draft:=v2-draft adopted / non-executable
normalization lint:=v2-draft adopted / validator not implemented
normalization mapper/round-trip proof:=not implemented
KDSL-Packet:=draft-non-executable / normalization required
Release Assets追加なし
既存tag移動なし
```
