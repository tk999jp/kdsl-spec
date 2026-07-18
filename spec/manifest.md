# KDSL Spec Manifest v2-draft-sync

目的: `kdsl-spec` 内の各fileの責務・正本性・参照関係を定義し、重複規則の更新不一致を防ぐ。

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
validator: partial heuristic helpers / non-authoritative
v2_direction: CompactPrompt / Safety Semantics / R1C / Packet / P1L-P1 contract / K1-PF1 runtime control / non-executable Packet→P1 previews
```

```text
v0.1.0-draft tag:=履歴として維持
v1.1.0-rc1:=experimental historical baseline
v1.1.0 stable:=hold
v2-draft:=優先設計線
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

```text
format: KDSL
profile: compact-prompt|dev-prompt|converter|lint
mode: readable|min|dense|lock
safety: normal|lock-critical|lock-all
lexicon: standard|kanji-v1
envelope: plain|packet-draft|result
```

```text
lexicon != mode
lexicon != profile
unknown profile/mode/safety/lexicon/envelope推測禁止
unknown registry/schema/ID推測禁止
Core保護語をLexicon/Registryで上書禁止
```

## 2. Specification layers

```text
Core:
  KDSL本体/operator/保護語/変換禁止/mode/safety

Profiles:
  用途別運用仕様

Lexicons:
  宣言済み構造alias。Core保護語を上書きしない

Registries:
  既存正本意味を参照するID/state/composition
  Registry ID != permission

ADPS Contracts:
  KDSL-DPから正規化されたP1LとP1 serialization
  valid != executable
  runtime binding/authority evaluationとは分離

Runtime Control:
  K1 canonical runtime-control semantics
  PF1 project-scoped exact definitions/restrictions/ceilings/capability requirements/routing
  valid != executable|authority grant
  binding evidence:=external content-addressed record
  evaluator/runtime bindingとは分離

Packet / Normalization:
  non-executable authoring/transport/mapping/preview evidence

R1:
  結果証跡/検収仕様

Lint:
  意味/safety gate/構造/authority/round-tripの保持・欠落検査

Bridge:
  KDSL-DP/ADPS/P1L/P1/R1/CP-Lift/Packet境界

Templates / Examples / Tools / Docs:
  補助資料。仕様正本・承認・RT:v・authorityの代替ではない

Project Status:
  repository現在状態の運用上の状態正本。仕様正本ではない
```

## 3. File responsibility map

| Path | Layer | Responsibility | Canonical? |
|---|---|---|---|
| `docs/project-status.md` | Status | repository/public/release/validator現在状態 | Operational status canonical |
| `spec/core/kdsl-spec.md` | Core | KDSL全体定義 / KDSL_PROMPT / KDSL_RESULT入口 | Yes |
| `spec/core/kdsl-core.md` | Core | operator / abbrev / 保護語 / 変換禁止 | Yes |
| `spec/core/kdsl-modes.md` | Core | mode / safety / high-risk | Yes |
| `spec/profiles/kdsl-profile-dev-prompt.md` | Profile | AI coding dev-prompt運用 | Profile canonical |
| `spec/profiles/kdsl-converter-prompt.md` | Profile | Converter出力契約 | Profile canonical |
| `spec/profiles/kdsl-profile-compact-prompt.md` | Profile draft | KDSL-CP | v2 draft |
| `spec/lexicons/kdsl-lexicon-kanji-v1.md` | Lexicon draft | KDSL-CP構造漢字alias | v2 draft |
| `spec/registry/README.md` | Registry index | Registry境界/一覧 | v2 draft |
| `spec/registry/kdsl-safety-gate-registry.md` | Registry | Safety Gate ID/state/inheritance | v2 draft adopted |
| `spec/registry/kdsl-safety-gate-composition.md` | Registry | additive multi-gate composition | v2 draft adopted |
| `spec/registry/kdsl-safety-semantics.md` | Registry semantics | bounded protected-language IR | v2 draft adopted subordinate |
| `spec/registry/kdsl-packet-base-registry.md` | Packet registry | normalization baseline IDs | v2 draft adopted / non-executable |
| `spec/registry/kdsl-packet-task-registry.md` | Packet registry | task-class IDs / minimum gate sets | v2 draft adopted / non-executable |
| `spec/registry/kdsl-packet-flow-registry.md` | Packet registry | semantic flow opcodes | v2 draft adopted / non-executable |
| `spec/adps/README.md` | ADPS index | P1L/P1 schema・lint・validator・Packet mapping index | v2 draft adopted index |
| `spec/adps/kdsl-p1l-contract-schema.md` | ADPS schema | lossless structured normalized contract | v2 draft adopted / non-executable |
| `spec/adps/kdsl-p1-compact-contract-schema.md` | ADPS serialization | P1Lのreversible compact serialization | v2 draft adopted subordinate / non-executable |
| `spec/runtime/README.md` | Runtime Control index | K1/PF1 schema・canonicalization・lint index | v2 draft adopted index |
| `spec/runtime/kdsl-k1-runtime-kernel-schema.md` | Runtime Control schema | canonical K1 semantics/state/binding requirements | v2 draft adopted / non-executable |
| `spec/runtime/kdsl-pf1-project-profile-schema.md` | Runtime Control schema | project-scoped PF1 defaults/restrictions/ceilings/capability/routing | v2 draft adopted / non-executable |
| `spec/runtime/kdsl-runtime-control-canonicalization.md` | Runtime Control identity | schema-ordered JSON projection / SHA-256 | v2 draft adopted |
| `spec/runtime/kdsl-binding-evidence-schema.md` | Runtime Control evidence | external content-addressed binding dimensions/provenance | v2 draft adopted / non-executable |
| `spec/packet/kdsl-packet-schema.md` | Packet schema | PACKET_DRAFT fields / authority / normalization boundary | v2 draft adopted / non-executable |
| `spec/packet/kdsl-packet-normalization-contract.md` | Normalization schema | generic mapping/loss/round-trip evidence | v2 draft adopted / non-executable |
| `spec/packet/kdsl-packet-p1-normalization-contract.md` | Target normalization | BASE-ADPS-P1→P1L/P1 preview mapping | v2 draft adopted subordinate / non-executable |
| `spec/packet/kdsl-packet-semantic-property-contract.md` | Packet property | strict source/preview property comparison | v2 draft adopted subordinate |
| `spec/r1/r1-result-spec.md` | R1 | KDSL_RESULT / RT / Evidence / Authority | Yes |
| `spec/r1/r1c-compact-result-schema.md` | R1 serialization | canonical R1 compact profile | v2 draft adopted subordinate |
| `spec/r1/r1c-optional-block-contract.md` | R1C contract | optional deep blocks | v2 draft adopted subordinate |
| `spec/lint/kdsl-lint-checklist.md` | Lint | Core/dev-prompt/R1 lint | Yes |
| `spec/lint/kdsl-compact-prompt-lint.md` | Lint | KDSL-CP / kanji-v1 / CP-Lift | v2 draft |
| `spec/lint/kdsl-safety-gate-registry-lint.md` | Lint | SG ID/state/composition/protected wording | v2 draft adopted |
| `spec/lint/kdsl-r1c-lint.md` | Lint | R1C order/RT/NEXT/COMMIT/round-trip | v2 draft adopted |
| `spec/lint/kdsl-p1-p1l-lint.md` | Lint | P1L/P1 profile/authority/runtime/round-trip | v2 draft adopted |
| `spec/lint/kdsl-k1-pf1-lint.md` | Lint | K1/PF1 identity/completion/authority/capability/routing/boundary | v2 draft adopted |
| `spec/lint/kdsl-binding-evidence-lint.md` | Lint | binding evidence identity/dimensions/provenance/boundary | v2 draft adopted |
| `spec/lint/kdsl-packet-lint.md` | Lint | Packet envelope/registry/gate/authority | v2 draft adopted |
| `spec/lint/kdsl-packet-normalization-lint.md` | Lint | generic normalization mapping/loss/round-trip | v2 draft adopted |
| `spec/lint/kdsl-packet-p1-normalization-lint.md` | Lint | Packet→P1L/P1 target preview/property | v2 draft adopted subordinate |
| `spec/bridge/kdsl-adps-bridge.md` | Bridge | KDSL/KDSL-DP/ADPS/P1L/P1/R1境界 | Yes |
| `spec/bridge/kdsl-cp-packet-bridge.md` | Bridge draft | CP-Lift / Packet境界 | v2 draft |
| `spec/glossary.md` | Glossary | canonical/v2-sync terms | Yes |
| `spec/glossary-v2-draft.md` | Glossary draft | v2 draft terms | v2 draft |
| `templates/*` | Templates | 再利用部品 | No |
| `examples/*` | Examples | 理解補助 | No |
| `tools/validator/*` | Tools | experimental heuristic parser/lint/property/round-trip | No |
| `docs/design/*` / `docs/reviews/*` | Design/Review | 判断・証跡記録 | No |

## 4. Canonical ownership

### 4.1 Core / protected wording

```text
canonical: spec/core/kdsl-core.md
references: spec/core/kdsl-spec.md / spec/lint/kdsl-lint-checklist.md
```

```text
構造alias追加可
Safety Gate参照ID追加可
保護語弱化禁止
禁止→禁 短縮禁止
未確認/未実行/承認待/断定禁止の弱化禁止
SG IDのみで保護語置換禁止
```

### 4.2 Mode / safety

```text
canonical: spec/core/kdsl-modes.md
mode: readable|min|dense|lock
safety: normal|lock-critical|lock-all
kanji selection:=mode:dense + lexicon:kanji-v1
```

### 4.3 Safety Gate Registry

```text
registry: kdsl-sg@0.1-draft
canonical draft: spec/registry/kdsl-safety-gate-registry.md
composition: spec/registry/kdsl-safety-gate-composition.md
bounded semantics: spec/registry/kdsl-safety-semantics.md
states: hold|satisfied|blocked|na
```

```text
Core/R1/Bridge safety meaning > Registry mapping > Profile usage > Example/Tool
Registry != 新しい実行権限
state:satisfied != unrelated authority
unknown SG ID/state→blocked
hold/blocked gate削除禁止
specialized gate != broader gate解除
current Full KDSL:=SG ID + complete protected wording
bounded semantic/property pass != complete safety proof|authority
```

### 4.4 KDSL-DP / P1L / P1

```text
boundary: spec/bridge/kdsl-adps-bridge.md
P1L: spec/adps/kdsl-p1l-contract-schema.md / kdsl-p1l@0.1-draft
P1: spec/adps/kdsl-p1-compact-contract-schema.md / kdsl-p1@0.1-draft
lint: spec/lint/kdsl-p1-p1l-lint.md
validator notes: tools/validator/kdsl-p1-contract-implementation-notes.md
```

Ownership:

```text
Core/Profile/R1/Bridge meaning
> P1L canonical v2-draft contract
> P1 subordinate serialization
> P1/P1L lint
> validator/example/tool
```

```text
KDSL-DP直接実行禁止
KDSL-DP→P1L/P1正規化必須
P1L/P1 valid != executable
P1L/P1 lint/round-trip pass != authority
profile completion != inference
all authority rails explicit
BINDING.executable:false
```

Authority rails:

```text
read/edit/stage/commit/push/release/public_repo/destructive_ops
```

Validator state:

```text
parser/validator/round-trip:=Phase 7C bounded first slice integrated
P1L marker:=shared AST v2 first-class registration
shared first-class P1L registration:=Phase 8 integrated
checker-local bootstrap:=removed
P1L/P1 corpus:=14 / failed 0
shared P1L compatibility corpus:=10 / failed 0
validator pass != runtime binding|authority|RT:v
```

Legacy boundary:

```text
project-local colon P1:=legacy operational evidence
loss=P→exact compatibility evidence時のみprofile_completed候補
loss=L意味推測禁止
AP/H意味推測禁止
missing Authority rails→canonical promotion blocked
```

### 4.4.1 K1 / PF1 Runtime Control

```text
index: spec/runtime/README.md
K1: spec/runtime/kdsl-k1-runtime-kernel-schema.md / kdsl-k1@0.1-draft
PF1: spec/runtime/kdsl-pf1-project-profile-schema.md / kdsl-pf1@0.1-draft
canonicalization: spec/runtime/kdsl-runtime-control-canonicalization.md / kdsl-runtime-control-c14n@0.1-draft
lint: spec/lint/kdsl-k1-pf1-lint.md
```

```text
Core/R1/Bridge meaning
> P1L/P1 contract meaning
> K1 runtime-control semantics
> PF1 project definitions
> binding-evidence schema
> bounded parser/validator
> future binding evaluator
> route/skill/tool
> example/template/tool
```

```text
K1/PF1 valid != executable|authority grant
PF1 may narrow but never widen P1L authority
capability != permission
Stop continuation != authority
routing != authority
binding evidence:=external content-addressed record
BINDING.executable:false under P1L/P1 v0.1 draft
parser/validator/exact compatibility:=Phase 9C bounded first slice integrated
binding-evidence schema:=kdsl-binding-evidence@0.1-draft adopted
runtime evaluator/binding:=not implemented
```

### 4.5 R1 / R1C

```text
R1 canonical: spec/r1/r1-result-spec.md
R1C: spec/r1/r1c-compact-result-schema.md / kdsl-r1c@0.1-draft
```

```text
canonical R1 > R1C serialization > R1C lint > validator/example
R1C != independent canonical result spec
11 required fields省略禁止
implicit default禁止
round-trip不成立→Full R1 fallback
build/diff/lint/test/CI pass != RT:v
RT:v=対象環境runtime確認済のみ
NEXT:=提案, 実行許可扱禁止
COMMIT:=実行済commitまたは推奨message, 自動commit許可扱禁止
```

### 4.6 Packet

```text
schema: spec/packet/kdsl-packet-schema.md / kdsl-packet@0.1-draft
registries: kdsl-packet-base/task/flow@0.1-draft
lint: spec/lint/kdsl-packet-lint.md
```

```text
KDSL-Packet:=non-executable authoring/transport schema
Packet != Full KDSL/P1L/P1/KDSL_RESULT
BASE/TASK/FLOW ID != authority
STATUS:non-executable固定
NORMALIZE.required:true固定
NORMALIZE.state:not_normalized固定
property pass != semantic equivalence|safety proof|normalization completion|authority
unknown schema/registry/ID/opcode推測禁止
PKT:v1使用禁止
```

### 4.7 Generic Packet normalization

```text
contract: spec/packet/kdsl-packet-normalization-contract.md
schema: kdsl-packet-normalization@0.1-draft
lint: spec/lint/kdsl-packet-normalization-lint.md
```

```text
NORMALIZATION_DRAFT:=non-executable mapping/loss/round-trip evidence
KDSL_PROMPT_PREVIEW != KDSL_PROMPT
TARGET.executable:false
semantic_equivalence:not_proven
AUTHORITY.execution_authority:none
normalization preview != executable target
```

### 4.8 Packet→P1L/P1 target normalization

```text
contract: spec/packet/kdsl-packet-p1-normalization-contract.md
schema: kdsl-packet-p1-normalization@0.1-draft
lint: spec/lint/kdsl-packet-p1-normalization-lint.md
mapper: tools/validator/kdsl_packet_normalize_p1.py
property: tools/validator/kdsl_packet_p1_property.py
implementation notes: tools/validator/kdsl-packet-p1-normalization-implementation-notes.md
```

Applicability:

```text
BASE.id: BASE-ADPS-P1
NORMALIZE.target: P1L|P1
source Packet semantic pass必須
```

Resolved preview contract:

```text
TARGET.schema: kdsl-p1l@0.1-draft|kdsl-p1@0.1-draft
TARGET.resolution: resolved
TARGET.executable: false
OUTPUT.marker: P1L_PREVIEW|P1_PREVIEW
OUTPUT.executable: false
SOURCE.packet_status: non-executable
SOURCE.normalize_state: not_normalized
ROUND_TRIP.structural_equivalence: pass
ROUND_TRIP.semantic_equivalence: not_proven
AUTHORITY.execution_authority: none
```

```text
P1L_PREVIEW != P1L:
P1_PREVIEW != P1|
Packet→P1L/P1 property pass != Packet normalized|runtime binding|authority|RT:v
```

Authority mapping:

```text
read/edit/stage/commit/push/release:=source rails exact copy
public_repo:=forbid
destructive_ops:=forbid
```

The additional rails are explicit non-widening safety floors, not hidden defaults.

Implementation state:

```text
Phase 7D target-specific mapper/property first slice integrated
corpus: 17 / failed 0
property consumer: NormalizationCompatibilityView
legacy normalization structural helper consumers: none
```

### 4.9 CompactPrompt / CP-Lift

```text
profile: spec/profiles/kdsl-profile-compact-prompt.md
lexicon: spec/lexicons/kdsl-lexicon-kanji-v1.md
bridge: spec/bridge/kdsl-cp-packet-bridge.md
```

```text
KDSL-CP required blocks: Goal/Input/Output/Guard/Check
kanji-v1 keys: 役/目/材/出/則/守/調/確
implementation/repo/runtime/public操作→CP-Lift to profile:dev-prompt
```

## 5. Duplication policy

Allowed:

```text
Core:=正本定義
Profile:=用途文脈で再掲
Lexicon:=alias定義
Registry:=正本意味の参照ID/state/composition
ADPS Contract:=正規化契約/serialization境界
Runtime Control:=K1/PF1 non-executable semantics/project definitions
Packet Contract:=non-executable mapping/property境界
R1:=結果検収文脈
Lint:=検査項目
Bridge:=境界規則
Template/Example/Design:=補助説明
```

Restrictions:

```text
正本と矛盾する再掲禁止
RegistryでCore/R1/Bridge意味変更禁止
Registry IDで保護語置換禁止
P1でP1L required meaning省略禁止
previewでcanonical executable-looking marker露出禁止
repository現在状態はdocs/project-status.mdと矛盾禁止
example/template/designを正本扱禁止
validator/property/toolをauthority/RT:v証明扱い禁止
```

## 6. Update policy

```text
Core operator/保護語変更→breaking候補
mode/safety意味変更→breaking候補
R1 RT:v/NEXT/COMMIT意味変更→breaking候補
KDSL-DP/P1L/P1境界変更→breaking候補
P1L required field/authority rail削除→breaking/prohibited
P1 compact key/ownership/grammar変更→breakingまたは新schema ID必須
P1L/P1 BINDING.executable:false弱化→breaking/prohibited
K1 state/authority/capability分離変更→breaking候補
PF1 ceiling vocabulary/canonicalization変更→breakingまたは新schema ID必須
K1/PF1 validをauthority/executable扱い→prohibited
Packet authority/normalization非実行境界弱化→breaking/prohibited
Packet P1 target mapping/preview marker意味変更→breakingまたは新schema ID必須
P1L_PREVIEW→P1L: / P1_PREVIEW→P1| promotion→prohibited without separate executable contract
shared parser marker登録変更→separate compatibility/consumer review必須
lint/validator heuristic追加→compatible/patch候補
validator/propertyを承認者扱い→禁止
未定義Packet実行許可→禁止
```

## 7. Promotion policy

v2 draft昇格時に必要:

```text
採用理由 / 不採用代替案 / 影響範囲
互換性: breaking|compatible|patch
必要lint/example/validator evidence
Core/R1/Bridge整合
保護語弱化なし
KDSL-DP/P1L/P1境界破損なし
Packet非実行境界保持
public履歴/公開済tag/Release Assets非操作
U明示承認
```

P1L/P1 additional checks:

```text
ownership固定
all authority rails explicit
profile completion evidence固定
P1 round-trip fallback
legacy alias推測禁止
RUNTIME pre-execution/result境界
BINDING.executable:false
```

K1/PF1 additional checks:

```text
exact id/revision/digest/canonicalization
completion != inference
PF1 ceiling non-widening
capability != permission
approval scope/operation/time/revocation exact
Stop continuation/routing != authority
binding evidence external/content-addressed/non-executable
bounded parser/validator scope明記 / binding-evidence schema明記 / evaluator未実装明記
```

Packet→P1L/P1 additional checks:

```text
all Packet fields mapped
source authority rails exact
additional rails explicit forbid
preview marker separation
Packet source not_normalized保持
semantic_equivalence:not_proven
execution_authority:none
```

## 8. Stable / release dependency

Stable/public-ready化に必要:

```text
README/status/manifest/glossary同期
review/checklist更新
validator maturity/limitations明記
sample expectation runner確認
P1L/P1 parser/validator/round-trip証拠
Packet/normalization mapping/property証拠
runtime binding/K1-PF1方針
public-facing guide/R1 quickstart
stable tag/release policy
U明示承認
```

Current decision:

```text
v1.1.0 stable:=hold
v2-draft:=continue
kdsl-sg@0.1-draft:=adopted
kdsl-r1c@0.1-draft:=adopted subordinate
kdsl-p1l@0.1-draft:=adopted canonical structured contract / non-executable
kdsl-p1@0.1-draft:=adopted subordinate serialization / non-executable
P1L/P1 validator/round-trip:=Phase 7C first bounded slice integrated
P1L shared AST v2 first-class registration:=Phase 8 integrated
P1L/P1 runtime binding:=not implemented
kdsl-k1@0.1-draft:=adopted canonical runtime-control semantics / non-executable / no authority grant
kdsl-pf1@0.1-draft:=adopted project runtime-control profile / non-executable / no authority grant
kdsl-runtime-control-c14n@0.1-draft:=adopted canonical projection/digest rules
K1/PF1 parser/validator/exact compatibility:=Phase 9C bounded first slice integrated
kdsl-binding-evidence@0.1-draft:=adopted external content-addressed evidence record / non-executable
kdsl-packet@0.1-draft:=adopted authoring schema / non-executable
kdsl-packet-normalization@0.1-draft:=adopted / non-executable
kdsl-packet-p1-normalization@0.1-draft:=Phase 7D target-specific first slice integrated
P1L_PREVIEW/P1_PREVIEW:=adopted non-executable target-specific markers
Packet source normalized-state promotion:=not implemented
KDSL-Packet:=draft-non-executable / normalization required
Release Assets追加なし
既存tag移動なし
```
