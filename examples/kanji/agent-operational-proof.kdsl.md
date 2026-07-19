# Agent運用回帰事例

形式lintとは別に、Agent goalを阻害しない状態遷移を固定する。

```text
目的: Agent状態遷移／承認境界／中断再開の回帰固定
Agent goal:=U明示scopeを必要最小契約で調査→実装→検証→完了
```

## 通常run

```text
事例: 通常
必須: KDSL_PROMPT／K1
禁止: P1L／P1／PF1

開始:
状態: 計画
現在: 初期化
完了: なし
未完: 調査／実装／試験／検証
検証: 未実行
実機: 不要
次: 調査
停止理由: なし

終了:
状態: 完了
現在: 結果確認
完了: 調査／実装／試験／検証
未完: なし
検証: 成功
実機: 不要
次: R1
停止理由: なし
```

## 承認境界

```text
事例: 承認境界
権限: 読取=可／編集=可／試験=可／commit=承認待／push=承認待
境界操作: commit

開始:
状態: 計画
現在: 初期化
完了: なし
未完: 調査／実装／試験／検証／commit／push
検証: 未実行
実機: 不要
次: 調査
停止理由: なし

境界:
状態: 停止
現在: commit直前
完了: 調査／実装／試験／検証
未完: commit／push
検証: 成功
実機: 不要
次: commit承認
停止理由: commit承認待
```

## 中断再開

```text
事例: 中断再開
再開: required

開始:
run: run-agent-proof-1
契約: P1L-agent-proof-1
baseline: main@HEAD
状態: 計画
現在: 初期化
完了: なし
未完: 調査／実装／試験／検証
検証: 未実行
実機: 不要
次: 調査
停止理由: なし

中断:
run: run-agent-proof-1
契約: P1L-agent-proof-1
baseline: main@HEAD
状態: 実行中
現在: 実装完了
完了: 調査／実装
未完: 試験／検証
検証: 一部
実機: 不要
次: 試験
停止理由: session中断

再開:
run: run-agent-proof-1
契約: P1L-agent-proof-1
baseline: main@HEAD
状態: 実行中
現在: 試験
完了: 調査／実装
未完: 試験／検証
検証: 一部
実機: 不要
次: 試験
停止理由: なし

終了:
run: run-agent-proof-1
契約: P1L-agent-proof-1
baseline: main@HEAD
状態: 完了
現在: 結果確認
完了: 調査／実装／試験／検証
未完: なし
検証: 成功
実機: 不要
次: R1
停止理由: なし
```

この事例のpassは状態遷移契約の自動回帰であり、Codex実run確認ではない。
