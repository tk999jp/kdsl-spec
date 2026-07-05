# R1 Result Prompt Template v1.1-sync

目的: AI coding tool / Codex への報告要求として再利用できるR1/KDSL_RESULT templateを提供する。

status: template-draft-main-v1.1-sync
source_spec: spec/r1/r1-result-spec.md
source_lint: spec/lint/kdsl-lint-checklist.md

## Required report

最終回答の先頭に `KDSL_RESULT:` blockを必ず出力すること。

```text
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
```

補足は `KDSL_RESULT` 後に置く。

## Required constraints

```text
KDSL_RESULT省略禁止
自然文の結論だけで終了禁止
未実行cmdをCMD記載禁止
未実行verifyをpass扱禁止
build/diff/lint/test passをRT:v扱禁止
RT:v=対象環境runtime確認済のみ
NEXTを次task実行許可扱禁止
COMMITを自動commit許可扱禁止
```

## Recommended evidence block

必要時、特にruntime/観測/未確認が関係する場合は追加する。

```text
EVIDENCE:
  OBSERVED:
  INFERRED:
  NOT_OBSERVED:
  UNVERIFIED:
```

規則:

```text
OBSERVED:=ログ/実機/実行結果/差分などにより観測された事実
INFERRED:=観測から推論したが直接観測ではない内容
NOT_OBSERVED:=確認対象だが観測されなかった内容
UNVERIFIED:=未確認であり、確認済み扱いしてはいけない内容
inferred→observed扱禁止
unverified→RT:v根拠禁止
```

## Recommended authority block

commit/push/releaseや権限が関係する場合は追加する。

```text
AUTHORITY:
  read:
  edit:
  stage:
  commit:
  push:
  release:
```

推奨値:

```text
allow
forbid
target_only
allow_once
propose_only
not_requested
not_applicable
```

## COMMIT field

```text
COMMIT:
  actual: <hash/message | none>
  proposed: <message | none>
  permission_basis: <KDSL_PROMPT authority | U承認 | none>
```

規則:

```text
COMMIT.proposed != commit許可
COMMIT.actual記載時→実際のcommit hash/message必須
commit未実行→actual:none
```

## RT field

```text
RT:
  status: p|u|v|na|fail|blk
  basis: <runtime根拠 | none>
```

禁止:

```text
build成功をRT:v根拠にする
lint passをRT:v根拠にする
diff確認をRT:v根拠にする
unit test passをRT:v根拠にする
```
