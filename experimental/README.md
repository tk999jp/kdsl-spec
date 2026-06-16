# Experimental

KDSL / R1 の拡張案・検証中メソッド置き場。

このディレクトリ内の内容は、Core正本ではない。

## 候補テーマ

```text
Actor Model
Protocol Stack / Work Stack
KDSL-HMI / R1-HMI
Contract Matrix
Evidence Ledger
Authority Rail
KDSL-Param
Python Validator
HMI-lint
```

## 扱い

```text
experimental内の案は正本扱い禁止
Core / R1 / Lintへ昇格する場合は理由と互換影響を記録
unknown profile/alias/preset推測禁止
実験案をAI coding toolへ直接実装指示として渡す場合はKDSL_PROMPT/P1相当へ正規化必須
```

## 禁止

```text
experimental案をCore仕様として引用禁止
experimental案をAI coding toolへ直接実装指示として渡すこと禁止
experimentalの略語/aliasを正本名として推測禁止
experimentalからCore/R1への自動継承禁止
```

## 昇格条件案

```text
実運用で効果確認
safety gate弱化なし
KDSL直投入性を壊さない
R1検収性が上がる
lint可能性あり
既存Coreとの衝突なし
未確認/未実行/RT:v/NEXT/COMMIT条件を弱化しない
```

## 昇格時の記録

```text
昇格元experimental file
採用理由
不採用にした代替案
Core/R1/Lint/Profileへの影響
互換性: breaking/compatible/patch
必要lint
必要example
```

## 現在の優先候補

```text
1. Authority Rail → R1/Templateへ段階導入
2. Evidence Ledger → R1へ段階導入
3. Actor Model → README/Profile説明へ段階導入
4. Protocol Stack → overview説明として維持
5. Python Validator → optional assistとして設計のみ
```
