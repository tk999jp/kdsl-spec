# KDSL Glossary — Kanji Core

## KDSL

```text
KDSL:=日本語promptを漢字語幹／記号／最小制御語へ再構成する、LLM直投入可能な漢字圧縮DSL
```

## 漢字圧縮

```text
漢字圧縮:=助詞削減＋重複統合＋漢字語幹化＋条件／遷移記号化＋最小制御語化
```

KEYの日本語化だけを意味しない。

## CompactPrompt

```text
CompactPrompt:=一般LLM／Project instructions向けの短いKDSL profile
```

漢字圧縮を既定維持し、標準構造は `目的／材料／出力／規則／確認`。実装用途でdev-promptへ変えても漢字identityは不変。

## KDSL-Intl

```text
KDSL-Intl:=非漢字言語／ASCII／英語KEY向け互換subset
```

KDSL本体ではない。無指定時は適用しない。

## 安全契機

```text
安全契機:=Uが明示した重大条件の意味消失を防ぐ限定保護
```

汎用AI統制frameworkではなく、推測増殖禁止。

## 不可侵条件

```text
明示禁止
明示未確認／未実行
明示承認待
明示rollback／revert
明示data／public保護
明示RT:v
```

## KDSL_PROMPT

```text
KDSL_PROMPT:=AI coding tool向け漢字圧縮作業prompt
```

日本語構造KEYを使用し、英語KEYを必須化しない。

## KDSL_RESULT

```text
KDSL_RESULT:=作業結果の短い一時報告
```

成果物・仕様書・引継書・roadmapではない。

## RT:v

```text
RT:v:=対象環境runtime確認済
```

build／diff／lint／test／CI passはRT:vではない。

## KDSL-DP

```text
KDSL-DP:=ADPS向けAuthoring形式
```

直接実行禁止。P1／P1L正規化必須。

## P1／P1L

```text
P1／P1L:=KDSL-DPから正規化される実行契約候補
```

valid／lint passだけでは実行許可にならない。詳細schemaはKDSL本体の必須architectureではない。

## Validator

```text
Validator:=形式・欠落・identity違反を検査する非権威的補助
```

validator passは意味同等・漢字圧縮品質・U承認・RT:v・release readinessを証明しない。

## 旧v2 framework

```text
Safety Gate Registry／R1C／Packet／Normalization／semantic parser／K1／PF1／Binding Evidence
```

漢字圧縮正本ではなくarchive資産。必要性が漢字圧縮上で証明された場合だけ再審査する。
