# R1C Blocked Example

status: review-candidate example
canonical: no

```text
KDSL_RESULT:
SCHEMA:kdsl-r1c@0.1-draft
STATUS:blocked
PHASE:Repository corrective preflight
S:worktreeに未確認差分があり実装を停止
FILES:[]
WHY:指定scope外の追跡済み差分を確認し、既存変更へ上乗せしない停止条件が発火したため
CMD:["git status -sb -uall","git diff --check"]
VERIFY:{"pass":["branch/ref確認","git diff --check"],"fail":[],"not_run":["implementation","build","target runtime"]}
RT:{"state":"p","basis":"実装未実施かつtarget runtime未実行"}
RISK:["runtime_unverified","未確認差分の帰属不明","実装状態未確認"]
NEXT:{"proposal":"未確認差分の帰属と今回scopeへの包含可否をU確認","authority":"proposal_only"}
COMMIT:{"actual":null,"proposed":null,"permission_basis":"none"}
```

Boundary notes:

```text
blocked→変更実施扱い禁止
FILES:[]→変更fileなし
VERIFY.not_run→実装/build/runtime未実行
RT:p→RT:v扱禁止
NEXT→確認提案であり実装許可ではない
COMMIT.actual:null→commit未実行
```
