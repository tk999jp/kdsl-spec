# KDSL Specification — 漢字圧縮Core再構築候補

## 定義

```text
KDSL:=日本語promptを漢字語幹／記号／最小制御語へ再構成するLLM直投入可能な漢字圧縮DSL
自然文=>助詞削減＋重複統合＋漢字語幹化＋条件／遷移記号化＋最小制御語化
```

第一目的は**漢字圧縮**。英語KEY化、汎用安全framework化、schema化、証跡管理を目的としない。

```text
第一目的:=漢字圧縮
成立条件:=意味保持／判断分岐保持／明示制約保持／LLM直投入／人間修正可能
最適化:=成立条件内で圧縮を高める
```

「第一目的」は成立条件を破ってよいという意味ではない。

## 本体と派生

```text
KDSL本体:=日本語漢字圧縮
KDSL-Intl:=非漢字言語／ASCII／英語KEYが必要な環境への派生subset
KDSL本体 > KDSL-Intl
```

英語KEY既定化／漢字optional化／Intl本体化は禁止。

## 最小構成

```text
format: KDSL
profile: dev-prompt
mode: min
safety: normal
language: ja
```

既定値を共有済みならheader省略可。ただしAI coding promptは先頭`KDSL_PROMPT:`を保持。

## 圧縮処理

```text
目的抽出
→重複／同義統合
→助詞削減
→漢字語幹化
→条件／遷移記号化
→必要時に正本値／同一意味参照化
→明示制約照合
```

KEY翻訳だけで完了禁止。短名は意味明確な日本語を優先し、未定義の一字aliasは禁止。長いhash／path／固定条件の反復は1回定義後に参照。ただし**定義箇所の技術識別子は保持**する。

```text
自然文: 共有された材料だけで判断できる場合はAI coding toolへ調査を丸投げしない
KDSL: 共有材判可→AI丸投禁止

自然文: 移動に成功したリンクだけを削除し、失敗したリンクは残す
KDSL: 移動成功link→src削除／失敗link→src保持
```

## 限定保護

入力で明示された禁止／未確認／未実行／承認待／rollback／revert／data破壊防止／public履歴保護／RT:v条件は削除・反転・弱化禁止。

```text
安全契機:=明示重大条件の意味保持
潜在risk推測→承認gate／停止条件／scope／Phase／architecture追加禁止
通常bug修正→high-risk自動昇格禁止
```

重大かつ即時影響のある追加riskはKDSL本文外に短く指摘し、入力契約へ混入しない。

## 変換禁止

```text
command／path／URL／repo／branch／tag／package／class／method／property／API／file名／拡張子／Windows path／inline code
```

code block原則保持。Uがblock全体を変換指定した場合のみ日本語制御文の変換可。command／path／code／API名は常に保持。

## 外部層との関係

```text
KDSL:=漢字圧縮prompt
KDSL-DP:=ADPS向けAuthoring形式
R1／KDSL_RESULT:=結果の簡潔報告
Agent実行管理!=KDSL本体
```

KDSL-DP直接実行禁止。KDSL-DP利用時はP1／P1L正規化必須。形式がvalidでも実行許可とは限らない。詳細は`spec/bridge/kdsl-adps-bridge.md`。
