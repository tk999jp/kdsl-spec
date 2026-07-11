# Safety Gate Registry Validator First Slice

status: implementation-candidate
script: `tools/validator/kdsl_safety_gate.py`
source_registry: `spec/registry/kdsl-safety-gate-registry.md`
source_composition: `spec/registry/kdsl-safety-gate-composition.md`
source_lint: `spec/lint/kdsl-safety-gate-registry-lint.md`

## 1. Purpose

Provide a lightweight heuristic validator for explicit `SAFETY_GATES:` records.

```text
validator:=構造/known ID/state/代表compositionの補助lint
validator != safety proof
validator != semantic equivalence proof
validator != U承認
validator != RT:v
validator != execution authority
```

## 2. First-slice checks

```text
registry:=kdsl-sg@0.1-draft
known IDs:=10 adopted v2-draft IDs
known states:=hold|satisfied|blocked|na
required entry fields:=id/state/scope/reason
ID重複検出
ID format検査
state:satisfied→evidence/authority必須
state:blocked→evidence欠落warn
state:na→非該当reason必須
dev-prompt baseline:=SG-SCOPE/SG-EVIDENCE/SG-AUTHORITY/SG-STOP
代表composition欠落検出
```

## 3. Composition heuristics

The first slice detects representative text triggers and requires the adopted additive composition.

```text
rollback/revert/未push破棄/git restore/git clean
→ SG-DESIGN/SG-ROLLBACK/baseline gates

data migration/data schema/保存形式/不可逆変換
→ SG-DESIGN/SG-DATA/baseline gates

public履歴/公開済tag/Release Assets/GitHub Release/stable-public-ready
→ SG-PUBLIC/SG-EVIDENCE/SG-AUTHORITY/SG-STOP

RT:v/実機確認/runtime verification
→ SG-EVIDENCE/SG-RUNTIME

KDSL-DP/ADPS Authoring/KDP
→ SG-KDSL-DP/SG-EVIDENCE/SG-AUTHORITY/SG-STOP
```

These are representative lexical heuristics, not a complete semantic trigger parser.

## 4. Context boundary

```text
SAFETY_GATES blockなし→対象外pass/info
profile:dev-promptまたはKDSL_PROMPTあり→baseline gate検査
current Full KDSL protected wording検査→このsliceでは未実装
inheritance across multiple documents/phases→未実装
aggregate state calculation across parent/child records→未実装
```

The `--target all` wrapper can include this checker because documents without a `SAFETY_GATES:` block are treated as out of scope.

## 5. Exit codes

```text
0: pass
1: warn
2: fail
```

Warnings currently cover a `blocked` entry without observed conflict/stop evidence. Unknown registry/ID/state, required-field absence, unsupported satisfaction basis, baseline absence, and composition absence are failures.

## 6. Non-substitution boundary

```text
state:satisfied != operation authority
not_required:=explicit authority non-requirement, automatic permissionではない
CI/validator pass != SG semantic proof
SG validator pass != protected wording保持証明
SG validator pass != Packet executable
```

## 7. Packet boundary

```text
Safety Gate validator実装 != Packet schema完成
Safety Gate validator実装 != BASE/TASK/FLOW registry完成
Safety Gate validator実装 != R1C schema完成
PKT:v1使用禁止保持
KDSL-Packet:=draft-non-executable保持
```

## 8. Known limitations

```text
single SAFETY_GATES blockのみ解析
YAML parserではなくline-based parser
quoted/multiline/nested valuesの完全解析なし
full natural-language parserなし
full negation parserなし
triggerが説明/例示か実操作かの完全識別なし
protected wording replacement lint未実装
parent-child inheritance lint未実装
```
