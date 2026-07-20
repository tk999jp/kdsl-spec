# KDSL Agent Execution Layer v1.1

## 0. 目的

```text
Agent目的:=U明示scopeを必要最小契約で調査→実装→検証→完了
```

Agent層の完成対象はschemaではなく、U価値としての作業完走。

```text
KDSL:=依頼内容を漢字圧縮
K1:=agent run状態
P1L:=厳密handoff用長形式契約
P1:=任意の短縮転送表現
PF1:=継続project既定
R1:=結果報告
```

```text
KDSL Core > Agent層
Agent層!=KDSL本体
Agent層!=汎用安全framework
```

## 1. 標準経路

Codex開発作業ではAgent駆動を使用する。ただし通常投入は最小構成とする。

```text
U自然文
→ChatGPT converter
→KDSL_PROMPT
→K1初期化
→Codex再帰実行
→R1
→ChatGPT
→U
```

標準必須:

```text
KDSL_PROMPT＋K1
```

次の場合だけ厳密契約を追加する。

```text
中断再開
複数agent handoff
長時間run
複雑な承認境界
project既定の再利用
U明示
→PF1参照→P1L生成→K1初期化
```

P1は転送量削減が必要な場合だけP1Lの代わりに使用する。P1LとP1の同時記載禁止。

## 2. Agent再帰

```text
K1確認
→未完から次作業選択
→明示権限照合
→実行
→検証
→K1更新
→完了条件判定
→未完ありなら再帰
```

Agentは明示scope内で次まで進める。

```text
調査→実装→targeted test→必要broader test→runtime候補提示
```

内部component完了、file数、test数、作業量、途中commitは停止理由にしない。

## 3. K1

K1は通常経路の最小状態block。

```text
K1:
状態: 計画|実行中|検証中|実機待|完了|停止|失敗
現在:
完了:
未完:
検証: 未実行|一部|成功|失敗
実機: 不要|未確認|確認済
次:
停止理由:
```

中断再開／handoff時だけ識別情報を追加する。

```text
run:
契約:
baseline:
PF1:
```

完了条件:

```text
状態=完了
→未完=なし
→検証=成功
→実機=不要|確認済
```

K1更新で目的・成功条件・対象・権限を変更しない。変更が必要ならKDSL_PROMPTまたはP1Lを再生成する。

## 3A. Run変更file帰属

Runは、1回の編集／実装／修正指示受領から対応R1または停止結果まで。production edit前に開始状態を固定し、終了時状態との差で今回runの変更fileを確定する。

```text
InitialHEAD:=run開始時HEAD
FinalHEAD:=run終了時HEAD

CommittedCandidate:=
InitialHEAD != FinalHEAD
  ? InitialHEAD→FinalHEAD差分のA／M／D path＋R／C旧path／新path
  : ∅

RunCandidate:=
開始時dirty／untracked
∪ 終了時dirty／untracked
∪ CommittedCandidate
∪ working tree rename旧path／新path
∪ working tree delete path

BaselineState:=
開始時dirty／untracked→開始時file state
開始時clean tracked→InitialHEAD上のfile state
開始時不存在→absent

FinalState:=
終了時working treeのexistence／kind／mode／content identity

RunChanged:={
  path∈RunCandidate
  | BaselineState(path) != FinalState(path)
}
```

file stateは、通常fileなら内容identity、linkならlink種別＋target、不存在なら`absent`を保持する。全repo fileの開始snapshotは不要。

```text
開始clean→終了変更: 含む
開始dirty→内容追加変化: 含む
開始dirty→内容不変: 含まない
今回新規作成／削除: 含む
今回rename: 旧path／新pathを含む
編集後に開始時状態へ復元: 含まない
test直接編集: 含む
test実行だけで未編集: 含まない
```

```text
R1.変更:=RunChangedの完全repo相対path全件
```

禁止:

```text
Task対象file一覧から推定
最終working tree全dirty列挙
editor表示fileから推定
test実行対象を変更file扱い
主要file＋総件数へ省略
pre-existing dirty不変fileを混入
```

baseline取得不能時はproduction editを開始しない。validator／lintはpath形式を検査できるが、実baselineとの意味一致は証明しない。

## 4. P1L

P1Lは厳密handoff／中断再開時の長形式契約。通常runでは省略可。

```text
P1L:
版: kdsl-agent@1.1
目的:
成功条件:
正本:
対象:
非対象:
権限:
  読取: 可
  編集: 可
  試験: 可
  commit: 承認待
承認境界:
作業:
検証:
実機要否: 要|不要
停止条件:
完了条件:
報告: R1
```

権限は今回runに関係する操作だけ記載する。

```text
記載済操作:=契約値を適用
未記載操作:=P1Lから許可しない
U明示指示>PF1>P1L生成時既定
PF1適用→権限拡張禁止
```

release／public履歴／破壊操作を使用しないrunで定型列挙しない。必要な場合だけ明示する。

## 5. P1

P1は任意の短縮転送表現。正本はP1LまたはKDSL_PROMPT。

```text
P1|版:kdsl-agent@1.1|目的:...|成功:...|正本:...|対象:...|非対象:...|権限:読取=可,編集=可,試験=可,commit=承認待|作業:...|検証:...|停止:...|完了:...|報告:R1
```

```text
P1:=任意短縮
P1!=可逆性保証
P1!=P1Lとの同時必須
P1欠落→Agent実行阻害なし
```

escape／round-tripが正式実装されるまで「可逆serialization」と称さない。

## 6. PF1

PF1は継続projectの既定。P1L生成前に参照する。

```text
PF1:
project:
正本:
既定profile: dev-prompt
既定mode: min
Phase方針:
権限既定:
承認必須:
試験方針:
実機方針:
報告方針:
```

```text
U明示指示>PF1
PF1でU禁止反転禁止
PF1で権限拡張禁止
PF1未確認値推測禁止
```

正規順序:

```text
U指示＋PF1
→KDSL_PROMPT／必要時P1L
→必要時P1
→K1初期化
```

## 7. 停止

停止は次だけ。

```text
明示停止条件成立
必要操作権限=承認待／不可
要件両立不能
必要正本取得不能
継続にscope変更必須
```

必要操作が承認待なら、その境界直前まで進めてK1を更新する。

## 8. 限定安全

```text
明示criticalだけ保持
潜在risk→新gate追加禁止
K1更新→scope追加禁止
PF1適用→権限拡張禁止
検証成功→RT:v自動昇格禁止
未依頼hardening→未完追加禁止
```

## 9. 非採用

```text
Safety Gate Registry
R1C
Packet／Normalization
共通AST／semantic parser
Binding Evidence
content digest／canonical JSON
runtime evaluator
```

## 10. 検証境界

```text
validator pass:=形式整合
運用回帰pass:=状態遷移／承認境界／再開契約／Run差分算出の自動確認
運用回帰pass!=Codex実効性
運用回帰pass!=実baseline取得確認
CI pass!=Codex runtime確認
```

`examples/kanji/agent-operational-proof.kdsl.md`を`tools/validator/kdsl_agent_operational_regression.py`で検証する。Codex再帰完走・中断再開・承認境界停止・実repositoryでのRunChanged帰属は実runで確認し、未確認時は未証明として扱う。
