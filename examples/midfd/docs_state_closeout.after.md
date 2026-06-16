# Example: MidFD docs/state closeout after

status: example
source: templates適用後の代表例
note: このexampleは正本ではない。`templates/base/kdsl_base_dev.md`、`templates/tasks/task_docs_state_closeout.md`、`templates/result/r1_result_spec.md` の利用例。

## After pattern

```text
KDSL_PROMPT:
use:
  base: templates/base/kdsl_base_dev.md
  task: templates/tasks/task_docs_state_closeout.md
  result: templates/result/r1_result_spec.md

Template読込:
  上記3template先読必須
  template_unreadable→停止
  unknown template/alias/preset推測禁止

PHASE: Network path resolution short cache corrective
STATUS_TO_RECORD: Runtime verified; closed
REPO: G:\source\repos\MidFD
BRANCH: main
HEAD_REQUIRED: a402ba5

AUTHORITY:
  read: allow
  edit: target_only
  stage: target_only
  commit: allow_once
  push: forbid
  release: forbid
  public_repo: forbid

TARGET_STATE_DOCS:
  - .codex/state/current_focus.md
  - .codex/state/open_questions.md
  - .codex/state/phase_backlog.md
  - .codex/state/decision_log.md
  - Docs/07_change_log_for_ai.md

RUNTIME_BASIS:
  source: U共有app.log
  RT: v
  valid_basis: U実機runtime log
  invalid_basis:
    - build pass
    - diff pass
    - lint pass
    - unit test pass

OBSERVED:
  - QuickAccess.Open approx 170-215ms
  - BuildItems approx 122-154ms
  - previous 2s delay not reproduced
  - UNC resolvedSync=False / reason=unc-path
  - ERROR/Exception/success=fail not found in shared log

NOT_OBSERVED:
  - cache=hit

UNVERIFIED:
  - cache hitによる改善
  - 操作実行時の実体確認キャッシュ化

MUST_RECORD:
  - QuickAccess表示遅延は改善
  - 前回2秒台遅延は再現せず
  - cache=hitは今回ログでは未観測
  - 改善理由をcache hitと断定しない
  - UNC同期probe回避は resolvedSync=False / reason=unc-path に基づく
  - RT:v根拠はU共有app.logのみ

STOP_EXTRA:
  - HEAD_REQUIRED不一致
  - branch不一致
  - target外変更必要
  - code変更必要
  - cache hit確認済み扱いしないとcloseout不能
  - RT:v解釈不確実
  - rollback/revert/reimplementation必要
  - 方針変更/要件変更が必要

VERIFY_EXTRA:
  - rg -n "Network path resolution short cache corrective|QuickAccess.Open|resolvedSync=False|cache=hit|Runtime verified; closed|runtime verification pending" .codex Docs

COMMIT_MESSAGE: State: close network path resolution short cache corrective
```

## 効果

```text
共通安全契約はbase templateへ移動
R1報告要求はresult templateへ移動
docs/state closeout固有の標準手順はtask templateへ移動
instance側にはPhase固有の観測/未観測/権限/HEADだけが残る
```

## 注意

```text
このafter例はtemplate本文を読める環境向け
AI coding toolがtemplateを読めない場合は停止
use参照だけで作業開始禁止
```
