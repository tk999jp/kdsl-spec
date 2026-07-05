# Validator MVP Design v1.1-sync

status: mvp-design-draft-main-v1.1-sync
implementation: not_started

## 1. Purpose

KDSL/R1 validatorのMVP範囲を定義する。

MVPは、完全な自然言語理解ではなく、Markdown/text内のblock・必須語・権限衝突を軽量検査する。

## 2. MVP priority

優先:

```text
R1 validator > template lint > KDSL core syntax lint
```

理由:

```text
R1は検収票として構造が明確
KDSL本文は半構造化で自然言語要素が多い
最初からparserを厳密化しすぎると運用を壊す
```

## 3. MVP targets

### Target A: R1 required block check

検査:

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

結果:

```text
missing block -> ERROR
```

### Target B: RT:v invalid basis keyword check

検査対象:

```text
RT: v
RT:v
status: v
```

同時に以下がbasis扱いされていないか確認:

```text
build pass
build成功
diff確認
diff pass
lint pass
unit test pass
静的確認
推測
validator pass
```

結果:

```text
RT:v + invalid basis only -> ERROR
RT:v + basis missing -> ERROR
```

### Target C: NEXT / COMMIT confusion check

検査:

```text
NEXT内に実行許可表現がある
COMMIT.proposedのみなのにactual扱い
COMMIT actualありだがhash/messageなし
```

結果:

```text
permission confusion -> ERROR/WARN
```

### Target D: AUTHORITY conflict check

検査:

```text
AUTHORITY.commit=propose_only + COMMIT.actualあり
AUTHORITY.commit=forbid + COMMIT.actualあり
AUTHORITY.push=forbid + push/update_ref記録あり
AUTHORITY.release=forbid + release/tag/assets記録あり
```

結果:

```text
authority conflict -> ERROR
```

### Target E: template reference check

検査:

```text
use: templates/... がある
参照templateが存在する
Template読込 / template_unreadable→停止 がある
unknown template/alias/preset推測禁止 がある
```

結果:

```text
missing template -> ERROR
missing unreadable-stop -> ERROR
missing unknown-template guard -> WARN/ERROR
```

## 4. MVP input/output

Input:

```text
file path or stdin text
mode: r1|template|auto
```

Output:

```text
VALIDATION_RESULT:
STATUS: pass|warn|fail
ERRORS:
WARNINGS:
INFO:
```

Exit codes:

```text
0=pass
1=warn
2=fail
3=tool_error
```

## 5. Non-goals for MVP

```text
自然言語完全解析
KDSL完全parser
template完全展開
実行済cmdの真偽確認
Runtime確認代行
U承認代行
D禁止解除
```

## 6. Implementation constraints

```text
Python標準ライブラリ中心
依存追加は最小限
Markdown parser必須化しない
正規表現+簡易block抽出から開始
validator pass != RT:v
validator pass != U承認
validator pass != 要件妥当性
```

## 7. Suggested file layout if implemented

```text
tools/validator/
  kdsl_validator.py
  tests/
    sample_r1_ok.md
    sample_r1_missing_block.md
    sample_r1_bad_rt.md
    sample_template_missing_guard.md
```

## 8. Stop conditions before implementation

```text
検査項目がD禁止解除に見える
validator passを承認扱いする文面が入る
RT:v代替に見える
公開release前提になる
外部依存が増えすぎる
```

## 9. Recommended next implementation phase

```text
Phase: validator-mvp-r1-only
scope:
  - KDSL_RESULT required block check
  - RT:v invalid basis check
  - NEXT/COMMIT basic confusion check
non_scope:
  - template expansion
  - GitHub Actions
  - public release
```
