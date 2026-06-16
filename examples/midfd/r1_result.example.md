# Example: MidFD R1 result

status: example
source: docs/state closeout template適用時のR1報告例
note: このexampleは正本ではない。R1の検収可能性を示すための例。

## R1 example

```text
KDSL_RESULT:
STATUS: success
PHASE: Network path resolution short cache corrective
S: U共有app.logに基づき、対象PhaseをRuntime verified; closedとしてstate/docsへcloseout。code変更なし。
FILES:
  changed:
    - .codex/state/current_focus.md
    - .codex/state/open_questions.md
    - .codex/state/phase_backlog.md
    - .codex/state/decision_log.md
    - Docs/07_change_log_for_ai.md
  out_of_scope: none
WHY: QuickAccess.Open/BuildItemsの2秒台遅延が再現せず、UNC同期probe回避がresolvedSync=False / reason=unc-pathで確認できたため。ただしcache=hitは未観測のため、cache hit改善とは断定しない。
CMD:
  - git status -sb
  - git log --oneline --decorate -n 8
  - git diff --stat
  - git diff --name-status
  - git diff --check
  - rg -n "Network path resolution short cache corrective|QuickAccess.Open|resolvedSync=False|cache=hit|Runtime verified; closed|runtime verification pending" .codex Docs
VERIFY:
  executed:
    - git diff --check: pass
    - git diff --stat: state/docs only
    - git diff --name-status: target files only
    - rg evidence keywords: pass
  not_run:
    - build
    - unit test
    - local runtime smoke
RT:
  status: v
  basis: U共有app.log
  invalid_basis_not_used:
    - build pass
    - diff pass
    - lint pass
    - unit test pass
RISK:
  - cache=hitは今回ログでは未観測
  - cache hitによる改善は未確認
NEXT: 必要なら別Phaseでcache hit観測条件を追加調査する提案のみ。次task実行許可ではない。
COMMIT:
  actual: <commit hash if executed>
  proposed: State: close network path resolution short cache corrective
  permission_basis: AUTHORITY.commit=allow_once if executed, otherwise proposed only

EVIDENCE:
  OBSERVED:
    - QuickAccess.Open approx 170-215ms
    - BuildItems approx 122-154ms
    - previous 2s delay not reproduced
    - resolvedSync=False / reason=unc-path
    - ERROR/Exception/success=fail not found in shared log
  INFERRED:
    - QuickAccess表示遅延改善はUNC同期probe回避とBuildItems短縮に基づく
  NOT_OBSERVED:
    - cache=hit
  UNVERIFIED:
    - cache hitによる改善
    - 操作実行時の実体確認キャッシュ化

AUTHORITY:
  read: allow
  edit: target_only
  stage: target_only
  commit: allow_once | propose_only
  push: forbid
  release: forbid
```

## 検収観点

```text
RT:vの根拠がU共有app.logになっている
build/diff/lint/test passをRT:v根拠にしていない
cache=hit未観測をNOT_OBSERVEDへ分離している
cache hit改善をUNVERIFIEDへ分離している
NEXTが提案のみになっている
COMMIT actual/proposed/permission_basisが分離されている
AUTHORITYでpush/releaseがforbidになっている
```
