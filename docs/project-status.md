# KDSL Project Status

```text
status: identity-restoration-audit
updated: 2026-07-18
branch: audit/kdsl-kanji-completion
baseline: canonical/kdsl-kanji
historical-base: 39a51b71950340b83f6e525dd1a76724530bb0df
framework-head: 031f11286526e77034da5d803e6b01bf0d61a60a
framework-archive: archive/kdsl-framework-20260718
```

## 目的

```text
漢字圧縮identity復元
現v2資産の機能単位全件監査
必要機能のみ選別回収
仕様／template／validator／実例の回帰整合
```

## 現在判定

```text
漢字identity baseline: 成立
v2全資産監査: 実行中
必要機能回収: 実行中
正規版判定: 未成立
GitHub default branch切替: 禁止／監査完了後
stable tag／release: 対象外／別途U承認必須
```

## 固定原則

```text
KDSL本体:=漢字圧縮
KDSL-Intl:=派生subset
安全契機:=明示重大条件の限定保護
R1:=簡潔一時報告
validator:=非権威
```

## 現v2系統

```text
扱い:=archive／回収元
今後のroadmap正本扱い禁止
既存Phase完了→継続義務扱い禁止
採否:=機能／意味単位
```

Phase 9E PR #145は未mergeで閉鎖。Issue #132／#144も旧roadmapとして閉鎖済み。

## 完成条件

```text
PR #1〜#145資産を機能群単位で採否確定
採用／簡略移植／Intl分離／不採用の未決=0
Core／Profile／Converter／CompactPrompt／R1／Lint／Bridge整合
active templateの英語構造KEY退行=0
漢字圧縮実例／R1実例／Intl実例の回帰成功
identity lint／document lint／R1 lint／sample runner成功
安全契機過剰追加=0
旧frameworkへのactive参照=0
```
