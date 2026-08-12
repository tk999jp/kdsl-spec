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
成立条件:=意味保持／LLM直投入／判断分岐保持／明示制約保持／Agent完走／出力安定／人間修正可能
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

## 2.1 契約保持

```text
契約世代:
同一事項競合→後発確定>先発確定>仮説／提案／状態観測
直近記述のみ→確定扱禁止
撤回済／置換済判断→再採用禁止
```

```text
正本:
状態観測／実装／test／Docs／State／KDSL_RESULT:=観測／状態／証跡
明示なし→契約正本扱禁止
下位情報→上位契約上書禁止
AI判断!=U確定
source／test／Docs／State相互一致!=上位契約変更根拠
派生観測:=上位契約の成立確認用証拠
U明示／canonical根拠なし→派生観測を新規契約へ昇格禁止
```

```text
意味scope:
対象外の観測可能意味変更禁止
集合演算／追加／置換／結合／clear／保存範囲／routing／fallback／default／副作用変更→semantic change
内部rename／refactor可; 対象外動作同値必須
```

これらは明示意味の世代・正本・scopeを保持する規則であり、潜在risk推測による安全条件追加ではない。

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

Codex開発作業では `agent: required`。通常会話、単発回答、変換のみは `agent: optional`。

```text
Agent目的:=U明示scopeを必要最小契約で調査→実装→検証→完了
```

Agent必須でもP1L／P1／PF1全量を自動必須化しない。

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

## 4.1 圧縮成立／正本参照

```text
圧縮成立:=重複統合→正本値／意味参照化→意味束化→助詞削減→漢字語幹化→条件記号化→最小制御語化
KEY構造化のみ!=圧縮成立
本文自然文維持＋日本語KEY化のみ!=圧縮成立
section分割目的の同義再掲禁止
```

同一長値・固定条件・同一契約意味は原則一回だけ定義し、以後は意味明確な短名で参照する。

```text
反復値:=hash／version／path／tag／Asset名／固定値／固定状態
反復意味:=公開不変／候補一致／対象外不変／承認済等の同一契約
正本: 候補:=<長値群>／公開:=<固定状態群>
以後: 候補一致／公開不変／remote=候補
```

変換禁止対象そのものは定義箇所で保持する。参照短名は技術識別子の翻訳ではない。

意味束:

```text
同一対象の複数固定要素→意味を変えず意味名へ統合可
例: Package＋size＋hash→候補
例: main＋tag→公開
例: Release＋対象外Asset＋source＋dirty→保全
意味束:=U明示／canonicalで既に存在する意味の圧縮名
意味束による新条件生成禁止
意味束定義後→成功／作業／検証／停止／報告は意味名参照優先
構成要素に条件差あり→無理な束化禁止
```

```text
section独立可読性目的の長値／意味再掲禁止
意味束定義済み構成要素のsection別再展開禁止
成功条件:=最終成立状態
検証:=成立確認方法
同じ成立状態を成功条件／検証／保持／停止条件／報告へ全文再掲禁止
成功条件の否定形を停止条件へ全複製禁止
```

派生条件:

```text
U明示条件／canonical条件:=保持
上位条件から導く具体観測→検証証拠として使用可
派生観測→新規成功条件／停止条件／保持条件へ自動昇格禁止
```

作業文:

```text
作業:=操作語幹＋対象＋遷移／Gate
方法説明／理由再説明／成功条件再掲禁止
```

制御語:

```text
技術識別子→保持
一般制御英語→安定漢字語ありなら漢字化
Candidate→候補
baseline→基線
read-only→読取
exact→完全一致
unrelated→対象外
fallback→代替
```

上記は例であり、API名・command・property名等へ機械適用しない。

短名はKDSL参照名であり、shell変数ではない。

```text
本文短名参照可
inline code内へ短名を未展開literalとして実行command化禁止
exact command要求時→実値展開
command構造提示時→command名保持＋引数対応を本文分離
```

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
agent: required

局面:
目的:
成功条件:
根拠:
正本:
権限:
承認境界:
対象:
非対象:
作業:
試験:
検証:
停止条件:
報告: R1

K1:
状態: 計画
現在: 初期化
完了: なし
未完:
検証: 未実行
実機: 不要|未確認
次: 調査
停止理由: なし
```

```text
KDSL_PROMPT前自然文禁止
本文:=漢字圧縮
英語構造KEY必須化禁止
不要KEYは省略可
正本定義済み長値／意味／意味束のsection再掲禁止
```

## 7 Agent層

```text
標準Agent:=KDSL_PROMPT＋K1
P1L:=厳密handoff／中断再開用長形式
P1:=任意短縮転送表現
PF1:=継続project既定
R1:=結果報告
```

P1L／PF1追加条件:

```text
中断再開
複数agent handoff
長時間run
複雑承認境界
project既定再利用
U明示
```

```text
PF1参照→P1L生成→K1初期化
P1使用時→P1Lと併記禁止
P1!=可逆性保証
K1更新→目的／scope／権限変更禁止
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
K1:=標準agent run状態
P1L:=条件付き厳密契約
P1:=条件付き短縮転送
PF1:=条件付きproject既定
R1／KDSL_RESULT:=結果報告
```

```text
KDSL-DP直接実行禁止
通常Agent→KDSL_PROMPT＋K1
厳密handoff→PF1参照＋P1L＋K1
P1L／P1 valid != 全操作許可
形式lint pass != Codex Agent実効性
```

Agent層はKDSL Coreの下位。P1／K1／PF1は漢字identityを上書きできない。Safety Gate Registry／Packet／R1C／Binding Evidenceを必須依存にしない。

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
