# KDSL Safety Gate Registry v0.1-draft

status: review-candidate
registry: kdsl-sg
version: 0.1-draft
canonical: no
intended_layer: Registry

## 1. Purpose

This registry defines stable candidate IDs for safety gates already expressed in KDSL Core, dev-prompt, R1, Lint, and Bridge specifications.

```text
Registry:=既存safety gate意味の参照ID/状態/継承規則
Registry != 新しい実行権限
Registry != protected wording削除許可
Registry != Packet/R1C実行契約
```

The registry does not weaken or replace the source specifications.

Priority:

```text
Core/R1/Bridge safety meaning > Registry mapping > Profile usage > Example/Tool
```

Conflict:

```text
Registry候補×既存正本→既存正本優先
意味衝突→blocked / 同期修正必須
```

## 2. Current boundary

Until adoption in `spec/manifest.md`:

```text
kdsl-sg@0.1-draft:=review candidate
SG ID単独使用→実行契約扱禁止
unknown SG ID推測禁止
KDSL-Packet直接実行禁止
R1C compact schema扱禁止
```

Even after registry adoption, current Full KDSL prompts must retain critical natural-language wording.

```text
SG ID:=補助参照
Guard/禁止/停止条件:=完全語保持
SG IDのみで禁止/未確認/承認/RT:v条件を置換禁止
```

## 3. Record shape

Candidate representation:

```text
SAFETY_GATES:
  registry: kdsl-sg@0.1-draft
  entries:
    - id: SG-EVIDENCE
      state: hold
      scope: <exact scope>
      reason: <applicability/current condition>
      evidence: <observed evidence reference | none>
      authority: <approval/authority reference | not_required | none>
```

Required fields:

```text
id
state
scope
reason
```

Conditional fields:

```text
evidence:=satisfied根拠またはblocked原因の観測
 authority:=操作/設計変更/公開操作等で権限が必要な場合
```

Restrictions:

```text
scope曖昧禁止
evidence未確認→確認済扱禁止
authority未確認→許可扱禁止
state:satisfiedのみで操作許可扱禁止
```

## 4. State model

Allowed states:

```text
hold
satisfied
blocked
na
```

Definitions:

```text
hold:=gate適用中, 前提/evidence/承認未充足, 関連操作禁止
satisfied:=必要根拠と必要authorityがexact scope内で充足
blocked:=違反/衝突/停止条件発火, 作業停止
na:=非該当を理由付きで確認済み
```

Default handling:

```text
state省略→hold
unknown state→blocked
unknown SG ID→blocked
required gate欠落→blocked
satisfied根拠不足→blocked
na理由なし→blocked
```

State precedence:

```text
blocked > hold > satisfied
na:=severity比較外
```

`na` does not override an inherited or trigger-detected gate.

Allowed transitions:

```text
hold→satisfied: 必要evidence/authority充足
hold→blocked: 違反/衝突/停止条件発火
blocked→hold: 原因解消済, ただし充足確認未完了
blocked→satisfied: 原因解消+全必要条件確認
satisfied→hold: scope拡大/evidence失効/前提変更
na→hold: trigger新規発生
```

Forbidden transition shortcuts:

```text
U承認のみ→SG-RUNTIME satisfied扱禁止
CI/validator pass→SG-AUTHORITY satisfied扱禁止
RT:v→commit/push/release許可扱禁止
NEXT/COMMIT提案→authority充足扱禁止
```

## 5. Inheritance and compression

```text
parentのhold/blocked gate→child Phase/Sliceへ継承必須
scope拡大→satisfied gate再評価, 必要時holdへ戻す
summary/view→hold/blocked gate全件保持
blocked/hold削除禁止
高risk gateの自然文展開削除禁止
```

`na` inheritance:

```text
parent na→child自動na禁止
child側で非該当理由再確認必須
```

Conflict resolution:

```text
同一IDでblocked/hold/satisfied衝突→blocked
同一IDでhold/satisfied衝突→hold
na×trigger evidence→hold|blocked
```

## 6. Registry entries

### SG-DESIGN

Purpose:

```text
要件変/方針変/実装policy変/正本変/UI契約変/data schema/public API/保存形式変更等のD禁止gate
```

Trigger:

```text
要件変更
方針変更
再実装
妥協案採用
正本変更
UI契約変更
data schema/public API/保存形式変更
```

Hold/block:

```text
未承認設計変更→hold
変更を既定方針として実装指示化→blocked
```

Satisfaction basis:

```text
U明示承認
exact scope
採用理由/代替案/影響範囲
必要なdecision record
```

Non-substitutes:

```text
AI推奨
NEXT提案
validator/CI pass
既存実装の推測
```

Source alignment:

```text
spec/core/kdsl-core.md D禁止
spec/profiles/kdsl-profile-dev-prompt.md D禁止
```

### SG-SCOPE

Purpose:

```text
原因未確/対象不明/予期しない差分時の広域修正・上乗せ防止
```

Trigger:

```text
実装/repo操作
原因未確
変更対象/非対象不明
unexpected diff/file/worktree state
preflight不一致
```

Hold/block:

```text
対象Slice不明→hold
未帰属差分へ上乗せ→blocked
原因未確の広域修正→blocked
```

Satisfaction basis:

```text
source-of-truth確認
対象/非対象明示
preflight結果
最小成立Slice
既存差分の帰属確認
```

Source alignment:

```text
spec/profiles/kdsl-profile-dev-prompt.md 最優先/GitHub/Repo
spec/lint/kdsl-lint-checklist.md
```

### SG-EVIDENCE

Purpose:

```text
観測/推論/未観測/未確認/未実行の混同防止
```

Trigger:

```text
実行済/確認済/成功/存在/原因/完了の主張
CMD/VERIFY/FILES/WHY報告
```

Hold/block:

```text
根拠未確認→hold
未実行を実行済扱→blocked
推論を観測扱→blocked
未確認を成功/確認済扱→blocked
```

Satisfaction basis:

```text
実行結果
差分/log/source
OBSERVED/INFERRED/NOT_OBSERVED/UNVERIFIED分離
```

Non-substitutes:

```text
推測
類似事例
validator passのみ
CI passのみ
```

Source alignment:

```text
spec/r1/r1-result-spec.md Evidence separation
spec/core/kdsl-core.md 保護語
```

### SG-RUNTIME

Purpose:

```text
RT:v誤認防止
```

Trigger:

```text
runtime確認
実機確認
RT:v
動作確認済の主張
```

Hold/block:

```text
Runtime未確認→hold
build/diff/lint/test/CI passをRT:v扱→blocked
```

Satisfaction basis:

```text
対象環境runtime確認
U実機観測
U共有runtime log
明示された実機確認結果
```

Non-substitutes:

```text
build pass
diff pass
lint pass
unit test pass
CI pass
静的確認
```

Source alignment:

```text
spec/r1/r1-result-spec.md RT
spec/core/kdsl-modes.md high-risk
```

### SG-AUTHORITY

Purpose:

```text
read/edit/stage/commit/push/release/destructive操作の権限混同防止
```

Trigger:

```text
write操作
commit/push
release/tag/assets
NEXT/COMMIT
public/destructive操作
```

Hold/block:

```text
必要authority未確認→hold
propose_only/forbidを実行→blocked
別操作の許可を横展開→blocked
```

Satisfaction basis:

```text
exact operation
exact target/scope
明示されたpermission basis
AUTHORITY field整合
```

Non-substitutes:

```text
COMMIT.proposed
NEXT
report
PR作成候補
validator/CI pass
```

Source alignment:

```text
spec/r1/r1-result-spec.md Authority separation
```

### SG-ROLLBACK

Purpose:

```text
rollback/revert/restore/clean/未push破棄によるdata・改善済差分損失防止
```

Trigger:

```text
rollback
revert
git restore/clean
未push破棄
全差分破棄
```

Hold/block:

```text
status/diff/退避未確認→hold
全体破棄短絡→blocked
改善済差分を未確認で破棄→blocked
```

Satisfaction basis:

```text
git status/diff確認
patch/status/stat/未追跡退避
問題Slice特定
必要authority
rollback後verify plan
```

Source alignment:

```text
spec/profiles/kdsl-profile-dev-prompt.md Rollback
spec/core/kdsl-core.md D禁止
```

### SG-PUBLIC

Purpose:

```text
public履歴/公開済tag/release/Release Assets保護
```

Trigger:

```text
public repo history
公開済tag
GitHub Release
Release Assets
stable/public-ready操作
```

Hold/block:

```text
別途U明示承認なし→hold
public履歴改竄/公開済tag移動/既存Assets上書前提→blocked
```

Satisfaction basis:

```text
exact public operation
exact ref/tag/release/asset target
別途U明示承認
non-rewrite/non-overwrite確認
```

Restrictions:

```text
承認があっても既存正本で禁止された履歴改竄を自動許可しない
新規公開操作と既存公開物変更を分離
```

Source alignment:

```text
spec/core/kdsl-core.md 保護語
spec/glossary.md public履歴
spec/profiles/kdsl-profile-dev-prompt.md GitHub/Repo
```

### SG-DATA

Purpose:

```text
data migration/破壊操作/data schema/保存形式変更時のdata保護
```

Trigger:

```text
data migration
破壊操作
data schema変更
保存形式変更
不可逆変換
```

Hold/block:

```text
backup/rollback/検証計画不足→hold
保護なし不可逆操作→blocked
未承認schema/保存形式変更→blocked
```

Satisfaction basis:

```text
data保護計画
backup/rollback手順
影響範囲
検証/復旧条件
必要なU承認
```

Source alignment:

```text
spec/core/kdsl-modes.md high-risk
spec/core/kdsl-core.md D禁止
```

### SG-KDSL-DP

Purpose:

```text
KDSL-DP直接実行防止
```

Trigger:

```text
KDSL-DP入力
ADPS Authoring形式
KDP参照
```

Hold/block:

```text
未正規化KDSL-DP→hold
KDSL-DPをAI coding toolへ直接実装指示として渡す→blocked
```

Satisfaction basis:

```text
P1/P1L正規化
必要validation
実行authority確認
```

Restrictions:

```text
KDSL-DP自体をstate:satisfiedの実行契約扱禁止
```

Source alignment:

```text
spec/core/kdsl-core.md ADPS境界語
spec/bridge/kdsl-adps-bridge.md
```

### SG-STOP

Purpose:

```text
停止条件/unknown registry/参照不能/契約衝突時の安全停止
```

Trigger:

```text
明示停止条件
unknown profile/mode/safety/lexicon/envelope/registry/ID
source/template/file/ref取得不能
contract conflict
preflight mismatch
```

Hold/block:

```text
追加確認で解消可能→hold
停止条件発火/契約衝突/unknown推測→blocked
```

Satisfaction basis:

```text
参照取得
正本確認
不一致解消
停止条件解除根拠
必要なU確認/承認
```

Non-substitutes:

```text
記憶
類似名
validator推測
存在推定
```

Source alignment:

```text
spec/core/kdsl-core.md unknown推測禁止
spec/lint/kdsl-lint-checklist.md
spec/bridge/kdsl-cp-packet-bridge.md Packet boundary
```

## 7. Applicability baseline

AI coding / dev-prompt work:

```text
SG-SCOPE
SG-EVIDENCE
SG-AUTHORITY
SG-STOP
```

Conditional:

```text
設計/方針/正本変更→SG-DESIGN
runtime claim→SG-RUNTIME
rollback/revert/discard→SG-ROLLBACK
public/tag/release/assets→SG-PUBLIC
data migration/destructive/schema/save format→SG-DATA
KDSL-DP→SG-KDSL-DP
```

Applicability does not mean every gate must be printed in every human-facing response. It means the gate must remain semantically enforced and must be explicit in future compact contracts that rely on registry references.

## 8. Typed non-substitution matrix

```text
U承認 != runtime evidence
runtime evidence != commit/push/release authority
CI/validator pass != semantic equivalence
CI/validator pass != U承認
NEXT != execution authority
COMMIT.proposed != commit authority
satisfied gate != unrelated gate satisfaction
```

## 9. Versioning

```text
registry name: kdsl-sg
candidate version: 0.1-draft
ID format: SG-[A-Z0-9-]+
ID semantics immutable within adopted major version
semantic breaking change→new major or new ID
unknown alias禁止
one-character gate alias禁止
```

No aliases are defined in v0.1-draft.

## 10. Packet/R1C boundary

This registry candidate does not make KDSL-Packet executable.

```text
SG registry候補あり != Packet schema完成
SG registry候補あり != BASE/TASK/FLOW registry完成
SG registry候補あり != R1C schema完成
SG registry候補あり != Packet lint完成
```

Therefore:

```text
PACKET_DRAFT status: non-executable保持
PKT:v1使用禁止保持
unknown BASE/TASK/FLOW/R1C推測禁止保持
AI coding tool直接投入禁止保持
```

## 11. Promotion requirements

Before adoption in `spec/manifest.md`:

```text
Core/R1/Bridge意味との整合review
ID/状態遷移lint
Full KDSL example
CP-Lift/Packet bridge更新
v2 glossary更新
unknown ID handling確認
CI sample runner pass
U明示承認
```

Promotion does not authorize stable/tag/release/Release Assets operations.
