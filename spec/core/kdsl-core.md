# KDSL Core v1.1-v2-sync

目的: KDSLの共通記法 / 保護語 / 変換文型 / ADPS境界語を定義する  
参照正本: `kdsl-spec.md`

## 基本

```text
format: KDSL
profile: <compact-prompt|dev-prompt|converter|lint>
mode: <readable|min|dense|lock>
safety: <normal|lock-critical|lock-all>
lexicon: <standard|kanji-v1>
envelope: <plain|packet-draft|result>
```

互換境界:

```text
rulebook:=v1.1 legacy profile name
rulebook新規使用禁止
rulebookを正式v2 profile扱い禁止
legacy rulebook入力→用途確認なしにcompact-prompt/lintへ自動補正禁止
unknown profile/mode/safety/lexicon/envelope推測禁止
```

優先: 意味保持 > safety gate保持 > 判断分岐保持 > 誤実装防止 > 文字数削減

## operator

```text
:  見出し/定義ラベル/値指定
/  並列列挙
,  軽分節
;  強分節
→  条件/処理遷移
=>  変換/書換
>  優先
=  略語定義/短い同値
:= 扱/状態指定
×  衝突/不可
```

注意:
- `>` は行頭使用禁止
- `=` を扱/状態指定に使わない
- `/` は並列列挙が基本、選択は必要時に補足
- `:=` は「状態/扱い」を明示するために使う

## abbrev

```text
U=ユーザー
GH=GitHub
AI tool=AI coding tool
D禁=D禁止
KDP=KDSL-DP
P1L=P1 readable form
RT=Runtime verification status
```

## ADPS境界語

```text
KDSL:=LLM直投入可能な安全gate保持型prompt記法
KDSL-DP:=ADPS向けAuthoring形式, 実行指示ではない
P1/P1L:=実行契約候補
K1/PF1:=Runtime Control
R1/KDSL_RESULT:=Evidence/結果証跡
```

重要:
```text
KDSL-DP直接実行禁止
KDSL-DP→P1/P1L正規化必須
unknown profile/alias/preset推測禁止
```

## D禁止

```text
D禁止=要件変/方針変/rollback/revert/再実装/未push破棄/正本変/UI契約変/妥協案/data schema/public API/保存形式変更を含む場合に実装指示禁止
```

## 保護語

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
RT:v
KDSL_RESULT NEXT
KDSL_RESULT COMMIT
```

## 禁止文型

```text
X禁止
X→Y扱禁止
X→Y混入禁止
X含→停止
X含→承認待
X未確認→断定禁止
X未実行→実行済扱禁止
X未確認→確認済扱禁止
X未確認→成功扱禁止
```

## 必須文型

```text
X必須
X先行
X分離
X確認
X記録
X退避
X遵守
X固定
```

## 条件文型

```text
X時→Y
X含→Y
X不可→停止
X不明→観測整理
X衝突→Y優先
X連続→診断先行
```

## 優先文型

```text
A>B
A優先
A正扱
A維持
A先行
```

## 変換禁止

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
