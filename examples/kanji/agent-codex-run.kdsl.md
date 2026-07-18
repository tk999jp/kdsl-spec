# Codex Agent最小実行例

通常のCodex開発runは `KDSL_PROMPT＋K1` を使用する。

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
根拠: U実機観測／関連code
正本: G:\source\repos\MidFD／main／baseline確認
権限: 読取／編集／試験=可、commit／push=承認待
承認境界: commit／push直前
対象: Bytes表示経路／関連test
非対象: 他表示format／未依頼hardening
作業: 原因限定→実装→targeted test→必要broader test
試験: 関連test／必要全体回帰
検証: Bytes表示／KB・MB非回帰
停止条件: 要件両立不能／正本取得不能／scope変更必須
報告: R1

K1:
状態: 計画
現在: 初期化
完了: なし
未完: 原因調査／実装／targeted test／必要broader test／結果確認
検証: 未実行
実機: 不要
次: 原因調査
停止理由: なし
```

実行後は同じK1を更新する。

```text
K1:
状態: 完了
現在: 完了判定
完了: 原因調査／実装／targeted test／必要broader test／結果確認
未完: なし
検証: 成功
実機: 不要
次: R1報告
停止理由: なし
```

## 厳密handoff時だけ追加

```text
handoff: required

P1L:
版: kdsl-agent@1.1
目的: Bytes表示不具合修正
成功条件: Bytes実値表示／KB・MB非回帰
正本: G:\source\repos\MidFD／main
対象: Bytes表示経路／関連test
非対象: 他表示format／未依頼hardening
権限:
  読取: 可
  編集: 可
  試験: 可
  commit: 承認待
  push: 承認待
承認境界: commit／push直前
作業: 原因限定→実装→targeted test→必要broader test
検証: Bytes表示／KB・MB非回帰
実機要否: 不要
停止条件: 要件両立不能／正本取得不能／scope変更必須
完了条件: 実装済／検証成功／未完なし
報告: R1

K1:
run: midfd-bytes-001
契約: P1L／Bytes表示不具合修正
baseline: main@確認済HEAD
PF1: MidFD既定
状態: 計画
現在: handoff受領
完了: なし
未完: 原因調査／実装／試験／検証
検証: 未実行
実機: 不要
次: baseline確認
停止理由: なし
```

P1を使う場合はP1Lの代替とし、同一promptへ併記しない。