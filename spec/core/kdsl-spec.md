# KDSL Specification — Kanji Core

## 0 定義

```text
KDSL:=日本語promptを漢字語幹／記号／最小制御語へ再構成する、LLM直投入可能な漢字圧縮DSL
自然文=>助詞削減+重複統合+漢字語幹化+条件記号化+最小制御語化
```

第一目的は**漢字圧縮**。単なる日本語化、英語KEY構造化、安全契約framework化、schema化、証跡管理を第一目的へ置かない。

```text
identity:=日本語／漢字圧縮／意味保持／LLM直投入／判断分岐保持／低tool依存／限定安全
```

## 1 派生subset

```text
KDSL本体:=漢字圧縮
KDSL-Intl:=非漢字言語／ASCII／英語KEY向け互換subset
KDSL本体 > KDSL-Intl
```

禁止:

```text
KDSL-Intlを本体扱い禁止
英語KEYを無指定既定化禁止
漢字表現をoptional lexiconへ降格禁止
非漢字対応を理由にidentity変更禁止
```

## 2 設計順位

```text
第一目的:=漢字圧縮
成立条件:=意味保持／LLM直投入／判断分岐保持／明示制約保持／出力安定／人間修正可能
```

不可侵:

```text
明示禁止
明示未確認／未実行
明示承認待
明示rollback／revert
明示data破壊防止
明示public履歴保護
明示RT:v条件
```

不可侵条件は意味消失防止の限定保護であり、汎用安全frameworkではない。

## 3 設計単位

```text
format: KDSL
profile: dev-prompt|compact-prompt|converter|lint
mode: readable|min|dense|lock
safety: normal|lock-critical|lock-all
agent: required|optional
language: ja
```

通常既定:

```text
format: KDSL
profile: dev-prompt
mode: min
safety: normal
agent: optional
language: ja
```

profile変更で漢字圧縮を解除しない。実装／repo操作／runtime確認を含んでも本文は漢字圧縮を維持する。

Agent層使用条件:

```text
repo書込／複数step実装／再帰完走／複数tool／中断再開／commit・push・release操作
→agent: required
```

通常会話、単発回答、変換のみは `agent: optional`。

## 4 漢字圧縮

KEY翻訳だけで完了扱いしない。

```text
GOAL→目的
WORK→作業
VERIFY→検証
```

だけでは不足。本文も助詞削減・重複統合・漢字語幹化・記号化する。

```text
helperがdestination parentを先に作成していても、cross-volume directory moveがdestination collisionで失敗しない。
=>
跨volume dir移動: helper先行dst親作成済→collision失敗禁止
```

標準構造KEY:

```text
局面／目的／成功条件／根拠／正本／権限／承認境界／対象／非対象／作業／試験／検証／停止条件／報告
```

CompactPrompt構造KEY:

```text
目的／材料／出力／規則／確認
```

未定義一字alias推測禁止。短い日本語KEYを優先する。

## 5 安全契機

```text
安全契機:=Uが明示した重大条件の限定保護
安全契機!=汎用AI行動統制framework
```

禁止:

```text
潜在risk推測→本文へ自動追加禁止
U未指定承認gate追加禁止
安全理由scope拡張禁止
安全理由Phase細分化禁止
安全理由architecture再設計禁止
通常改修high-risk自動昇格禁止
追加hardeningを完成条件へ混入禁止
「念のため」停止条件追加禁止
```

`lock-critical`は明示critical箇所だけを保護する。

## 6 KDSL_PROMPT

```text
KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: normal
agent: optional

局面:
目的:
成功条件:
根拠:
正本:
対象:
非対象:
作業:
試験:
検証:
停止条件:
報告:
```

```text
KDSL_PROMPT前自然文禁止
本文:=漢字圧縮
英語構造KEY必須化禁止
```

## 7 Agent層

```text
KDSL:=依頼内容を漢字圧縮
P1L:=agent実行内容の正規長形式
P1:=P1Lの可逆短縮
K1:=agent run状態
PF1:=project既定
R1:=結果報告
```

`agent: required`時:

```text
P1L／P1／K1必須
継続project／project既定あり→PF1必須
PF1なし→全条件をP1Lへ明示
```

```text
P1L／P1 valid != 全操作許可
実行許可:=P1L権限rail
K1更新→目的／scope／権限変更禁止
PF1→P1L権限拡張禁止
```

Agent層正本は `spec/agent/kdsl-agent-execution.md`。

## 8 KDSL_RESULT

KDSL_RESULTは短い一時報告であり、仕様書・引継書・roadmapではない。

```text
KDSL_RESULT:
状態:
局面:
要約:
変更:
理由:
実行:
検証:
実機:
危険:
次:
commit:
```

```text
未実行command→実行欄記載禁止
未実行verify→pass扱禁止
build／lint／test／CI pass != RT:v
RT:v:=対象環境runtime確認済のみ
次:=提案、実行許可扱禁止
commit:=実行済commitまたは推奨message
自動commit許可扱禁止
```

## 9 境界

```text
KDSL:=LLM直投入可能な漢字圧縮prompt
KDSL-DP:=Agent向けAuthoring形式
P1／P1L:=agent実行時の正規契約
K1:=agent run状態制御
PF1:=project既定制約
R1／KDSL_RESULT:=結果報告
```

```text
KDSL-DP直接実行禁止
KDSL-DP→P1L／P1正規化必須
P1L／P1 valid != 全操作許可
通常会話／単発prompt→Agent層省略可
repo実装／再帰完走／複数tool→Agent層必須
```

Agent層はKDSL Coreの下位。P1／K1／PF1は漢字identityを上書きできない。Safety Gate Registry／Packet／R1C／Binding EvidenceをAgent層の必須依存にしない。

## 10 変換禁止

```text
command／path／URL／repo名／branch名／tag名／package名
class名／method名／property名／API名／file名／拡張子／Windows path／inline code
```

英語技術識別子を無理に漢字化しない。

## 11 identity変更

次はbreakingであり、U明示承認必須。

```text
漢字圧縮を第一目的から外す
英語KEYを既定化
漢字をoptional化
KDSL-Intlを本体化
安全契機を第一目的化
Agent層をKDSL本体より上位化
```
