# Public Readiness

```text
repository: public
仕様状態: identity-restoration-audit
stable release: none
Release Assets: none
```

repositoryは既にpublicだが、`canonical/kdsl-kanji`を正式default branchへ切り替える前に、漢字identity監査とbranch rules設定を完了する。

## 公開上の説明

```text
KDSL:=日本語promptを漢字語幹／記号／最小制御語へ再構成する漢字圧縮DSL
KDSL-Intl:=非漢字言語向け派生subset
R1:=短い結果報告
```

旧説明の「安全gate保持型Human-AI work contract framework」をKDSL本体の定義として使用しない。

## 完了済み

```text
LICENSEあり
漢字Core再構築
CompactPrompt／Intl profile
日本語R1
軽量validator／sample runner
v2資産監査
旧framework archive
```

## 正本切替前に必要

```text
監査branch CI成功
canonical/kdsl-kanjiへ監査結果merge
GitHub default branch切替
canonical branch rules設定
main旧系統の凍結表示維持
```

## Release

stable tag／GitHub Release／Release Assetsは今回scope外。作成にはUの別途明示承認が必要。

```text
public repository != stable specification
CI pass != release readiness
```
