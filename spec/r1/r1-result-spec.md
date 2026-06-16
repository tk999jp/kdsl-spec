# R1 Result Specification v0.1-draft

目的: AI coding tool / Codex の作業結果を、人間と統括LLMが検収可能な証跡として返すための結果仕様を定義する。

位置づけ:

```text
R1:=Evidence / 結果証跡
KDSL_RESULT:=R1系の人間/AI向け結果block
```

## 1. 基本契約

AI coding tool / Codex の最終回答は、必要時に先頭へ `KDSL_RESULT:` blockを出力する。

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

補足自然文は `KDSL_RESULT` の後に置く。

禁止:

```text
KDSL_RESULT省略禁止
自然文の結論だけで終了禁止
未実行cmdをCMD記載禁止
未実行verifyをpass扱禁止
build/diff/lint/test passをRT:v扱禁止
NEXTを次task実行許可扱禁止
COMMITを自動commit許可扱禁止
```

## 2. STATUS

```text
success: 指示範囲内で完了
partial: 一部完了/一部未完了
blocked: 停止条件/承認待/前提不一致で停止
noop: 変更不要/実施対象なし
failed: 実行失敗
needs_user: ユーザー確認/承認が必要
```

## 3. RT

Runtime verification status.

```text
p=runtime確認未完了
u=U実機確認待ち
v=対象環境runtime確認済
na=runtime対象なし
fail=runtime確認失敗
blk=runtime確認不能
```

制約:

```text
RT:v=対象環境runtime確認済のみ
build pass != RT:v
diff pass != RT:v
lint pass != RT:v
test pass != RT:v
U実機観測に基づくRT:vは根拠を明記
Runtime未確認→RT:u|RT:p + RISK:runtime_unverified
docs/guidance only→理由明記でRT:na可
```

## 4. CMD / VERIFY

CMD:

```text
実行したcommandのみ記載
未実行cmd記載禁止
推奨cmd/次候補cmdはCMDへ混入禁止
```

VERIFY:

```text
実行した検証のみ記載
未実行verifyをpass扱禁止
未実行verifyはnot_runとして記録可
```

## 5. FILES / WHY

FILES:

```text
変更ファイルのみ記録
閲覧のみのファイルは必要時にinspectedとして分離
対象外変更が出た場合はRISK/STOPへ記録
```

WHY:

```text
変更理由を記録
推測と観測を混同禁止
未確認要因を断定禁止
```

## 6. NEXT / COMMIT

NEXT:

```text
NEXT:=提案
NEXTを次task実行許可扱禁止
NEXTに実行許可が必要な作業を含む場合は承認待を明記
```

COMMIT:

```text
COMMIT:=実行済commitまたは推奨message
COMMITを自動commit許可扱禁止
commit実行済ならcommit hash/messageを明記
commit未実行ならproposed messageとして明記
```

## 7. Evidence separation

R1では、観測・推論・未観測・未確認を分離する。

推奨構造:

```text
EVIDENCE:
OBSERVED:
INFERRED:
NOT_OBSERVED:
UNVERIFIED:
```

規則:

```text
observed=false→confirmed扱禁止
not_observed→確認済扱禁止
unverified→RT:v根拠禁止
inferred→observed扱禁止
```

## 8. Authority separation

R1は権限状態を混同しない。

```text
commit候補 != commit許可
push候補 != push許可
NEXT != 実行許可
report != approval
```

推奨追加block:

```text
AUTHORITY:
read:
edit:
stage:
commit:
push:
release:
```

## 9. R1 lint minimum

```text
KDSL_RESULT先頭固定
STATUS/PHASE/S/FILES/WHY/CMD/VERIFY/RT/RISK/NEXT/COMMIT保持
未実行cmd→CMD記載禁止保持
未実行verify→pass扱禁止保持
RT:v条件保持
build/diff/lint/test pass != RT:v保持
NEXT:=提案保持
COMMIT:=推奨message/実行済commit保持
NEXT実行許可扱禁止保持
COMMIT自動commit許可扱禁止保持
観測/推論/未観測/未確認分離
```
