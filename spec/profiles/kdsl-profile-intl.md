# KDSL-Intl Profile v1.0

## 位置づけ

```text
KDSL-Intl:=非漢字言語／ASCII／英語KEY向け互換subset
KDSL本体 > KDSL-Intl
```

KDSL-IntlはKDSL本体ではない。漢字を利用できない環境・言語で、KDSLの意味論と分岐を移植するための派生subset。

## 適用条件

```text
UがIntl／英語／ASCIIを明示
対象環境が漢字非対応
出力言語が非漢字言語
```

無指定時適用禁止。

## 継承

```text
意味保持
判断分岐保持
明示禁止保持
未確認／未実行保持
command／path／API名保持
KDSL-DP直接実行禁止
RT:v条件
```

## 禁止

```text
KDSL-Intlをdefault化禁止
KDSL本体のidentity変更根拠に使用禁止
英語KEY互換を理由に漢字Coreを弱化禁止
```
