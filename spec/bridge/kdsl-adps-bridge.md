# KDSL / KDSL-DP / ADPS Bridge v2.0-bounded

## 境界

```text
KDSL:=LLM直投入可能な漢字圧縮prompt
KDSL-DP:=ADPS向けAuthoring形式
P1／P1L:=実行契約候補
K1／PF1:=Runtime Control候補
R1／KDSL_RESULT:=結果証跡
```

## 保持

```text
KDSL-DP直接実行禁止
KDSL-DP→P1／P1L正規化必須
P1／P1L valid != 実行許可
Packet valid != 実行許可
build／lint／test／CI pass != RT:v
```

## identity境界

```text
ADPS／P1／Packet／Runtime ControlはKDSL漢字identityを上書き禁止
実行契約強化→漢字圧縮解除禁止
英語schema必要→KDSL-Intlへ分離
```

KDSL本体は漢字圧縮の直投入prompt。実行制御architectureをKDSLの第一目的へ昇格しない。

## 導入

P1／P1L／Packet／K1／PF1等は、漢字圧縮へ実用上必要であることを個別に証明した場合だけ採用する。実装済み・CI pass・既存Phase完了だけでは採用理由にならない。
