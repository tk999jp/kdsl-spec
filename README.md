# kdsl-spec

KDSL（漢字圧縮DSL）と最小R1結果仕様の再構築repository。

## 定義

```text
KDSL:=日本語promptを漢字語幹／記号／最小制御語へ再構成する、LLM直投入可能な漢字圧縮DSL
```

第一目的は漢字圧縮。意味保持・判断分岐・明示制約を維持し、英語KEYや非漢字表現は `KDSL-Intl` 派生subsetとして扱う。

```text
KDSL本体:=漢字圧縮
KDSL-Intl:=非漢字言語／ASCII／英語KEY向け互換subset
KDSL本体 > KDSL-Intl
```

## 設計順位

```text
漢字圧縮
> 意味保持
> LLM直投入可能
> 判断分岐保持
> 明示制約保持
> 出力安定
> 人間修正可能
```

安全契機は第一目的ではない。Uが明示した重大条件の意味消失を防ぐ限定保護であり、潜在risk推測による自動増殖を禁止する。

## 正本候補

```text
全体定義: spec/core/kdsl-spec.md
記法: spec/core/kdsl-core.md
mode／安全契機: spec/core/kdsl-modes.md
dev-prompt: spec/profiles/kdsl-profile-dev-prompt.md
converter: spec/profiles/kdsl-converter-prompt.md
CompactPrompt: spec/profiles/kdsl-profile-compact-prompt.md
Intl subset: spec/profiles/kdsl-profile-intl.md
R1: spec/r1/r1-result-spec.md
lint: spec/lint/kdsl-lint-checklist.md
境界: spec/bridge/kdsl-adps-bridge.md
参照地図: spec/manifest.md
用語: spec/glossary.md
```

## 現在状態

```text
branch: audit/kdsl-kanji-completion
status: identity-restoration-audit
base: canonical/kdsl-kanji
historical-base: 39a51b71950340b83f6e525dd1a76724530bb0df
framework-archive: archive/kdsl-framework-20260718
```

`canonical/kdsl-kanji`は漢字identity復元baseline。現v2 framework全資産の機能単位監査・必要機能回収・回帰検証が完了するまで正式canonical扱いしない。

現v2 framework系統は回収元。既存実装量・CI実績・Phase完了記録だけで採用しない。採用条件は、漢字圧縮へ実用上必要／有効であること。

## 運用原則

```text
英語KEY既定禁止
漢字optional化禁止
安全理由のscope／Phase／architecture増殖禁止
KDSL_RESULT成果物化禁止
validator非権威
build／lint／test／CI pass != RT:v
command／path／API名保持
KDSL-DP直接実行禁止
```

## 検証

```bash
python tools/validator/kdsl_identity_lint.py
python tools/validator/run_canonical_samples.py
```

GitHub Actionsの `KDSL Validation` で同じ検証を実行する。
