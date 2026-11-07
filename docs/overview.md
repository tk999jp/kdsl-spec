# KDSL 概要 — identity再構築候補

```text
KDSL:=日本語prompt→漢字語幹／記号／最小制御語
第一目的:=漢字圧縮
成立条件:=意味保持／判断分岐保持／明示制約保持／LLM直投入／人間修正可能
```

- 旧Coreの漢字圧縮identityを維持。
- 明示禁止・未確認・未実行・承認待等は意味欠落防止の限定保護。
- 入力外のrisk・承認gate・追加作業をKDSLへ混入しない。
- R1／Agent／ADPSは必要時に参照する外部層。
- `min`を既定、`dense`は実投入の利益と意味保持で選択。
- 旧資料・旧schema・validatorの存在だけを採用理由にしない。

正本地図：`spec/manifest.md`。
