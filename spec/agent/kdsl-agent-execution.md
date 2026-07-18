# KDSL Agent Execution Layer v1.0

## 0. 位置づけ

```text
KDSL:=何を依頼するかを漢字圧縮
P1L:=agent実行内容を損失なく固定する長形式契約
P1:=P1Lの短縮serialization
K1:=1回のagent run状態
PF1:=project固有の既定条件
R1:=実行結果の短い報告
```

Agent層はKDSL Coreの下位層。KDSLの第一目的・漢字identityを変更しない。

```text
KDSL Core > Agent層
Agent層!=KDSL本体
Agent層!=汎用安全framework
```

## 1. 使用条件

次のいずれかを含む時、Agent層を使用する。

```text
repo書込
複数step実装
再帰完走
複数tool使用
中断再開
commit／push／release操作
```

通常会話、単発回答、変換だけの依頼では省略可。

```text
agent: required|optional
```

`agent: required`時:

```text
P1L必須
P1必須
K1必須
継続project／project既定あり→PF1必須
PF1なし→全条件をP1Lへ明示
```

## 2. 正規経路

```text
U自然文
→ChatGPT converter
→KDSL dev-prompt／KDSL-DP
→P1L正規化
→P1短縮
→PF1適用
→K1初期化
→Codex agent再帰実行
→R1
→ChatGPT
→U
```

## 3. P1L

### 3.1 目的

P1Lは、ChatGPTからCodexへ渡す実行契約の損失なし長形式。

```text
P1L:
版: kdsl-agent@1
実行方式: agent再帰|単発
目的:
成功条件:
正本:
対象:
非対象:
権限:
  読取: 可|不可|承認待|対象外
  編集: 可|不可|承認待|対象外
  試験: 可|不可|承認待|対象外
  stage: 可|不可|承認待|対象外
  commit: 可|不可|承認待|対象外
  push: 可|不可|承認待|対象外
  release: 可|不可|承認待|対象外
  public履歴: 可|不可|承認待|対象外
  破壊操作: 可|不可|承認待|対象外
承認境界:
作業:
試験:
検証:
実機要否: 要|不要
停止条件:
完了条件:
報告: R1
```

### 3.2 権限

```text
権限元:=U明示指示／Project明示指示／PF1
権限推測追加禁止
P1L valid != 全操作許可
必要操作=承認待→その境界直前まで実行可
対象外操作→実行禁止
PF1適用→権限拡張禁止／同値または縮小のみ
```

Uが修正・実装を明示した場合、明示scope内の読取／編集／試験はP1Lへ正規化可。commit／push／release／public履歴変更／破壊操作は、UまたはPF1の明示条件を必要とする。

### 3.3 変更境界

P1L成立後、K1は目的・scope・権限を変更できない。

```text
目的／成功条件／対象／権限変更
→P1L再生成
→必要時U確認
```

通常実装補正、targeted test追加、明示scope内の内部整理はP1L変更に当たらない。

## 4. P1

P1はP1Lの短縮serialization。意味省略禁止。

```text
P1|版:kdsl-agent@1|実行方式:agent再帰|目的:...|成功条件:...|正本:...|対象:...|非対象:...|権限:読取=可,編集=可,試験=可,stage=対象外,commit=対象外,push=対象外,release=対象外,public履歴=不可,破壊操作=不可|承認境界:...|作業:...|試験:...|検証:...|実機要否:不要|停止条件:...|完了条件:...|報告:R1
```

```text
P1→P1L復元不能→P1不成立
P1 field省略禁止
P1権限rail省略禁止
P1 compact化→漢字identity解除禁止
```

## 5. K1

### 5.1 状態

```text
K1:
状態: 計画|実行中|検証中|実機待|完了|停止|失敗
現在:
完了:
未完:
検証: 未実行|一部|成功|失敗
実機: 不要|未確認|確認済
次遷移:
停止理由:
```

### 5.2 再帰

```text
K1確認
→未完から次作業選択
→P1権限照合
→実行
→検証
→K1更新
→完了条件判定
→未完ありなら再帰
```

停止条件:

```text
P1L停止条件成立
必要操作権限=承認待／不可
要件両立不能
必要正本取得不能
実行継続で明示scope変更必須
```

内部component完了、file数、test数、作業量、途中commitは停止理由にしない。

### 5.3 完了

```text
K1状態=完了
→未完=なし
→検証=成功
→実機要否=不要なら実機=不要
→実機要否=要なら実機=確認済
```

build／lint／test／CI成功だけで実機確認済へ変更禁止。

## 6. PF1

PF1は継続projectの既定条件。P1L生成時に参照し、P1Lへ展開する。

```text
PF1:
project:
正本:
既定profile: dev-prompt
既定mode: min
Phase方針:
権限既定:
  読取:
  編集:
  試験:
  stage:
  commit:
  push:
  release:
  public履歴:
  破壊操作:
承認必須:
試験方針:
実機方針:
報告方針:
```

```text
PF1:=project既定
PF1!=今回依頼
U明示指示>PF1
PF1でU禁止反転禁止
PF1で権限拡張禁止
PF1未確認値推測禁止
```

## 7. Agent駆動と安全契機

Agent層は実行状態を管理する。潜在risk探索やgate自動生成は行わない。

```text
安全契機:=P1Lへ明示条件を保持
K1:=実行状態遷移
PF1:=project既定供給
```

禁止:

```text
潜在risk→新承認gate自動追加
K1更新→scope追加
PF1適用→権限拡張
検証成功→RT:v自動昇格
未依頼hardening→未完追加
```

## 8. 非採用

Agent層v1では次を導入しない。

```text
Safety Gate Registry
R1C
Packet／Normalization
共通AST／semantic parser
Binding Evidence
content digest／canonical JSON
runtime evaluator
```

必要性が実用上確認された場合のみ、Agent層の独立拡張として再審査する。

## 9. 正規判定

```text
P1L:=正規長形式
P1:=P1L可逆短縮
K1:=run状態正本
PF1:=project既定正本
R1:=結果報告
```

validator passは実行許可・意味同等・RT:vの証明ではない。