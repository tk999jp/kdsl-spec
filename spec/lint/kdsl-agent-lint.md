# KDSL Agent Lint v1.0

## 対象

```text
P1L
P1
K1
PF1
```

## P1L

必須:

```text
版
実行方式
目的
成功条件
正本
対象
非対象
権限
承認境界
作業
試験
検証
実機要否
停止条件
完了条件
報告
```

権限rail必須:

```text
読取／編集／試験／stage／commit／push／release／public履歴／破壊操作
```

値:

```text
可／不可／承認待／対象外
```

禁止:

```text
rail省略
未定義権限値
P1L valid=全操作許可扱い
PF1による権限拡張
```

## P1

```text
marker:=P1|
separator:=|
権限separator:=,
key／value:=:
rail／value:==
```

P1L必須fieldと全権限railを保持する。P1からP1Lへ復元不能ならfail。

## K1

必須:

```text
状態／現在／完了／未完／検証／実機／次遷移／停止理由
```

状態:

```text
計画／実行中／検証中／実機待／完了／停止／失敗
```

完了条件:

```text
状態=完了→未完=なし
状態=完了→検証=成功
状態=完了→実機=不要|確認済
```

K1内の目的／対象／権限再定義はfail。

## PF1

必須:

```text
project／正本／既定profile／既定mode／Phase方針／権限既定／承認必須／試験方針／実機方針／報告方針
```

PF1権限railはP1Lと同一。PF1値をP1Lへ適用する時、同値または縮小だけ許可する。

## 共通

```text
漢字圧縮identity保持
英語構造KEY既定化禁止
Safety Gate Registry依存禁止
Packet依存禁止
R1C依存禁止
Binding Evidence必須化禁止
validator pass != 実行許可
validator pass != RT:v
```
