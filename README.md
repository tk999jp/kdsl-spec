# KDSL — 漢字圧縮Core 再構築候補

```text
KDSL:=日本語prompt→漢字語幹／記号／最小制御語へ再構成するLLM直投入可能な漢字圧縮DSL
第一目的:=漢字圧縮
成立条件:=意味保持／判断分岐保持／明示制約保持／直投入可能／人間修正可能
```

## 最小利用

自然文：

> 共有された材料で判断できる場合は、AI coding toolに調査を丸投げしないでください。

KDSL：

```text
共有材判可→AI丸投禁止
```

開発指示では先頭に `KDSL_PROMPT:` を置き、本文も漢字語幹化する。基本は `mode:min`。`dense` は意味保持を満たし、投入効率に利点がある場合に選択する。

## 責務

- `spec/core/`：漢字圧縮の定義／記法／mode。ここがKDSL本体。
- `spec/profiles/`：用途別の変換指針。
- `spec/r1/`：作業結果の簡潔報告。KDSL本体ではない。
- `spec/bridge/`：KDSL-DP／ADPSとの限定境界。KDSL本体を上書きしない。
- `spec/lint/`：変換レビューの観点。形式合格は意味同等の証明ではない。
- `examples/kanji/`：人間が査読する比較例。

参照優先順位と非正本の扱いは `spec/manifest.md`。旧branchの`experimental/`・`templates/`・旧`docs/reviews/`は現行仕様の根拠にしない。

## 簡易検査

```bash
python -m unittest discover -s tools/validator -p 'test_*.py' -v
```

この検査はサンプルの短縮、保護文字列、基本記法の退行を確認するだけであり、任意LLMの意味同等、Agent完走、実機確認を保証しない。

## 起点と採用方針

```text
基点:=39a51b71950340b83f6e525dd1a76724530bb0df
参照:=c49d73a5bc6dfec884068903c9a157fc4ae2edd2
移植:=機能／意味単位の選別
現main:=参照資産／無条件正本化禁止
```

本ブランチは再構築候補。`main`へのmerge・release・RT:vは未実施。
