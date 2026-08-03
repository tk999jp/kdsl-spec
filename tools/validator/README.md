# Validator

KDSL漢字identity、standalone配布物、Agent契約、RunChanged、圧縮評価、R1境界を検査する軽量補助。

## 実装

```text
kdsl_identity_lint.py:=正本identity／必須file／禁止構造
kdsl_standalone_lint.py:=compiled prompt必須要素／非正本境界／投入量上限
kdsl_document_lint.py:=active template／exampleの英語KEY・旧v2構造・未定義alias
kdsl_agent_lint.py:=KDSL_PROMPT＋K1／条件付きP1L・P1・PF1契約
kdsl_agent_operational_regression.py:=Agent状態遷移回帰
kdsl_run_changed_git_regression.py:=Git baseline／final stateからRunChanged算出回帰
kdsl_compression_evaluation.py:=min／dense圧縮量・概念marker評価
r1_result_lint.py:=日本語KDSL_RESULT field順／RT:v／次／commit境界
run_canonical_samples.py:=valid／invalid corpus＋active document回帰
```

## 標準実行

```bash
python tools/validator/kdsl_identity_lint.py
python tools/validator/kdsl_standalone_lint.py
python tools/validator/kdsl_agent_lint.py examples/kanji/agent-codex-run.kdsl.md
python tools/validator/kdsl_agent_operational_regression.py
python tools/validator/kdsl_run_changed_git_regression.py
python tools/validator/kdsl_compression_evaluation.py
python tools/validator/run_canonical_samples.py
```

個別document／R1検査:

```bash
python tools/validator/kdsl_document_lint.py <file...>
python tools/validator/r1_result_lint.py <result-file>
```

## 境界

```text
validator:=非権威的補助
validator pass != 意味同等
validator pass != 漢字圧縮品質の最終判断
validator pass != Agent実効性
validator pass != ユーザー承認
validator pass != RT:v
validator pass != release readiness
```

## 履歴

実装開始前の`*-design.md`は現行toolと重複し、旧英語field／Safety Gate／Authority中心設計を含むため`main`から除外した。詳細はGit履歴、`v0.1.0-draft` tag、`archive/kdsl-framework-20260718`で保持する。
