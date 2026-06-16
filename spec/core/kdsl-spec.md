# KDSL Specification v0.1-draft

目的: 日本語promptを、LLM直投入可能な安全gate保持型圧縮記法へ変換する。

対象:

```text
ChatGPT
Codex
AI coding tool
長文運用prompt
開発支援prompt
```

基本思想:

```text
日本語の助詞/句読点/敬語/重複説明を削り、禁止/承認/未確認/停止条件/責務分離を保持する
```

優先:

```text
意味保持 > safety gate保持 > 判断分岐保持 > 誤実装防止 > 文字数削減 > 人間可読性
```

非目的:

```text
極限記号遊び
美文
自然文維持
自動token最適化
展開pipeline前提
```

## 0. 定義

KDSL:

```text
日本語運用promptを対象にした漢字圧縮DSL。
自然文を、漢字語幹 / 記号 / 最小制御語へ再構成する。
LLMへそのまま投入できることを前提にする。
完全な形式言語ではなく、LLM向けの半構造化prompt記法である。
```

基本形:

```text
自然文=>漢字語幹+記号+最小制御語
```

例:

```text
共有材料で判断可能な内容をAI coding toolへ丸投げしない
=> 共有材判可→AI丸投禁止
```

KDSLの核:

```text
日本語
漢字圧縮
安全gate保持
判断routing
直投入可能
低tool依存
未確認事故防止
rollback事故防止
```

## 1. 設計単位

KDSLはversion差ではなく、次の構成で運用する。

```text
format: KDSL
profile: <用途>
mode: <圧縮強度>
safety: <安全保持強度>
```

例:

```text
format: KDSL
profile: dev-prompt
mode: min
safety: lock-critical
```

profile:

```text
dev-prompt
converter
lint
rulebook
```

mode:

```text
readable
min
dense
lock
```

safety:

```text
normal
lock-critical
lock-all
```

## 2. 位置づけ

```text
LLMLingua系: 自動圧縮器
Λ記法系: 展開pipeline前提DSL
KDSL: 日本語安全契約promptの直投入圧縮記法
```

KDSLの主目的はtoken削減そのものではない。主目的は、開発運用prompt内の安全gateを保持したまま圧縮すること。

重視:

```text
禁止
承認
未確認
未実行
停止条件
rollback/revert
実機確認分離
public履歴保護
正本保護
判断routing
KDSL-DP直接実行禁止
P1/P1L正規化必須
RT:v条件
KDSL_RESULT NEXT/COMMIT条件
```

## 3. KDSL / KDSL-DP / ADPS

KDSL本体:

```text
汎用の安全gate保持型prompt記法
LLM直投入可能
```

KDSL-DP:

```text
ADPS向けAuthoring形式
実行指示ではない
P1/P1Lへ正規化するまで実行不可
```

ADPS関連:

```text
P1/P1L:=実行契約候補
K1/PF1:=Runtime Control
R1/KDSL_RESULT:=Evidence/結果証跡
```

重要:

```text
KDSL-DPはKDSL-familyだが、KDSL本体の直投入前提を継承しない
KDSL-DP直接実行禁止
KDSL-DP→P1/P1L正規化必須
```

## 4. KDSL_PROMPT

ChatGPTがCodex/AI coding tool向けpromptを作る場合の先頭固定block。

```text
KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: lock-critical
```

禁止:

```text
KDSL_PROMPT前自然文
D禁止時KDSL_PROMPT出力
```

## 5. KDSL_RESULT

Codex/AI coding toolの最終報告に要求する先頭固定block。

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

制約:

```text
未実行cmd→CMD記載禁止
未実行verify→pass扱禁止
build/diff/lint/test pass != RT:v
RT:v=対象環境runtime確認済のみ
NEXT:=提案, 実行許可扱禁止
COMMIT:=推奨message/実行済commit, 自動commit許可扱禁止
```

## 6. 互換方針

```text
KDSL operator意味変更→breaking
profile名前空間変更→breaking
保護語追加→compatible
lint warning追加→compatible
説明/例追加→patch
```
