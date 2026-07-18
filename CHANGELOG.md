# Changelog

## Unreleased — Kanji Identity Restoration

### Restored

- KDSL第一目的を漢字圧縮へ復元。
- KDSL-Intlを非漢字言語向け派生subsetへ分離。
- dev-prompt／converter／CompactPromptを漢字既定へ統合。
- 安全契機を明示重大条件の限定保護へ縮小。
- KDSL_RESULTを日本語fieldの簡潔一時報告へ復元。

### Added

- `spec/profiles/kdsl-profile-compact-prompt.md`
- `docs/reviews/kdsl-v2-asset-audit.md`
- `tools/validator/kdsl_document_lint.py`
- `tools/validator/r1_result_lint.py`
- `tools/validator/run_canonical_samples.py`
- `.gitignore`

### Reworked

- Core／manifest／glossary／overview／public readiness。
- active task templateを日本語構造KEYへ置換。
- 現役例と歴史例を分離。
- GitHub Actionsをidentity＋sample回帰へ変更。

### Archived

次は正規KDSL本体へ採用せず、`archive/kdsl-framework-20260718`へ保持。

```text
lexicon:kanji-v1／KDSL-CP漢／CP-Lift
Safety Gate Registry／R1C／Packet／Normalization
semantic parser v2／P1 schema／K1／PF1／Binding Evidence
大量closeout／status同期
```

採否詳細: `docs/reviews/kdsl-v2-asset-audit.md`

### Release

```text
stable tag: 未作成
GitHub Release: 未作成
Release Assets: なし
```

release操作は今回scope外。Uの別途明示承認が必要。

## Historical v0.1.0-draft

```text
tag: v0.1.0-draft
tag_target: 89f508c4c8d5ea49a315e60cd3157b089942afee
```

初期draftと以後の旧framework履歴は改変せず保持する。
