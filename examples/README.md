# Examples

KDSL／R1の非正本例。

## 現役例

```text
examples/kanji/midfd-dev-prompt.kdsl.md
examples/kanji/blog-meta.kdsl.md
examples/intl/blog-meta.kdsl-intl.md
```

```text
kanji:=KDSL本体の漢字圧縮例
intl:=明示指定時だけ使う派生subset例
```

## 歴史例

`examples/midfd/*` は初期R1／template設計の歴史例。英語field、Evidence、Authority等を含み、現行KDSL／R1の正規出力例として使用しない。

## 扱い

```text
examplesは正本ではない
現行仕様確認→examples/kanji優先
例内のrepo／branch／値を現状態扱い禁止
歴史例から旧v2 architectureを復元禁止
```
