# KDSL Glossary — Kanji Core + Agent Layer

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

## Agent層

```text
Agent層:=ChatGPT／Codex間の実行契約・run状態・project既定を扱うKDSL Core下位層
```

repo書込、複数step実装、再帰完走、複数tool、中断再開で使用する。KDSLの第一目的を変更しない。

## P1L

```text
P1L:=Agent実行内容を損失なく固定する正規長形式
```

目的、成功条件、正本、scope、権限rail、作業、検証、停止条件、完了条件を保持する。

## P1

```text
P1:=P1Lの可逆短縮serialization
```

field・権限rail省略禁止。P1からP1Lへ復元不能なら不成立。

## K1

```text
K1:=1回のAgent run状態
```

計画／実行中／検証中／実機待／完了／停止／失敗を管理する。目的・scope・権限を変更しない。

## PF1

```text
PF1:=継続projectの既定profile／権限／試験／実機／報告方針
```

U明示指示を上書きせず、P1L権限を拡張しない。

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

日本語構造KEYを使用し、英語KEYを必須化しない。Agent使用時はP1L／P1／K1／PF1を接続する。

## KDSL_RESULT

```text
KDSL_RESULT:=作業結果の短い一時報告
```

成果物・仕様書・引継書・roadmapではない。P1L／P1／K1／PF1の複製もしない。

## RT:v

```text
RT:v:=対象環境runtime確認済
```

build／diff／lint／test／CI passはRT:vではない。

## KDSL-DP

```text
KDSL-DP:=Agent向けAuthoring形式
```

直接実行禁止。P1L／P1正規化必須。

## Validator

```text
Validator:=形式・欠落・identity違反を検査する非権威的補助
```

validator passは意味同等・実行許可・漢字圧縮品質・U承認・RT:v・release readinessを証明しない。

## 旧v2 framework

```text
Safety Gate Registry／R1C／Packet／Normalization／semantic parser
旧P1／P1L canonical JSON schema
旧K1／PF1 canonicalization／Binding Evidence／runtime evaluator
```

現Agent層の正本ではなくarchive資産。必要性が実用上証明された場合だけ機能単位で再審査する。
