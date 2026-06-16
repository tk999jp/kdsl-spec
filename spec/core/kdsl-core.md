# KDSL Core v0.1-draft

目的: KDSLの共通記法 / 保護語 / 変換文型 / ADPS境界語を定義する。

## 基本

```text
format: KDSL
profile: <dev-prompt|converter|lint|rulebook>
mode: <readable|min|dense|lock>
safety: <normal|lock-critical|lock-all>
```

優先:

```text
意味保持 > safety gate保持 > 判断分岐保持 > 誤実装防止 > 文字数削減
```

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

```text
> 行頭使用禁止
= を扱/状態指定に使用禁止
:= は状態/扱い明示に使用
/ は並列列挙を基本とする
```

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
P1/P1L正規化必須
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

```text
原則変換禁止
Uがcode block全体を変換対象として明示した場合のみ変換可
command/path/code/API名は常に変換禁止
```
