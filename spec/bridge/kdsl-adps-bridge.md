# KDSL／ADPS 境界 — 最小保持

```text
KDSL:=漢字圧縮prompt／LLM直投入可
KDSL-DP:=ADPS向けAuthoring形式／直接実行禁止
P1／P1L:=実行契約候補
K1／PF1:=必要時の状態／Project既定
R1／KDSL_RESULT:=簡潔結果
```

```text
KDSL-DP→P1／P1L正規化必須
P1／P1L valid != 実行許可
Packet valid != 実行許可
K1更新→目的／scope／権限変更禁止
RT:v:=対象環境runtime確認済のみ
```

通常のKDSL promptをP1・P1L・PF1で覆う必要はない。Agent・ADPSの契約はKDSL Core下位。安全gate registry／Packet／semantic parser等をKDSL本文の必須依存へ追加しない。
