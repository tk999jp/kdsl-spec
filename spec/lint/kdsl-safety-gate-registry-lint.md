# KDSL Safety Gate Registry Lint v0.1-draft

status: review-candidate
source: spec/registry/kdsl-safety-gate-registry.md
validator: not_implemented

## 1. Purpose

Detect missing, weakened, conflicting, or authority-confusing safety gate records.

```text
lint pass != semantic equivalence
lint pass != safety proof
lint pass != RT:v
lint pass != U承認
lint pass != execution authority
lint pass != release readiness
```

## 2. Structural checks

```text
registry name/versionあり
entries listあり
id/state/scope/reasonあり
ID重複なし
ID format=SG-[A-Z0-9-]+
known IDのみ
known stateのみ: hold|satisfied|blocked|na
```

Failure:

```text
unknown registry→不合格
unknown SG ID→不合格
unknown state→不合格
required field欠落→不合格
```

## 3. State checks

### hold

```text
applicability/reasonあり
関連操作を許可済扱禁止
不足evidence/authorityを明示
```

### satisfied

```text
exact scopeあり
必要evidenceあり
必要authorityあり
別gate充足への横展開なし
```

### blocked

```text
block原因あり
停止対象あり
解除条件を必要時明示
blocked gate削除禁止
```

### na

```text
非該当理由あり
trigger evidenceなし
inherited gateをnaで上書禁止
```

## 4. Required gate applicability

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
runtime claim/RT:v→SG-RUNTIME
rollback/revert/restore/clean/破棄→SG-ROLLBACK
public/tag/release/Release Assets→SG-PUBLIC
data migration/破壊/schema/保存形式→SG-DATA
KDSL-DP→SG-KDSL-DP
```

Missing applicable gate:

```text
compact registry contract→不合格
current Full KDSL natural-language contract→gate意味保持を検査し、ID欠落だけでは不合格にしない
```

## 5. Protected wording checks

Current Full KDSL:

```text
SG IDのみで禁止文を置換禁止
禁止/未確認/未実行/承認待/断定禁止を完全語保持
RT:v条件保持
NEXT/COMMIT権限分離保持
KDSL-DP直接実行禁止保持
public履歴/公開済tag/Release Assets保護保持
```

Invalid:

```text
SG-DESIGNのみでD禁止文なし
SG-RUNTIMEのみでRT:v条件なし
SG-AUTHORITYのみでcommit/push/release権限条件なし
SG-KDSL-DPのみでP1/P1L正規化条件なし
```

## 6. Inheritance checks

```text
parent hold/blocked→childへ保持
scope拡大時satisfied再評価
summary/viewでhold/blocked欠落なし
parent na→child自動naなし
```

State conflict:

```text
blocked×hold/satisfied→blocked採用
hold×satisfied→hold採用
na×trigger→hold|blocked
```

Unsafe downgrade:

```text
blocked→satisfied without resolution/evidence→不合格
hold→satisfied without evidence/authority→不合格
satisfied scope拡大後も再評価なし→不合格
```

## 7. Typed non-substitution checks

```text
U承認→SG-RUNTIME satisfied扱禁止
CI/validator pass→SG-AUTHORITY satisfied扱禁止
RT:v→commit/push/release許可扱禁止
NEXT→実行許可扱禁止
COMMIT.proposed→commit許可扱禁止
SG-EVIDENCE satisfied→SG-RUNTIME自動satisfied禁止
```

## 8. Gate-specific minimum checks

### SG-DESIGN

```text
変更対象/影響範囲/承認basis確認
未承認方針変→実装指示禁止
```

### SG-SCOPE

```text
source-of-truth/target/non-target/preflight確認
原因未確→広域修正禁止
未帰属差分上乗せ禁止
```

### SG-EVIDENCE

```text
観測/推論/未観測/未確認分離
未実行→実行済扱禁止
未確認→確認済/成功扱禁止
```

### SG-RUNTIME

```text
RT:v basisあり
build/diff/lint/test/CI pass != RT:v
```

### SG-AUTHORITY

```text
operation別authority分離
propose_only/forbid遵守
```

### SG-ROLLBACK

```text
status/diff/退避/scope/verify plan確認
全体破棄短絡禁止
```

### SG-PUBLIC

```text
別途U明示承認
exact public target
public履歴改竄/公開済tag移動/既存Assets上書前提禁止
```

### SG-DATA

```text
data保護/backup/rollback/verify/承認確認
```

### SG-KDSL-DP

```text
KDSL-DP直接実行禁止
P1/P1L正規化必須
```

### SG-STOP

```text
unknown registry/ID推測禁止
参照不能を存在/内容確認済扱禁止
停止条件発火時blocked保持
```

## 9. Packet/R1C boundary checks

```text
SG registry候補あり→Packet executable扱禁止
PKT:v1使用禁止保持
PACKET_DRAFT status:non-executable/schema:undefined保持
unknown BASE/TASK/FLOW/R1C推測禁止
```

## 10. Result classification

Pass:

```text
known ID/state
required fieldsあり
applicable gate保持
state/evidence/authority整合
protected wording弱化なし
Packet非実行境界保持
```

Conditional pass:

```text
low-risk説明文の表記差のみ
意味変化risk記録済
```

Fail:

```text
unknown ID/state
required gate欠落
blocked/hold削除
satisfied根拠不足
naによるgate bypass
protected wording置換
authority/runtime/evidence混同
Packet直接実行化
```

## 11. Validator boundary

```text
validator未実装→自動pass扱禁止
future validator pass != semantic equivalence
future validator pass != U承認
future validator pass != RT:v
future validator pass != release readiness
```
