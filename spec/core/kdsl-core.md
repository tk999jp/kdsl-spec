# KDSL Core v2.2-kanji-canonical

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
重複統合
正本参照化
助詞削減
同義説明統合
漢字語幹化
条件→
変換=>
優先>
状態:=
衝突×
並列/
```

圧縮成立:

```text
KEY翻訳のみ×
本文自然文維持＋日本語KEY化のみ×
section分割目的の同義再掲×
同一長値／固定条件→原則1回定義→以後短名参照
成功条件:=最終成立状態
検証:=成立確認方法
```

```text
hash／version／path／tag／固定値反復→正本へ集約
section独立可読性目的の値再掲禁止
技術識別子保持
非識別子の制御英語→安定漢字語ありなら漢字化
```

短名は意味明確な日本語を優先し、未定義一字aliasを生成しない。

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

## 契約保持

```text
同一事項競合→後発確定>先発確定>仮説／提案／状態観測
直近記述のみ→確定扱禁止
撤回済／置換済判断→再採用禁止
状態観測／実装／test／Docs／State／結果証跡→明示なし契約正本扱禁止
下位情報→上位契約上書禁止
AI判断!=U確定
source／test／Docs／State相互一致!=上位契約変更根拠
```

```text
対象外の観測可能意味変更禁止
意味変更:=集合演算／追加／置換／結合／clear／保存範囲／routing／fallback／default／副作用
内部rename／refactor可; 対象外動作同値必須
```

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
