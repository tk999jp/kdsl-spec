# KDSL Glossary — Kanji Core + Agent

## KDSL

```text
KDSL:=日本語promptを漢字語幹／記号／最小制御語へ再構成する、LLM直投入可能な漢字圧縮DSL
```

## 漢字圧縮

```text
漢字圧縮:=助詞削減＋重複統合＋漢字語幹化＋条件／遷移記号化＋最小制御語化
```

KEY日本語化だけを意味しない。

## Agent goal

```text
Agent goal:=U明示scopeを必要最小契約で調査→実装→検証→完了
```

## K1

```text
K1:=通常Agent runの最小状態block
```

未完作業、検証、実機、次遷移を管理する。中断再開／handoff時だけrun／契約／baselineを追加する。

## P1L

```text
P1L:=厳密handoff／中断再開用の長形式契約
```

通常runでは省略可。PF1を参照して生成し、今回runに関係する権限だけ明示する。

## P1

```text
P1:=任意の短縮転送表現
```

P1Lと同時記載しない。escape／round-trip実装前は可逆性を保証しない。

## PF1

```text
PF1:=継続projectの既定条件
```

U明示指示より下位。P1L生成前に参照し、権限を拡張しない。

## CompactPrompt

```text
CompactPrompt:=一般LLM／Project instructions向けの短いKDSL profile
```

標準構造は `目的／材料／出力／規則／確認`。

## KDSL-Intl

```text
KDSL-Intl:=非漢字言語／ASCII／英語KEY向け互換subset
```

KDSL本体ではない。

## 安全契機

```text
安全契機:=Uが明示した重大条件の意味消失を防ぐ限定保護
```

汎用AI統制frameworkではなく、推測増殖禁止。

## KDSL_PROMPT

```text
KDSL_PROMPT:=AI coding tool向け漢字圧縮作業prompt
```

Codex開発runではK1を併用する。

## KDSL_RESULT／R1

```text
KDSL_RESULT:=作業結果の短い一時報告
```

成果物・仕様書・引継書・roadmapではない。

## RT:v

```text
RT:v:=対象環境runtime確認済
```

build／diff／lint／test／CI passはRT:vではない。

## Validator

```text
Validator:=形式・欠落・identity違反を検査する非権威的補助
```

validator passは意味同等・Agent実効性・U承認・RT:v・release readinessを証明しない。

## 旧v2 framework

```text
Safety Gate Registry／R1C／Packet／Normalization／semantic parser／重P1 schema／旧K1／Binding Evidence
```

archive資産。必要性が実用上確認された場合だけ再審査する。