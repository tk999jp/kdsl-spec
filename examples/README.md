# Examples

KDSL / R1 の変換例・運用例置き場。

## 現在の例

```text
examples/
  midfd/
    docs_state_closeout.before.md
    docs_state_closeout.after.md
    r1_result.example.md
```

## MidFD docs/state closeout example

目的:

```text
長文のKDSL_PROMPT beforeを、template適用後のafterへ整理し、R1結果例で検収可能性を示す。
```

ファイル:

```text
docs_state_closeout.before.md:
  共通安全規則・今回固有観測・停止条件・R1報告要求がフル展開された長文例

docs_state_closeout.after.md:
  templates/base + templates/tasks + templates/result を使い、instance固有情報だけに圧縮した例

r1_result.example.md:
  OBSERVED / INFERRED / NOT_OBSERVED / UNVERIFIED と AUTHORITY を分離したKDSL_RESULT例
```

## 扱い

```text
examplesは正本ではない
Core/R1/Lintの理解補助
実運用で有効だったprompt/結果を匿名化または整理して保存
exampleを実運用promptとして使う場合はKDSL_PROMPTへ正規化必須
example内の値を現行repo状態として扱うこと禁止
```
