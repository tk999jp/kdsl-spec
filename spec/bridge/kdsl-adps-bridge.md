# KDSL / KDSL-DP / ADPS Bridge v0.3

目的: KDSL本体とKDSL-DP / ADPS / P1L / P1 / KDSL_PROMPT / KDSL_RESULTの境界を定義する。

## 1. 位置づけ

```text
KDSL:=LLM直投入可能な安全gate保持型prompt記法
KDSL-DP:=ADPS向けAuthoring形式, 実行指示ではない
P1L:=KDSL-DP等から正規化されたlossless structured contract candidate
P1:=P1Lに従属するcompact serialization
K1/PF1:=Runtime Control
R1:=Evidence
KDSL_RESULT:=R1系の人間/AI向け結果block
```

KDSL-DPはKDSL-familyだが、KDSL本体の直投入前提を継承しない。

Canonical v2-draft schema:

```text
P1L: spec/adps/kdsl-p1l-contract-schema.md / kdsl-p1l@0.1-draft
P1:  spec/adps/kdsl-p1-compact-contract-schema.md / kdsl-p1@0.1-draft
K1:  spec/runtime/kdsl-k1-runtime-kernel-schema.md / kdsl-k1@0.1-draft
PF1: spec/runtime/kdsl-pf1-project-profile-schema.md / kdsl-pf1@0.1-draft
runtime c14n: spec/runtime/kdsl-runtime-control-canonicalization.md / kdsl-runtime-control-c14n@0.1-draft
lint: spec/lint/kdsl-p1-p1l-lint.md / spec/lint/kdsl-k1-pf1-lint.md
```

Ownership:

```text
Core/Profile/R1/Bridge canonical meaning
> P1L canonical v2-draft contract schema
> P1 compact serialization profile
> P1/P1L lint
> K1 runtime-control semantics
> PF1 exact project definitions
> K1/PF1 lint
> validator/example/tool
```

## 2. 禁止

```text
KDSL-DP直接実行禁止
KDSL-DPをCodex/AI coding toolへ実装指示として渡すこと禁止
P1L/P1 validを実行許可扱い禁止
P1L/P1 lint/round-trip passをauthority扱い禁止
unknown profile/alias/preset推測禁止
build/diff/lint/test passをRT:v扱禁止
KDSL_RESULT NEXTを次task実行許可扱禁止
KDSL_RESULT COMMITを自動commit許可扱禁止
```

## 3. 正規化と実行境界

```text
KDSL-DP
→ normalize
P1L
→ optional compact serialization
P1
→ runtime binding / authority evaluation
execution candidate
→ run
R1/KDSL_RESULT
```

```text
P1L:=lossless structured normalized contract schema
P1:=P1Lのreversible compact serialization
P1 != independent canonical contract
```

状態分離:

```text
KDSL-DP valid
P1L structurally valid
P1 serialization valid
profile binding valid
runtime binding valid
execution authority sufficient
executable
executed
verified
runtime verified
```

禁止同値:

```text
KDSL-DP valid = executable
P1L valid = executable
P1 valid = executable
P1/P1L lint pass = executable|authority
P1/P1L structural_pass = semantic equivalence|safety proof|authority
executed = verified
verified = runtime verified
build pass = RT:v
```

`kdsl-p1l@0.1-draft` / `kdsl-p1@0.1-draft`では:

```text
BINDING.state default: unbound
BINDING.executable: false固定
runtime binding implementation: out of scope
```

## 4. P1L / P1 contract requirements

P1L required top-level fields:

```text
META/SOURCE/PROFILE/TASK/SCOPE/CONTEXT/GOAL/PLAN/GUARD/STOP/VERIFY/RUNTIME/OUTPUT/AUTHORITY/NORMALIZATION/BINDING
```

Required authority rails:

```text
read/edit/stage/commit/push/release/public_repo/destructive_ops
```

```text
missing rail→blocked
read allow != edit allow
edit allow != commit allow
commit allow != push allow
push allow != release allow
PLAN/FLOW != authority
```

Profile completion:

```text
exact profile id/revision/digest + field default evidence必須
profile completion != inference
unknown alias/preset/profile→blocked
completed valueはP1L canonical projectionへ展開必須
```

Runtime contract values:

```text
pending|user_required|not_applicable
```

Result-only RT values:

```text
v|fail|blk→R1/R1Cのみ
```

P1L/P1で実行前にRT:vを自己申告禁止。

## 5. P1 compact serialization

Canonical P1:

```text
P1|SCHEMA=kdsl-p1@0.1-draft|STATUS=contract-candidate|...
```

P1は全P1L required projectionをcanonical JSON segmentとして保持する。

```text
P1→P1L再構成不能/critical loss/unknown alias→blocked
implicit default禁止
exact strings保持
P1 round-trip structural_pass != semantic equivalence/safety proof/authority
```

既存project-local `P1|M:...|T:F|...` はlegacy operational evidenceであり、自動canonical扱い禁止。

```text
loss=P→exact compatibility evidence時のみprofile_completed候補
loss=L意味推測禁止
AP/H意味推測禁止
Authority rails不在→canonical昇格blocked
```

## 6. K1 / PF1 Runtime Control

```text
K1/PF1 valid != executable|authority grant
PF1 may narrow but never widen P1L authority
capability != permission
Stop continuation != authority
routing != authority
binding evidence:=external content-addressed record referenced by P1L.BINDING.runtime_control
```

```text
K1/PF1 parser/validator/exact compatibility:=Phase 9C bounded first slice
binding-evidence field schema:=kdsl-binding-evidence@0.1-draft
runtime evaluator/binding:=not implemented
BINDING.executable:false fixed under P1L/P1 v0.1 draft
```

## 7. KDSL_PROMPT

ChatGPTがAI coding tool向けpromptを作る場合は、先頭を `KDSL_PROMPT:` に固定する。

```text
KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: lock-critical
...
```

禁止:

```text
KDSL_PROMPT前に自然文前置き
D禁止時のKDSL_PROMPT出力
KDSL-DP直接実行扱い
P1L/P1 schema/lint passのみでKDSL_PROMPT生成許可扱い
```

P1L/P1はKDSL_PROMPTと同一ではない。runtime binding/authority評価を経ないP1L/P1から実行指示を生成してはならない。

## 8. KDSL_RESULT

Codex / AI coding tool の最終回答には、先頭に `KDSL_RESULT:` を要求する。

```text
KDSL_RESULT:
STATUS:
PHASE:
S:
FILES:
WHY:
CMD:
VERIFY:
RT:
RISK:
NEXT:
COMMIT:
```

STATUS:

```text
success/partial/blocked/noop/failed/needs_user
```

RT:

```text
p=runtime確認未完了
u=U実機確認待ち
v=対象環境runtime確認済
na=runtime対象なし
fail=runtime確認失敗
blk=runtime確認不能
```

P1L/P1の`RUNTIME`はpre-execution dispositionであり、KDSL_RESULT/R1の実行結果RTと混同しない。

## 9. KDSL本体への影響

KDSL本体は汎用直投入記法のまま維持する。  
ADPS/KDSL-DP/P1L/P1規則は、ADPS向けprofileまたはdev-prompt用途で適用する。  
KDSL本体のmode/profile/safety変更は、KDSL-DP/P1L/P1へ自動継承しない。

互換方針:

```text
KDSL operator意味変更→breaking
profile名前空間変更→breaking
KDSL-DP直接実行境界変更→breaking/prohibited
P1L required field/authority rail削除→breaking/prohibited
P1 compact key意味変更→breakingまたは新schema ID必須
保護語追加→compatible
lint warning追加→compatible
説明/例追加→patch
```

## 10. Packet relation

Canonical P1/P1L schema adoption alone does not resolve Packet normalization.

```text
Packet→P1L/P1 mapping:=separate Phase 7D
Packet normalization preview:=non-executable
P1L_PREVIEW/P1_PREVIEW != P1L:/P1|
Packet executable promotion禁止
```

## 11. Non-goals

```text
runtime evaluator/resolver implementation
binding-evidence record generation
BINDING.executable:true
executable transformer
automatic AI tool execution
complete semantic equivalence proof
complete safety proof
Packet executable promotion
stable/public-ready/tag/release/Release Assets operation
```
