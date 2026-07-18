# Codex Agent実行例

```text
KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: normal
agent: required

局面: 実装修正
目的: Bytes表示不具合修正
成功条件: Bytes選択時に実値表示／既存KB・MB表示維持
正本: G:\source\repos\MidFD／main
権限: P1L参照
承認境界: commit／pushはU明示時のみ
対象: Bytes表示経路／関連test
非対象: 他表示format／未依頼hardening
作業: 原因限定→実装→targeted test→必要broader test
試験: 関連test／全体回帰
検証: 表示分岐／既存format非回帰
停止条件: 要件両立不能／正本取得不能／scope変更必須
報告: R1

P1L:
版: kdsl-agent@1
実行方式: agent再帰
目的: Bytes表示不具合修正
成功条件: Bytes実値表示／KB・MB非回帰
正本: G:\source\repos\MidFD／main
対象: Bytes表示経路／関連test
非対象: 他表示format／未依頼hardening
権限:
  読取: 可
  編集: 可
  試験: 可
  stage: 対象外
  commit: 承認待
  push: 承認待
  release: 対象外
  public履歴: 不可
  破壊操作: 不可
承認境界: commit／push直前
作業: 原因限定→実装→targeted test→必要broader test
試験: 関連test／全体回帰
検証: Bytes表示／KB・MB非回帰
実機要否: 不要
停止条件: 要件両立不能／正本取得不能／scope変更必須
完了条件: 実装済／検証成功／未完なし
報告: R1

P1|版:kdsl-agent@1|実行方式:agent再帰|目的:Bytes表示不具合修正|成功条件:Bytes実値表示／KB・MB非回帰|正本:G:\source\repos\MidFD／main|対象:Bytes表示経路／関連test|非対象:他表示format／未依頼hardening|権限:読取=可,編集=可,試験=可,stage=対象外,commit=承認待,push=承認待,release=対象外,public履歴=不可,破壊操作=不可|承認境界:commit／push直前|作業:原因限定→実装→targeted test→必要broader test|試験:関連test／全体回帰|検証:Bytes表示／KB・MB非回帰|実機要否:不要|停止条件:要件両立不能／正本取得不能／scope変更必須|完了条件:実装済／検証成功／未完なし|報告:R1

K1:
状態: 完了
現在: 完了判定
完了: 原因限定／実装／targeted test／全体回帰
未完: なし
検証: 成功
実機: 不要
次遷移: R1報告
停止理由: なし

PF1:
project: MidFD
正本: G:\source\repos\MidFD／main
既定profile: dev-prompt
既定mode: min
Phase方針: 1機能=1Phase／明示scope完走
権限既定:
  読取: 可
  編集: 可
  試験: 可
  stage: 対象外
  commit: 承認待
  push: 承認待
  release: 対象外
  public履歴: 不可
  破壊操作: 不可
承認必須: commit／push／release／public履歴／破壊操作
試験方針: targeted test→必要broader test
実機方針: U実機観測のみRT:v
報告方針: 最小R1／scope外課題追加禁止
```
