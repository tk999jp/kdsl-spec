# KDSL Specification v1.1-ADPS-aware-v2-sync

目的: 日本語promptを、LLM直投入可能な安全gate保持型圧縮記法へ変換する  
対象: ChatGPT / Codex / AI coding tool / 長文運用prompt / 開発支援prompt  
基本思想: 日本語の助詞/句読点/敬語/重複説明を削り、禁止/承認/未確認/停止条件/責務分離を保持する  
優先: 意味保持 > 安全gate保持 > 判断分岐保持 > 誤実装防止 > 文字数削減 > 人間可読性  
非目的: 極限記号遊び / 美文 / 自然文維持 / 自動token最適化 / 展開pipeline前提

---

## 0 定義

KDSL:  
日本語運用promptを対象にした漢字圧縮DSL。  
自然文を、漢字語幹 / 記号 / 最小制御語へ再構成する。  
LLMへそのまま投入できることを前提にする。  
完全な形式言語ではなく、LLM向けの半構造化prompt記法である。

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

---

## 1 設計単位

KDSLはversion差ではなく、次の直交軸で運用する。

```text
format: KDSL
profile: <用途>
mode: <圧縮強度>
safety: <安全保持強度>
lexicon: <宣言済み語彙/alias集合>
envelope: <契約block形式>
```

例:
```text
format: KDSL
profile: dev-prompt
mode: min
safety: lock-critical
lexicon: standard
envelope: plain
```

### format

```text
format: KDSL
```

### profile

正式値:

```text
profile: compact-prompt
profile: dev-prompt
profile: converter
profile: lint
```

互換境界:

```text
rulebook:=v1.1 legacy profile name
rulebook新規使用禁止
rulebookを正式v2 profile扱い禁止
legacy rulebook入力→用途確認なしにcompact-prompt/lintへ自動補正禁止
unknown profile推測禁止
```

### mode

```text
mode: readable
mode: min
mode: dense
mode: lock
```

廃止:
```text
mode: converter
```

理由: converterは圧縮強度ではなく用途であるため、`profile: converter` に統合する。

### safety

```text
safety: normal
safety: lock-critical
safety: lock-all
```

### lexicon

```text
lexicon: standard
lexicon: kanji-v1
```

制約:

```text
lexicon != mode
lexicon != profile
unknown lexicon推測禁止
Core保護語をLexiconで上書禁止
```

### envelope

```text
envelope: plain
envelope: packet-draft
envelope: result
```

制約:

```text
packet-draft:=non-executable
result:=KDSL_RESULT/R1系
unknown envelope推測禁止
```

---

## 2 位置付

KDSLは、既存手法とは次のように異なる。

```text
LLMLingua系: 自動圧縮器
Λ記法系: 展開pipeline前提DSL
KDSL: 日本語安全契約promptの直投入圧縮記法
```

KDSLの主目的はtoken削減そのものではない。  
主目的は、開発運用prompt内の安全gateを保持したまま圧縮すること。

KDSLは次を重視する。

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
RT:v条件
KDSL_RESULT NEXT/COMMIT条件
```

---

## 3 KDSL / KDSL-DP / ADPS

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
KDSL-DPはKDSL-familyだが、KDSL本体の直投入前提を継承しない。
KDSL-DP直接実行禁止。
KDSL-DP→P1/P1L正規化必須。
```

---

## 4 演算子

KDSLでは演算子の多義性を避ける。  
特に `=` は略語定義/短い同値に限定し、扱/状態指定には `:=` を使う。

### `:`
見出し / 定義ラベル / 値指定

### `/`
並列列挙を基本とする。選択を明示する場合は補足する。

### `,`
軽分節

### `;`
強分節 / 1行内規則分離

### `→`
条件 / 処理遷移
```text
A→B = A時B
```

### `=>`
変換 / 書換
```text
A=>B = AをBへ変換
```

### `>`
優先順位
```text
A>B = AをBより優先
```
Markdown衝突回避: `>` は行頭で使わない。

### `=`
略語定義 / 短い同値。状態指定には使わない。

### `:=`
扱 / 状態指定
```text
A:=B = AをBとして扱う / Aの状態をBと指定する
```

### `×`
衝突 / 不可 / 禁止組合

---

## 5 operator / abbrev 宣言

Project filesを参照できない環境へKDSL promptを単独で渡す場合、冒頭に最小宣言を置く。

```text
format: KDSL
operator: `→`=条件/遷移, `=>`=変換, `>`=優先, `:=`=扱/状態指定, `×`=衝突/不可, `/`=並列
abbrev: U=ユーザー, GH=GitHub, AI tool=AI coding tool, D禁=D禁止
```

---

## 6 変換禁止

```text
inline code内
command
path
URL
repo名
branch名
tag名
package名
class/method/property/API名
file名/拡張子
Windows path
```

code block内:
- 原則変換禁止
- Uがcode block全体を変換対象として明示した場合は変換可
- command/path/code/API名は常に変換禁止

---

## 7 保護語

```text
禁止
必須
未確認
未実行
承認
承認待
停止条件
正本
rollback
revert
未push
破棄
退避
実行済扱
確認済扱
成功扱
断定禁止
実機確認分離
public履歴
公開済tag
Release Assets
KDSL-DP直接実行禁止
P1/P1L正規化必須
RT:v
KDSL_RESULT NEXT
KDSL_RESULT COMMIT
```

---

## 8 出力固定語

### KDSL_PROMPT

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

### KDSL_RESULT

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
COMMIT:=推奨message, 自動commit許可扱禁止
```

---

## 9 mode / safety

詳細は `kdsl-modes.md` を正とする。

基本:
```text
mode: readable|min|dense|lock
safety: normal|lock-critical|lock-all
優先: safety > high-risk判定 > mode > profile
```

---

## 10 lint

詳細は `kdsl-lint-checklist.md` を正とする。

最低限:
```text
D禁止保持
rollback/revert保持
未確認/未実行扱禁止保持
実機確認分離保持
public保護保持
command/path/code/API名保持
KDSL-DP直接実行禁止保持
RT:v条件保持
KDSL_RESULT NEXT/COMMIT条件保持
```
