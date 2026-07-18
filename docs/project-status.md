# KDSL Project Status

```text
status: canonical
updated: 2026-07-18
branch: canonical/kdsl-kanji
historical-base: 39a51b71950340b83f6e525dd1a76724530bb0df
framework-head: 031f11286526e77034da5d803e6b01bf0d61a60a
framework-archive: archive/kdsl-framework-20260718
```

## 完了

```text
漢字圧縮identity復元: 完了
PR #1〜#145機能群監査: 完了
旧Core以降309-path監査: 完了
必要機能選別回収: 完了
Core／Profile／Template／R1／Lint／Bridge整合: 完了
validator compile: pass
identity lint: pass
canonical regression: pass
```

## 正本

```text
KDSL本体:=漢字圧縮
KDSL-Intl:=派生subset
安全契機:=明示重大条件の限定保護
R1:=簡潔一時報告
validator:=非権威
```

## 回収

```text
CompactPrompt用途profile
漢字document lint
日本語R1 lint
valid／invalid回帰corpus
GitHub Actions
.gitignore
```

## 不採用

```text
漢字optional lexicon／英語KEY既定／旧CompactPrompt漢字別名
Safety Gate Registry／R1C／Packet／Normalization
semantic parser v2／P1 schema／K1／PF1／Binding Evidence
closeout／status同期の自己増殖
```

詳細: `docs/reviews/kdsl-v2-asset-audit.md`

## 旧系統

```text
main:=frozen legacy framework
archive/kdsl-framework-20260718:=回収元保存
旧roadmap:=停止
```

Phase 9E PR #145は未mergeで閉鎖。Issue #132／#144も旧roadmapとして閉鎖済み。

## Repository管理

```text
GitHub default branch: mainのまま／UI切替待ち
正規default候補: canonical/kdsl-kanji
canonical branch rules: UI確認／設定待ち
stable tag／release: 対象外／別途U承認必須
```

仕様再構築は完了。残るのはGitHub管理画面上のdefault branch切替とbranch rules設定のみ。
