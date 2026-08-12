# KDSL Eval Pilot 01

```text
状態:=closeout
確認日:=2026-08-13
対象:=Python抽象背景動画Generator
方式:=one-shot比較
Core変更:=なし
一般化:=未実施
```

## 目的

KDSLの第一目的である漢字圧縮について、自然文より短いTask表現でも完成品質を維持できるかを、創造判断を含むAI coding Taskで初期確認する。

本Pilotは統計的benchmarkではない。1 Task・各条件1 runの方向性確認であり、全model／全Agent／全repositoryへの一般保証を目的としない。

## Task

Pythonで背景動画素材Generatorを作成。

必須:

```text
Effect:=matrix/noise/lineart
入力:=CLI/JSON config
出力:=MP4/Preview PNG
共通parameter:=width/height/fps/duration/seed/speed/palette/output
matrix:=density/font_size/fall_speed/trail/glow
noise:=scale/contrast/drift/octaves
lineart:=line_count/thickness/motion/curve/spacing
基準:=1920x1080/30fps/10秒/seed指定可
品質:=3 Effect視覚差/parameter実効/README/Windows Python利用
```

architecture／library／preset詳細／visual designは実装側判断とした。

## 条件

```text
A:=単体LLM＋自然文
B:=単体LLM＋KDSL
C:=Codex orchestration構成＋自然文
D:=Codex orchestration構成＋KDSL
```

C/Dは同一`AGENTS.md`＋同一custom agent定義を配置。Task固有差は自然文／KDSL表現のみ。

`Codex orchestration構成`は、orchestrator／custom-agent利用可能環境を意味する。実行transcriptを保存していないため、各custom agentの実spawn回数・担当実行は未証明。

## One-shot条件

```text
U初回指示:=1回
追加補足:=なし
追加訂正:=なし
各case結果の相互参照:=なし
```

CaseDに残存した`prompt2.txt`はTask投入に使用していないため、追加指示とは扱わない。

## Task prompt量

空白／tokenizer共通尺度ではなく、保存promptの文字数による簡易比較。

```text
A自然文:=1517 chars
B KDSL:=874 chars
削減:=42.4%

C自然文:=1517 chars
D KDSL:=908 chars
削減:=40.1%
```

この値はTask固有promptのみ。C/Dの常設`AGENTS.md`／agent定義量を含まない。

## 実行確認

同一短時間条件で全caseの3 Effectを再生成。

```text
probe:=640x360/12fps/1.5秒/seed=42
対象動画:=4 case × 3 Effect = 12
結果:=全12動画生成成功
形式:=H.264/yuv420p/18 frames
```

各case付属test:

```text
A:=6/6 pass
B:=2/2 pass
C:=5/5 pass
D:=5/5 pass
```

上記passは当該成果物・当該環境の確認。Windows実機一般性、任意dependency version、将来modelでの再現を保証しない。

## 観測

### KDSL

```text
B/A:
Task prompt約42%短縮
必須機能欠落なし
3 Effect/CLI/JSON/MP4/PNG/seed/parameter/README成立
完成品質:=非劣性の初期観測

D/C:
Task prompt約40%短縮
必須機能欠落なし
映像成立度／構成は今回Dが良好
```

約40%短縮はKDSLの一般圧縮率ではなく、このTask pairの実測。

### Visual

4 caseすべて背景動画Generatorとして成立。Matrix／Noise／Line Artの見た目には明確な差が生じた。

今回の目視ではA/B/DがCより映像表現上まとまりやすかったが、Visual評価には主観が含まれるため、KDSL一般優位の証拠として扱わない。

### Agent構成

今回のTaskでは、Codex orchestration構成が単体条件を明確に上回る結果は観測されなかった。

```text
Agent優位:=未証明
Agent劣位:=一般化禁止
```

Task規模、分割適性、orchestration overhead、visual coherence等が影響し得る。追試なしで原因を確定しない。

## 結論

このPilotで支持された限定結論:

```text
1. KDSL Task prompt→自然文比約40%短縮
2. 今回Task→KDSLで必須機能欠落なし
3. 単体条件→KDSL完成品質の非劣性を初期観測
4. Codex構成→自然文よりKDSL側が今回良好
5. Agent追加自体の品質優位→未証明
```

未証明:

```text
統計的有意差
全Task一般性
全model一般性
全Agent一般性
KDSL絶対優位
Agent実spawn詳細
総context token優位
```

## 設計判断

```text
Core新syntax追加:=不要
Agent必須化:=不要
KDSL役割:=高密度意味伝達層を維持
Core freeze:=維持
次運用:=実Task利用→再現性ある問題発生時のみ仕様feedback
```

KDSLをAgent framework／workflow engine／Spec管理へ拡張しない。外部層との配置は`docs/usage-placement.md`を参照する。
