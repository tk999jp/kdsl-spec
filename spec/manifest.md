# KDSL Spec Manifest — Kanji Core

## 参照順位

```text
1. U明示指示
2. spec/core/kdsl-spec.md
3. spec/core/kdsl-core.md
4. spec/core/kdsl-modes.md
5. profile／R1／lint／bridge正本
6. templates／examples
7. tools／validator
8. docs／review
```

## 正本地図

| Path | 責務 |
|---|---|
| `spec/core/kdsl-spec.md` | KDSL identity／第一目的／全体定義 |
| `spec/core/kdsl-core.md` | 演算子／圧縮文型／保護語／変換禁止 |
| `spec/core/kdsl-modes.md` | 圧縮強度／限定安全 |
| `spec/profiles/kdsl-profile-dev-prompt.md` | 開発prompt |
| `spec/profiles/kdsl-profile-compact-prompt.md` | 一般LLM／Project向け短縮prompt |
| `spec/profiles/kdsl-converter-prompt.md` | 変換契約 |
| `spec/profiles/kdsl-profile-intl.md` | 非漢字派生subset |
| `spec/r1/r1-result-spec.md` | 簡潔結果報告 |
| `spec/lint/kdsl-lint-checklist.md` | identity／圧縮／過剰安全lint |
| `spec/bridge/kdsl-adps-bridge.md` | KDSL-DP／ADPS境界 |
| `spec/glossary.md` | 用語 |

## 所有

```text
漢字identity:=spec/core/kdsl-spec.md
演算子:=spec/core/kdsl-core.md
mode／safety:=spec/core/kdsl-modes.md
CompactPrompt:=spec/profiles/kdsl-profile-compact-prompt.md
Intl境界:=spec/profiles/kdsl-profile-intl.md
R1:=spec/r1/r1-result-spec.md
```

下位fileが上位正本と競合する場合、上位を優先する。

## 非正本

```text
templates
examples
tools／validator
docs／reviews
archive branch
```

validator pass・CI pass・実装量・Phase完了記録を正本化根拠にしない。

## 旧v2資産

```text
Safety Gate Registry／R1C／Packet／Normalization／semantic parser／P1 schema／K1／PF1／Binding Evidence
:= archive/kdsl-framework-20260718の回収候補
:= KDSL本体の正本ではない
```

採否記録は `docs/reviews/kdsl-v2-asset-audit.md` を参照する。

## 変更分類

breaking:

```text
漢字圧縮を第一目的から外す
漢字をoptional化
英語KEYを既定化
KDSL-Intlを本体化
安全契機を主目的化
```

compatible:

```text
圧縮例追加
明示保護語追加
lint追加
```

patch:

```text
説明修正
誤記修正
example追加
```
