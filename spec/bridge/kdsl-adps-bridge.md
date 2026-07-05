# KDSL / KDSL-DP / ADPS Bridge v0.2

目的: KDSL本体とKDSL-DP / ADPS / KDSL_PROMPT / KDSL_RESULTの境界を定義する。

## 1. 位置づけ

```text
KDSL:=LLM直投入可能な安全gate保持型prompt記法
KDSL-DP:=ADPS向けAuthoring形式, 実行指示ではない
P1/P1L:=実行契約候補
K1/PF1:=Runtime Control
R1:=Evidence
KDSL_RESULT:=R1系の人間/AI向け結果block
```

KDSL-DPはKDSL-familyだが、KDSL本体の直投入前提を継承しない。

## 2. 禁止

```text
KDSL-DP直接実行禁止
KDSL-DPをCodex/AI coding toolへ実装指示として渡すこと禁止
unknown profile/alias/preset推測禁止
build/diff/lint/test passをRT:v扱禁止
KDSL_RESULT NEXTを次task実行許可扱禁止
KDSL_RESULT COMMITを自動commit許可扱禁止
```

## 3. 正規化

```text
KDSL-DP
→ normalize
P1/P1L
→ runtime binding
run
→ R1/KDSL_RESULT
```

状態分離:
```text
KDSL-DP valid != executable
P1/P1L valid != executable
P1 lint pass != executable
executed != verified
verified != runtime verified
build pass != RT:v
```

## 4. KDSL_PROMPT

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
```

## 5. KDSL_RESULT

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

## 6. KDSL本体への影響

KDSL本体は汎用直投入記法のまま維持する。  
ADPS/KDSL-DP規則は、ADPS向けprofileまたはdev-prompt用途で適用する。  
KDSL本体のmode/profile/safety変更は、KDSL-DPへ自動継承しない。

互換方針:
```text
KDSL operator意味変更→breaking
profile名前空間変更→breaking
保護語追加→compatible
lint warning追加→compatible
説明/例追加→patch
```
