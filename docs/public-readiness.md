# Public Readiness

```text
repository: public
仕様状態: canonical
stable release: none
Release Assets: none
```

repositoryはpublic。漢字identity監査、正本内容の`main`反映、default branch切替、main branch rules設定を完了した。

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
正本内容main反映
GitHub default branch: main
main branch rules設定
```

## Repository系統

```text
正本: main
旧framework保存: archive/kdsl-framework-20260718
旧正本名canonical/kdsl-kanji: 削除対象
```

## Release

stable tag／GitHub Release／Release Assetsは今回scope外。作成にはUの別途明示承認が必要。

```text
public repository != stable specification
CI pass != release readiness
```
