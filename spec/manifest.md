# KDSL 正本地図 — 再構築候補

## 参照順位

```text
1. U明示指示
2. 本manifestが指すCore
3. 用途別profile
4. R1／bridge／lint
5. examples／tools／旧資料
```

| 責務 | 正本候補 |
|---|---|
| identity／成立条件 | `spec/core/kdsl-spec.md` |
| 演算子／基本文型／保護対象 | `spec/core/kdsl-core.md` |
| 圧縮mode | `spec/core/kdsl-modes.md` |
| 一般変換 | `spec/profiles/kdsl-converter-prompt.md` |
| 開発指示 | `spec/profiles/kdsl-profile-dev-prompt.md` |
| 簡潔結果 | `spec/r1/r1-result-spec.md` |
| 外部契約との境界 | `spec/bridge/kdsl-adps-bridge.md` |
| 人手lint | `spec/lint/kdsl-lint-checklist.md` |

```text
KDSL Core > profiles > R1／bridge > lint > examples／validator
```

同名の旧資料・履歴・テスト実装がCoreの意味を上書きしない。Agent管理は圧縮言語とは別責務。validator passは正本性／意味同等／実行権限／RT:vを証明しない。
