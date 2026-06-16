# Example: MidFD docs/state closeout before

status: example
source: MidFD運用で出た長文closeout promptを整理した代表例
note: このexampleは正本ではない。実運用promptの重複・長文化を示すためのbefore例。

## 概要

このbefore例は、`Network path resolution short cache corrective` のcloseoutで、共通安全規則・今回固有観測・停止条件・R1報告要求が1つのKDSL_PROMPT内にフル展開されていた状態を示す。

## Before pattern

```text
KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: lock-critical

Phase: Network path resolution short cache corrective closeout

目的:
Network path resolution short cache corrective を、ユーザー実機ログ確認に基づき Runtime verified; closed として state/docs にcloseoutする。
コード変更は行わない。
QuickAccess表示遅延が改善されたこと、UNC同期probe回避が効いていること、cache=hit は未観測だが resolvedSync=False / reason=unc-path により目的達成したことを、過大記録せず正確に残す。

前提:
- 対象repoは G:\source\repos\MidFD
- dev正本は private tk999jp/MidFD-dev
- 現HEAD想定は a402ba5
- a402ba5 は origin/main へpush済み
- 本closeoutは docs/state only
- コード変更禁止
- ユーザー共有 app.log により実機Runtime確認済み
- QuickAccess.Open は概ね約170〜215ms
- BuildItems は概ね約122〜154ms
- 前回の2秒台遅延は再現していない
- cache=hit は今回ログでは未観測
- UNC系は resolvedSync=False / reason=unc-path により同期probe回避を確認
- ERROR / Exception / success=fail は今回ログ上では見当たらない
- RT:v は今回のユーザー実機ログ確認に基づくものとしてのみ記録する
- build pass / diff pass / lint pass / unit test pass を RT:v の理由にしない
- NEXT は提案であり、次タスク実行許可ではない
- COMMIT は推奨メッセージであり、自動commit許可ではない

対象Slice:
- .codex/state/current_focus.md
- .codex/state/open_questions.md
- .codex/state/phase_backlog.md
- .codex/state/decision_log.md
- Docs/07_change_log_for_ai.md

非対象:
- code変更
- QuickAccess追加改修
- cache仕様変更
- diagnosticsログ仕様変更
- build再実行必須化
- public repo操作
- Release作業
- rollback / revert
- data schema変更
- public API変更
- 保存形式変更

禁止:
- コード変更禁止
- Services/ / Dialogs/ / MainForm.cs 変更禁止
- QuickAccess挙動変更禁止
- cache hitを確認済み扱い禁止
- cache hitによる改善と断定禁止
- 未確認項目をRuntime verified扱い禁止
- build成功をRT:v理由にすること禁止
- git add . 禁止
- public repo操作禁止
- 公開済tag移動禁止
- Release Assets上書き前提操作禁止

停止条件:
- git status -sb でコード差分が存在する
- HEADが a402ba5 でない
- origin/main とHEADが一致していない
- state/docs以外を変更する必要が出た
- cache hit確認済みのように記録しないとcloseoutできない
- Runtimeログの解釈に不確実性があり、RT:v と記録できない
- rollback / revert / 再実装が必要になる
- ユーザー承認が必要な方針変更を含む

作業手順:
1. git status -sb / git log / git diff確認
2. 対象state/docs確認
3. closeout内容を反映
4. 必須記録要素を入れる
5. git diff --check / git diff --stat / rg確認
6. 必要なら対象ファイルのみstageしcommit

報告形式:
KDSL_RESULT:
STATUS:
PHASE:
S:
FILES:
WHY:
CMD:
VERIFY:
RT:
RISK:
NEXT:
COMMIT:

報告禁止:
- KDSL_RESULT省略禁止
- 未実行cmdをCMD記載禁止
- 未実行verifyをpass扱禁止
- build/diff/lint/test passをRT:v扱禁止
- cache hit未観測をcache hit確認済みにしないこと
- NEXTを次task実行許可扱禁止
- COMMITを自動commit許可扱禁止
```

## 問題点

```text
共通安全規則が毎回フル展開される
今回固有の観測値が共通規則に埋もれる
commit候補とcommit許可が混ざりやすい
R1報告要求が毎回重複する
template化してよい共通部分が多い
```
