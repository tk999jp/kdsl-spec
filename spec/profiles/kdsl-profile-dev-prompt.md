# KDSL Profile: dev-prompt v3.0-kanji-agent

## 目的

ChatGPT／Codex／AI coding tool向け開発promptを、漢字圧縮identityとAgent契約を維持して記述する。

## 既定

```text
format: KDSL
profile: dev-prompt
mode: min
safety: normal
agent: required
language: ja
```

優先:

```text
漢字圧縮 > 要件保持 > Agent完走 > 判断安定 > 明示scope完走 > 誤実装防止 > 必要最小限安全
```

## 基本

```text
共有材→先読
共有材判可→AI丸投禁止
U実機観測／NG指摘／明示要望>AI推測
原因未確→原因範囲外の広域修正禁止
1機能=1Phase
Phase:=U価値として完成する機能単位
```

内部component・test・docs・closeoutだけを独立Phase化しない。

## KDSL_PROMPT

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
```

本文も漢字語幹／記号／最小制御語へ圧縮する。

## Agent契約

`dev-prompt`をCodexへ渡す時、同一prompt内または参照可能な正本に次を含める。

```text
P1L:=実行契約長形式
P1:=P1L可逆短縮
K1:=run状態
PF1:=project既定
```

必須:

```text
P1L／P1／K1
```

条件付き必須:

```text
継続project／project既定あり→PF1
PF1なし→全条件をP1Lへ明示
```

権限rail:

```text
読取／編集／試験／stage／commit／push／release／public履歴／破壊操作
```

権限はU明示指示・Project明示指示・PF1から正規化する。潜在risk推測でrailを追加・強化しない。

## Agent再帰

```text
K1確認
→未完選択
→P1権限照合
→実行
→検証
→K1更新
→完了条件判定
→未完ありなら再帰
```

Agentは明示scope内で次まで完走する。

```text
調査→実装→targeted test→必要broader test→runtime候補提示
```

途中の内部Slice完了、file数、test数、作業量、途中commitを停止理由にしない。

停止は次だけ。

```text
P1L停止条件成立
必要操作権限=承認待／不可
要件両立不能
必要正本なし
baseline破棄必須
明示scope変更必須
```

必要操作が承認待の場合、承認境界直前まで進めてK1を更新する。

## K1完了

```text
状態=完了
→未完=なし
→検証=成功
→実機要否=不要なら実機=不要
→実機要否=要なら実機=確認済
```

build／lint／test／CI passだけで実機確認済へ変更禁止。

## 安全契機

```text
明示criticalのみP1Lへ保持
U未指定gate追加禁止
追加hardening混入禁止
安全理由scope拡張禁止
安全理由Phase細分化禁止
K1更新による未依頼課題追加禁止
```

## D禁止限定

D禁止は、要件変更・方針反転・rollback／revert・未push破棄・public履歴改変・破壊的data変更に限定する。

通常bug修正、既存仕様内補正、targeted test、内部整理、明示scope内完成をD禁止へ自動昇格しない。

## KDSL_RESULT

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

KDSL_RESULTは簡潔な一時報告。P1L／P1／K1／PF1の複製、成果物、引継書、roadmap、新規課題発見装置ではない。

```text
未実行command→実行欄記載禁止
未実行verify→pass扱禁止
build／lint／test／CI pass != RT:v
次:=提案
自動commit許可扱い禁止
```
