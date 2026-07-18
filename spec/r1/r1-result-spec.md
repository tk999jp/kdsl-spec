# R1 Result Specification v2.0-minimal

## 位置づけ

```text
R1:=作業結果の短い証跡
KDSL_RESULT:=R1の標準報告block
```

R1は成果物・仕様書・引継書・次期roadmapではない。

## 標準

```text
KDSL_RESULT:
状態:
局面:
要約:
変更:
理由:
実行:
検証:
実機:
危険:
次:
commit:
```

## 状態

```text
成功
一部
停止
変更なし
失敗
U確認待
```

## 規則

```text
実行:=実行したcommandのみ
検証:=実行したverifyのみ
未実行command→実行欄記載禁止
未実行verify→pass扱禁止
build／diff／lint／test／CI pass != RT:v
実機:v:=対象環境runtime確認済のみ
次:=提案、実行許可扱禁止
commit:=実行済commitまたは推奨message
自動commit許可扱禁止
```

## 範囲

報告は依頼scope内だけ。

自動追加禁止:

```text
新hardening
別Phase候補
将来architecture
未依頼改善課題
大量の観測分類
権限registry
```

重大な未解決riskがscope内にある場合だけ `危険:` へ簡潔に記載する。

## 任意

必要時のみ:

```text
根拠:
未確認:
権限:
```

任意blockを既定必須化しない。
