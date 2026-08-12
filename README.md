# KDSL

KDSLは、日本語promptを漢字語幹／記号／最小制御語へ再構成し、LLMへ直接投入可能な形へ圧縮するDSLです。

```text
自然文
=> 助詞削減
 + 重複統合
 + 正本値／意味参照化
 + 漢字語幹化
 + 条件／遷移記号化
 + 最小制御語化
```

第一目的は**漢字圧縮**です。

KDSLは、英語KEY中心の汎用schema、安全契約framework、証跡管理方式を本体として定義しません。非漢字言語向けは派生subset `KDSL-Intl` として扱います。

## Canonical identity

```text
KDSL:=日本語promptを対象にした漢字圧縮DSL
KDSL本体:=漢字圧縮
KDSL-Intl:=非漢字言語／ASCII／英語KEY向け互換subset
KDSL本体 > KDSL-Intl
```

Core:

- `spec/core/kdsl-spec.md`
- `spec/core/kdsl-core.md`
- `spec/core/kdsl-modes.md`

Profiles:

- `spec/profiles/kdsl-profile-dev-prompt.md`
- `spec/profiles/kdsl-profile-compact-prompt.md`
- `spec/profiles/kdsl-converter-prompt.md`
- `spec/profiles/kdsl-profile-intl.md`

Agent:

- `spec/agent/kdsl-agent-execution.md`

Result:

- `spec/r1/r1-result-spec.md`

Lint:

- `spec/lint/kdsl-lint-checklist.md`
- `spec/lint/kdsl-agent-lint.md`

## 圧縮原則

KEYを日本語へ翻訳するだけではKDSL圧縮になりません。本文も圧縮します。

```text
helperがdestination parentを先に作成していても、
cross-volume directory moveがdestination collisionで失敗しない。

=>

跨volume dir移動: helper先行dst親作成済→collision失敗禁止
```

同一hash／version／path／固定状態、または同一の公開不変／候補一致等の契約意味は原則一回だけ定義し、以後は意味明確な短名で参照します。

```text
正本:
候補:=<長値群>
公開:=<固定状態群>

成功条件:
候補一致／公開不変
```

上位契約の成立確認用に導いた具体観測は検証証拠として使用できますが、U明示／canonical根拠なしに新しい成功条件・停止条件へ昇格させません。

## mode

```text
readable:=人間review重視
min:=実運用標準／中密度
dense:=AI直投入／高密度
lock:=明示critical箇所の意味保持重視
```

全modeで漢字圧縮を維持します。

`dense`は`min`成立条件を保持し、自然文残留・同義再掲をさらに削ります。意味保持可能な範囲では、説明追加を理由に`min`より膨張させません。

## dev-prompt

開発promptでも漢字圧縮を解除しません。

```text
KDSL_PROMPT:
目的:
成功条件:
対象:
作業:
検証:
```

必要なKEYだけを使い、同一内容のsection横断再掲を避けます。

契約保持では、次を区別します。

```text
直近U確定 > canonical contract > 確認済実機契約 > State > source/test
AI判断 != U確定
source/test/Docs/State相互一致 != 契約変更根拠
```

確定契約testの期待値変更には上位根拠を要求しますが、通常bug修正や既存契約への復元を一律承認gate化しません。

## standalone converter

ChatGPT Project instructions等へ投入する非正本配布prompt:

- `prompts/kdsl-converter-standalone.md`

正本と競合した場合は正本を優先します。

## validation

補助validator:

- identity lint
- standalone lint／behavior
- Agent lint／operational regression
- RunChanged regression
- compression evaluation
- canonical sample regression

validator passは、意味同等・圧縮品質・U承認・RT:v・release readinessの証明ではありません。

## history

KDSLはv2系で増えたframework-heavy資産を監査し、漢字圧縮identityを中心に再構築しています。監査記録は`docs/reviews/`を参照してください。

## license

MIT
