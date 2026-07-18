# KDSL Core v2.0-kanji-canonical

## 優先

```text
漢字圧縮 > 意味保持 > 直投入性 > 判断分岐保持 > 明示制約保持 > 出力安定
```

## 演算子

```text
:  見出／定義
/  並列
,  軽分節
;  強分節
→  条件／遷移
=>  変換
>  優先
=  略語定義／短い同値
:= 扱／状態
×  衝突／不可
```

```text
>行頭使用禁止
=を状態指定に使用禁止
未定義alias推測禁止
```

## 基本文型

```text
X禁止
X→Y扱禁止
X未確認→確認済扱禁止
X未実行→実行済扱禁止
X時→Y
X含→Y
X不可→停止
X衝突→Y優先
A:=B
A>B
```

## 圧縮処理

```text
助詞削減
重複統合
同義説明統合
漢字語幹化
条件→
変換=>
優先>
状態:=
衝突×
並列/
```

KEY翻訳のみで完成扱い禁止。

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
破棄
実行済扱
確認済扱
成功扱
断定禁止
public履歴
公開済tag
Release Assets
KDSL-DP直接実行禁止
P1／P1L正規化必須
RT:v
```

保護語は明示箇所だけに適用し、自動増殖させない。

## D禁止

```text
D禁止対象:
U要件変更
明示方針反転
rollback／revert
未push差分破棄
public履歴改変
公開済tag／Release Assets変更
data schema／保存形式の破壊的変更
```

```text
通常bug修正
既存仕様内補正
targeted test追加
内部実装整理
明示scope内完成作業
```

は自動的にD禁止へ昇格しない。

## 変換禁止

```text
command
path
URL
repo名
branch名
tag名
package名
class／method／property／API名
file名／拡張子
Windows path
inline code
```

code blockは原則保持。Uがblock全体を変換対象として明示した場合もcommand／path／code／API名は保持する。
