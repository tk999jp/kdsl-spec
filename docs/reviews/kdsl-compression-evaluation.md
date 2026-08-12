# KDSL Compression Evaluation

## 目的

KDSLの漢字圧縮が、単なるKEY翻訳ではなく本文圧縮として成立しているかを実例で確認する。

## 既存評価

3分類sample（AI coding／業務meta／創作seed）で、空白除外Unicode codepoint数を測定する。

```text
min本文／dense本文
min header込み／dense header込み
概念marker保持
```

この測定はtokenizer非依存の文字量評価であり、model token数や意味同等性の完全証明ではない。

## 追加観測 — 2026-08-12

長いRelease Asset差替promptで、値参照化だけでは圧縮不足が残ることを確認した。

主な残存:

```text
同一の公開不変／候補一致等を複数sectionへ意味再展開
成功条件の否定形を停止条件へ反復
作業手順の自然文説明残留
上位禁止から導いた観測詳細の独立契約化
正本短名をshell変数のようにinline commandへ埋込む曖昧さ
```

対応:

```text
値参照→値／意味参照へ拡張
派生観測:=検証証拠; U明示／canonical根拠なし契約昇格×
作業:=操作語幹＋対象＋遷移／Gate
短名:=KDSL参照名; inline command literal化×
```

canonical例:

```text
examples/kanji/midfd-release-asset-reference.kdsl.md
```

例では`候補`／`公開`に加え、`配布`／`保全`を意味参照として定義し、成功／作業／検証で同一意味の再展開を削減する。

## 判定境界

```text
validator pass != 意味同等
validator pass != 漢字圧縮品質の完全証明
文字数削減 != 実model token削減保証
canonical例 pass != ChatGPT Project RT:v
```

実Project runtimeでは、同一入力の旧出力／新出力を比較し、意味保持・長値反復・意味反復・自然文残留・入力外条件増殖を確認する。
