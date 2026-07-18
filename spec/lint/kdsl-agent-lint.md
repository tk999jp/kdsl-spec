# KDSL Agent Lint v1.1

## 目的

```text
Agent lint:=最小run状態と条件付き厳密契約の形式検査
```

形式lintはCodex Agent実効性・実行許可・RT:vを証明しない。

## 標準Agent

`agent: required`時の必須:

```text
KDSL_PROMPT
K1
```

P1L／P1／PF1は通常必須ではない。

## K1

必須:

```text
状態／現在／完了／未完／検証／実機／次／停止理由
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

中断再開／handoff時のみ追加必須:

```text
run／契約／baseline
```

K1内の目的／対象／権限再定義はfail。

## P1L

P1Lは厳密handoff／中断再開時だけ使用する。

必須:

```text
版／目的／成功条件／正本／対象／非対象／権限／承認境界／作業／検証／実機要否／停止条件／完了条件／報告
```

権限は今回runに関係する操作だけ記載する。値は `可／不可／承認待／対象外`。

```text
全rail列挙強制禁止
未記載操作:=P1Lから許可しない
PF1適用→権限拡張禁止
```

## P1

```text
P1:=任意短縮
P1Lと同時記載禁止
P1!=可逆性保証
```

P1使用時は最低限、版／目的／成功／正本／対象／権限／作業／検証／停止／完了／報告を保持する。

## PF1

PF1は継続project既定。

```text
project／正本／既定profile／既定mode／Phase方針／権限既定／承認必須／試験方針／実機方針／報告方針
```

PF1はP1L生成前に参照し、U明示指示を反転・拡張しない。

## 共通

```text
漢字圧縮identity保持
英語構造KEY既定化禁止
Safety Gate Registry依存禁止
Packet依存禁止
R1C依存禁止
Binding Evidence必須化禁止
validator pass != 実行許可
validator pass != Codex Agent実効性
validator pass != RT:v
```