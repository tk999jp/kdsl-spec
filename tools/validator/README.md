# Validator

KDSL漢字identityと最小R1境界を検査する軽量補助。

## 実装

```text
kdsl_identity_lint.py:=正本identity／必須file／禁止構造確認
kdsl_document_lint.py:=active template／exampleの英語KEY・旧v2構造・未定義alias検出
r1_result_lint.py:=日本語KDSL_RESULT field順／RT:v／次／commit境界確認
run_canonical_samples.py:=valid／invalid corpus＋active document回帰
```

## 実行

```bash
python tools/validator/kdsl_identity_lint.py
python tools/validator/run_canonical_samples.py
```

個別:

```bash
python tools/validator/kdsl_document_lint.py <file...>
python tools/validator/r1_result_lint.py <result-file>
```

## 境界

```text
validator:=非権威的補助
validator pass != 意味同等
validator pass != 漢字圧縮品質の最終判断
validator pass != U承認
validator pass != RT:v
validator pass != release readiness
```

## 非採用

旧v2の共通AST、Packet parser、Safety Gate Registry、R1C、P1／K1等のvalidatorは正規branchへ移植しない。必要な状態反転防止・field順・source保持の考え方だけを軽量lintへ回収した。

既存の `*-design.md` は歴史設計資料であり、現行実装正本ではない。
