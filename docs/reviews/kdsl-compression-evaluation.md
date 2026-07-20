# KDSL漢字圧縮 定量評価

```text
確認日: 2026-07-20
対象: AI coding／業務blog meta／創作seed
尺度: 空白除外Unicode文字数
semantic check: 21概念marker保持
LLM token: model依存のため未測定
```

## 結果

| sample | 自然文 | min本文 | min投入全体 | dense本文 | dense投入全体 |
|---|---:|---:|---:|---:|---:|
| AI coding | 415 | 269（35.2%削減） | 331（20.2%削減） | 244（41.2%削減） | 308（25.8%削減） |
| 業務／blog meta | 348 | 170（51.1%削減） | 224（35.6%削減） | 163（53.2%削減） | 222（36.2%削減） |
| 創作seed | 398 | 198（50.3%削減） | 252（36.7%削減） | 197（50.5%削減） | 256（35.7%削減） |
| 合計 | 1,161 | 637（45.1%削減） | 807（30.5%削減） | 604（48.0%削減） | 786（32.3%削減） |

## 判断

```text
漢字圧縮効果: 成立
min本文: 45.1%削減
min投入全体: 30.5%削減
dense本文: 48.0%削減
dense投入全体: 32.3%削減
概念保持: 21/21 marker pass
```

### 良い点

- 業務prompt／創作promptはheader込みでも約36%削減。
- AI coding promptは識別子・権限・RunChanged条件を保持して25.8%削減。
- 明示禁止、未確認分離、数値条件、出力件数を削らず圧縮できた。

### 問題点

- header固定費により、本文削減率より投入全体削減率が約15ポイント低下。
- denseは常にminより短いとは限らない。創作seedではdense投入全体がminより4文字長い。
- dense差が小さいpromptでは、一行化・記号化による人間可読性低下に対し圧縮利益が小さい。

## 運用判断

```text
通常運用:=mode:min
mode:dense:=本文追加削減が有意な場合／AI直投入優先時
dense採用条件:=minより実投入量減少
短prompt:=header固定費確認
比較時:=本文／投入全体を分離計測
```

`dense`を高圧縮名だけで自動選択しない。今回の3 sampleではAI codingとblog metaはdenseが短いが、創作seedはminが短い。

## 検証

```bash
python tools/validator/kdsl_compression_evaluation.py
```

scriptは各sampleの文字数、15%以上の投入全体削減、21概念marker保持を確認する。marker passは完全な意味同等性やLLM応答品質を証明しない。
