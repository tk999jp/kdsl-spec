# Project Status

status: canonical
branch: main

## Current

KDSL canonical identity is Kanji compression. Agent execution remains subordinate to the Kanji Core. Framework-heavy v2 assets remain archived unless selectively recovered by demonstrated need.

## Canonical

```text
KDSL:=日本語promptを漢字語幹／記号／最小制御語へ再構成する漢字圧縮DSL
KDSL本体:=漢字圧縮
KDSL-Intl:=派生subset
Agent層:=KDSL Core下位
R1:=最小結果報告
validator:=補助／非権威
```

## Active assets

```text
spec/core/
spec/profiles/
spec/agent/
spec/r1/
spec/lint/
spec/bridge/
prompts/kdsl-converter-standalone.md
templates/
examples/
tools/validator/
```

## Validation

GitHub Actions `KDSL Validation` runs identity, standalone, Agent, RunChanged, compression, and canonical sample checks.

```text
形式pass != 意味同等
形式pass != Agent実効性
形式pass != U承認
形式pass != RT:v
```

## Archive boundary

Framework-heavy assets remain outside the active canonical dependency graph:

```text
Safety Gate Registry
R1C
Packet／Normalization
共通AST／semantic parser
Binding Evidence
runtime evaluator
```

No future phase or adoption is implied solely by archived implementation existence.
