# KDSL Overview

```text
状態:=漢字identity復元監査
KDSL:=日本語prompt向け漢字圧縮DSL
R1:=短い作業結果報告
```

## 目的

KDSLは、自然文promptを次へ再構成する。

```text
自然文
=> 助詞削減
 + 重複統合
 + 漢字語幹化
 + 条件／遷移記号化
 + 最小制御語化
```

第一目的は漢字圧縮。安全契機は、入力で明示された禁止・未確認・rollback等を圧縮時に落とさないための限定保護である。

## 構成

```text
Core:=identity／記法／mode
Profile:=dev-prompt／compact-prompt／converter／Intl
R1:=簡潔KDSL_RESULT
Lint:=漢字退行／意味欠落／過剰安全検出
Bridge:=KDSL-DP／P1境界
Template／Example:=非正本の実用部品
```

## 非漢字言語

```text
KDSL本体:=漢字圧縮
KDSL-Intl:=非漢字言語向け派生subset
```

英語KEYは無指定の既定にしない。

## 安全契機

保持:

```text
明示禁止
明示未確認／未実行
明示承認待
明示rollback／revert
明示data／public保護
明示RT:v
```

追加禁止:

```text
潜在risk推測
未指定承認gate
安全理由scope／Phase／architecture拡張
未依頼hardening
```

## R1

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

R1は成果物ではなく一時報告。build／test／CI passはRT:vではない。

## 現在の検証

```bash
python tools/validator/kdsl_identity_lint.py
python tools/validator/run_canonical_samples.py
```

validatorは補助であり、意味同等・U承認・runtime・release readinessを証明しない。

## 旧v2系統

Safety Gate Registry、R1C、Packet、Normalization、semantic parser、P1 schema、K1／PF1、Binding Evidenceは `archive/kdsl-framework-20260718` の回収候補。KDSL本体の正本ではない。

採否詳細は `docs/reviews/kdsl-v2-asset-audit.md` を参照する。
