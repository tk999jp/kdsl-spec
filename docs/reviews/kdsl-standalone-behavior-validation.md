# KDSL Standalone Converter 実効性検証

```text
確認日: 2026-08-05
対象: prompts/kdsl-converter-standalone.md
方式: 参照変換corpus＋静的behavior regression
状態: repository側pass／ChatGPT Project実投入RT:u
```

## 目的

standalone converterの存在・必須語だけでなく、代表入力に対する変換結果が次を保持することを回帰可能にする。

```text
漢字圧縮
A〜G mode
明示禁止
未確認／未実行／承認待
command／path／API名
出力Lock
安全条件非増殖
min／dense採用判断
```

## Corpus

```text
examples/behavior/standalone-cases.toml
case: 12
kind: 7
required marker: 63
exact identifier: 12
min／dense pair: 2
```

対象case:

```text
AI coding min／dense
創作seed min／dense
C dense結果のみ
D min／dense比較
E lintのみ
F CompactPrompt
G KDSL-Intl
承認待／未実行／RT未確認
Windows path／command／API名保持
入力外安全条件非追加
```

## 検査

```text
case数／id一意性
kind coverage
required marker保持
forbidden marker不在
identifier完全一致
先頭形式
C出力Lock
D比較section
E変換未実施
F CompactPrompt構造
G Intl派生境界
min／dense mode表記
pair実投入量→短いmode推奨
```

## 結果

```text
cases: 12/12 pass
kinds: 7/7 pass
required markers: 63/63 pass
identifiers: 12/12 pass
mode pairs: 2/2 pass
output lock violation: 0
safety growth violation: 0
```

実行:

```bash
python tools/validator/kdsl_standalone_behavior.py
```

## 境界

この検証は、人間review済み参照変換結果に対するbounded regressionである。

```text
pass!=任意LLMが同一出力を生成
pass!=完全意味同等
pass!=全model／全platform品質保証
pass!=ChatGPT Project RT:v
```

ChatGPT Projectへ`prompts/kdsl-converter-standalone.md`を実際に設定し、同corpusを投入したruntime確認は未実行。

```text
実機: RT:u
理由: Project設定／実model応答の外部観測未実施
```
