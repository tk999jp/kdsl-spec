# KDSL Base Dev Prompt Template v3.0-kanji-agent

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
権限: P1L参照
承認境界:
対象:
非対象:
作業:
試験:
検証:
停止条件:
報告: R1

P1L:
版: kdsl-agent@1
実行方式: agent再帰
目的:
成功条件:
正本:
対象:
非対象:
権限:
  読取: {{可|不可|承認待|対象外}}
  編集: {{可|不可|承認待|対象外}}
  試験: {{可|不可|承認待|対象外}}
  stage: {{可|不可|承認待|対象外}}
  commit: {{可|不可|承認待|対象外}}
  push: {{可|不可|承認待|対象外}}
  release: {{可|不可|承認待|対象外}}
  public履歴: {{可|不可|承認待|対象外}}
  破壊操作: {{可|不可|承認待|対象外}}
承認境界:
作業:
試験:
検証:
実機要否: {{要|不要}}
停止条件:
完了条件:
報告: R1

P1|版:kdsl-agent@1|実行方式:agent再帰|目的:{{目的}}|成功条件:{{成功条件}}|正本:{{正本}}|対象:{{対象}}|非対象:{{非対象}}|権限:読取={{値}},編集={{値}},試験={{値}},stage={{値}},commit={{値}},push={{値}},release={{値}},public履歴={{値}},破壊操作={{値}}|承認境界:{{境界}}|作業:{{作業}}|試験:{{試験}}|検証:{{検証}}|実機要否:{{要否}}|停止条件:{{停止条件}}|完了条件:{{完了条件}}|報告:R1

K1:
状態: 計画
現在: 初期化
完了: なし
未完: {{作業一覧}}
検証: 未実行
実機: {{不要|未確認}}
次遷移: 調査
停止理由: なし

PF1:
project: {{project}}
正本: {{正本}}
既定profile: dev-prompt
既定mode: min
Phase方針: 1機能=1Phase／明示scope完走
権限既定:
  読取: {{値}}
  編集: {{値}}
  試験: {{値}}
  stage: {{値}}
  commit: {{値}}
  push: {{値}}
  release: {{値}}
  public履歴: {{値}}
  破壊操作: {{値}}
承認必須: {{操作}}
試験方針: targeted test→必要broader test
実機方針: U実機観測のみRT:v
報告方針: 最小R1／scope外課題追加禁止
```

基本:

```text
漢字圧縮>要件保持>Agent完走>明示scope完走>必要最小限安全
共有材判可→AI丸投禁止
U観測>AI推測
1機能=1Phase
内部Slice完了→停止理由禁止
```

Agent:

```text
K1確認→未完選択→P1権限照合→実行→検証→K1更新→未完ありなら再帰
K1更新→目的／対象／権限変更禁止
PF1→P1L権限拡張禁止
必要操作=承認待→境界直前まで実行
```

安全:

```text
明示criticalのみP1Lへ保持
U未指定gate追加禁止
安全理由scope／Phase／architecture拡張禁止
追加hardening混入禁止
```

報告:

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
