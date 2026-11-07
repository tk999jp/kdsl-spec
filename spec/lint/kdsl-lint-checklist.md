# KDSL Lint — 簡潔チェック

## 必須

- 漢字圧縮が第一。KEY日本語化だけではなく本文も語幹化。
- 意味・数量・条件・否定の作用範囲・判断分岐を保持。
- 明示禁止／未確認／未実行／承認待／rollback・revert／data・public保護／RT:vを弱化しない。
- command／path／URL／branch／tag／API名／inline codeを変換しない。
- 入力外の承認gate／停止条件／Phase／architecture／hardeningを追加しない。
- 同義反復を統合。長値定義を繰り返さない。曖昧一字aliasは禁止。
- `→`の条件と手順、`/`の並列と選択を混同しない。
- min／denseの違いが本文の圧縮に現れている。
- denseの意味欠落を文字数減少だけで正当化しない。
- AI codingでは`KDSL_PROMPT:`を先頭に置く。
- R1で未実行を実行扱い、test成功をRT:v扱いしない。

## 検査の限界

```text
形式lint pass != 意味同等
文字数削減 != token削減
概念marker保持 != 判断分岐完全保持
サンプル回帰pass != 任意LLM実効性
CI pass != U承認／RT:v
```

異常を見つけた場合は、依頼scope内の修正を優先し、未依頼の高負荷frameworkを増設しない。
