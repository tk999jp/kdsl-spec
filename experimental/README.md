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

## 昇格条件案

```text
実運用で効果確認
safety gate弱化なし
KDSL直投入性を壊さない
R1検収性が上がる
lint可能性あり
既存Coreとの衝突なし
```
