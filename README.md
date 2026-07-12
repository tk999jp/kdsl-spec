# KDSL / R1 Specification

KDSLとR1を管理する、**public experimental preview** repositoryです。

- **KDSL**: 禁止・承認・未確認・停止条件などを保持する、LLM向け半構造化prompt記法
- **R1 / KDSL_RESULT**: AI支援作業の実行結果・検証・Runtime・権限状態を分離する結果証跡仕様

> このrepositoryはstable standardではありません。Validatorはヒューリスティックなlint補助であり、意味等価性・安全性・承認・Runtime確認・release readinessを証明しません。

## Current status

```text
repository: tk999jp/kdsl-spec
branch: main
visibility: public
published_release: v1.1.0-rc1
release_class: experimental preview / prerelease
public_ready: no
stable_release: none
Release Assets: none
license: MIT
validator: partial / non-authoritative
unified expectations: 257 / failed 0
required KDSL Validation check: pending / issue #39
```

運用状態の正本は [`docs/project-status.md`](docs/project-status.md)、仕様参照関係の正本は [`spec/manifest.md`](spec/manifest.md) です。

## Start here

1. [`docs/overview.md`](docs/overview.md) — KDSL/R1の目的と全体像
2. [`docs/r1-quickstart.md`](docs/r1-quickstart.md) — KDSL_RESULTの最小利用方法
3. [`spec/core/kdsl-spec.md`](spec/core/kdsl-spec.md) — KDSL Core入口
4. [`spec/r1/r1-result-spec.md`](spec/r1/r1-result-spec.md) — R1正本
5. [`examples/public/README.md`](examples/public/README.md) — 外部向け非規範例

## Why KDSL?

長いpromptは、短縮や再編集の過程で次の境界が落ちやすくなります。

```text
禁止事項
承認 / 承認待
未確認 / 未実行
rollback / revert
実機確認分離
public履歴 / 公開済tag / Release Assets保護
正本 / data保護
停止条件
```

KDSLは、単なるtoken削減ではなく、これらを保持したままpromptを短く・構造的にすることを目的とします。

```text
意味保持 > safety gate保持 > 判断分岐保持 > 誤実装防止 > 文字数削減
```

## KDSL axes

```text
format: KDSL
profile: compact-prompt|dev-prompt|converter|lint
mode: readable|min|dense|lock
safety: normal|lock-critical|lock-all
lexicon: standard|kanji-v1
envelope: plain|packet-draft|result
```

Named compositions:

```text
KDSL-CP:=profile:compact-prompt
KDSL-CP漢:=profile:compact-prompt + mode:dense + lexicon:kanji-v1
KDSL-R1:=envelope:result / KDSL_RESULT
KDSL-Packet:=v2-draft authoring envelope / non-executable
```

`rulebook`はv1.1 legacy profile名です。新規使用は禁止され、用途確認なしに他profileへ自動補正しません。

## CompactPrompt and CP-Lift

KDSL-CPは一般LLM、Project files、単体instruction向けです。

Required blocks:

```text
Goal / Input / Output / Guard / Check
```

次を含む場合は `profile:dev-prompt` へCP-Liftします。

```text
実装 / 改修 / 削除
repo / path / branch / commit操作
file / API / command変更
rollback / revert
Runtime / RT:v
public履歴 / tag / Release Assets
data migration / 正本変更
AI coding toolへの投入
```

## KDSL-DP and Packet boundaries

```text
KDSL-DP直接実行禁止
KDSL-DP→P1/P1L正規化必須
KDSL-Packet:=non-executable
packet-draft直接実行禁止
PKT:v1使用禁止
normalization未完了→実行禁止
```

Registry・lint・validator・property checkの成功は、実行権限ではありません。

## Why R1?

AI coding toolの報告では、実行・検証・推論・Runtime・権限が混同されやすくなります。R1はこれらを分離し、人間が検収できる形にします。

Canonical KDSL_RESULT fields:

```text
KDSL_RESULT:
STATUS:
PHASE:
S:
FILES:
WHY:
CMD:
VERIFY:
RT:
RISK:
NEXT:
COMMIT:
```

Critical boundaries:

```text
未実行cmd→CMD記載禁止
未実行verify→pass扱禁止
build/diff/lint/test/CI pass != RT:v
RT:v:=対象環境runtime確認済のみ
NEXT:=提案, 実行許可扱禁止
COMMIT:=実行済commitまたは推奨message, 自動commit許可扱禁止
```

R1の最小利用例は [`docs/r1-quickstart.md`](docs/r1-quickstart.md) を参照してください。

## Repository map

| Path | Responsibility | Authority |
|---|---|---|
| `docs/project-status.md` | repository現在状態 | Operational status canonical |
| `spec/manifest.md` | file責務・正本参照関係 | Canonical map |
| `spec/core/` | KDSL記法・保護語・mode/safety | Canonical |
| `spec/profiles/` | 用途別profile | Profile canonical / v2 draft |
| `spec/r1/` | KDSL_RESULT / Evidence / RT / Authority | Canonical R1 + subordinate drafts |
| `spec/lint/` | 保持・弱化・欠落検査 | Canonical / adopted draft |
| `spec/bridge/` | KDSL-DP / ADPS / CP-Lift / Packet境界 | Canonical / draft |
| `spec/registry/` | Safety Gate / Packet ID・state | v2 draft |
| `examples/` | 理解補助 | Non-normative |
| `tools/validator/` | 実験的lint helper | Non-authoritative |
| `docs/reviews/` | 設計・統合記録 | Non-canonical |

## Validation

Unified sample suite:

```text
python tools/validator/run_all_samples.py
```

Focused wrapper examples:

```text
python tools/validator/kdsl_validate.py --target compact <file>
python tools/validator/kdsl_validate.py --target r1 <file>
python tools/validator/kdsl_validate.py --target r1c <file>
python tools/validator/kdsl_validate.py --target packet <file>
python tools/validator/kdsl_validate.py --target packet-semantic <file>
python tools/validator/kdsl_validate.py --target normalization <file>
```

Validator boundaries:

```text
validator pass != semantic equivalence
validator pass != complete safety proof
validator pass != U承認
validator pass != RT:v
validator pass != release readiness
```

## Public examples

External-facing examples are under [`examples/public/`](examples/public/README.md).

```text
examples/public/r1_result_valid.example.md
examples/public/r1_result_authority_guard.example.md
```

Examples are not Core specification and do not grant execution, commit, push, release, or Runtime authority.

## Release policy

```text
v0.1.0-draft tag:=履歴として維持
v1.1.0-rc1:=experimental historical baseline
v1.1.0 stable:=保留
既存tag移動禁止
Release Assets操作禁止
stable/public-ready化→別途U明示承認必須
```

## License

MIT License. See [`LICENSE`](LICENSE).
